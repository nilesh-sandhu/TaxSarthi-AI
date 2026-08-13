from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):

    __tablename__ = "users"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # User Information
    # =====================================================

    full_name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    mobile = Column(
        String(20),
        unique=True,
        nullable=False,
    )

    hashed_password = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(20),
        default="user",
        nullable=False,
    )

    # =====================================================
    # Common Fields
    # =====================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================
    documents = relationship(
    "Document",
    back_populates="user",
    cascade="all, delete-orphan",
    )
    
    business_profiles = relationship(
        "BusinessProfile",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    chat_history = relationship(
        "ChatHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<User(id={self.id}, email='{self.email}')>"
        )