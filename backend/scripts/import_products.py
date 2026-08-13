import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

from core.database import SessionLocal
from models.category import Category
from models.product_master import ProductMaster


# ---------------------------------------------------------
# FILE
# ---------------------------------------------------------

DATA_DIR = BACKEND_DIR / "data"

PRODUCT_FILE = DATA_DIR / "product_master.csv"

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def clean_text(value):

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return str(value).strip()


def parse_gst_rate(value):

    text = clean_text(value)

    if not text:
        return None

    try:
        return float(
            text.replace("%", "").strip()
        )
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

def get_or_create_category(
    db: Session,
    category_name: str,
):

    category_name = clean_text(category_name)

    if not category_name:
        category_name = "General"

    category = (
        db.query(Category)
        .filter(
            Category.name == category_name
        )
        .first()
    )

    if category:
        return category.id

    category = Category(
        name=category_name,
        description=f"Product category: {category_name}",
        is_active=True,
    )

    db.add(category)
    db.flush()

    print(
        f"Created category: "
        f"{category_name} "
        f"(id={category.id})"
    )

    return category.id


# ---------------------------------------------------------
# PRODUCT IMPORT
# ---------------------------------------------------------

def import_products(db: Session):

    print("\n" + "=" * 70)
    print("TAXSARTHI AI - PRODUCT MASTER IMPORT")
    print("=" * 70)

    print(
        f"\nProduct CSV:\n{PRODUCT_FILE}"
    )

    # -----------------------------------------------------
    # FILE CHECK
    # -----------------------------------------------------

    if not PRODUCT_FILE.exists():

        print("\nERROR: Product CSV not found.")

        print(
            f"Expected:\n{PRODUCT_FILE}"
        )

        return

    # -----------------------------------------------------
    # READ CSV
    # -----------------------------------------------------

    df = pd.read_csv(
        PRODUCT_FILE,
        dtype=str,
    ).fillna("")

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    print(
        f"\nCSV records found: {len(df):,}"
    )

    print(
        f"Columns: {', '.join(df.columns)}"
    )

    # -----------------------------------------------------
    # REQUIRED COLUMNS
    # -----------------------------------------------------

    required_columns = {
        "product_name",
        "category",
        "hsn_code",
        "gst_rate",
        "description",
    }

    missing = (
        required_columns
        - set(df.columns)
    )

    if missing:

        print(
            "\nERROR: Missing columns:"
        )

        print(missing)

        return

    # -----------------------------------------------------
    # COUNTERS
    # -----------------------------------------------------

    inserted = 0
    updated = 0
    skipped = 0

    category_cache = {}

    # -----------------------------------------------------
    # PROCESS PRODUCTS
    # -----------------------------------------------------

    for index, row in df.iterrows():

        product_name = clean_text(
            row["product_name"]
        )

        category_name = clean_text(
            row["category"]
        )

        hsn_code = clean_text(
            row["hsn_code"]
        )

        gst_rate = parse_gst_rate(
            row["gst_rate"]
        )

        description = clean_text(
            row["description"]
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not product_name:

            skipped += 1
            continue

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        if category_name not in category_cache:

            category_cache[
                category_name
            ] = get_or_create_category(
                db,
                category_name,
            )

        category_id = category_cache[
            category_name
        ]

        # -------------------------------------------------
        # EXISTING PRODUCT
        # -------------------------------------------------

        product = (
            db.query(ProductMaster)
            .filter(
                ProductMaster.product_name
                == product_name
            )
            .first()
        )

        # -------------------------------------------------
        # UPDATE
        # -------------------------------------------------

        if product:

            product.category_id = category_id

            product.hsn_code = (
                hsn_code
                if hsn_code
                else None
            )

            product.gst_rate = gst_rate

            product.description = (
                description
            )

            product.is_active = True

            updated += 1

        # -------------------------------------------------
        # INSERT
        # -------------------------------------------------

        else:

            product = ProductMaster(

                product_name=product_name,

                category_id=category_id,

                hsn_code=(
                    hsn_code
                    if hsn_code
                    else None
                ),

                gst_rate=gst_rate,

                description=description,

                is_active=True,
            )

            db.add(product)

            inserted += 1

        # -------------------------------------------------
        # BATCH COMMIT
        # -------------------------------------------------

        if (index + 1) % 25 == 0:

            db.commit()

            print(
                f"Processed {index + 1:>3} | "
                f"Inserted {inserted:>3} | "
                f"Updated {updated:>3} | "
                f"Skipped {skipped:>3}"
            )

    # -----------------------------------------------------
    # FINAL COMMIT
    # -----------------------------------------------------

    db.commit()

    print("\n" + "=" * 70)
    print("PRODUCT IMPORT COMPLETE")
    print("=" * 70)

    print(
        f"Inserted : {inserted:,}"
    )

    print(
        f"Updated  : {updated:,}"
    )

    print(
        f"Skipped  : {skipped:,}"
    )

    print(
        f"Total    : {inserted + updated:,}"
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    db = SessionLocal()

    try:

        import_products(db)

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