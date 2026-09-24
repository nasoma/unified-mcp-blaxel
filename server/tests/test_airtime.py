import pytest
import requests
from africastalking.Service import AfricasTalkingException

from services import airtime


class FakeAirtime:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def send(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.response


def sent_response(status="Sent", error_message="None"):
    return {
        "errorMessage": "None",
        "numSent": 1,
        "responses": [
            {
                "phoneNumber": "+254712345678",
                "amount": "KES 10.0000",
                "status": status,
                "errorMessage": error_message,
            }
        ],
    }


@pytest.fixture
def fake_airtime(monkeypatch):
    def install(**kwargs):
        fake = FakeAirtime(**kwargs)
        monkeypatch.setattr(airtime, "airtime", fake)
        return fake
    return install


@pytest.mark.parametrize(
    "raw",
    ["0712345678", "712345678", "254712345678", "+254712345678", "+254 712 345 678", "0712-345-678"],
)
def test_format_phone_number_accepts_kenyan_mobile_formats(raw):
    assert airtime.format_phone_number(raw) == "+254712345678"


def test_format_phone_number_accepts_01_prefix():
    assert airtime.format_phone_number("0110123456") == "+254110123456"


@pytest.mark.parametrize(
    "raw",
    ["", "12345", "07123456789", "071234567", "0812345678", "+255712345678", "07123abc78", "+254254712345678"],
)
def test_format_phone_number_rejects_invalid_numbers(raw):
    with pytest.raises(ValueError):
        airtime.format_phone_number(raw)


def test_load_airtime_reports_success(fake_airtime):
    fake = fake_airtime(response=sent_response())
    result = airtime.load_airtime("0712345678", 10, "KES")
    assert result == "Successfully sent KES 10 airtime to +254712345678"
    assert fake.calls[0]["phone_number"] == "+254712345678"


def test_load_airtime_parses_json_text_response(fake_airtime):
    import json
    fake_airtime(response=json.dumps(sent_response()))
    assert airtime.load_airtime("0712345678", 10, "KES").startswith("Successfully sent")


def test_load_airtime_reports_failed_recipient_status(fake_airtime):
    fake_airtime(response=sent_response(status="Failed", error_message="Insufficient Credit"))
    result = airtime.load_airtime("0712345678", 10, "KES")
    assert result.startswith("Error:")
    assert "Failed" in result and "Insufficient Credit" in result


def test_load_airtime_reports_empty_responses(fake_airtime):
    fake_airtime(response={"errorMessage": "A duplicate request was received", "responses": []})
    result = airtime.load_airtime("0712345678", 10, "KES")
    assert result.startswith("Error:")
    assert "duplicate request" in result


def test_load_airtime_rejects_invalid_number_without_calling_api(fake_airtime):
    fake = fake_airtime(response=sent_response())
    result = airtime.load_airtime("12345", 10, "KES")
    assert result.startswith("Invalid input:")
    assert fake.calls == []


def test_load_airtime_handles_api_exception(fake_airtime):
    fake_airtime(error=AfricasTalkingException("Invalid API key"))
    assert airtime.load_airtime("0712345678", 10, "KES") == "Africa's Talking API error: Invalid API key"


def test_load_airtime_handles_unexpected_exception(fake_airtime):
    fake_airtime(error=requests.ConnectionError("network down"))
    result = airtime.load_airtime("0712345678", 10, "KES")
    assert result.startswith("Unexpected error sending airtime:")


def test_check_balance_handles_api_exception(monkeypatch, fake_airtime):
    fake_airtime()

    class FailingApplication:
        @staticmethod
        def fetch_application_data():
            raise AfricasTalkingException("Unauthorized")

    monkeypatch.setattr(airtime.africastalking, "Application", FailingApplication)
    assert airtime.check_balance() == "Africa's Talking API error: Unauthorized"
