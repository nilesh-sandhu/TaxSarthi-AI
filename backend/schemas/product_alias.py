from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Base Schema
# =====================================================

class ProductAliasBase(BaseModel):

    product_id: int

    alias: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )


# =====================================================
# Create
# =====================================================

class ProductAliasCreate(ProductAliasBase):
    pass


# =====================================================
# Update
# =====================================================

class ProductAliasUpdate(BaseModel):

    product_id: Optional[int] = None

    alias: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================================
# Response
# =====================================================

class ProductAliasResponse(ProductAliasBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )