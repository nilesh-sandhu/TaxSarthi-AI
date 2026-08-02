from pydantic import BaseModel
from datetime import datetime


class NotificationCreate(BaseModel):
    notification_no: str
    title: str
    summary: str
    issue_date: str
    pdf_link: str | None = None


class NotificationUpdate(BaseModel):
    notification_no: str
    title: str
    summary: str
    issue_date: str
    pdf_link: str | None = None


class NotificationResponse(BaseModel):
    id: int
    notification_no: str
    title: str
    summary: str
    issue_date: str
    pdf_link: str | None
    created_at: datetime

    class Config:
        from_attributes = True