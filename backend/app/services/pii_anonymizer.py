"""
PII Anonymisation Service.

Uses **AWS Comprehend** ``detect_pii_entities`` to find PII in text, replaces each
entity with a deterministic placeholder (e.g. ``[NAME_1]``, ``[PHONE_1]``), and
maintains a reversible mapping so that LLM responses can be de-anonymised
before returning to the user.

Fallback: a regex-based detector that covers the most common Indian PII
patterns (Aadhaar, PAN, phone, e-mail, PIN codes) when Comprehend is
unavailable.

Enterprise design:
  - The original PII values NEVER leave the backend.
  - Only anonymised text is sent to any LLM / embedding model.
  - The PII mapping lives only in the in-memory session store and is
    automatically purged when the session expires.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
#  Data structures
# ---------------------------------------------------------------------------

@dataclass
class PIIEntity:
    """A single detected PII span."""
    entity_type: str          # NAME, PHONE, EMAIL, ADDRESS, DATE_OF_BIRTH …
    text: str                 # the original value
    start: int                # char offset in source text
    end: int                  # char offset in source text
    score: float = 1.0        # confidence 0-1
    source: str = "comprehend"  # "comprehend" | "regex"


@dataclass
class PIIMapping:
    """Reversible mapping between original PII and placeholders."""
    placeholder_to_original: Dict[str, str] = field(default_factory=dict)
    original_to_placeholder: Dict[str, str] = field(default_factory=dict)
    entity_counts: Dict[str, int] = field(default_factory=dict)

    def add(self, entity_type: str, original: str) -> str:
        """Register a PII value and return its placeholder."""
        # If we've already seen this exact value, reuse the placeholder
        if original in self.original_to_placeholder:
            return self.original_to_placeholder[original]

        count = self.entity_counts.get(entity_type, 0) + 1
        self.entity_counts[entity_type] = count
        placeholder = f"[{entity_type}_{count}]"

        self.placeholder_to_original[placeholder] = original
        self.original_to_placeholder[original] = placeholder
        return placeholder

    def deanonymise(self, text: str) -> str:
        """Replace all placeholders in *text* with their original values."""
        result = text
        # Sort by longest placeholder first to avoid partial replacements
        for placeholder in sorted(
            self.placeholder_to_original, key=len, reverse=True
        ):
            result = result.replace(
                placeholder, self.placeholder_to_original[placeholder]
            )
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "placeholder_to_original": dict(self.placeholder_to_original),
            "entity_counts": dict(self.entity_counts),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PIIMapping":
        p2o = d.get("placeholder_to_original", {})
        o2p = {v: k for k, v in p2o.items()}
        return cls(
            placeholder_to_original=p2o,
            original_to_placeholder=o2p,
            entity_counts=d.get("entity_counts", {}),
        )


# ---------------------------------------------------------------------------
#  Regex-based PII detector (fallback / supplement)
# ---------------------------------------------------------------------------

# Patterns are tuned for Indian medical-report PII

_PATTERNS: List[Tuple[str, re.Pattern]] = [
    # Indian mobile: +91-XXXXXXXXXX or 10-digit starting with 6-9
    ("PHONE", re.compile(
        r"(?<!\d)(?:\+91[\-\s]?)?[6-9]\d{9}(?!\d)"
    )),
    # E-mail
    ("EMAIL", re.compile(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}"
    )),
    # Aadhaar (12-digit, optionally space-separated in groups of 4)
    ("AADHAAR", re.compile(
        r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    )),
    # PAN card (ABCDE1234F)
    ("PAN", re.compile(
        r"\b[A-Z]{5}\d{4}[A-Z]\b"
    )),
    # Indian PIN code (6 digits, first digit 1-9)
    ("PIN_CODE", re.compile(
        r"(?<!\d)[1-9]\d{5}(?!\d)"
    )),
    # Date of birth variants: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    ("DATE_OF_BIRTH", re.compile(
        r"\b(?:(?:0[1-9]|[12]\d|3[01])[\/\-](?:0[1-9]|1[0-2])[\/\-](?:19|20)\d{2})"
        r"|(?:(?:19|20)\d{2}[\/\-](?:0[1-9]|1[0-2])[\/\-](?:0[1-9]|[12]\d|3[01]))\b"
    )),
    # Common name prefixes in Indian medical docs  (Mr./Mrs./Dr. + capitalised words)
    ("NAME", re.compile(
        r"(?:(?:Mr|Mrs|Ms|Dr|Shri|Smt|Baby|Master)\.?\s+)"
        r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}"
    )),
    # Patient Name / Name: pattern
    ("NAME", re.compile(
        r"(?:Patient\s*(?:Name)?|Name)\s*[:]\s*([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})",
        re.IGNORECASE,
    )),
    # Address lines (long enough sequences after "Address:" label)
    ("ADDRESS", re.compile(
        r"(?:Address|Addr)\s*[:]\s*(.{10,120}?)(?:\n|$)",
        re.IGNORECASE,
    )),
]


def _regex_detect(text: str) -> List[PIIEntity]:
    """Detect PII using regex patterns (no AWS call)."""
    entities: List[PIIEntity] = []
    seen_spans: set = set()

    for entity_type, pattern in _PATTERNS:
        for m in pattern.finditer(text):
            # Use group(1) if it exists (capturing group), else group(0)
            matched_text = m.group(1) if m.lastindex and m.lastindex >= 1 else m.group(0)
            span = (m.start(), m.end())

            # Skip overlapping spans
            if any(s[0] <= span[0] < s[1] or s[0] < span[1] <= s[1] for s in seen_spans):
                continue

            seen_spans.add(span)
            entities.append(PIIEntity(
                entity_type=entity_type,
                text=matched_text.strip(),
                start=span[0],
                end=span[1],
                score=0.85,
                source="regex",
            ))

    return entities


# ---------------------------------------------------------------------------
#  AWS Comprehend PII detector
# ---------------------------------------------------------------------------

def _comprehend_detect(
    comprehend_client,
    text: str,
    language: str = "en",
) -> List[PIIEntity]:
    """
    Detect PII using Amazon Comprehend ``DetectPiiEntities``.
    Comprehend supports texts up to 100 KB (UTF-8).
    """
    # Comprehend max size is 100 KB
    truncated = text[:99_000]

    try:
        response = comprehend_client.detect_pii_entities(
            Text=truncated,
            LanguageCode=language,
        )
    except Exception as e:
        logger.warning(f"Comprehend PII detection failed: {e}")
        return []

    entities: List[PIIEntity] = []
    for ent in response.get("Entities", []):
        start = ent["BeginOffset"]
        end = ent["EndOffset"]
        entities.append(PIIEntity(
            entity_type=ent["Type"],       # NAME, ADDRESS, PHONE, EMAIL, …
            text=truncated[start:end],
            start=start,
            end=end,
            score=ent.get("Score", 1.0),
            source="comprehend",
        ))

    return entities


# ---------------------------------------------------------------------------
#  Main service
# ---------------------------------------------------------------------------

class PIIAnonymiser:
    """
    Stateless anonymisation service.

    Usage::

        anonymiser = PIIAnonymiser()
        anon_text, mapping = anonymiser.anonymise(text, comprehend_client)
        # … send anon_text to LLM …
        original_response = mapping.deanonymise(llm_response)
    """

    # PII types we always redact (high-risk identifiers)
    HIGH_RISK_TYPES = {
        "NAME", "PHONE", "EMAIL", "ADDRESS",
        "DATE_OF_BIRTH", "AADHAAR", "PAN",
        "SSN", "CREDIT_DEBIT_NUMBER", "CREDIT_DEBIT_CVV",
        "CREDIT_DEBIT_EXPIRY", "BANK_ACCOUNT_NUMBER", "BANK_ROUTING",
        "PASSPORT_NUMBER", "DRIVER_ID", "PIN", "PIN_CODE",
        "USERNAME", "PASSWORD", "AWS_ACCESS_KEY", "AWS_SECRET_KEY",
        "IP_ADDRESS", "MAC_ADDRESS", "URL",
    }

    # PII types we keep (they are medically relevant and NOT identifying)
    KEEP_TYPES = {
        "AGE",           # needed for medical context
        "DATE",          # lab-report dates are useful
    }

    def anonymise(
        self,
        text: str,
        comprehend_client=None,
        language: str = "en",
        min_confidence: float = 0.6,
    ) -> Tuple[str, PIIMapping]:
        """
        Detect and replace PII in *text*.

        Returns (anonymised_text, mapping).
        The *mapping* should be stored in the session so responses can be
        de-anonymised later.
        """
        if not text or not text.strip():
            return text, PIIMapping()

        # --- Step 1: Detect PII ---
        entities: List[PIIEntity] = []

        # Primary: AWS Comprehend
        if comprehend_client:
            entities = _comprehend_detect(comprehend_client, text, language)
            logger.info(f"Comprehend detected {len(entities)} PII entities")

        # Supplement / fallback: regex (catches Indian-specific IDs that
        # Comprehend may miss, e.g. Aadhaar, PAN)
        regex_entities = _regex_detect(text)
        if regex_entities:
            # Merge, avoiding duplicates on overlapping spans
            existing_spans = {(e.start, e.end) for e in entities}
            for re_ent in regex_entities:
                overlaps = any(
                    s[0] <= re_ent.start < s[1] or s[0] < re_ent.end <= s[1]
                    for s in existing_spans
                )
                if not overlaps:
                    entities.append(re_ent)
            logger.info(
                f"Regex added {len(regex_entities)} entities "
                f"({len(entities)} total after merge)"
            )

        if not entities:
            return text, PIIMapping()

        # --- Step 2: Filter by confidence and type ---
        entities = [
            e for e in entities
            if e.score >= min_confidence
            and e.entity_type not in self.KEEP_TYPES
        ]

        # Sort by start offset descending so replacements don't shift indices
        entities.sort(key=lambda e: e.start, reverse=True)

        # --- Step 3: Replace with placeholders ---
        mapping = PIIMapping()
        anon_text = text

        for ent in entities:
            # Only redact high-risk types (or anything Comprehend flags that
            # isn't in our explicit keep-list)
            if ent.entity_type in self.HIGH_RISK_TYPES or ent.source == "comprehend":
                placeholder = mapping.add(ent.entity_type, ent.text)
                anon_text = anon_text[:ent.start] + placeholder + anon_text[ent.end:]

        detected_types = list(mapping.entity_counts.keys())
        total_redacted = sum(mapping.entity_counts.values())
        logger.info(
            f"PII anonymisation complete: {total_redacted} entities redacted "
            f"(types: {detected_types})"
        )

        return anon_text, mapping

    def deanonymise(self, text: str, mapping: PIIMapping) -> str:
        """Convenience wrapper around ``mapping.deanonymise``."""
        return mapping.deanonymise(text)


# Global singleton
pii_anonymiser = PIIAnonymiser()
