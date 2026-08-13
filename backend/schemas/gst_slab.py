from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GSTSlabBase(BaseModel):

    hsn_id: int

    gst_rate: float

    cgst: float

    sgst: float

    igst: float

    cess: float = 0

    notification_no: Optional[str] = None

    effective_from: date

    effective_to: Optional[date] = None


class GSTSlabCreate(GSTSlabBase):
    pass


class GSTSlabUpdate(BaseModel):

    gst_rate: Optional[float] = None

    cgst: Optional[float] = None

    sgst: Optional[float] = None

    igst: Optional[float] = None

    cess: Optional[float] = None

    notification_no: Optional[str] = None

    effective_from: Optional[date] = None

    effective_to: Optional[date] = None

    is_active: Optional[bool] = None


class GSTSlabResponse(GSTSlabBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )