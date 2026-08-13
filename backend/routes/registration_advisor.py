from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.registration_advisor import (
    RegistrationAdvisorResponse,
)

from services.registration_advisor import (
    registration_advisor,
)

router = APIRouter(
    prefix="/registration-advisor",
    tags=["Registration Advisor"],
)


@router.get(
    "/{business_id}",
    response_model=RegistrationAdvisorResponse,
)
def get_registration_advice(
    business_id: int,
    db: Session = Depends(get_db),
):

    user_id = 1

    return registration_advisor(
        user_id,
        business_id,
        db,
    )