from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GSTRuleBase(BaseModel):

    rule_name: str

    rule_value: str

    description: Optional[str] = None

    effective_from: date

    effective_to: Optional[date] = None


class GSTRuleCreate(GSTRuleBase):
    pass


class GSTRuleUpdate(BaseModel):

    rule_name: Optional[str] = None

    rule_value: Optional[str] = None

    description: Optional[str] = None

    effective_from: Optional[date] = None

    effective_to: Optional[date] = None

    is_active: Optional[bool] = None


class GSTRuleResponse(GSTRuleBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )