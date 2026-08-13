class RecommendationEngine:

    @staticmethod
    def generate(validation):

        recommendations = []

        errors = validation.get("errors", [])

        mapping = {

            "Supplier GSTIN missing.": {
                "priority": "HIGH",
                "recommendation": "Enter the supplier GSTIN before claiming Input Tax Credit (ITC)."
            },

            "Supplier GSTIN is invalid.": {
                "priority": "HIGH",
                "recommendation": "Verify the GSTIN on the GST Portal before processing the invoice."
            },

            "Invoice Number missing.": {
                "priority": "MEDIUM",
                "recommendation": "Every GST invoice should have a unique invoice number."
            },

            "Total Amount missing.": {
                "priority": "HIGH",
                "recommendation": "Enter the taxable value and invoice total correctly."
            },

            "GST calculation mismatch.": {
                "priority": "HIGH",
                "recommendation": "Recalculate CGST, SGST or IGST as per GST rules."
            },

            "HSN missing.": {
                "priority": "MEDIUM",
                "recommendation": "Mention the HSN code for every taxable product."
            },

            "Invalid HSN Code.": {
                "priority": "HIGH",
                "recommendation": "Verify the HSN code using the GST HSN database."
            }

        }

        for error in errors:

            if error in mapping:

                recommendations.append(

                    mapping[error]

                )

        if not recommendations:

            recommendations.append({

                "priority": "LOW",

                "recommendation": "Invoice passed all validations."

            })

        return recommendations