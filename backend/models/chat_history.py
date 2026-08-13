from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from core.database import Base


class ChatHistory(Base):

    __tablename__ = "chat_history"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # User
    # =====================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    # =====================================================
    # Chat Information
    # =====================================================

    role = Column(
        String(20),
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    # =====================================================
    # Metadata
    # =====================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    user = relationship(
        "User",
        back_populates="chat_history",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<ChatHistory(id={self.id}, role='{self.role}')>"
        )