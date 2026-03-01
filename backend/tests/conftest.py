"""
Shared pytest fixtures for AccessAI backend tests.
"""

import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime

# Ensure backend is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── Sample data ──────────────────────────────────────────────

SAMPLE_MEDICAL_TEXT = """
PATHOLOGY LAB REPORT
Patient Name: Rajesh Kumar
Age: 45 Years | Sex: Male
Date: 15/01/2025

COMPLETE BLOOD COUNT (CBC)
Hemoglobin: 8.2 g/dL (Ref: 14.0-18.0 g/dL)
WBC Count: 12500 cells/mcL (Ref: 4500-11000)
RBC Count: 4.1 million/mcL (Ref: 4.7-6.1)
Platelets: 185000 /mcL (Ref: 150000-400000)

BLOOD SUGAR
Fasting Glucose: 280 mg/dL (Ref: 70-100 mg/dL)
HBA1C: 9.2% (Ref: 4.0-5.7%)

RENAL FUNCTION
Creatinine: 2.8 mg/dL (Ref: 0.7-1.3 mg/dL)
BUN: 38 mg/dL (Ref: 7-20 mg/dL)

THYROID
TSH: 8.5 mIU/L (Ref: 0.4-4.0 mIU/L)
"""

SAMPLE_CRITICAL_TEXT = """
EMERGENCY LAB REPORT
Hemoglobin: 3.8 g/dL
Potassium: 7.2 mEq/L
Glucose: 45 mg/dL
Troponin: 0.8 ng/mL
"""

SAMPLE_NORMAL_TEXT = """
ROUTINE CHECK-UP
Hemoglobin: 15.0 g/dL
Glucose: 90 mg/dL
Creatinine: 0.9 mg/dL
Sodium: 140 mEq/L
Potassium: 4.2 mEq/L
"""

SAMPLE_ANALYSIS_RESULT = {
    "summary": "Your blood report shows some concerning values that need medical attention.",
    "key_findings": [
        {
            "test_name": "Hemoglobin",
            "value": "8.2 g/dL",
            "normal_range": "14.0-18.0 g/dL",
            "status": "low",
            "explanation": "Your hemoglobin is lower than normal, indicating possible anemia.",
        },
        {
            "test_name": "Fasting Glucose",
            "value": "280 mg/dL",
            "normal_range": "70-100 mg/dL",
            "status": "high",
            "explanation": "Your blood sugar is quite high.",
        },
    ],
    "abnormal_values": [
        {
            "test_name": "Hemoglobin",
            "value": "8.2 g/dL",
            "normal_range": "14.0-18.0 g/dL",
            "severity": "moderate",
            "explanation": "Moderate anemia detected.",
        },
        {
            "test_name": "Fasting Glucose",
            "value": "280 mg/dL",
            "normal_range": "70-100 mg/dL",
            "severity": "severe",
            "explanation": "Blood sugar is significantly elevated.",
        },
        {
            "test_name": "Creatinine",
            "value": "2.8 mg/dL",
            "normal_range": "0.7-1.3 mg/dL",
            "severity": "moderate",
            "explanation": "Kidney function may be impaired.",
        },
    ],
    "things_to_note": [
        "Multiple abnormal values suggest a need for comprehensive follow-up.",
        "High blood sugar combined with kidney markers needs attention.",
    ],
    "questions_for_doctor": [
        "What is causing my anemia?",
        "Is my blood sugar indicating diabetes?",
        "Should I be concerned about my kidney values?",
        "What follow-up tests do I need?",
        "Do I need to change my diet or medication?",
    ],
    "confidence_notes": "Analysis is based on standard reference ranges.",
    "confidence": 82,
    "model": "anthropic.claude-haiku-4-5-20251001-v1:0",
    "language": "en",
}


@pytest.fixture
def sample_medical_text():
    return SAMPLE_MEDICAL_TEXT


@pytest.fixture
def sample_critical_text():
    return SAMPLE_CRITICAL_TEXT


@pytest.fixture
def sample_normal_text():
    return SAMPLE_NORMAL_TEXT


@pytest.fixture
def sample_analysis_result():
    return SAMPLE_ANALYSIS_RESULT.copy()


@pytest.fixture
def mock_bedrock_runtime():
    """Mock Bedrock Runtime client returning a valid analysis JSON."""
    import json

    mock = MagicMock()
    response_body = json.dumps(
        {"content": [{"text": json.dumps(SAMPLE_ANALYSIS_RESULT)}]}
    ).encode("utf-8")

    mock_stream = MagicMock()
    mock_stream.read.return_value = response_body
    mock.invoke_model.return_value = {"body": mock_stream}
    return mock


@pytest.fixture
def mock_sns_client():
    """Mock SNS client."""
    mock = MagicMock()
    mock.publish.return_value = {"MessageId": "test-msg-id-12345"}
    return mock


@pytest.fixture
def mock_comprehend_client():
    """Mock Comprehend client for PII detection."""
    mock = MagicMock()
    mock.detect_pii_entities.return_value = {
        "Entities": [
            {
                "Type": "NAME",
                "BeginOffset": 32,
                "EndOffset": 44,
                "Score": 0.99,
            },
            {
                "Type": "PHONE",
                "BeginOffset": 100,
                "EndOffset": 110,
                "Score": 0.95,
            },
        ]
    }
    return mock


@pytest.fixture
def mock_session_with_analysis():
    """A session dict that already has OCR + analysis results."""
    return {
        "session_id": "test-session-123",
        "document_id": "test-doc-456",
        "status": "completed",
        "status_message": "Analysis complete!",
        "ocr_result": {
            "text": SAMPLE_MEDICAL_TEXT,
            "confidence": 92.5,
            "key_value_pairs": [],
            "tables": [],
        },
        "analysis_result": SAMPLE_ANALYSIS_RESULT.copy(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
