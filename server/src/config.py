import os
import logging
from decimal import Decimal
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Settings:
    # Payment Settings
    EXCHANGE_RATE: Decimal = Decimal(os.getenv("EXCHANGE_RATE", "129.0"))
    UPWORK_FEE: Decimal = Decimal(os.getenv("UPWORK_FEE", "0.99"))
    UPWORK_RATE: Decimal = Decimal(os.getenv("UPWORK_RATE", "0.884"))

    # Email Settings
    SENDER: Optional[str] = os.getenv("SENDER")
    SENDER_NAME: Optional[str] = os.getenv("SENDER_NAME")
    REGION: Optional[str] = os.getenv("REGION")
    AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get("AWS_SECRET_ACCESS_KEY")
    SES_MAX_ATTEMPTS: int = int(os.getenv("SES_MAX_ATTEMPTS", "2"))
    SES_CONNECT_TIMEOUT: int = int(os.getenv("SES_CONNECT_TIMEOUT", "10"))
    SES_READ_TIMEOUT: int = int(os.getenv("SES_READ_TIMEOUT", "30"))

    # Airtime Settings
    AFRICASTALKING_USERNAME: Optional[str] = os.getenv("username")
    AFRICASTALKING_API_KEY: Optional[str] = os.getenv("api_key")
    CURRENCY_CODE: str = os.getenv("currency_code", "KES")
    USER_COUNTRY: str = os.getenv("country", "kenya").lower()

    # Server Settings
    HOST: str = os.getenv("BL_SERVER_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("BL_SERVER_PORT", "80"))

    # Agnost Settings
    AGNOST_ID: Optional[str] = os.getenv("AGNOST_ID")

    # Shinzo Settings
    SHINZO_TOKEN: Optional[str] = os.getenv("SHINZO_TOKEN")

    @classmethod
    def validate(cls) -> None:
        """
        Validate configuration at startup.
        Raises RuntimeError for invalid payment settings.
        Logs warnings for missing optional service credentials.
        """
        # Payment rates must be positive
        if cls.EXCHANGE_RATE <= 0:
            raise RuntimeError(f"EXCHANGE_RATE must be positive, got: {cls.EXCHANGE_RATE}")
        if cls.UPWORK_RATE <= 0:
            raise RuntimeError(f"UPWORK_RATE must be positive, got: {cls.UPWORK_RATE}")
        if cls.UPWORK_FEE < 0:
            raise RuntimeError(f"UPWORK_FEE cannot be negative, got: {cls.UPWORK_FEE}")

        # Warn about missing optional service credentials
        email_vars = [cls.SENDER, cls.AWS_ACCESS_KEY_ID, cls.AWS_SECRET_ACCESS_KEY, cls.REGION]
        if not all(email_vars):
            missing = [name for name, val in [
                ("SENDER", cls.SENDER),
                ("AWS_ACCESS_KEY_ID", cls.AWS_ACCESS_KEY_ID),
                ("AWS_SECRET_ACCESS_KEY", cls.AWS_SECRET_ACCESS_KEY),
                ("REGION", cls.REGION),
            ] if not val]
            logger.warning("Email service unavailable — missing: %s", ", ".join(missing))

        airtime_vars = [cls.AFRICASTALKING_USERNAME, cls.AFRICASTALKING_API_KEY]
        if not all(airtime_vars):
            missing = [name for name, val in [
                ("username", cls.AFRICASTALKING_USERNAME),
                ("api_key", cls.AFRICASTALKING_API_KEY),
            ] if not val]
            logger.warning("Airtime service unavailable — missing: %s", ", ".join(missing))

settings = Settings()
