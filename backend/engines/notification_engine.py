from sqlalchemy.orm import Session

from models.notification import Notification


# =====================================================
# Latest Government Notifications
# =====================================================

def latest_notifications(
    db: Session,
    limit: int = 10,
):

    notifications = (
        db.query(Notification)
        .filter(
            Notification.is_active == True
        )
        .order_by(
            Notification.notification_date.desc(),
            Notification.created_at.desc(),
        )
        .limit(limit)
        .all()
    )

    return [
        notification_summary(notification)
        for notification in notifications
    ]


# =====================================================
# Search Notifications
# =====================================================

def search_notification(
    keyword: str,
    db: Session,
    limit: int = 5,
):

    notifications = (
        db.query(Notification)
        .filter(
            Notification.is_active == True,
            Notification.title.ilike(
                f"%{keyword}%"
            ),
        )
        .order_by(
            Notification.notification_date.desc()
        )
        .limit(limit)
        .all()
    )

    return [
        notification_summary(notification)
        for notification in notifications
    ]


# =====================================================
# Notification Summary
# =====================================================

def notification_summary(notification):

    return {

        "id":
            notification.id,

        "title":
            notification.title,

        "message":
            notification.message,

        "notification_number":
            notification.notification_number,

        "notification_date":
            notification.notification_date,

        "type":
            notification.type,

        "priority":
            notification.priority,

        "source":
            notification.source,

        "applicable_to":
            notification.applicable_to,

    }