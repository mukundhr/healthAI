"""
Tests for the SMS Service.
Covers: message formatting, phone validation, multilingual output, SNS integration.
"""

import pytest
from unittest.mock import MagicMock

from app.services.sms_service import SMSService, sms_service


class TestSMSServiceFormatting:
    """Tests for SMS message formatting."""

    def setup_method(self):
        self.service = SMSService()
        self.analysis = {
            "summary": "Your blood report shows elevated glucose and low hemoglobin.",
            "emergency": {
                "has_emergency": True,
                "alerts": [
                    {
                        "test_name": "Glucose",
                        "message": "Dangerously low blood sugar.",
                    }
                ],
            },
            "abnormal_values": [
                {
                    "test_name": "Hemoglobin",
                    "value": "8.2 g/dL",
                    "severity": "moderate",
                },
                {
                    "test_name": "Glucose",
                    "value": "280 mg/dL",
                    "severity": "severe",
                },
            ],
            "questions_for_doctor": [
                "What is causing my anemia?",
                "Should I start diabetes medication?",
            ],
        }

    def test_format_english(self):
        msg = self.service._format_summary_sms(self.analysis, language="en")
        assert "AccessAI" in msg
        assert "Medical Report Summary" in msg
        assert "Hemoglobin" in msg
        assert "Please visit a doctor" in msg

    def test_format_hindi(self):
        msg = self.service._format_summary_sms(self.analysis, language="hi")
        assert "AccessAI" in msg
        assert "मेडिकल रिपोर्ट" in msg
        assert "डॉक्टर" in msg

    def test_format_kannada(self):
        msg = self.service._format_summary_sms(self.analysis, language="kn")
        assert "AccessAI" in msg
        assert "ವೈದ್ಯಕೀಯ" in msg

    def test_emergency_alerts_included(self):
        msg = self.service._format_summary_sms(self.analysis, language="en")
        assert "URGENT" in msg
        assert "Glucose" in msg
        assert "108" in msg  # ambulance number

    def test_no_emergency_section_when_none(self):
        analysis = {**self.analysis, "emergency": {"has_emergency": False, "alerts": []}}
        msg = self.service._format_summary_sms(analysis, language="en")
        assert "URGENT" not in msg

    def test_abnormal_values_included(self):
        msg = self.service._format_summary_sms(self.analysis, language="en")
        assert "Abnormal" in msg
        assert "Hemoglobin" in msg

    def test_doctor_questions_included(self):
        msg = self.service._format_summary_sms(self.analysis, language="en")
        assert "Ask your doctor" in msg
        assert "anemia" in msg

    def test_schemes_included_when_requested(self):
        schemes = {
            "schemes": [
                {
                    "name": "Ayushman Bharat",
                    "coverage": "Up to ₹5 lakh",
                    "helpline": "14555",
                }
            ]
        }
        msg = self.service._format_summary_sms(
            self.analysis, language="en", include_schemes=True, schemes=schemes
        )
        assert "Ayushman Bharat" in msg
        assert "14555" in msg

    def test_schemes_omitted_when_not_requested(self):
        msg = self.service._format_summary_sms(
            self.analysis, language="en", include_schemes=False
        )
        assert "Govt Schemes" not in msg

    def test_message_truncated_to_max_length(self):
        # Create analysis with very long summary
        long_analysis = {
            **self.analysis,
            "summary": "A" * 2000,
        }
        msg = self.service._format_summary_sms(long_analysis, language="en")
        assert len(msg) <= SMSService.MAX_SMS_LENGTH

    def test_empty_analysis_still_produces_message(self):
        msg = self.service._format_summary_sms({}, language="en")
        assert "AccessAI" in msg
        assert "Please visit a doctor" in msg


class TestSMSSending:
    """Tests for SMS send logic."""

    def setup_method(self):
        self.service = SMSService()

    @pytest.mark.asyncio
    async def test_send_success(self, mock_sns_client):
        self.service.initialize(mock_sns_client)
        result = await self.service.send_summary(
            phone_number="+919876543210",
            analysis={"summary": "Test"},
            language="en",
        )
        assert result["success"] is True
        assert result["message_id"] == "test-msg-id-12345"
        mock_sns_client.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_invalid_phone(self, mock_sns_client):
        self.service.initialize(mock_sns_client)
        with pytest.raises(ValueError, match="Invalid phone number"):
            await self.service.send_summary(
                phone_number="1234567890",  # no +91 prefix
                analysis={"summary": "Test"},
            )

    @pytest.mark.asyncio
    async def test_send_short_phone(self, mock_sns_client):
        self.service.initialize(mock_sns_client)
        with pytest.raises(ValueError):
            await self.service.send_summary(
                phone_number="+9198765",  # too short
                analysis={"summary": "Test"},
            )

    @pytest.mark.asyncio
    async def test_send_without_initialization(self):
        with pytest.raises(RuntimeError, match="not initialized"):
            await self.service.send_summary(
                phone_number="+919876543210",
                analysis={"summary": "Test"},
            )

    @pytest.mark.asyncio
    async def test_send_sns_failure(self, mock_sns_client):
        mock_sns_client.publish.side_effect = Exception("SNS error")
        self.service.initialize(mock_sns_client)
        result = await self.service.send_summary(
            phone_number="+919876543210",
            analysis={"summary": "Test"},
        )
        assert result["success"] is False
        assert "Failed" in result["message"]

    @pytest.mark.asyncio
    async def test_sns_called_with_correct_attributes(self, mock_sns_client):
        self.service.initialize(mock_sns_client)
        await self.service.send_summary(
            phone_number="+919876543210",
            analysis={"summary": "Test"},
        )
        call_kwargs = mock_sns_client.publish.call_args[1]
        assert call_kwargs["PhoneNumber"] == "+919876543210"
        attrs = call_kwargs["MessageAttributes"]
        assert attrs["AWS.SNS.SMS.SenderID"]["StringValue"] == "AccessAI"
        assert attrs["AWS.SNS.SMS.SMSType"]["StringValue"] == "Transactional"


class TestGlobalSMSInstance:
    def test_global_instance_exists(self):
        assert sms_service is not None
        assert isinstance(sms_service, SMSService)
