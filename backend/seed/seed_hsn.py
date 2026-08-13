from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.hsn import HSNMaster
from models.category import Category


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "hsn_master.csv"


def seed_hsn():

    db: Session = SessionLocal()

    inserted = 0
    skipped = 0
    duplicate_csv = 0
    categories_created = 0

    try:

        if not CSV_PATH.exists():
            print(f"❌ HSN file not found: {CSV_PATH}")
            return

        df = pd.read_csv(
            CSV_PATH,
            dtype=str,
        ).fillna("")

        print(f"📄 HSN rows found: {len(df)}")

        required_columns = {
            "hsn_code",
            "description",
        }

        if not required_columns.issubset(df.columns):

            print("❌ Invalid HSN CSV")
            print("Required:", required_columns)
            print("Found:", list(df.columns))

            return

        # =====================================================
        # REMOVE DUPLICATE HSN CODES FROM CSV
        # =====================================================

        df["hsn_code"] = (
            df["hsn_code"]
            .astype(str)
            .str.strip()
        )

        df["description"] = (
            df["description"]
            .astype(str)
            .str.strip()
        )

        before = len(df)

        df = df[
            df["hsn_code"] != ""
        ]

        df = df.drop_duplicates(
            subset=["hsn_code"],
            keep="first",
        )

        duplicate_csv = (
            before
            - len(df)
        )

        print(
            f"🔄 Duplicate CSV rows removed: "
            f"{duplicate_csv}"
        )

        # =====================================================
        # EXISTING DATABASE CODES
        # =====================================================

        existing_codes = {
            row[0]
            for row in db.query(
                HSNMaster.hsn_code
            ).all()
        }

        print(
            f"🗄️ Existing HSN records: "
            f"{len(existing_codes)}"
        )

        # =====================================================
        # INSERT
        # =====================================================

        for _, row in df.iterrows():

            hsn_code = row[
                "hsn_code"
            ].strip()

            description = row[
                "description"
            ].strip()

            if not hsn_code:
                skipped += 1
                continue

            # -------------------------------------------------
            # Already in database
            # -------------------------------------------------

            if hsn_code in existing_codes:

                skipped += 1
                continue

            # -------------------------------------------------
            # Find / Create Category
            # -------------------------------------------------

            chapter = hsn_code[:2]

            category_name = (
                f"HSN Chapter {chapter}"
            )

            category = (
                db.query(Category)
                .filter(
                    Category.name
                    == category_name
                )
                .first()
            )

            if category is None:

                category = Category(
                    name=category_name,
                    description=(
                        f"HSN Chapter {chapter}"
                    ),
                )

                db.add(category)
                db.flush()

                categories_created += 1

            # -------------------------------------------------
            # Insert HSN
            # -------------------------------------------------

            hsn = HSNMaster(
                hsn_code=hsn_code,
                description=description,
                category_id=category.id,
                is_active=True,
            )

            db.add(hsn)

            # IMPORTANT:
            # Add immediately to our local set so a duplicate
            # cannot be inserted during this same run.

            existing_codes.add(
                hsn_code
            )

            inserted += 1

            # -------------------------------------------------
            # Batch Commit
            # -------------------------------------------------

            if inserted % 500 == 0:

                db.commit()

                print(
                    f"⏳ Inserted so far: "
                    f"{inserted}"
                )

        db.commit()

        print()
        print(
            "======================================"
        )
        print(
            "✅ HSN SEED COMPLETED"
        )
        print(
            "======================================"
        )
        print(
            f"HSN Inserted       : {inserted}"
        )
        print(
            f"HSN Skipped        : {skipped}"
        )
        print(
            f"CSV Duplicates     : {duplicate_csv}"
        )
        print(
            f"Categories Created : {categories_created}"
        )
        print(
            f"Unique CSV HSN     : {len(df)}"
        )
        print(
            "======================================"
        )

    except Exception as e:

        db.rollback()

        print(
            "❌ HSN Seed Error:",
            e,
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    seed_hsn()