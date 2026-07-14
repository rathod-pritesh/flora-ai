# import smtplib

# from email.mime.text import MIMEText

from app.core.config import (
#     SMTP_SERVER,
#     SMTP_PORT,
#     SMTP_EMAIL,
#     SMTP_PASSWORD
    RESEND_API_KEY
)
import resend


def send_otp_email(
    email: str,
    otp: str,
    subject: str = "Verification Code"
):
    resend.Emails.send({
        "from": "Zentriom <onboarding@resend.dev>",
        "to": [email],
        "subject": subject,
        "html": f"""
        <div style="font-family: Arial, sans-serif;">
            <h2>Zentriom Verification Code</h2>

            <p>Your verification code is:</p>

            <h1>{otp}</h1>

            <p>This code will expire shortly.</p>
        </div>
        """
    })