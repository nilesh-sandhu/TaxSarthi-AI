from sqlalchemy.orm import Session

from models.document import Document


class DocumentRepository:

    # =====================================================
    # Create Document
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        document: Document,
    ):

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    # =====================================================
    # Get Document
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: int,
    ):

        return (

            db.query(Document)

            .filter(
                Document.id == document_id
            )

            .first()

        )

    # =====================================================
    # Get User Documents
    # =====================================================

    @staticmethod
    def get_all(
        db: Session,
        user_id: int,
    ):

        return (

            db.query(Document)

            .filter(
                Document.user_id == user_id
            )

            .order_by(
                Document.created_at.desc()
            )

            .all()

        )

    # =====================================================
    # Update Document
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        document: Document,
    ):

        db.commit()

        db.refresh(document)

        return document

    # =====================================================
    # Delete Document
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        document: Document,
    ):

        db.delete(document)

        db.commit()