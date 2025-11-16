import os
from typing import List
from decimal import Decimal, InvalidOperation
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import json
import re
import africastalking
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
try:
    EXCHANGE_RATE = os.getenv("EXCHANGE_RATE")
    UPWORK_FEE = os.getenv("UPWORK_FEE", "0.99")
    UPWORK_RATE = os.getenv("UPWORK_RATE", "0.884")
    SENDER = os.getenv("SENDER")
    SENDER_NAME = os.getenv("SENDER_NAME")
    REGION = os.getenv("REGION")
    username = os.getenv("username")
    api_key = os.getenv("api_key")
    currency_code = os.getenv("currency_code", "KES")
    user_country = os.getenv("country", "kenya").lower()
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

except (ValueError, TypeError) as e:
    raise ValueError(f"Environment variable error: {str(e)}")

# Initialize MCP server with HTTP transport
mcp = FastMCP(
    "UnifiedMCP",
    stateless_http=True,
    host=os.getenv("BL_SERVER_HOST", "0.0.0.0"),
    port=os.getenv("BL_SERVER_PORT", "80"),
)


def parse_payment_amounts(input_str: str) -> List[Decimal]:
    """Parse comma-separated payment amounts with validation."""
    if not input_str or not input_str.strip():
        raise ValueError("Payment amount cannot be empty")

    amounts = []
    for item in input_str.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            amount = Decimal(item)
            if amount < 0:
                raise ValueError(f"Payment amount cannot be negative: {amount}")
            amounts.append(amount)
        except InvalidOperation:
            raise ValueError(f"Invalid payment amount: '{item}'")

    if not amounts:
        raise ValueError("No valid payment amounts found")
    return amounts


@mcp.tool()
def convert_to_kes(input_str: str) -> str:
    """
    Convert Upwork payment amounts from USD to Kenyan Shillings.
    Args:
        input_str: Payment amount(s) in USD. Single amount or comma-separated.
    Returns:
        Formatted conversion showing USD payout and equivalent KES amount.
    """
    try:
        amounts = parse_payment_amounts(input_str)
        total_usd = sum(amounts)
        after_fee = max(total_usd - Decimal(str(UPWORK_FEE)), Decimal("0"))
        after_rate = after_fee * Decimal(str(UPWORK_RATE))
        kes_amount = after_rate * Decimal(str(EXCHANGE_RATE))

        if len(amounts) > 1:
            amounts_str = " + ".join(f"${float(amt):.2f}" for amt in amounts)
            result = f"Payments: {amounts_str} = ${float(total_usd):.2f} total\n"
        else:
            result = f"Payment: ${float(total_usd):.2f}\n"

        result += f"KES equivalent: {float(kes_amount):.2f} KShs"
        return result

    except ValueError as e:
        error_msg = f"Error: {str(e)}"
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        return error_msg


def extract_number_from_text(text: str) -> Decimal:
    """Extract number from text, handling commas and mixed text/numbers."""
    text = text.lower().strip()
    number_pattern = r"[\d,]+(?:\.\d+)?"
    matches = re.findall(number_pattern, text)

    if not matches:
        raise ValueError("No valid number found in input")

    number_str = max(matches, key=lambda x: len(x.replace(",", "")))
    clean_number = number_str.replace(",", "")
    return Decimal(clean_number)


@mcp.tool()
def calculate_gross_needed(target_kes: str) -> str:
    """
    Calculate gross USD payment needed to receive target KES amount.
    Args:
        target_kes: Target amount in KES (e.g., "9000", "9,000", "I need 9,000").
    Returns:
        Gross USD payment needed from Upwork to achieve target KES.
    """
    try:
        target = extract_number_from_text(target_kes)
        if target <= 0:
            return "Error: Target KES amount must be positive"

        usd_after_rate = target / Decimal(str(EXCHANGE_RATE))
        usd_after_fee = usd_after_rate / Decimal(str(UPWORK_RATE))
        gross_usd_needed = usd_after_fee + Decimal(str(UPWORK_FEE))

        result = f"To receive {float(target):,.2f} KES:\n"
        result += f"Gross USD payment needed: ${float(gross_usd_needed):.2f}\n"
        result += f"After Upwork processing: {float(target):,.2f} KES"
        return result

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@mcp.tool()
def send_email(recipient: str, subject: str, body_html: str) -> str:
    """Send an HTML email using AWS SES."""
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, SENDER, REGION]):
        return "Error: Missing required AWS environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, SENDER, REGION)."

    ses_client = boto3.client(
        "ses",
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(retries={"max_attempts": 2, "mode": "standard"}),
    )

    formatted_sender = f"{SENDER_NAME} <{SENDER}>" if SENDER_NAME else SENDER

    email_data = {
        "Source": formatted_sender,
        "Destination": {"ToAddresses": [recipient]},
        "Message": {
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": body_html, "Charset": "UTF-8"}},
        },
    }

    try:
        response = ses_client.send_email(**email_data)
        return f"Email sent! Message ID: {response['MessageId']}"
    except ClientError as e:
        return f"Error sending email: {e.response['Error']['Message']}"


# Airtime functionality
COUNTRY_CODES = {"kenya": "+254"}
supported_countries = {
    "+254": {"name": "Kenya", "currency": "KES", "min_amount": 5, "max_amount": 10000}
}

africastalking.initialize(username, api_key)
airtime = africastalking.Airtime


def format_phone_number(phone_number):
    """Format phone number with Kenya country code."""
    phone_number = str(phone_number).strip()

    if user_country != "kenya":
        raise ValueError("Only Kenya is supported. Set country to 'kenya'.")

    country_code = COUNTRY_CODES["kenya"]

    if phone_number.startswith("0"):
        return country_code + phone_number[1:]
    elif phone_number.startswith("+254"):
        return phone_number
    else:
        return country_code + phone_number


@mcp.tool(description="Check the airtime balance for your account.")
async def check_balance() -> str:
    """Check Africa's Talking account balance."""
    try:
        response = africastalking.Application.fetch_application_data()
        if "UserData" in response and "balance" in response["UserData"]:
            return f"Account Balance: {response['UserData']['balance']}"
        return "Balance information not available at the moment. Try again later."
    except Exception as e:
        return f"Error fetching balance: {str(e)}"


@mcp.tool(description="Load airtime to a specified telephone number.")
async def load_airtime(phone_number: str, amount: float, currency_code: str) -> str:
    """Load airtime to a phone number."""
    try:
        if currency_code != "KES":
            return "Error: Only KES currency is supported for Kenya."

        if amount < 5 or amount > 10000:
            return "Error: Amount must be between 5 and 10,000 KES."

        formatted_number = format_phone_number(phone_number)

        airtime.send(
            phone_number=formatted_number, amount=amount, currency_code=currency_code
        )

        return (
            f"Successfully sent {currency_code} {amount} airtime to {formatted_number}"
        )
    except Exception as e:
        return f"Encountered error while sending airtime: {str(e)}"


@mcp.prompt()
async def airtime_transfer_assistant() -> str:
    """Assistant for planning and executing airtime transfers in Kenya."""
    return """You are an Africa's Talking Airtime Transfer Assistant for Kenya. Help users:

1. **Plan Airtime Transfers:**
   - Validate phone numbers with +254 country code
   - Suggest amounts between 5 and 10,000 KES
   - Check account balance before transfers
   - Provide currency conversion guidance for KES

2. **Best Practices:**
   - Always validate phone numbers first
   - Check account balance before large transfers

3. **Troubleshooting:**
   - Help diagnose failed transfers
   - Explain error messages
   - Suggest solutions for common issues

4. **Supported Country:**
   - Kenya (KES): +254 - Min: 5, Max: 10,000

Always prioritize user safety and account security. Recommend testing in sandbox mode first."""


@mcp.resource("africastalking://supported-countries")
async def get_supported_countries() -> str:
    """Get supported country (Kenya) and limits."""
    return json.dumps(
        {
            "supported_countries": supported_countries,
            "total_countries": len(supported_countries),
            "usage_note": "Use +254 prefix for Kenyan phone numbers",
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
