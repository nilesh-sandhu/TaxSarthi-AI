from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.business_profile import BusinessProfileRepository
from schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileUpdate,
)


# =====================================================
# Create Business Profile
# =====================================================

def create_business_profile(
    profile: BusinessProfileCreate,
    user_id: int,
    db: Session,
):

    return BusinessProfileRepository.create(
        db=db,
        profile=profile,
        user_id=user_id,
    )


# =====================================================
# Get All Business Profiles
# =====================================================

def get_business_profiles(
    user_id: int,
    db: Session,
):

    return BusinessProfileRepository.get_all(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Get Business Profile By ID
# =====================================================

def get_business_profile(
    business_id: int,
    db: Session,
):

    business = BusinessProfileRepository.get_by_id(
        db=db,
        business_id=business_id,
    )

    if not business:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found.",
        )

    return business


# =====================================================
# Update Business Profile
# =====================================================

def update_business_profile(
    business_id: int,
    profile: BusinessProfileUpdate,
    db: Session,
):

    business = BusinessProfileRepository.get_by_id(
        db=db,
        business_id=business_id,
    )

    if not business:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found.",
        )

    return BusinessProfileRepository.update(
        db=db,
        business=business,
        updated_data=profile,
    )


# =====================================================
# Delete Business Profile
# =====================================================

def delete_business_profile(
    business_id: int,
    db: Session,
):

    business = BusinessProfileRepository.get_by_id(
        db=db,
        business_id=business_id,
    )

    if not business:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found.",
        )

    return BusinessProfileRepository.delete(
        db=db,
        business=business,
    )