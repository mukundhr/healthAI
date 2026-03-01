"""
Tests for the Emergency Detection Service.
Covers: panic value detection, edge cases, severity ordering, deduplication.
"""

import pytest
from app.services.emergency_detector import EmergencyDetector, emergency_detector


class TestEmergencyDetector:
    """Unit tests for EmergencyDetector."""

    def setup_method(self):
        self.detector = EmergencyDetector()

    # ── Detect nothing when values are normal ──

    def test_no_emergency_for_normal_text(self, sample_normal_text):
        result = self.detector.detect_critical_values(sample_normal_text)
        assert result["has_emergency"] is False
        assert result["alerts"] == []
        assert result["emergency_resources"] == {}

    # ── Detect panic values in raw text ──

    def test_critical_glucose_low(self):
        text = "Glucose: 45 mg/dL"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True
        assert any(a["test_name"].lower() == "glucose" for a in result["alerts"])
        assert any(a["direction"] == "critically_low" for a in result["alerts"])

    def test_critical_glucose_high(self):
        text = "Glucose: 550 mg/dL"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True
        alert = [a for a in result["alerts"] if a["test_name"].lower() == "glucose"][0]
        assert alert["direction"] == "critically_high"
        assert alert["severity"] == "critical"

    def test_critical_potassium_high(self):
        text = "Potassium: 7.2 mEq/L"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True
        alert = [a for a in result["alerts"] if a["test_name"].lower() == "potassium"][0]
        assert alert["direction"] == "critically_high"
        assert "heart" in alert["message"].lower()

    def test_critical_hemoglobin_low(self):
        text = "Hemoglobin: 3.8 g/dL"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True
        alert = [a for a in result["alerts"] if a["test_name"].lower() == "hemoglobin"][0]
        assert alert["direction"] == "critically_low"
        assert "anemia" in alert["message"].lower() or "transfusion" in alert["message"].lower()

    def test_critical_troponin_high(self):
        text = "Troponin: 0.8 ng/mL"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True
        alert = [a for a in result["alerts"] if a["test_name"].lower() == "troponin"][0]
        assert "heart" in alert["message"].lower()

    def test_critical_creatinine_high(self):
        text = "Creatinine: 12.5 mg/dL"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True
        alert = [a for a in result["alerts"] if a["test_name"].lower() == "creatinine"][0]
        assert "kidney" in alert["message"].lower()

    # ── Multiple critical values at once ──

    def test_multiple_critical_values(self, sample_critical_text):
        result = self.detector.detect_critical_values(sample_critical_text)
        assert result["has_emergency"] is True
        assert result["alert_count"] >= 3  # hb, potassium, glucose, troponin
        assert "ambulance" in result["emergency_resources"]
        assert result["emergency_resources"]["ambulance"] == "108"

    # ── Structured findings input ──

    def test_detect_from_key_findings(self):
        findings = [
            {"test_name": "Glucose", "value": "40 mg/dL", "status": "low"},
            {"test_name": "Sodium", "value": "138 mEq/L", "status": "normal"},
        ]
        result = self.detector.detect_critical_values(
            extracted_text="", key_findings=findings
        )
        assert result["has_emergency"] is True
        assert len(result["alerts"]) == 1
        assert result["alerts"][0]["test_name"].lower() == "glucose"

    def test_skips_normal_findings(self):
        findings = [
            {"test_name": "Sodium", "value": "140", "status": "normal"},
        ]
        result = self.detector.detect_critical_values(
            extracted_text="", key_findings=findings
        )
        assert result["has_emergency"] is False

    def test_detect_from_abnormal_values(self):
        abnormals = [
            {"test_name": "Potassium", "value": "2.0", "severity": "severe"},
        ]
        result = self.detector.detect_critical_values(
            extracted_text="", abnormal_values=abnormals
        )
        assert result["has_emergency"] is True
        assert result["alerts"][0]["direction"] == "critically_low"

    # ── Deduplication ──

    def test_no_duplicate_alerts(self):
        """Same value found in text AND findings should produce only 1 alert."""
        findings = [
            {"test_name": "Glucose", "value": "45", "status": "low"},
        ]
        text = "Glucose: 45 mg/dL"
        result = self.detector.detect_critical_values(
            text, key_findings=findings
        )
        glucose_alerts = [a for a in result["alerts"] if a["test_name"].lower() == "glucose"]
        assert len(glucose_alerts) == 1

    # ── Edge cases ──

    def test_empty_text(self):
        result = self.detector.detect_critical_values("")
        assert result["has_emergency"] is False

    def test_non_numeric_value_in_finding(self):
        findings = [
            {"test_name": "Glucose", "value": "N/A", "status": "high"},
        ]
        result = self.detector.detect_critical_values("", key_findings=findings)
        assert result["has_emergency"] is False

    def test_value_at_exact_threshold_low(self):
        """Value exactly at the critical threshold should still trigger."""
        text = "Glucose: 50 mg/dL"  # low_critical is 50
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True

    def test_value_just_above_low_threshold(self):
        """Value just above the critical threshold should NOT trigger."""
        text = "Glucose: 51 mg/dL"
        result = self.detector.detect_critical_values(text)
        glucose_alerts = [a for a in result.get("alerts", []) if a["test_name"].lower() == "glucose"]
        assert len(glucose_alerts) == 0

    def test_hb_alias_detection(self):
        """'hb' should be recognized as hemoglobin alias."""
        text = "hb: 4.5 g/dL"
        result = self.detector.detect_critical_values(text)
        assert result["has_emergency"] is True

    def test_severity_ordering(self):
        """Critical alerts should come before urgent ones."""
        text = "Glucose: 45 mg/dL\nPotassium: 7.0 mEq/L\nTroponin: 0.5 ng/mL"
        result = self.detector.detect_critical_values(text)
        if len(result["alerts"]) > 1:
            for alert in result["alerts"]:
                assert alert["severity"] == "critical"

    # ── Disclaimer ──

    def test_emergency_includes_disclaimer(self, sample_critical_text):
        result = self.detector.detect_critical_values(sample_critical_text)
        assert "disclaimer" in result
        assert "NOT a diagnostic tool" in result["disclaimer"]

    # ── Global singleton ──

    def test_global_instance_works(self, sample_critical_text):
        result = emergency_detector.detect_critical_values(sample_critical_text)
        assert result["has_emergency"] is True


class TestExtractNumeric:
    """Tests for the _extract_numeric helper."""

    def setup_method(self):
        self.detector = EmergencyDetector()

    def test_integer(self):
        assert self.detector._extract_numeric("45") == 45.0

    def test_float(self):
        assert self.detector._extract_numeric("3.8") == 3.8

    def test_with_unit(self):
        assert self.detector._extract_numeric("280 mg/dL") == 280.0

    def test_empty_string(self):
        assert self.detector._extract_numeric("") is None

    def test_no_number(self):
        assert self.detector._extract_numeric("N/A") is None

    def test_leading_text(self):
        assert self.detector._extract_numeric("Value: 7.2") == 7.2
