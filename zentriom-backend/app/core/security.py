from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES
)

def create_access_token(user_id: str):
    
    expire = datetime.utcnow() + timedelta(
        minutes=JWT_EXPIRE_MINUTES
    )
    
    payload = {
        "sub": user_id,
        "exp": expire
    }
    
    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )