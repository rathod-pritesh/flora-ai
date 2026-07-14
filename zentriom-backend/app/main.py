from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.grammer import router as grammer_router
from app.api.linkedin import router as linkedin_router
from app.api.code_explainer import router as code_explainer_router

from app.api.history import router as history_router

from app.db.database import engine, Base
from app.models.users import User
from app.models.password_reset_otp import PasswordResetOTP
from app.models.signup_otp import SignupOTP
from app.models.ai_history import AIHistory

app = FastAPI(
    docs_url=None if os.getenv("APP_ENV") == "production" else "/docs",
    redoc_url=None if os.getenv("APP_ENV") == "production" else "/redocs",
    openapi_url=None if os.getenv("APP_ENV") == "production" else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://zentriom-ai.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(grammer_router)
app.include_router(linkedin_router)
app.include_router(code_explainer_router)
app.include_router(history_router)

@app.get("/")
def root():
    return {"message": "Zentriom Backend Running!!"}