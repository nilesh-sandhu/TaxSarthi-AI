from sqlalchemy.orm import Session

from models.hsn import HSNMaster
from schemas.hsn import (
    HSNCreate,
    HSNUpdate,
)


class HSNRepository:

    # =====================================================
    # Create HSN
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        hsn: HSNCreate,
    ):

        new_hsn = HSNMaster(
            **hsn.model_dump()
        )

        db.add(new_hsn)
        db.commit()
        db.refresh(new_hsn)

        return new_hsn

    # =====================================================
    # Get All HSN
    # =====================================================

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(HSNMaster)
            .filter(
                HSNMaster.is_active == True
            )
            .order_by(
                HSNMaster.hsn_code.asc()
            )
            .all()
        )

    # =====================================================
    # Get HSN By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        hsn_id: int,
    ):

        return (
            db.query(HSNMaster)
            .filter(
                HSNMaster.id == hsn_id,
                HSNMaster.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Get HSN By Code
    # =====================================================

    @staticmethod
    def get_by_code(
        db: Session,
        hsn_code: str,
    ):

        return (
            db.query(HSNMaster)
            .filter(
                HSNMaster.hsn_code == hsn_code,
                HSNMaster.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Search HSN
    # =====================================================

    @staticmethod
    def search(
        db: Session,
        keyword: str,
    ):

        return (
            db.query(HSNMaster)
            .filter(
                HSNMaster.is_active == True,
                HSNMaster.hsn_code.ilike(
                    f"%{keyword}%"
                ),
            )
            .all()
        )

    # =====================================================
    # Update HSN
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        hsn: HSNMaster,
        updated_data: HSNUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                hsn,
                key,
                value,
            )

        db.commit()
        db.refresh(hsn)

        return hsn

    # =====================================================
    # Soft Delete
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        hsn: HSNMaster,
    ):

        hsn.is_active = False

        db.commit()
        db.refresh(hsn)

        return hsn