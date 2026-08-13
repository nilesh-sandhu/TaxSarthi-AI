from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComplianceBase(BaseModel):

    title: str

    description: str

    compliance_type: str

    due_days: Optional[int] = None

    priority: str = "Medium"


class ComplianceCreate(ComplianceBase):
    pass


class ComplianceUpdate(BaseModel):

    title: Optional[str] = None

    description: Optional[str] = None

    compliance_type: Optional[str] = None

    due_days: Optional[int] = None

    priority: Optional[str] = None

    is_active: Optional[bool] = None


class ComplianceResponse(ComplianceBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )