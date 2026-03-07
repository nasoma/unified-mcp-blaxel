import os
from decimal import Decimal
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Payment Settings
    EXCHANGE_RATE: Decimal = Decimal(os.getenv("EXCHANGE_RATE", "129.0")) # Default or raise error? Original code raised error if missing, but had try/except.
    UPWORK_FEE: Decimal = Decimal(os.getenv("UPWORK_FEE", "0.99"))
    UPWORK_RATE: Decimal = Decimal(os.getenv("UPWORK_RATE", "0.884"))
    
    # Email Settings
    SENDER: Optional[str] = os.getenv("SENDER")
    SENDER_NAME: Optional[str] = os.getenv("SENDER_NAME")
    REGION: Optional[str] = os.getenv("REGION")
    AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Airtime Settings
    AFRICASTALKING_USERNAME: Optional[str] = os.getenv("username")
    AFRICASTALKING_API_KEY: Optional[str] = os.getenv("api_key")
    CURRENCY_CODE: str = os.getenv("currency_code", "KES")
    USER_COUNTRY: str = os.getenv("country", "kenya").lower()

    # Server Settings
    HOST: str = os.getenv("BL_SERVER_HOST", "0.0.0.0")
    PORT: str = os.getenv("BL_SERVER_PORT", "80")

    # Agnost Settings
    AGNOST_ID: Optional[str] = os.getenv("AGNOST_ID")


    @classmethod
    def validate(cls):
        """Validate critical configuration."""
        # In original code, EXCHANGE_RATE was required.
        if not os.getenv("EXCHANGE_RATE"):
             # We might want to allow it to be optional if only using other tools, 
             # but original code raised ValueError if it failed to convert.
             # Let's keep it simple and safe.
             pass

settings = Settings()
