from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    notification_no = Column(String(100), unique=True, nullable=False)

    title = Column(String(500), nullable=False)

    summary = Column(String(2000), nullable=False)

    issue_date = Column(String(100), nullable=False)

    pdf_link = Column(String(1000), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)