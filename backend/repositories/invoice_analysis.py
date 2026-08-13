from sqlalchemy.orm import Session

from models.invoice_analysis import InvoiceAnalysis


class InvoiceAnalysisRepository:

    # =====================================================
    # Create Analysis
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        analysis: InvoiceAnalysis,
    ):

        try:

            print("\n========== SAVING INVOICE ANALYSIS ==========")

            db.add(analysis)

            db.commit()

            db.refresh(analysis)

            print(f"Saved Successfully | ID : {analysis.id}")

            print("=============================================\n")

            return analysis

        except Exception as e:

            db.rollback()

            print("\n========== DATABASE ERROR ==========")
            print(e)
            print("====================================\n")

            raise e

    # =====================================================
    # Get By Document ID
    # =====================================================

    @staticmethod
    def get_by_document(
        db: Session,
        document_id: int,
    ):

        analysis = (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.document_id == document_id
            )

            .first()

        )

        if analysis:

            print(
                f"Analysis Found for Document {document_id}"
            )

        else:

            print(
                f"No Analysis Found for Document {document_id}"
            )

        return analysis

    # =====================================================
    # Get By Analysis ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        analysis_id: int,
    ):

        return (

            db.query(InvoiceAnalysis)

            .filter(
                InvoiceAnalysis.id == analysis_id
            )

            .first()

        )

    # =====================================================
    # Get All
    # =====================================================

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (

            db.query(InvoiceAnalysis)

            .order_by(
                InvoiceAnalysis.created_at.desc()
            )

            .all()

        )

    # =====================================================
    # Update
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        analysis: InvoiceAnalysis,
    ):

        try:

            db.commit()

            db.refresh(analysis)

            return analysis

        except Exception as e:

            db.rollback()

            raise e

    # =====================================================
    # Delete
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        analysis: InvoiceAnalysis,
    ):

        try:

            db.delete(analysis)

            db.commit()

            return True

        except Exception as e:

            db.rollback()

            raise e