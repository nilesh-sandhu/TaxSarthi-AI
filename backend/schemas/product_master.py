from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Base Schema
# =====================================================

class ProductMasterBase(BaseModel):

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    category_id: int

    hsn_code: str = Field(
        ...,
        max_length=20,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# =====================================================
# Create
# =====================================================

class ProductMasterCreate(ProductMasterBase):
    pass


# =====================================================
# Update
# =====================================================

class ProductMasterUpdate(BaseModel):

    product_name: Optional[str] = None

    category_id: Optional[int] = None

    hsn_code: Optional[str] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================================
# Response
# =====================================================

class ProductMasterResponse(ProductMasterBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )