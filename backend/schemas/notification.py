from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):

    business_id: Optional[int] = None

    title: str

    message: str

    type: str

    priority: str = "Medium"

    expires_at: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):

    title: Optional[str] = None

    message: Optional[str] = None

    priority: Optional[str] = None

    is_read: Optional[bool] = None

    expires_at: Optional[datetime] = None


class NotificationResponse(NotificationBase):

    id: int

    user_id: int

    is_read: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )