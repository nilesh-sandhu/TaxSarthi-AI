from sqlalchemy.orm import Session

from models.gst_slab import GSTSlab
from schemas.gst_slab import (
    GSTSlabCreate,
    GSTSlabUpdate,
)


class GSTSlabRepository:

    @staticmethod
    def create(db: Session, slab: GSTSlabCreate):

        obj = GSTSlab(**slab.model_dump())

        db.add(obj)

        db.commit()

        db.refresh(obj)

        return obj

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(GSTSlab)
            .filter(GSTSlab.is_active == True)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, slab_id: int):

        return (
            db.query(GSTSlab)
            .filter(GSTSlab.id == slab_id)
            .first()
        )

    @staticmethod
    def get_by_hsn(db: Session, hsn_id: int):

        return (
            db.query(GSTSlab)
            .filter(GSTSlab.hsn_id == hsn_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        slab: GSTSlab,
        updated_data: GSTSlabUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(slab, key, value)

        db.commit()

        db.refresh(slab)

        return slab

    @staticmethod
    def delete(
        db: Session,
        slab: GSTSlab,
    ):

        slab.is_active = False

        db.commit()

        db.refresh(slab)

        return slab