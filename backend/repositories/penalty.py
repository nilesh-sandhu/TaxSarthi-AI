from sqlalchemy.orm import Session

from models.penalty import Penalty


class PenaltyRepository:

    @staticmethod
    def create(db: Session, penalty: Penalty):

        db.add(penalty)
        db.commit()
        db.refresh(penalty)

        return penalty

    @staticmethod
    def get_all(db: Session):

        return db.query(Penalty).all()

    @staticmethod
    def get_by_id(
        db: Session,
        penalty_id: int,
    ):

        return (
            db.query(Penalty)
            .filter(Penalty.id == penalty_id)
            .first()
        )

    @staticmethod
    def search(
        db: Session,
        query: str,
    ):

        return (
            db.query(Penalty)
            .filter(
                Penalty.title.ilike(f"%{query}%")
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        penalty: Penalty,
    ):

        db.commit()
        db.refresh(penalty)

        return penalty

    @staticmethod
    def delete(
        db: Session,
        penalty: Penalty,
    ):

        db.delete(penalty)
        db.commit()