"""
TaxSarthi AI
Complete GST + HSN Master Data Importer

Data:
    backend/data/hsn_master.csv
    backend/data/gst-rate-list.xlsx

Run from project root:
    python backend/scripts/import_gst_data.py
"""

import re
import sys
from datetime import date
from pathlib import Path
from decimal import Decimal

import pandas as pd
from sqlalchemy.orm import Session

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from core.database import SessionLocal
from models.category import Category
from models.hsn import HSNMaster
from models.gst_slab import GSTSlab
from models.product_master import ProductMaster
from models.gst_slab import GSTSlab

# =========================================================
# FILES
# =========================================================

DATA_DIR = BACKEND_DIR / "data"
PRODUCT_FILE = DATA_DIR / "product_master_demo.csv"

EFFECTIVE_FROM = date(2025, 9, 22)
NOTIFICATION_NO = "CBIC Notification 9/2025-Central Tax (Rate)"


# =========================================================
# HELPERS
# =========================================================

def clean_text(value):
    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return str(value).strip()


def normalize_hsn(value):
    return re.sub(
        r"[^0-9]",
        "",
        clean_text(value),
    )


def parse_gst_rate(value):
    text = clean_text(value).lower()

    if not text:
        return None

    if text in {
        "exempt",
        "nil",
        "nil rate",
        "0",
        "0%",
    }:
        return 0.0

    if "varies" in text:
        return None

    try:
        return float(
            text.replace("%", "").strip()
        )
    except (TypeError, ValueError):
        return None


def get_or_create_hsn_category(db: Session):
    """
    HSNMaster.category_id is NOT NULL.

    HSN records are reference/master classifications, so
    they are attached to a dedicated generic category.
    """

    category = (
        db.query(Category)
        .filter(
            Category.name == "HSN Master"
        )
        .first()
    )

    if category:
        return category.id

    category = Category(
        name="HSN Master",
        description=(
            "Government HSN classification master data"
        ),
        is_active=True,
    )

    db.add(category)
    db.flush()

    print(
        f"Created HSN Master category: id={category.id}"
    )

    return category.id


# =========================================================
# HSN IMPORT
# =========================================================

def import_hsn_master(db: Session):
    print("\n" + "=" * 70)
    print("IMPORTING HSN MASTER")
    print("=" * 70)

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"HSN CSV not found:\n{CSV_FILE}"
        )

    df = pd.read_csv(
        CSV_FILE,
        dtype=str,
    ).fillna("")

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    required = {
        "hsn_code",
        "description",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing CSV columns: {missing}"
        )

    print(
        f"CSV records found: {len(df):,}"
    )

    category_id = get_or_create_hsn_category(
        db
    )

    inserted = 0
    updated = 0
    skipped = 0

    # Track HSN codes already processed in this import run.
    # The CSV contains duplicate HSN codes.
    seen_hsn_codes = set()

    for index, row in df.iterrows():

        code = normalize_hsn(
            row["hsn_code"]
        )

        description = clean_text(
            row["description"]
        )

        if not code or not description:
            skipped += 1
            continue

        # -------------------------------------------------
        # IMPORTANT:
        # The CSV contains duplicate HSN codes.
        # SQLAlchemy's session may not flush pending inserts
        # before the next query, so the database UNIQUE
        # constraint can still be hit inside the same batch.
        # Track codes in this import run and skip duplicates.
        # -------------------------------------------------
        if code in seen_hsn_codes:
            skipped += 1
            continue

        seen_hsn_codes.add(code)

        existing = (
            db.query(HSNMaster)
            .filter(
                HSNMaster.hsn_code == code
            )
            .first()
        )

        if existing:

            existing.description = description

            if existing.category_id is None:
                existing.category_id = category_id

            existing.is_active = True

            updated += 1

        else:

            db.add(
                HSNMaster(
                    hsn_code=code,
                    description=description,
                    category_id=category_id,
                    is_active=True,
                )
            )

            inserted += 1

        if (index + 1) % 500 == 0:
            db.commit()

            print(
                f"Processed {index + 1:,} | "
                f"Inserted {inserted:,} | "
                f"Updated {updated:,}"
            )

    db.commit()

    print("\nHSN IMPORT COMPLETE")
    print(
        f"Inserted : {inserted:,}"
    )
    print(
        f"Updated  : {updated:,}"
    )
    print(
        f"Skipped  : {skipped:,}"
    )


# =========================================================
# GST RATE IMPORT
# =========================================================

def import_gst_rates(db: Session):
    print("\n" + "=" * 70)
    print("IMPORTING GST RATE LIST")
    print("=" * 70)

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"GST Excel not found:\n{EXCEL_FILE}"
        )

    # The workbook contains 3 title/blank rows.
    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Rate list",
        header=3,
        dtype=str,
    ).fillna("")

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    required = {
        "GST rate",
        "HSN heading",
        "Chapter",
        "Description",
        "Sub-codes",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing Excel columns: {missing}"
        )

    print(
        f"GST rows found: {len(df):,}"
    )

    inserted = 0
    updated = 0
    skipped = 0
    varied = 0

    for index, row in df.iterrows():

        heading = normalize_hsn(
            row["HSN heading"]
        )

        rate = parse_gst_rate(
            row["GST rate"]
        )

        sub_codes = clean_text(
            row["Sub-codes"]
        )

        if not heading or rate is None:
            if sub_codes:
                varied += 1
            else:
                skipped += 1
            continue

        # A row with Sub-codes means the 4-digit heading
        # does not by itself establish one rate.
        # Do not invent a rate for all 8-digit HSNs.
        if sub_codes:
            varied += 1
            continue

        # HSN master can contain 4, 6 or 8 digit codes.
        # A tariff heading applies to records beginning
        # with the same first 4 digits.
        hsn_rows = (
            db.query(HSNMaster)
            .filter(
                HSNMaster.hsn_code.like(
                    f"{heading}%"
                ),
                HSNMaster.is_active.is_(True),
            )
            .all()
        )

        if not hsn_rows:
            skipped += 1
            continue

        cgst = rate / 2
        sgst = rate / 2
        igst = rate

        for hsn in hsn_rows:

            slab = (
                db.query(GSTSlab)
                .filter(
                    GSTSlab.hsn_id == hsn.id,
                    GSTSlab.effective_from
                    == EFFECTIVE_FROM,
                )
                .first()
            )

            if slab:

                slab.gst_rate = rate
                slab.cgst = cgst
                slab.sgst = sgst
                slab.igst = igst
                slab.cess = 0.0
                slab.notification_no = (
                    NOTIFICATION_NO
                )
                slab.effective_to = None
                slab.is_active = True

                updated += 1

            else:

                db.add(
                    GSTSlab(
                        hsn_id=hsn.id,
                        gst_rate=rate,
                        cgst=cgst,
                        sgst=sgst,
                        igst=igst,
                        cess=0.0,
                        notification_no=(
                            NOTIFICATION_NO
                        ),
                        effective_from=(
                            EFFECTIVE_FROM
                        ),
                        effective_to=None,
                        is_active=True,
                    )
                )

                inserted += 1

        if (index + 1) % 50 == 0:
            db.commit()

            print(
                f"Processed {index + 1:,} | "
                f"GST slabs inserted {inserted:,} | "
                f"updated {updated:,}"
            )

    db.commit()

    print("\nGST IMPORT COMPLETE")
    print(
        f"Inserted slabs       : {inserted:,}"
    )
    print(
        f"Updated slabs        : {updated:,}"
    )
    print(
        f"Skipped rows         : {skipped:,}"
    )
    print(
        f"Variable-rate rows   : {varied:,}"
    )


# =========================================================
# VERIFY
# =========================================================

def verify_database(db: Session):

    print("\n" + "=" * 70)
    print("DATABASE VERIFICATION")
    print("=" * 70)

    hsn_count = (
        db.query(HSNMaster)
        .filter(
            HSNMaster.is_active.is_(True)
        )
        .count()
    )

    gst_count = (
        db.query(GSTSlab)
        .filter(
            GSTSlab.is_active.is_(True)
        )
        .count()
    )

    category = (
        db.query(Category)
        .filter(
            Category.name == "HSN Master"
        )
        .first()
    )

    print(
        f"HSNMaster records : {hsn_count:,}"
    )
    print(
        f"GSTSlab records   : {gst_count:,}"
    )
    print(
        "HSN category      : "
        + (
            str(category.id)
            if category
            else "NOT FOUND"
        )
    )

    test_codes = [
        "8471",
        "8517",
        "8528",
        "8418",
        "8415",
        "6109",
    ]

    print("\nGST TEST RECORDS")

    for prefix in test_codes:

        result = (
            db.query(
                HSNMaster,
                GSTSlab,
            )
            .join(
                GSTSlab,
                GSTSlab.hsn_id
                == HSNMaster.id,
            )
            .filter(
                HSNMaster.hsn_code.like(
                    f"{prefix}%"
                ),
                GSTSlab.is_active.is_(True),
            )
            .order_by(
                HSNMaster.hsn_code.asc()
            )
            .first()
        )

        if result:

            hsn, slab = result

            print(
                f"{hsn.hsn_code} | "
                f"{hsn.description[:60]} | "
                f"GST {slab.gst_rate}%"
            )

        else:

            print(
                f"{prefix} -> NOT FOUND"
            )


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n")
    print("=" * 70)
    print("TAXSARTHI AI - GST/HSN DATA IMPORT")
    print("=" * 70)

    print(
        f"\nHSN CSV:\n{CSV_FILE}"
    )

    print(
        f"\nGST Excel:\n{EXCEL_FILE}"
    )

    if not CSV_FILE.exists():
        print(
            "\nERROR: HSN CSV not found."
        )
        return

    if not EXCEL_FILE.exists():
        print(
            "\nERROR: GST Excel not found."
        )
        return

    db = SessionLocal()

    try:

        import_hsn_master(db)

        import_gst_rates(db)

        verify_database(db)

        print("\n" + "=" * 70)
        print("IMPORT SUCCESSFUL")
        print("=" * 70)

    except Exception as error:

        db.rollback()

        print("\n" + "=" * 70)
        print("IMPORT FAILED")
        print("=" * 70)

        print(
            f"\nError: {error}"
        )

        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()