from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# =====================================================
# Base
# =====================================================

class InvoiceAnalysisBase(BaseModel):

    invoice_number: Optional[str] = None

    supplier: Optional[str] = None

    gstin: Optional[str] = None

    invoice_date: Optional[str] = None

    total_amount: Optional[float] = None

    risk_score: int = 100

    validation_status: str = "Pending"

    recommendations: Optional[str] = None

    errors: Optional[str] = None


# =====================================================
# Create
# =====================================================

class InvoiceAnalysisCreate(
    InvoiceAnalysisBase
):

    document_id: int


# =====================================================
# Update
# =====================================================

class InvoiceAnalysisUpdate(BaseModel):

    risk_score: Optional[int] = None

    validation_status: Optional[str] = None

    recommendations: Optional[str] = None

    errors: Optional[str] = None


# =====================================================
# Response
# =====================================================

class InvoiceAnalysisResponse(
    InvoiceAnalysisBase
):

    id: int

    document_id: int

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True