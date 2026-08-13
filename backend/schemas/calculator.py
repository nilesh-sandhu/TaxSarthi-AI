from pydantic import BaseModel


class GSTCalculatorRequest(BaseModel):

    amount: float
    gst_rate: float
    calculation_type: str
    interstate: bool = False


class GSTCalculatorResponse(BaseModel):

    taxable_amount: float
    gst_amount: float
    cgst: float
    sgst: float
    igst: float
    total_amount: float