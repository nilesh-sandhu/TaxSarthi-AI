from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Text,
)

from core.database import Base


class GSTRule(Base):

    __tablename__ = "gst_rules"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    rule_name = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    rule_value = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    effective_from = Column(
        Date,
        nullable=False,
    )

    effective_to = Column(
        Date,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

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

    def __repr__(self):

        return (
            f"<GSTRule("
            f"{self.rule_name}="
            f"{self.rule_value})>"
        )