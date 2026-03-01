"""
Tests for the Medical Analysis Service.
Covers: prompt building, response parsing, confidence calculation, local abnormal detection.
"""

import json
import pytest
from unittest.mock import MagicMock, patch

from app.services.medical_analysis import MedicalAnalysisService, medical_analysis_service


class TestPromptBuilding:
    """Tests for prompt construction."""

    def setup_method(self):
        self.service = MedicalAnalysisService()

    def test_english_prompt(self):
        prompt = self.service._build_structured_prompt("Some text", "en")
        assert "Respond in English" in prompt
        assert "AccessAI" in prompt
        assert "Some text" in prompt
        assert "valid JSON" in prompt

    def test_hindi_prompt(self):
        prompt = self.service._build_structured_prompt("Some text", "hi")
        assert "Hindi" in prompt
        assert "हिंदी" in prompt

    def test_kannada_prompt(self):
        prompt = self.service._build_structured_prompt("Some text", "kn")
        assert "Kannada" in prompt
        assert "ಕನ್ನಡ" in prompt

    def test_prompt_includes_key_value_pairs(self):
        kvs = [{"key": "Hemoglobin", "value": "15 g/dL"}]
        prompt = self.service._build_structured_prompt("text", "en", key_value_pairs=kvs)
        assert "Hemoglobin" in prompt
        assert "15 g/dL" in prompt
        assert "KEY-VALUE PAIRS" in prompt

    def test_prompt_includes_tables(self):
        tables = [[["Test", "Value"], ["Hb", "15"]]]
        prompt = self.service._build_structured_prompt("text", "en", tables=tables)
        assert "TABLE 1" in prompt
        assert "Hb" in prompt

    def test_prompt_safety_guidelines(self):
        prompt = self.service._build_structured_prompt("text", "en")
        assert "NEVER provide a diagnosis" in prompt
        assert "uncertainty" in prompt.lower()
        assert "consulting a doctor" in prompt.lower()

    def test_prompt_requests_json_format(self):
        prompt = self.service._build_structured_prompt("text", "en")
        assert '"summary"' in prompt
        assert '"key_findings"' in prompt
        assert '"abnormal_values"' in prompt
        assert '"questions_for_doctor"' in prompt


class TestResponseParsing:
    """Tests for LLM response parsing."""

    def setup_method(self):
        self.service = MedicalAnalysisService()

    def test_parse_valid_json(self):
        raw = json.dumps({"summary": "Test", "key_findings": []})
        result = self.service._parse_analysis_response(raw)
        assert result["summary"] == "Test"

    def test_parse_json_in_code_block(self):
        raw = '```json\n{"summary": "Test", "key_findings": []}\n```'
        result = self.service._parse_analysis_response(raw)
        assert result["summary"] == "Test"

    def test_parse_json_in_generic_code_block(self):
        raw = '```\n{"summary": "Test"}\n```'
        result = self.service._parse_analysis_response(raw)
        assert result["summary"] == "Test"

    def test_parse_json_embedded_in_text(self):
        raw = 'Here is the analysis:\n{"summary": "Test", "key_findings": []}\nDone.'
        result = self.service._parse_analysis_response(raw)
        assert result["summary"] == "Test"

    def test_parse_completely_malformed(self):
        raw = "This is not JSON at all."
        result = self.service._parse_analysis_response(raw)
        # Should return fallback structure
        assert "summary" in result
        assert "questions_for_doctor" in result
        assert len(result["questions_for_doctor"]) == 5


class TestConfidenceCalculation:
    """Tests for the confidence scoring system."""

    def setup_method(self):
        self.service = MedicalAnalysisService()

    def test_base_confidence(self):
        analysis = {"key_findings": [{"a": 1}, {"b": 2}, {"c": 3}], "confidence_notes": ""}
        score = self.service._calculate_confidence(analysis, 90, "A" * 500)
        assert 70 <= score <= 95

    def test_low_ocr_penalized(self):
        analysis = {"key_findings": [{"a": 1}] * 5, "confidence_notes": ""}
        high_ocr = self.service._calculate_confidence(analysis, 95, "A" * 500)
        low_ocr = self.service._calculate_confidence(analysis, 50, "A" * 500)
        assert high_ocr > low_ocr

    def test_no_findings_penalized(self):
        with_findings = {"key_findings": [{"a": 1}] * 5, "confidence_notes": ""}
        without_findings = {"key_findings": [], "confidence_notes": ""}
        s1 = self.service._calculate_confidence(with_findings, 90, "A" * 500)
        s2 = self.service._calculate_confidence(without_findings, 90, "A" * 500)
        assert s1 > s2

    def test_short_text_penalized(self):
        analysis = {"key_findings": [{"a": 1}] * 5, "confidence_notes": ""}
        long_text = self.service._calculate_confidence(analysis, 90, "A" * 500)
        short_text = self.service._calculate_confidence(analysis, 90, "A" * 50)
        assert long_text > short_text

    def test_uncertainty_words_penalized(self):
        certain = {"key_findings": [{"a": 1}] * 5, "confidence_notes": "Clear results."}
        uncertain = {"key_findings": [{"a": 1}] * 5, "confidence_notes": "I'm uncertain about several values."}
        s1 = self.service._calculate_confidence(certain, 90, "A" * 500)
        s2 = self.service._calculate_confidence(uncertain, 90, "A" * 500)
        assert s1 > s2

    def test_score_clamped_to_range(self):
        # Even with all penalties, should not go below 10
        worst_case = {"key_findings": [], "confidence_notes": "uncertain and unclear"}
        score = self.service._calculate_confidence(worst_case, 30, "x")
        assert 10 <= score <= 95


class TestLocalAbnormalDetection:
    """Tests for the local regex-based abnormal value cross-check."""

    def setup_method(self):
        self.service = MedicalAnalysisService()

    def test_detects_high_glucose(self):
        text = "Glucose: 280 mg/dL"
        results = self.service._detect_abnormal_values_locally(text)
        glucose = [r for r in results if r["test_name"] == "glucose"]
        assert len(glucose) == 1
        assert glucose[0]["status"] == "high"
        assert glucose[0]["extracted_value"] == 280.0

    def test_detects_low_hemoglobin(self):
        text = "Hemoglobin: 8.2 g/dL"
        results = self.service._detect_abnormal_values_locally(text)
        hb = [r for r in results if r["test_name"] == "hemoglobin"]
        assert len(hb) == 1
        assert hb[0]["status"] == "low"

    def test_detects_normal_value(self):
        text = "Sodium: 140 mEq/L"
        results = self.service._detect_abnormal_values_locally(text)
        na = [r for r in results if r["test_name"] == "sodium"]
        assert len(na) == 1
        assert na[0]["status"] == "normal"

    def test_multiple_values(self, sample_medical_text):
        results = self.service._detect_abnormal_values_locally(sample_medical_text)
        test_names = [r["test_name"] for r in results]
        assert "hemoglobin" in test_names or "hb" in test_names
        assert any(r["status"] in ("high", "low") for r in results)

    def test_unknown_test_skipped(self):
        text = "FooBarTest: 999 units"
        results = self.service._detect_abnormal_values_locally(text)
        assert len(results) == 0

    def test_reference_ranges_populated(self):
        """Sanity check that REFERENCE_RANGES has expected tests."""
        refs = self.service.REFERENCE_RANGES
        assert "hemoglobin" in refs
        assert "glucose" in refs
        assert "creatinine" in refs
        assert "tsh" in refs
        assert "potassium" in refs


class TestMedicalAnalysisIntegration:
    """Integration tests using mock Bedrock."""

    def setup_method(self):
        self.service = MedicalAnalysisService()

    @pytest.mark.asyncio
    async def test_analyze_returns_structured_response(self, mock_bedrock_runtime, sample_medical_text):
        result = await self.service.analyze(
            bedrock_runtime=mock_bedrock_runtime,
            extracted_text=sample_medical_text,
            language="en",
            ocr_confidence=92.0,
        )
        assert "summary" in result
        assert "key_findings" in result
        assert "confidence" in result
        assert "model" in result
        assert result["language"] == "en"

    @pytest.mark.asyncio
    async def test_analyze_with_low_confidence_text(self, mock_bedrock_runtime):
        result = await self.service.analyze(
            bedrock_runtime=mock_bedrock_runtime,
            extracted_text="Short.",
            language="en",
            ocr_confidence=40.0,
        )
        # Confidence should be lower due to short text + low OCR
        assert result["confidence"] < 80

    @pytest.mark.asyncio
    async def test_analyze_bedrock_failure(self):
        mock = MagicMock()
        mock.invoke_model.side_effect = Exception("Bedrock unavailable")
        with pytest.raises(Exception, match="Bedrock unavailable"):
            await self.service.analyze(
                bedrock_runtime=mock,
                extracted_text="Test text",
                language="en",
            )

    def test_global_singleton(self):
        assert medical_analysis_service is not None
        assert isinstance(medical_analysis_service, MedicalAnalysisService)
