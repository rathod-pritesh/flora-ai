from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.grammer import router as grammer_router
from app.api.linkedin import router as linkedin_router

from app.db.database import engine, Base
from app.models.users import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

User.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(grammer_router)
app.include_router(linkedin_router)

@app.get("/")
def root():
    return {"message": "Zentriom Backend Running!!"}