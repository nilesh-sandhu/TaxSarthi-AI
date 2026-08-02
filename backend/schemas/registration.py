from pydantic import BaseModel


class RegistrationRequest(BaseModel):
    annual_turnover: float
    state: str
    business_type: str
    interstate_supply: bool


class RegistrationResponse(BaseModel):
    gst_required: bool
    reason: str
    threshold_limit: float