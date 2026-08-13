from datetime import datetime

from core.database import SessionLocal
from models.notification import Notification


notifications = [
    {
        "notification_number": "02/2026 - Central Tax",
        "title": "02/2026 - Central Tax",
        "message": (
            "Seeks to empower the Principal Bench of the Appellate Tribunal, "
            "New Delhi constituted under sub-section (3) of section 109 of "
            "the said Act to hear appeals made under section 101B of the said Act."
        ),
        "notification_date": datetime(2026, 5, 7),
        "type": "GST",
        "priority": "High",
        "source": "CBIC",
        "applicable_to": "GST Taxpayers",
        "is_active": True,
    },
    {
        "notification_number": "01/2026 - Central Tax",
        "title": "01/2026 - Central Tax",
        "message": (
            "Seeks to extend the due date for furnishing the return in "
            "FORM GSTR-3B for the month of March, 2026 till the twenty-first "
            "day of April, 2026."
        ),
        "notification_date": datetime(2026, 4, 21),
        "type": "GST",
        "priority": "High",
        "source": "CBIC",
        "applicable_to": "GST Taxpayers",
        "is_active": True,
    },
]


def seed_notifications():
    db = SessionLocal()

    added = 0
    skipped = 0

    try:
        for item in notifications:

            existing = (
                db.query(Notification)
                .filter(
                    Notification.notification_number
                    == item["notification_number"]
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            db.add(Notification(**item))
            added += 1

        db.commit()

        print("===================================")
        print("2026 GST Notifications Seeded")
        print("Added:", added)
        print("Skipped:", skipped)
        print("===================================")

    except Exception as e:
        db.rollback()
        print("ERROR:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_notifications()