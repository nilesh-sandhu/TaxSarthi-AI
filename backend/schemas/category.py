from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Base Schema
# =====================================================

class CategoryBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Electronics"],
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        examples=["Electronic products and accessories"],
    )


# =====================================================
# Create
# =====================================================

class CategoryCreate(CategoryBase):
    pass


# =====================================================
# Update
# =====================================================

class CategoryUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    is_active: Optional[bool] = None


# =====================================================
# Response
# =====================================================

class CategoryResponse(CategoryBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )