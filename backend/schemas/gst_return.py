from pydantic import BaseModel
from datetime import datetime


class GSTReturnCreate(BaseModel):
    return_name: str
    description: str
    due_date: str
    frequency: str
    late_fee: str


class GSTReturnUpdate(BaseModel):
    return_name: str
    description: str
    due_date: str
    frequency: str
    late_fee: str


class GSTReturnResponse(BaseModel):
    id: int
    return_name: str
    description: str
    due_date: str
    frequency: str
    late_fee: str
    created_at: datetime

    class Config:
        from_attributes = True