from sqlalchemy.orm import Session

from models.hsn import HSNMaster
from models.gst_slab import GSTSlab


class HSNValidator:

    @staticmethod
    def validate(
        hsn_code: str,
        invoice_rate: float,
        db: Session,
    ):

        result = {

            "valid": False,

            "expected_rate": None,

            "message": ""

        }

        hsn = (

            db.query(HSNMaster)

            .filter(
                HSNMaster.hsn_code == hsn_code
            )

            .first()

        )

        if not hsn:

            result["message"] = "HSN Code not found."

            return result

        slab = (

            db.query(GSTSlab)

            .filter(
                GSTSlab.hsn_id == hsn.id
            )

            .first()

        )

        if not slab:

            result["message"] = "GST Slab not found."

            return result

        result["expected_rate"] = float(

            slab.gst_rate

        )

        result["valid"] = (

            result["expected_rate"]

            == invoice_rate

        )

        if result["valid"]:

            result["message"] = "GST Rate Verified."

        else:

            result["message"] = (

                f"Expected GST "

                f"{result['expected_rate']}%"

            )

        return result