from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.services.auth_service import verify_google_token
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
    )
from app.db.dependencies import get_db
from app.models.users import User

import random

from datetime import datetime, timedelta

from app.models.password_reset_otp import PasswordResetOTP
from app.models.signup_otp import SignupOTP

from app.services.email_service import send_otp_email
from app.services.otp_service import create_otp_record, verify_otp_code


router = APIRouter()

class GoogleLoginRequest(BaseModel):
    token: str
    
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class SignupSendOTPRequest(BaseModel):
    name: str
    email: str
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
class ForgotPasswordRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str
    
class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    password: str

@router.post("/auth/google")
def google_login(data: GoogleLoginRequest, db: Session = Depends(get_db)):
    print("Received token:", data.token[:50])
    
    user_info = verify_google_token(data.token)
    
    user = db.query(User).filter(
        User.email == user_info["email"]
    ).first()
    
    if user:
        if not user.google_id:
            user.google_id = user_info["google_id"]
        if user_info.get("picture"):
            user.picture = user_info["picture"]
        user.name = user_info["name"]
    else:
        user = User(
            google_id=user_info["google_id"],
            email=user_info["email"],
            name=user_info["name"],
            picture=user_info.get("picture")
        )
        db.add(user)
        
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered with another account."
        )
    
    token = create_access_token(
        str(user.id)
    )
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "picture": user.picture
        }
    }
    
@router.post("/auth/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    otp_record = (
        db.query(SignupOTP)
        .filter(
            SignupOTP.email == data.email,
            SignupOTP.verified == True
        )
        .first()
    )
    
    if not otp_record:
        raise HTTPException(
            status_code=400,
            detail="Email not verified"
        )
        
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=400,
            detail="Verification code expired"
        )
        
    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(
            data.password
        )
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    db.delete(otp_record)
    db.commit()
    
    token = create_access_token(
        str(user.id)
    )
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "picture": user.picture
        }
    }
    
@router.post("/auth/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )
    
    if (
        not user
        or not user.password_hash
        or not verify_password(
            data.password,
            user.password_hash
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    token = create_access_token(
        str(user.id)
    )
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "picture": user.picture
        }
    }
    
@router.post("/auth/signup/send-otp")
def signup_send_otp(
    data: SignupSendOTPRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    otp = create_otp_record(db, SignupOTP, data.email)
    
    try:
        send_otp_email(
            data.email,
            otp,
            subject="Email Verification OTP"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unable to send verification code."
        )
    
    return {
        "success": True,
        "message": "Verification code sent."
    }

@router.post("/auth/signup/verify-otp")
def signup_verify_otp(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    try:
        otp_record = verify_otp_code(db, SignupOTP, data.email, data.otp)
    except HTTPException as e:
        if e.detail == "OTP expired":
            raise HTTPException(status_code=400, detail="Verification code expired.")
        elif e.detail == "Invalid OTP" or e.detail == "OTP not found":
            raise HTTPException(status_code=400, detail="Invalid verification code.")
        raise e
        
    otp_record.verified = True
    db.commit()
    
    return {
        "success": True,
        "message": "Email verified successfully."
    }

@router.post("/auth/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    otp = create_otp_record(db, PasswordResetOTP, data.email)
    
    send_otp_email(
        data.email,
        otp
    )
    
    return {
        "success": True,
        "message": "OTP sent successfully"
    }
    
@router.post("/auth/verify-otp")
def verify_otp(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    verify_otp_code(db, PasswordResetOTP, data.email, data.otp)
    return {
        "success": True
    }
    
@router.post("/auth/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    otp_record = verify_otp_code(db, PasswordResetOTP, data.email, data.otp)
    
    user = (
        db.query(User)
        .filter(
            User.email == data.email
        )
        .first()
    )
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    user.password_hash = hash_password(
        data.password
    )
    
    db.commit()
    
    db.delete(otp_record)
    
    db.commit()
    
    return {
        "success": True,
        "message": "Password reset successful"
    }