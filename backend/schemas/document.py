from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Base Schema
# =====================================================

class DocumentBase(BaseModel):

    document_name: str

    document_type: str

    business_id: Optional[int] = None


# =====================================================
# Upload Schema
# =====================================================

class DocumentCreate(DocumentBase):

    pass


# =====================================================
# Update Schema
# =====================================================

class DocumentUpdate(BaseModel):

    document_name: Optional[str] = None

    document_type: Optional[str] = None

    status: Optional[str] = None

    extracted_text: Optional[str] = None


# =====================================================
# Response Schema
# =====================================================

class DocumentResponse(DocumentBase):

    id: int

    user_id: int

    file_path: str

    extracted_text: Optional[str] = None

    status: str

    uploaded_at: datetime

    processed_at: Optional[datetime] = None

    created_at: datetime

    updated_at: datetime

    # Invoice analysis result
    analysis: Optional[dict[str, Any]] = None

    model_config = ConfigDict(
        from_attributes=True
    )