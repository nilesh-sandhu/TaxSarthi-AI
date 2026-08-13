from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)

from services.notification import (
    create_notification,
    get_notifications,
    get_notification,
    update_notification,
    delete_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("/", response_model=NotificationResponse)
def add_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):

    user_id = 1  # TODO: Replace with authenticated user

    return create_notification(
        notification,
        user_id,
        db,
    )


@router.get("/", response_model=list[NotificationResponse])
def all_notifications(
    db: Session = Depends(get_db),
):

    user_id = 1

    return get_notifications(
        user_id,
        db,
    )


@router.get("/{notification_id}", response_model=NotificationResponse)
def single_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):

    return get_notification(
        notification_id,
        db,
    )


@router.put("/{notification_id}", response_model=NotificationResponse)
def edit_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
):

    return update_notification(
        notification_id,
        notification,
        db,
    )


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):

    return delete_notification(
        notification_id,
        db,
    )