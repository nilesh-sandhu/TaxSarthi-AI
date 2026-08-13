from pydantic import BaseModel


class RegistrationAdvisorResponse(BaseModel):

    gst_required: bool

    registration_type: str

    reason: str

    recommended_returns: list[str]

    next_steps: list[str]