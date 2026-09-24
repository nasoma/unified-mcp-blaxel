import africastalking
import json
import re
from africastalking.Service import AfricasTalkingException
from config import settings

# Initialize Africa's Talking
if settings.AFRICASTALKING_USERNAME and settings.AFRICASTALKING_API_KEY:
    africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
    airtime = africastalking.Airtime
else:
    airtime = None

COUNTRY_CODES = {"kenya": "+254"}
# Kenyan mobile numbers: 7xxxxxxxx or 1xxxxxxxx, optionally prefixed by 0, 254 or +254
KENYA_MOBILE_PATTERN = re.compile(r"^(?:\+?254|0)?([17]\d{8})$")
SUCCESS_STATUSES = {"sent", "success"}
SUPPORTED_COUNTRIES = {
    "+254": {"name": "Kenya", "currency": "KES", "min_amount": 5, "max_amount": 10000}
}

def format_phone_number(phone_number: str) -> str:
    """Validate a Kenyan mobile number and return it in +254XXXXXXXXX format."""
    if settings.USER_COUNTRY != "kenya":
        raise ValueError("Only Kenya is supported. Set country to 'kenya'.")

    cleaned = re.sub(r"[\s\-()]", "", str(phone_number))
    match = KENYA_MOBILE_PATTERN.match(cleaned)
    if not match:
        raise ValueError(
            f"'{phone_number}' is not a valid Kenyan mobile number "
            "(expected e.g. 0712345678 or +254712345678)."
        )
    return COUNTRY_CODES["kenya"] + match.group(1)

def _parse_send_response(response) -> str | None:
    """Return an error message if the send response reports a failure, else None."""
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            return f"Unexpected response from Africa's Talking: {response}"
    if not isinstance(response, dict):
        return f"Unexpected response from Africa's Talking: {response}"

    results = response.get("responses") or []
    if not results:
        error = response.get("errorMessage")
        return f"No airtime was queued: {error or 'empty response'}"

    result = results[0]
    status = str(result.get("status", ""))
    if status.lower() not in SUCCESS_STATUSES:
        error = result.get("errorMessage") or response.get("errorMessage") or "unknown error"
        return f"Airtime transfer failed (status: {status or 'unknown'}): {error}"
    return None

def check_balance() -> str:
    """Check Africa's Talking account balance."""
    if not airtime:
        return "Error: Africa's Talking credentials not configured."

    try:
        # This is a blocking call
        response = africastalking.Application.fetch_application_data()
        if "UserData" in response and "balance" in response["UserData"]:
            return f"Account Balance: {response['UserData']['balance']}"
        return "Balance information not available. Unexpected response structure."
    except AfricasTalkingException as e:
        return f"Africa's Talking API error: {str(e)}"
    except Exception as e:
        return f"Unexpected error fetching balance: {str(e)}"

def load_airtime(phone_number: str, amount: float, currency_code: str) -> str:
    """Load airtime to a phone number."""
    if not airtime:
        return "Error: Africa's Talking credentials not configured."

    try:
        if currency_code != "KES":
            return "Error: Only KES currency is supported for Kenya."

        if amount < 5 or amount > 10000:
            return "Error: Amount must be between 5 and 10,000 KES."

        formatted_number = format_phone_number(phone_number)

        # This is a blocking call
        response = airtime.send(
            phone_number=formatted_number, amount=amount, currency_code=currency_code
        )

        error = _parse_send_response(response)
        if error:
            return f"Error: {error}"
        return f"Successfully sent {currency_code} {amount} airtime to {formatted_number}"
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except AfricasTalkingException as e:
        return f"Africa's Talking API error: {str(e)}"
    except Exception as e:
        return f"Unexpected error sending airtime: {str(e)}"

def get_supported_countries() -> str:
    """Get supported country (Kenya) and limits."""
    return json.dumps(
        {
            "supported_countries": SUPPORTED_COUNTRIES,
            "total_countries": len(SUPPORTED_COUNTRIES),
            "usage_note": "Use +254 prefix for Kenyan phone numbers",
        },
        indent=2,
    )
