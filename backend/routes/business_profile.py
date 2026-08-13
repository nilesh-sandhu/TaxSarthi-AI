from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from core.database import get_db

from dependencies.auth import get_current_user

from models.user import User

from schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileUpdate,
    BusinessProfileResponse,
)

from services.business_profile import (
    create_business_profile,
    get_business_profiles,
    get_business_profile,
    update_business_profile,
    delete_business_profile,
)

from models.business_profile import BusinessProfile


router = APIRouter(
    prefix="/business-profiles",
    tags=["Business Profiles"],
)


# =====================================================
# CREATE BUSINESS PROFILE
# =====================================================

@router.post(
    "/",
    response_model=BusinessProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    profile: BusinessProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_business_profile(
        profile=profile,
        user_id=current_user.id,
        db=db,
    )


# =====================================================
# GET ALL BUSINESS PROFILES
# =====================================================

@router.get(
    "/",
    response_model=list[BusinessProfileResponse],
)
def all_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_business_profiles(
        user_id=current_user.id,
        db=db,
    )


# =====================================================
# GET SINGLE BUSINESS PROFILE
# =====================================================

@router.get(
    "/{business_id}",
    response_model=BusinessProfileResponse,
)
def single_profile(
    business_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    business = get_business_profile(
        business_id=business_id,
        db=db,
    )

    if business is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found.",
        )

    # -------------------------------------------------
    # Ownership check
    # -------------------------------------------------

    if business.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this business profile.",
        )

    return business


# =====================================================
# UPDATE BUSINESS PROFILE
# =====================================================

@router.put(
    "/{business_id}",
    response_model=BusinessProfileResponse,
)
def edit_profile(
    business_id: int,
    profile: BusinessProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    business = get_business_profile(
        business_id=business_id,
        db=db,
    )

    if business is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found.",
        )

    # -------------------------------------------------
    # Ownership check
    # -------------------------------------------------

    if business.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this business profile.",
        )

    return update_business_profile(
        business_id=business_id,
        profile=profile,
        db=db,
    )


# =====================================================
# DELETE BUSINESS PROFILE
# =====================================================

@router.delete(
    "/{business_id}",
)
def remove_profile(
    business_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    business = get_business_profile(
        business_id=business_id,
        db=db,
    )

    if business is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found.",
        )

    # -------------------------------------------------
    # Ownership check
    # -------------------------------------------------

    if business.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this business profile.",
        )

    return delete_business_profile(
        business_id=business_id,
        db=db,
    )