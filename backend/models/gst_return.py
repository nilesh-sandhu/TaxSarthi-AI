from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from core.database import Base


class GSTReturn(Base):
    __tablename__ = "gst_returns"

    id = Column(Integer, primary_key=True, index=True)

    return_name = Column(String(100), nullable=False)

    description = Column(String(1000), nullable=False)

    due_date = Column(String(100), nullable=False)

    frequency = Column(String(100), nullable=False)

    late_fee = Column(String(100), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)