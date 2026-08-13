from datetime import date

from sqlalchemy.orm import Session

from models.circular import Circular


# =====================================================
# Seed GST Government Circulars
# =====================================================

def seed_circulars(db: Session):

    circulars = [

        {
            "circular_no": "Circular-01-GST",

            "title": (
                "GST Circular - General Compliance Guidance"
            ),

            "subject": (
                "GST compliance and taxpayer guidance"
            ),

            "description": (
                "This circular record is maintained in "
                "TaxSarthi AI for GST compliance reference."
            ),

            "issue_date": date(2025, 3, 27),

            "reference": (
                "CBIC GST Circular Repository"
            ),

            "is_active": True,
        },

    ]

    added = 0
    skipped = 0

    for item in circulars:

        exists = (
            db.query(Circular)
            .filter(
                Circular.circular_no
                == item["circular_no"]
            )
            .first()
        )

        if exists:
            skipped += 1
            continue

        db.add(
            Circular(**item)
        )

        added += 1

    db.commit()

    print(
        "Circulars Added:",
        added
    )

    print(
        "Circulars Skipped:",
        skipped
    )

    print(
        "GST Circular Seed Completed."
    )


# =====================================================
# Run Seeder
# =====================================================

if __name__ == "__main__":

    from core.database import SessionLocal

    db = SessionLocal()

    try:
        seed_circulars(db)

    finally:
        db.close()