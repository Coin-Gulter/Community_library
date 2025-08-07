import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using the SMTP configuration from settings.
    """
    # Create the email message
    message = MIMEMultipart()
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:

            # Login if credentials are provided
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, message.as_string())
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        # In a real application, better more robust error logging here
        print(f"Failed to send email to {to_email}: {e}")
