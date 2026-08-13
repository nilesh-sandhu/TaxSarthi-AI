from typing import Literal

from pydantic import BaseModel, Field
from typing import List, Optional


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
    source: Optional[str] = None
    product: Optional[str] = None
    hsn: Optional[str] = None
    hsn_description: Optional[str] = None
    gst_rate: Optional[float] = None
    taxable_value: Optional[float] = None
    gst_amount: Optional[float] = None
    total_invoice_value: Optional[float] = None
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    igst: Optional[float] = None
    cess: Optional[float] = None
    notification_no: Optional[str] = None
    classification_required: Optional[bool] = None
    hsn_options: Optional[List[dict]] = None