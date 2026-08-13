from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from core.database import SessionLocal

from models.product_master import ProductMaster
from models.hsn import HSNMaster
from models.category import Category


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "data"
    / "product_master.csv"
)


# ============================================================
# SEED PRODUCTS
# ============================================================

def seed_products():

    db: Session = SessionLocal()

    inserted = 0
    updated = 0
    skipped = 0

    try:

        # ----------------------------------------------------
        # LOAD CSV
        # ----------------------------------------------------

        df = pd.read_csv(
            CSV_PATH
        )

        print(
            f"📄 Product rows found: {len(df)}"
        )

        # ----------------------------------------------------
        # CLEAN COLUMN NAMES
        # ----------------------------------------------------

        df.columns = [
            str(column).strip().lower()
            for column in df.columns
        ]

        required_columns = {
            "product_name",
            "hsn_code",
            "gst_rate",
            "category",
        }

        missing = (
            required_columns
            - set(df.columns)
        )

        if missing:

            raise ValueError(
                "Missing CSV columns: "
                + ", ".join(
                    sorted(missing)
                )
            )

        # ----------------------------------------------------
        # PROCESS EVERY PRODUCT
        # ----------------------------------------------------

        for _, row in df.iterrows():

            product_name = str(
                row["product_name"]
            ).strip()

            hsn_code = str(
                row["hsn_code"]
            ).strip()

            category_name = str(
                row["category"]
            ).strip()

            # ------------------------------------------------
            # VALIDATE
            # ------------------------------------------------

            if (
                not product_name
                or product_name.lower()
                == "nan"
            ):
                skipped += 1
                continue

            if (
                not hsn_code
                or hsn_code.lower()
                == "nan"
            ):
                skipped += 1
                continue

            # ------------------------------------------------
            # GST RATE
            # ------------------------------------------------

            try:

                gst_rate = float(
                    row["gst_rate"]
                )

            except (
                TypeError,
                ValueError,
            ):

                print(
                    f"⚠️ Invalid GST rate for "
                    f"{product_name}"
                )

                skipped += 1
                continue

            # ------------------------------------------------
            # CATEGORY
            # ------------------------------------------------

            category = (
                db.query(Category)
                .filter(
                    Category.name
                    == category_name
                )
                .first()
            )

            if not category:

                category = Category(
                    name=category_name,
                    description=category_name,
                )

                db.add(category)

                db.flush()

            # ------------------------------------------------
            # CHECK EXISTING PRODUCT
            # ------------------------------------------------

            product = (
                db.query(ProductMaster)
                .filter(
                    ProductMaster.product_name
                    == product_name
                )
                .first()
            )

            # ------------------------------------------------
            # HSN IS OPTIONAL
            #
            # ProductMaster must NOT fail simply because
            # HSNMaster does not contain the HSN code.
            # ------------------------------------------------

            hsn = (
                db.query(HSNMaster)
                .filter(
                    HSNMaster.hsn_code
                    == hsn_code
                )
                .first()
            )

            description = (
                hsn.description
                if hsn
                else product_name
            )

            # ------------------------------------------------
            # UPDATE EXISTING
            # ------------------------------------------------

            if product:

                product.category_id = (
                    category.id
                )

                product.hsn_code = (
                    hsn_code
                )

                product.description = (
                    description
                )

                # IMPORTANT
                # Save GST from CSV
                if hasattr(
                    product,
                    "gst_rate",
                ):
                    product.gst_rate = (
                        gst_rate
                    )

                updated += 1

                continue

            # ------------------------------------------------
            # CREATE NEW PRODUCT
            # ------------------------------------------------

            product_data = {
                "product_name": product_name,
                "category_id": category.id,
                "hsn_code": hsn_code,
                "description": description,
            }

            # Only add gst_rate if the model supports it
            if hasattr(
                ProductMaster,
                "gst_rate",
            ):

                product_data[
                    "gst_rate"
                ] = gst_rate

            product = ProductMaster(
                **product_data
            )

            db.add(product)

            inserted += 1

        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------

        db.commit()

        print(
            "\n======================================"
        )

        print(
            "✅ PRODUCT SEED COMPLETED"
        )

        print(
            "======================================"
        )

        print(
            f"Products Inserted : {inserted}"
        )

        print(
            f"Products Updated  : {updated}"
        )

        print(
            f"Products Skipped   : {skipped}"
        )

        print(
            f"CSV Products       : {len(df)}"
        )

        print(
            "======================================"
        )

    except Exception as e:

        db.rollback()

        print(
            "\n❌ Product Seed Error:"
        )

        print(e)

        raise

    finally:

        db.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    seed_products()