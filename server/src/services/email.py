import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from config import settings

# Initialize client lazily or at module level if settings are available
_ses_client = None

def get_ses_client():
    global _ses_client
    if _ses_client is None:
        if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.REGION]):
            return None
        
        _ses_client = boto3.client(
            "ses",
            region_name=settings.REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(
                retries={"max_attempts": settings.SES_MAX_ATTEMPTS, "mode": "standard"},
                connect_timeout=settings.SES_CONNECT_TIMEOUT,
                read_timeout=settings.SES_READ_TIMEOUT,
            ),
        )
    return _ses_client

def send_email(recipient: str, subject: str, body_html: str) -> str:
    """Send an HTML email using AWS SES."""
    if not settings.SENDER:
         return "Error: Missing SENDER configuration."

    ses_client = get_ses_client()
    if not ses_client:
        return "Error: Missing required AWS environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION)."

    formatted_sender = f"{settings.SENDER_NAME} <{settings.SENDER}>" if settings.SENDER_NAME else settings.SENDER

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
