from datetime import datetime

from sqlalchemy.orm import Session

from models.notification import Notification


# =====================================================
# Seed GST Government Notifications
# =====================================================

def seed_notifications(db: Session):

    notifications = [

        {
            "title": (
                "Notification No. 11/2025-Central Tax"
            ),

            "message": (
                "The Central Government issued "
                "Notification No. 11/2025-Central Tax "
                "dated 27 March 2025, making the "
                "Second Amendment to the CGST Rules, 2017."
            ),

            "notification_number":
                "11/2025-Central Tax",

            "notification_date":
                datetime(2025, 3, 27),

            "type":
                "GST",

            "priority":
                "Medium",

            "source":
                "CBIC",

            "applicable_to":
                "GST Registered Taxpayers",

            "is_active":
                True,

        },

    ]


    added = 0

    skipped = 0


    for item in notifications:

        exists = (

            db.query(Notification)

            .filter(

                Notification.notification_number
                == item["notification_number"]

            )

            .first()

        )


        if exists:

            skipped += 1

            continue


        db.add(
            Notification(**item)
        )

        added += 1


    db.commit()


    print(
        "Notifications Added:",
        added
    )

    print(
        "Notifications Skipped:",
        skipped
    )

    print(
        "GST Notification Seed Completed."
    )
    # =====================================================
# Run Seeder
# =====================================================

if __name__ == "__main__":

    from core.database import SessionLocal

    db = SessionLocal()

    try:

        seed_notifications(db)

    finally:

        db.close()