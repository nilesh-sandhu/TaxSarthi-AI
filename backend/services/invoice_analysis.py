import json

from sqlalchemy.orm import Session

from models.invoice_analysis import InvoiceAnalysis
from repositories.invoice_analysis import InvoiceAnalysisRepository
from analysis.reports.audit_report import AuditReport

class InvoiceAnalysisService:

    # =====================================================
    # Save Analysis
    # =====================================================

    @staticmethod
    def save_analysis(
        db: Session,
        document_id: int,
        report: dict,
    ):

        invoice = report.get("invoice", {})

        validation = report.get("validation", {})

        risk = report.get("risk", {})

        recommendations = report.get(
            "recommendations",
            [],
        )

        analysis = InvoiceAnalysis(

            document_id=document_id,

            invoice_number=invoice.get(
                "invoice_number"
            ),

            supplier=invoice.get(
                "supplier"
            ),

            gstin=invoice.get(
                "supplier_gstin"
            ),

            invoice_date=invoice.get(
                "invoice_date"
            ),

            total_amount=invoice.get(
                "total_amount"
            ),

            risk_score=risk.get(
                "score",
                100,
            ),

            validation_status=(

                "Valid"

                if validation.get(
                    "valid",
                    False,
                )

                else "Invalid"

            ),

            recommendations=json.dumps(

                recommendations,

                indent=2,

            ),

            errors=json.dumps(

                validation.get(
                    "errors",
                    [],
                ),

                indent=2,

            ),

        )

        # =====================================================
        # Save Database
        # =====================================================

        saved = InvoiceAnalysisRepository.create(

            db=db,

            analysis=analysis,

        )

        # =====================================================
        # Generate Audit Report
        # =====================================================

        audit_report = AuditReport.generate(

            report

        )

        # =====================================================
        # Console Output
        # =====================================================

        print("\n")

        print("=" * 70)

        print("           INVOICE ANALYSIS SAVED")

        print("=" * 70)

        print(f"Document ID    : {document_id}")

        print(f"Invoice Number : {analysis.invoice_number}")

        print(f"Supplier       : {analysis.supplier}")

        print(f"GSTIN          : {analysis.gstin}")

        print(f"Risk Score     : {analysis.risk_score}")

        print("=" * 70)

        print("\n")

        print(audit_report)

        print("\n")

        return saved

    # =====================================================
    # Get Analysis
    # =====================================================

    @staticmethod
    def get_analysis(
        db: Session,
        document_id: int,
    ):

        analysis = InvoiceAnalysisRepository.get_by_document(

            db=db,

            document_id=document_id,

        )

        if analysis is None:

            return {

                "success": False,

                "message": "Analysis not found.",

            }

        return {

            "success": True,

            "analysis": {

                "document_id": analysis.document_id,

                "invoice_number": analysis.invoice_number,

                "supplier": analysis.supplier,

                "gstin": analysis.gstin,

                "invoice_date": analysis.invoice_date,

                "total_amount": analysis.total_amount,

                "risk_score": analysis.risk_score,

                "validation_status": analysis.validation_status,

                "recommendations": json.loads(

                    analysis.recommendations

                )

                if analysis.recommendations

                else [],

                "errors": json.loads(

                    analysis.errors

                )

                if analysis.errors

                else [],

                "created_at": analysis.created_at,

            },

        }