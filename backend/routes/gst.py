from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.gst import (
    GSTCalculationRequest,
    GSTCalculationResponse,
    ProductGSTRequest,
    ProductGSTResponse,
)

from services.gst import calculate_gst
from core.database import get_db

from engines.gst_engine import product_gst


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


@router.post(
    "/product",
    response_model=ProductGSTResponse,
)
def gst_product_lookup(
    request: ProductGSTRequest,
    db: Session = Depends(get_db),
):
    """Lookup GST/HSN for a product name (used by frontend)."""
    result = product_gst(
        product_name=request.product_name,
        amount=request.amount,
        interstate=request.interstate,
        db=db,
    )

    # Ensure returned dict conforms: pydantic will validate/serialize
    return result