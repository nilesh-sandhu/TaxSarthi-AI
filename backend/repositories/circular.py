from sqlalchemy.orm import Session

from models.circular import Circular


class CircularRepository:

    @staticmethod
    def create(
        db: Session,
        circular: Circular,
    ):

        db.add(circular)

        db.commit()

        db.refresh(circular)

        return circular

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(Circular)
            .order_by(Circular.issue_date.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        circular_id: int,
    ):

        return (
            db.query(Circular)
            .filter(Circular.id == circular_id)
            .first()
        )

    @staticmethod
    def search(
        db: Session,
        query: str,
    ):

        return (
            db.query(Circular)
            .filter(
                Circular.title.ilike(f"%{query}%")
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        circular: Circular,
    ):

        db.commit()

        db.refresh(circular)

        return circular

    @staticmethod
    def delete(
        db: Session,
        circular: Circular,
    ):

        db.delete(circular)

        db.commit()