from datetime import date
from pathlib import Path
import re

import pandas as pd
from sqlalchemy.orm import Session

from core.database import SessionLocal

from models.hsn import HSNMaster
from models.gst_slab import GSTSlab


BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "data" / "gst-rate-list.xlsx"


def parse_gst_rate(value):

    if pd.isna(value):
        return 0.0

    value = str(value).strip()

    if value.lower() in [
        "exempt",
        "nil",
        "nil rated",
        "nil rate",
    ]:
        return 0.0

    match = re.search(r"(\d+(\.\d+)?)", value)

    if match:
        return float(match.group(1))

    return 0.0


def seed_gst_slabs():

    db: Session = SessionLocal()

    try:

        if not EXCEL_PATH.exists():
            raise FileNotFoundError(
                f"Excel file not found: {EXCEL_PATH}"
            )

        df = pd.read_excel(
            EXCEL_PATH,
            header=3,
        )

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            hsn_code = str(
                row["HSN heading"]
            ).strip()

            if (
                hsn_code.lower() == "nan"
                or hsn_code == ""
            ):
                continue

            hsn = (
                db.query(HSNMaster)
                .filter(
                    HSNMaster.hsn_code == hsn_code
                )
                .first()
            )

            if not hsn:
                skipped += 1
                continue

            existing = (
                db.query(GSTSlab)
                .filter(
                    GSTSlab.hsn_id == hsn.id
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            gst = parse_gst_rate(
                row["GST rate"]
            )

            db.add(
                GSTSlab(
                    hsn_id=hsn.id,
                    gst_rate=gst,
                    cgst=gst / 2,
                    sgst=gst / 2,
                    igst=gst,
                    cess=0,
                    notification_no="GST Rate List",
                    effective_from=date.today(),
                    effective_to=None,
                )
            )

            inserted += 1

        db.commit()

        print(f"✅ GST Slabs Inserted : {inserted}")
        print(f"⏭️ GST Slabs Skipped : {skipped}")

    except Exception as e:

        db.rollback()
        print(f"❌ Error: {e}")

    finally:

        db.close()


if __name__ == "__main__":
    seed_gst_slabs()