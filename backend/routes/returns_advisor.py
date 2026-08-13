from fastapi import APIRouter

from schemas.returns import ReturnAdvisorRequest
from services.return_engine import get_returns

router = APIRouter(
    prefix="/returns",
    tags=["GST Return Advisor"],
)


@router.post("/advisor")
def advisor(data: ReturnAdvisorRequest):

    return get_returns(
        data.registration_type
    )