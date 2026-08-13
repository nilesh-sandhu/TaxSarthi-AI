from sqlalchemy.orm import Session

from models.invoice_analysis import InvoiceAnalysis


class DuplicateDetector:

    @staticmethod
    def check(
        invoice: dict,
        db: Session,
    ):

        invoice_number = invoice.get(
            "invoice_number"
        )

        supplier_gstin = invoice.get(
            "supplier_gstin"
        )

        total_amount = invoice.get(
            "total_amount"
        )

        duplicates = []

        # ==========================================
        # Duplicate Invoice Number
        # ==========================================

        if invoice_number:

            existing = (

                db.query(InvoiceAnalysis)

                .filter(
                    InvoiceAnalysis.invoice_number == invoice_number
                )

                .all()

            )

            if existing:

                duplicates.append({

                    "severity": "HIGH",

                    "issue": "Duplicate Invoice Number",

                    "count": len(existing),

                })

        # ==========================================
        # Same GSTIN + Same Amount
        # ==========================================

        if supplier_gstin and total_amount:

            existing = (

                db.query(InvoiceAnalysis)

                .filter(
                    InvoiceAnalysis.gstin == supplier_gstin,
                    InvoiceAnalysis.total_amount == total_amount,
                )

                .all()

            )

            if existing:

                duplicates.append({

                    "severity": "MEDIUM",

                    "issue": "Same GSTIN and Invoice Amount already exists.",

                    "count": len(existing),

                })

        return duplicates