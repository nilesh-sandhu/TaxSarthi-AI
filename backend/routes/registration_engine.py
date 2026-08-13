from fastapi import APIRouter

from schemas.registration import RegistrationRequest
from backend.routes.registration_engine import registration_engine

router = APIRouter(
    prefix="/registration",
    tags=["Registration Advisor"],
)


@router.post("/advisor")
def advisor(data: RegistrationRequest):

    result = registration_engine(
        business_type=data.business_type,
        turnover=data.turnover,
        state=data.state,
        interstate=data.interstate,
        ecommerce=data.ecommerce,
        gstin=data.gstin,
    )

    return result