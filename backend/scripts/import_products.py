import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from core.database import SessionLocal
from models.product import Product

CSV_FILE = BASE_DIR / "data" / "product_master.csv"


def import_products():

    db: Session = SessionLocal()

    try:

        print("=" * 60)
        print("TaxSarthi AI - Product Importer")
        print("=" * 60)

        df = pd.read_csv(CSV_FILE)

        imported = 0
        skipped = 0

        for _, row in df.iterrows():

            name = str(row["product_name"]).strip()

            existing = (
                db.query(Product)
                .filter(Product.name == name)
                .first()
            )

            if existing:
                skipped += 1
                continue

            product = Product(
                name=name,
                category=row["category"],
                gst_rate=float(row["gst_rate"]),
                hsn_code=str(row["hsn_code"]),
                description=str(row["aliases"]),
            )

            db.add(product)
            imported += 1

        db.commit()

        print(f"Imported : {imported}")
        print(f"Skipped  : {skipped}")

    except Exception as e:

        db.rollback()
        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    import_products()