class RiskEngine:

    @staticmethod
    def calculate(validation):

        score = 100

        reasons = []

        errors = validation.get("errors", [])

        deductions = {
            "Supplier GSTIN missing.": 25,
            "Supplier GSTIN is invalid.": 25,
            "Invoice Number missing.": 15,
            "Total Amount missing.": 20,
            "GST calculation mismatch.": 20,
            "HSN missing.": 10,
            "Invalid HSN Code.": 10,
        }

        for error in errors:

            deduction = deductions.get(error, 5)

            score -= deduction

            reasons.append({

                "issue": error,

                "deduction": deduction,

            })

        if score < 0:
            score = 0

        if score >= 90:
            level = "LOW"

        elif score >= 70:
            level = "MEDIUM"

        elif score >= 40:
            level = "HIGH"

        else:
            level = "CRITICAL"

        return {

            "score": score,

            "level": level,

            "reasons": reasons,

        }