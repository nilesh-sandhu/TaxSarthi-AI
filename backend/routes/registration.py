from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db

from repositories.business_profile import BusinessProfileRepository
from services.registration import check_registration

router = APIRouter(
    prefix="/registration",
    tags=["GST Registration"],
)


@router.get("/check/{user_id}")
def registration_check(
    user_id: int,
    db: Session = Depends(get_db),
):

    profile = BusinessProfileRepository.get_by_user(
        db,
        user_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found."
        )

    return check_registration(profile)