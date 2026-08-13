from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from core.database import SessionLocal

from models.product_master import ProductMaster
from models.product_alias import ProductAlias


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "product_master.csv"


def seed_product_alias():

    db: Session = SessionLocal()

    try:

        if not CSV_PATH.exists():
            raise FileNotFoundError(
                f"CSV file not found: {CSV_PATH}"
            )

        df = pd.read_csv(CSV_PATH)

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            product_name = str(
                row["product_name"]
            ).strip()

            aliases = str(
                row["aliases"]
            ).strip()

            if (
                product_name.lower() == "nan"
                or product_name == ""
            ):
                continue

            product = (
                db.query(ProductMaster)
                .filter(
                    ProductMaster.product_name == product_name
                )
                .first()
            )

            if not product:
                continue

            alias_list = [
                alias.strip()
                for alias in aliases.split("|")
                if alias.strip()
            ]

            for alias in alias_list:

                existing = (
                    db.query(ProductAlias)
                    .filter(
                        ProductAlias.alias == alias
                    )
                    .first()
                )

                if existing:
                    skipped += 1
                    continue

                db.add(
                    ProductAlias(
                        product_id=product.id,
                        alias=alias,
                    )
                )

                inserted += 1

        db.commit()

        print(f"✅ Product Aliases Inserted : {inserted}")
        print(f"⏭️ Product Aliases Skipped : {skipped}")

    except Exception as e:

        db.rollback()
        print(f"❌ Error: {e}")

    finally:

        db.close()


if __name__ == "__main__":
    seed_product_alias()