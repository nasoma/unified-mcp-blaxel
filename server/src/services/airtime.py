import africastalking
import json
from africastalking.Service import AfricasTalkingException
from config import settings

# Initialize Africa's Talking
if settings.AFRICASTALKING_USERNAME and settings.AFRICASTALKING_API_KEY:
    africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
    airtime = africastalking.Airtime
else:
    airtime = None

COUNTRY_CODES = {"kenya": "+254"}
SUPPORTED_COUNTRIES = {
    "+254": {"name": "Kenya", "currency": "KES", "min_amount": 5, "max_amount": 10000}
}

def format_phone_number(phone_number: str) -> str:
    """Format phone number with Kenya country code."""
    phone_number = str(phone_number).strip()

    if settings.USER_COUNTRY != "kenya":
        raise ValueError("Only Kenya is supported. Set country to 'kenya'.")

    country_code = COUNTRY_CODES["kenya"]

    if phone_number.startswith("0"):
        return country_code + phone_number[1:]
    elif phone_number.startswith("+254"):
        return phone_number
    else:
        return country_code + phone_number

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
    except africastalking.AfricasTalkingException as e:
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
        airtime.send(
            phone_number=formatted_number, amount=amount, currency_code=currency_code
        )

        return f"Successfully sent {currency_code} {amount} airtime to {formatted_number}"
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except africastalking.AfricasTalkingException as e:
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
