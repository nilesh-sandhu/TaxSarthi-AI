from sqlalchemy.orm import Session

from models.notification import Notification
from schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)


class NotificationRepository:

    @staticmethod
    def create(
        db: Session,
        notification: NotificationCreate,
        user_id: int,
    ):

        obj = Notification(
            user_id=user_id,
            **notification.model_dump()
        )

        db.add(obj)

        db.commit()

        db.refresh(obj)

        return obj

    @staticmethod
    def get_all(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        notification_id: int,
    ):

        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        notification: Notification,
        data: NotificationUpdate,
    ):

        values = data.model_dump(
            exclude_unset=True
        )

        for key, value in values.items():

            setattr(notification, key, value)

        db.commit()

        db.refresh(notification)

        return notification

    @staticmethod
    def delete(
        db: Session,
        notification: Notification,
    ):

        db.delete(notification)

        db.commit()