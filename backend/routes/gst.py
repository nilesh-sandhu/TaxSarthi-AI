from fastapi import APIRouter

from schemas.gst import (
    GSTCalculationRequest,
    GSTCalculationResponse,
)

from services.gst import calculate_gst

router = APIRouter(
    prefix="/gst",
    tags=["GST Calculator"],
)


@router.post(
    "/calculate",
    response_model=GSTCalculationResponse,
)
def gst_calculator(request: GSTCalculationRequest):
    return calculate_gst(request)