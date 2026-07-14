from datetime import datetime, timedelta
import random
from fastapi import HTTPException
from sqlalchemy.orm import Session

def generate_otp() -> str:
    return str(random.randint(1000, 9999))

def create_otp_record(db: Session, model_class, email: str, expires_minutes: int = 10) -> str:
    # Delete existing OTP records for this email
    db.query(model_class).filter(model_class.email == email).delete()
    
    # Generate new OTP
    otp = generate_otp()
    
    # Create new record
    otp_record = model_class(
        email=email,
        otp_code=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=expires_minutes)
    )
    db.add(otp_record)
    db.commit()
    return otp

def verify_otp_code(db: Session, model_class, email: str, otp: str):
    otp_record = (
        db.query(model_class)
        .filter(model_class.email == email)
        .first()
    )
    
    if not otp_record:
        raise HTTPException(
            status_code=404,
            detail="OTP not found"
        )
        
    if otp_record.otp_code != otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )
        
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=400,
            detail="OTP expired"
        )
        
    return otp_record
