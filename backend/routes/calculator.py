from fastapi import APIRouter

from schemas.calculator import GSTCalculatorRequest
from services.gst_calculator import calculate_gst

router = APIRouter(
    prefix="/calculator",
    tags=["GST Calculator"],
)


@router.post("/")
def gst_calculator(data: GSTCalculatorRequest):

    return calculate_gst(
        amount=data.amount,
        gst_rate=data.gst_rate,
        calculation_type=data.calculation_type,
        interstate=data.interstate,
    )