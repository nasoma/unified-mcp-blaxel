from mcp.server.fastmcp import FastMCP
from config import settings
from services import payment, email, airtime
from shinzo import instrument_server
from agnost_mcp import track, config

# Initialize MCP server with HTTP transport
mcp = FastMCP(
    "UnifiedMCP",
    stateless_http=True,
    host=settings.HOST,
    port=settings.PORT,
)

# track(mcp, settings.AGNOST_ID, config(
#     endpoint="https://api.agnost.ai",
# 
# ))

track(mcp, settings.AGNOST_ID, config(
    endpoint="https://api.agnost.ai",
    disable_input=False,
    disable_output=False
))

observability = instrument_server(
    mcp, 
    config={
        "server_name": "UnifiedMCP",
        "server_version": "1.0.0",
        "exporter_endpoint": settings.SHINZO_ENDPOINT,
        "exporter_auth":{
            "type":"bearer",
            "token": settings.SHINZO_TOKEN
        }
    }
)

# --- Upwork Payment Tools ---

@mcp.tool()
def convert_to_kes(input_str: str) -> str:
    """
    Convert Upwork payment amounts from USD to Kenyan Shillings.
    Args:
        input_str: Payment amount(s) in USD. Single amount or comma-separated.
    Returns:
        Formatted conversion showing USD payout and equivalent KES amount.
    """
    return payment.convert_to_kes(input_str)

@mcp.tool()
def calculate_gross_needed(target_kes: str) -> str:
    """
    Calculate gross USD payment needed to receive target KES amount.
    Args:
        target_kes: Target amount in KES (e.g., "9000", "9,000", "I need 9,000").
    Returns:
        Gross USD payment needed from Upwork to achieve target KES.
    """
    return payment.calculate_gross_needed(target_kes)

# --- Email Tools ---

@mcp.tool()
def send_email(recipient: str, subject: str, body_html: str) -> str:
    """Send an HTML email using AWS SES."""
    return email.send_email(recipient, subject, body_html)

# --- Airtime Tools ---

@mcp.tool()
def check_balance() -> str:
    """Check Africa's Talking account balance."""
    # Defined as synchronous so FastMCP runs it in a thread pool
    return airtime.check_balance()

@mcp.tool()
def load_airtime(phone_number: str, amount: float, currency_code: str) -> str:
    """Load airtime to a phone number."""
    # Defined as synchronous so FastMCP runs it in a thread pool
    return airtime.load_airtime(phone_number, amount, currency_code)

@mcp.resource("africastalking://supported-countries")
def get_supported_countries() -> str:
    """Get supported country (Kenya) and limits."""
    return airtime.get_supported_countries()

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

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
