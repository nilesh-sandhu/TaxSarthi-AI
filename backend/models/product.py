from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    gst_rate = Column(Float, nullable=False)
    hsn_code = Column(String(20), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)