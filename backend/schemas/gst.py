from typing import Literal

from pydantic import BaseModel, Field


class GSTCalculationRequest(BaseModel):
    amount: float = Field(..., ge=0)
    gst_rate: float = Field(..., ge=0)
    calculation_type: Literal["exclusive", "inclusive"] = "exclusive"
    interstate: bool = False


class GSTCalculationResponse(BaseModel):
    calculation_type: str
    interstate: bool

    base_amount: float
    gst_rate: float
    gst_amount: float

    cgst: float
    sgst: float
    igst: float

    total_amount: float


class ProductGSTRequest(BaseModel):
    product_name: str
    amount: float = 0.0
    interstate: bool = False


class ProductGSTResponse(BaseModel):
    success: bool
    source: str | None = None
    product: str | None = None
    hsn: str | None = None
    hsn_description: str | None = None
    gst_rate: float | None = None
    taxable_value: float | None = None
    gst_amount: float | None = None
    total_invoice_value: float | None = None
    cgst: float | None = None
    sgst: float | None = None
    igst: float | None = None
    cess: float | None = None
    notification_no: str | None = None
    classification_required: bool | None = None
    hsn_options: list | None = None