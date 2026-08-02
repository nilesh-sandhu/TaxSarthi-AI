from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Create Product
# -----------------------------
class ProductCreate(BaseModel):
    name: str
    category: str
    gst_rate: float
    hsn_code: str
    description: str


# -----------------------------
# Update Product
# -----------------------------
class ProductUpdate(BaseModel):
    name: str
    category: str
    gst_rate: float
    hsn_code: str
    description: str


# -----------------------------
# Response
# -----------------------------
class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    gst_rate: float
    hsn_code: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True