from pydantic import BaseModel
from typing import Literal


class GSTCalculationRequest(BaseModel):
    amount: float
    gst_rate: float
    calculation_type: Literal["exclusive", "inclusive"]


class GSTCalculationResponse(BaseModel):
    calculation_type: str
    base_amount: float
    gst_rate: float
    gst_amount: float
    cgst: float
    sgst: float
    igst: float
    total_amount: float