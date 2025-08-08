import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using an SMTP connection upgraded with STARTTLS.
    """
    if not settings.SMTP_SERVER:
        print("SMTP settings not configured. Skipping email.")
        return

    message = MIMEMultipart()
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server using a standard SMTP connection.
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)

        # --- THIS IS THE CRUCIAL FIX ---
        # Upgrade the connection to a secure one using STARTTLS.
        server.starttls()

        # Login if credentials are provided.
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        # Send the email and close the connection.
        server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, message.as_string())
        server.quit()

        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
