from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Create FAQ
# -----------------------------
class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str


# -----------------------------
# Update FAQ
# -----------------------------
class FAQUpdate(BaseModel):
    question: str
    answer: str
    category: str


# -----------------------------
# FAQ Response
# -----------------------------
class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True