from fastapi import APIRouter

from schemas.registration import (
    RegistrationRequest,
    RegistrationResponse,
)

from services.registration import check_registration

router = APIRouter(
    prefix="/registration",
    tags=["GST Registration"],
)


@router.post(
    "/check",
    response_model=RegistrationResponse,
)
def registration_check(request: RegistrationRequest):
    return check_registration(request)