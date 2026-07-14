import smtplib

from email.mime.text import MIMEText

from app.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_EMAIL,
    SMTP_PASSWORD
)

def send_otp_email(
    email: str,
    otp: str,
    subject: str = "Password Reset OTP"
):
    msg = MIMEText(
        f"Your OTP is: {otp}"
    )
    
    msg["Subject"] = subject
    
    msg["From"] = SMTP_EMAIL
    
    msg["To"] = email
    
    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:
        
        server.starttls()
        
        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )
        
        server.send_message(msg)