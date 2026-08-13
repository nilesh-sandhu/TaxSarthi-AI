from analysis.invoice.risk_engine import RiskEngine
from analysis.invoice.recommendation_engine import RecommendationEngine
from analysis.invoice.fraud_engine import FraudEngine
from analysis.invoice.compliance_engine import ComplianceEngine


class InvoiceReport:

    @staticmethod
    def generate(
        invoice,
        validation,
        duplicates,
    ):

        # =====================================================
        # Risk Analysis
        # =====================================================

        risk = RiskEngine.calculate(
            validation
        )

        # =====================================================
        # Recommendations
        # =====================================================

        recommendations = RecommendationEngine.generate(
            validation
        )

        # =====================================================
        # Fraud Detection
        # =====================================================

        fraud = FraudEngine.detect(
            invoice
        )

        # =====================================================
        # Build Report
        # =====================================================

        report = {

            "success": True,

            "invoice": invoice,

            "validation": validation,

            "risk": risk,

            "fraud": fraud,

            "duplicates": duplicates,

            "recommendations": recommendations,

            "summary": {

                "invoice_number": invoice.get(
                    "invoice_number"
                ),

                "invoice_date": invoice.get(
                    "invoice_date"
                ),

                "supplier": invoice.get(
                    "supplier"
                ),

                "buyer": invoice.get(
                    "buyer"
                ),

                "supplier_gstin": invoice.get(
                    "supplier_gstin"
                ),

                "buyer_gstin": invoice.get(
                    "buyer_gstin"
                ),

                "total_amount": invoice.get(
                    "total_amount"
                ),

                "taxable_amount": invoice.get(
                    "taxable_amount"
                ),

                "cgst": invoice.get(
                    "cgst"
                ),

                "sgst": invoice.get(
                    "sgst"
                ),

                "igst": invoice.get(
                    "igst"
                ),

                "total_items": len(
                    invoice.get(
                        "items",
                        [],
                    )
                ),

                "duplicate_count": len(
                    duplicates
                ),

                "fraud_count": len(
                    [
                        f for f in fraud
                        if f.get("severity") != "NONE"
                    ]
                ),

                "validation_error_count": len(
                    validation.get(
                        "errors",
                        [],
                    )
                ),

            },

        }

        # =====================================================
        # Compliance Evaluation
        # =====================================================

        compliance = ComplianceEngine.evaluate(
            report
        )

        report["compliance"] = compliance

        return report