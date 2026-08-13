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