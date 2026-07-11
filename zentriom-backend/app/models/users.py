from sqlalchemy import Column, Integer, String

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    google_id = Column(String, unique=True, nullable=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    picture = Column(String, nullable=True)

    password_hash = Column(String, nullable=True)