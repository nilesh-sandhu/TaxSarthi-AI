from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CircularBase(BaseModel):

    circular_no: str

    title: str

    subject: Optional[str] = None

    description: str

    issue_date: date

    reference: Optional[str] = None


class CircularCreate(CircularBase):
    pass


class CircularUpdate(BaseModel):

    title: Optional[str] = None

    subject: Optional[str] = None

    description: Optional[str] = None

    issue_date: Optional[date] = None

    reference: Optional[str] = None

    is_active: Optional[bool] = None


class CircularResponse(CircularBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )