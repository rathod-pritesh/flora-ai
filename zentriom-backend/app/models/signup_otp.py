from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.db.database import Base

class SignupOTP(Base):
    __tablename__ = "signup_otps"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    otp_code = Column(String(4), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    verified = Column(Boolean, default=False, nullable=False)
