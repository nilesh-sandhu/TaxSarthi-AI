from sqlalchemy.orm import Session

from models.business_profile import BusinessProfile
from schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileUpdate,
)


class BusinessProfileRepository:

    # =====================================================
    # Create Business Profile
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        profile: BusinessProfileCreate,
        user_id: int,
    ):

        business = BusinessProfile(
            user_id=user_id,
            **profile.model_dump(),
        )

        db.add(business)
        db.commit()
        db.refresh(business)

        return business

    # =====================================================
    # Get All Businesses of User
    # =====================================================

    @staticmethod
    def get_all(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(BusinessProfile)
            .filter(
                BusinessProfile.user_id == user_id,
                BusinessProfile.is_active == True,
            )
            .order_by(BusinessProfile.business_name.asc())
            .all()
        )

    # =====================================================
    # Get Business By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        business_id: int,
    ):

        return (
            db.query(BusinessProfile)
            .filter(
                BusinessProfile.id == business_id,
                BusinessProfile.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Update Business
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        business: BusinessProfile,
        updated_data: BusinessProfileUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                business,
                key,
                value,
            )

        db.commit()
        db.refresh(business)

        return business

    # =====================================================
    # Soft Delete Business
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        business: BusinessProfile,
    ):

        business.is_active = False

        db.commit()
        db.refresh(business)

        return business