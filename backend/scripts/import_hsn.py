import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# -----------------------------------
# Add Backend to Path
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# -----------------------------------
# Database
# -----------------------------------
from core.database import SessionLocal

# -----------------------------------
# Model
# -----------------------------------
from models.hsn import HSN

# -----------------------------------
# CSV Path
# -----------------------------------
CSV_FILE = BASE_DIR / "data" / "hsn_master.csv"


def import_hsn():

    db: Session = SessionLocal()

    try:

        print("=" * 60)
        print("TaxSarthi AI - HSN Importer")
        print("=" * 60)

        # -----------------------------
        # Read CSV
        # -----------------------------
        df = pd.read_csv(CSV_FILE)

        print(f"CSV Records : {len(df)}")

        # -----------------------------
        # Clean Data
        # -----------------------------
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

        # Remove blank HSN codes
        df = df[df["hsn_code"] != ""]

        # Remove duplicate HSN codes from CSV
        df = df.drop_duplicates(
            subset=["hsn_code"],
            keep="first"
        )

        print(f"Records after cleaning : {len(df)}")

        imported = 0
        skipped = 0

        # -----------------------------
        # Import
        # -----------------------------
        for _, row in df.iterrows():

            hsn_code = row["hsn_code"]
            description = row["description"]

            if description == "":
                skipped += 1
                continue

            # Already exists?
            existing = (
                db.query(HSN)
                .filter_by(hsn_code=hsn_code)
                .first()
            )

            if existing:
                skipped += 1
                continue

            try:

                new_hsn = HSN(
                    hsn_code=hsn_code,
                    description=description,
                )

                db.add(new_hsn)
                db.commit()

                imported += 1

                if imported % 500 == 0:
                    print(f"Imported : {imported}")

            except IntegrityError:

                db.rollback()
                skipped += 1

            except Exception:

                db.rollback()
                skipped += 1

        print("\n" + "=" * 60)
        print("Import Completed")
        print("=" * 60)
        print(f"Imported : {imported}")
        print(f"Skipped  : {skipped}")
        print("=" * 60)

    except Exception as e:

        print("\nERROR")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    import_hsn()