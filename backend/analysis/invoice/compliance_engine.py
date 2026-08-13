class ComplianceEngine:

    @staticmethod
    def evaluate(report):

        validation = report.get("validation", {})
        fraud = report.get("fraud", [])
        duplicates = report.get("duplicates", [])
        risk = report.get("risk", {})

        status = "COMPLIANT"

        reasons = []

        if validation.get("errors"):

            status = "NON-COMPLIANT"

            reasons.extend(validation["errors"])

        if fraud:

            status = "NON-COMPLIANT"

            for item in fraud:

                if item.get("severity") != "NONE":

                    reasons.append(item["issue"])

        if duplicates:

            status = "REVIEW REQUIRED"

            for item in duplicates:

                reasons.append(item["issue"])

        return {

            "status": status,

            "risk_level": risk.get("level"),

            "score": risk.get("score"),

            "reasons": reasons,

        }