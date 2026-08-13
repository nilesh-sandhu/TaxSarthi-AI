from pydantic import BaseModel


class ReturnAdvisorRequest(BaseModel):
    registration_type: str


class ReturnAdvisorResponse(BaseModel):
    registration_type: str
    returns: list
    recommendation: str