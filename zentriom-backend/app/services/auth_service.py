from google.oauth2 import id_token
from google.auth.transport import requests

from app.core.config import GOOGLE_CLIENT_ID

def verify_google_token(token: str):
    user_info = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=10
    )
    
    return {
        "google_id": user_info["sub"],
        "email": user_info["email"],
        "name": user_info.get("name"),
        "picture": user_info.get("picture")
    }
    