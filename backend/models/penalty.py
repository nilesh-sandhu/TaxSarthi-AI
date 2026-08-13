from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from core.database import Base


class Penalty(Base):

    __tablename__ = "penalties"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    penalty_type = Column(
        String(255),
        nullable=False,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=True,
    )

    applicable_section = Column(
        String(100),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )