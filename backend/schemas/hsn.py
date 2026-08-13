from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Base Schema
# =====================================================

class HSNBase(BaseModel):

    hsn_code: str = Field(
        ...,
        min_length=4,
        max_length=20,
    )

    category_id: int

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
    )


# =====================================================
# Create Schema
# =====================================================

class HSNCreate(HSNBase):
    pass


# =====================================================
# Update Schema
# =====================================================

class HSNUpdate(BaseModel):

    hsn_code: Optional[str] = None

    category_id: Optional[int] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================================
# Response Schema
# =====================================================

class HSNResponse(HSNBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )