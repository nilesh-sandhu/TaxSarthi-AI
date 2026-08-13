from sqlalchemy import func
from sqlalchemy.orm import Session

from models.document import Document
from models.invoice_analysis import InvoiceAnalysis

from ai.executive_summary import ExecutiveSummary


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session):

        # =====================================================
        # Overview
        # =====================================================

        total_documents = db.query(Document).count()

        total_invoices = db.query(
            InvoiceAnalysis
        ).count()

        valid_invoices = (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.validation_status == "Valid"
            )

            .count()

        )

        invalid_invoices = (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.validation_status == "Invalid"
            )

            .count()

        )

        # =====================================================
        # Risk Distribution
        # =====================================================

        high_risk = (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.risk_score < 60
            )

            .count()

        )

        medium_risk = (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.risk_score >= 60,
                InvoiceAnalysis.risk_score < 80,
            )

            .count()

        )

        low_risk = (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.risk_score >= 80
            )

            .count()

        )

        average_score = (

            db.query(
                func.avg(
                    InvoiceAnalysis.risk_score
                )
            )

            .scalar()

        )

        average_score = round(
            average_score or 0,
            2,
        )

        # =====================================================
        # Compliance Percentage
        # =====================================================

        compliance_percentage = 0

        if total_invoices > 0:

            compliance_percentage = round(

                (valid_invoices / total_invoices) * 100,

                2,

            )

        # =====================================================
        # Dashboard Health
        # =====================================================

        if average_score >= 90:

            dashboard_health = "Excellent"

        elif average_score >= 75:

            dashboard_health = "Good"

        elif average_score >= 60:

            dashboard_health = "Average"

        else:

            dashboard_health = "Needs Attention"

        # =====================================================
        # Recent Invoices
        # =====================================================

        recent = (

            db.query(InvoiceAnalysis)

            .order_by(
                InvoiceAnalysis.created_at.desc()
            )

            .limit(5)

            .all()

        )

        recent_invoices = []

        for invoice in recent:

            recent_invoices.append({

                "invoice_number": invoice.invoice_number,

                "supplier": invoice.supplier,

                "risk_score": invoice.risk_score,

                "status": invoice.validation_status,

                "amount": invoice.total_amount,

                "date": str(invoice.created_at),

            })

        # =====================================================
        # AI Executive Summary
        # =====================================================

        stats = {

            "total_documents": total_documents,

            "total_invoices": total_invoices,

            "valid_invoices": valid_invoices,

            "invalid_invoices": invalid_invoices,

            "average_score": average_score,

            "high_risk": high_risk,

            "medium_risk": medium_risk,

            "low_risk": low_risk,

            "compliance_percentage": compliance_percentage,

        }

        executive_summary = ExecutiveSummary.generate(
            stats
        )

        # =====================================================
        # Final Response
        # =====================================================

        return {

            "overview": {

                "total_documents": total_documents,

                "total_invoices": total_invoices,

                "valid_invoices": valid_invoices,

                "invalid_invoices": invalid_invoices,

                "compliance_percentage": compliance_percentage,

                "dashboard_health": dashboard_health,

            },

            "risk": {

                "average_score": average_score,

                "high": high_risk,

                "medium": medium_risk,

                "low": low_risk,

            },

            "recent_invoices": recent_invoices,

            "executive_summary": executive_summary,

        }