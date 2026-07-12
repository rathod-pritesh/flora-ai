from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index
)

from datetime import datetime

from sqlalchemy.orm import relationship

from app.db.database import Base


class AIHistory(Base):
    __tablename__ = "ai_history"

    __table_args__ = (
        Index("idx_ai_history_user_id", "user_id"),
        Index("idx_ai_history_category", "category"),
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )

    title = Column(String(255))

    input_text = Column(
        Text,
        nullable=False
    )

    output_text = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    user = relationship(
        "User",
        back_populates="history"
    )