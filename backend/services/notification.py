from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.notification import NotificationRepository
from schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)


def create_notification(
    notification: NotificationCreate,
    user_id: int,
    db: Session,
):

    return NotificationRepository.create(
        db,
        notification,
        user_id,
    )


def get_notifications(
    user_id: int,
    db: Session,
):

    return NotificationRepository.get_all(
        db,
        user_id,
    )


def get_notification(
    notification_id: int,
    db: Session,
):

    notification = NotificationRepository.get_by_id(
        db,
        notification_id,
    )

    if not notification:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    return notification


def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    db: Session,
):

    notification = NotificationRepository.get_by_id(
        db,
        notification_id,
    )

    if not notification:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    return NotificationRepository.update(
        db,
        notification,
        data,
    )


def delete_notification(
    notification_id: int,
    db: Session,
):

    notification = NotificationRepository.get_by_id(
        db,
        notification_id,
    )

    if not notification:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    NotificationRepository.delete(
        db,
        notification,
    )

    return {
        "message": "Notification deleted successfully."
    }