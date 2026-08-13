from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PenaltyBase(BaseModel):

    penalty_type: str

    title: str

    description: str

    amount: Optional[float] = None

    applicable_section: Optional[str] = None


class PenaltyCreate(PenaltyBase):
    pass


class PenaltyUpdate(BaseModel):

    penalty_type: Optional[str] = None

    title: Optional[str] = None

    description: Optional[str] = None

    amount: Optional[float] = None

    applicable_section: Optional[str] = None

    is_active: Optional[bool] = None


class PenaltyResponse(PenaltyBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )