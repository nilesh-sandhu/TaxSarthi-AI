import re


class InvoiceValidator:

    @staticmethod
    def validate(invoice):

        errors = []

        recommendations = []

        # =====================================================
        # GSTIN Validation
        # =====================================================

        gstin = invoice.get("supplier_gstin")

        if gstin:

            pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]{3}$"

            if not re.match(pattern, gstin):

                errors.append(
                    "Invalid Supplier GSTIN."
                )

            else:

                recommendations.append(
                    "Supplier GSTIN verified."
                )

        else:

            errors.append(
                "Supplier GSTIN missing."
            )

        # =====================================================
        # Invoice Number
        # =====================================================

        if not invoice.get("invoice_number"):

            errors.append(
                "Invoice Number missing."
            )

        # =====================================================
        # Total Amount
        # =====================================================

        if invoice.get("total_amount") is None:

            errors.append(
                "Total Amount missing."
            )

        return {

            "valid": len(errors) == 0,

            "errors": errors,

            "recommendations": recommendations,

        }