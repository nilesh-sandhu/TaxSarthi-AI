from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Base Schema
# =====================================================

class BusinessProfileBase(BaseModel):

    business_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    owner_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    business_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    turnover: Decimal

    gstin: Optional[str] = Field(
        default=None,
        max_length=15,
    )

    registration_type: Optional[str] = None

    interstate: bool = False

    ecommerce: bool = False

    composition_scheme: bool = False

    business_status: str = "Active"


# =====================================================
# Create
# =====================================================

class BusinessProfileCreate(BusinessProfileBase):
    pass


# =====================================================
# Update
# =====================================================

class BusinessProfileUpdate(BaseModel):

    business_name: Optional[str] = None

    owner_name: Optional[str] = None

    business_type: Optional[str] = None

    state: Optional[str] = None

    turnover: Optional[Decimal] = None

    gstin: Optional[str] = None

    registration_type: Optional[str] = None

    interstate: Optional[bool] = None

    ecommerce: Optional[bool] = None

    composition_scheme: Optional[bool] = None

    business_status: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================================
# Response
# =====================================================

class BusinessProfileResponse(BusinessProfileBase):

    id: int

    user_id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )