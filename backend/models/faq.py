from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from core.database import Base


class FAQ(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(String(500), nullable=False)

    answer = Column(String(2000), nullable=False)

    category = Column(String(100), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)