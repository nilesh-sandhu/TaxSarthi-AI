from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.hsn import (
    HSNCreate,
    HSNUpdate,
    HSNResponse,
)

from services.hsn import (
    create_hsn,
    get_all_hsn,
    get_hsn,
    search_hsn,
    search_product,
    update_hsn,
    delete_hsn,
)

router = APIRouter(
    prefix="/hsn",
    tags=["HSN Master"],
)


# =====================================================
# Create HSN
# =====================================================

@router.post(
    "/",
    response_model=HSNResponse,
    status_code=201,
)
def add_hsn(
    hsn: HSNCreate,
    db: Session = Depends(get_db),
):

    return create_hsn(
        hsn,
        db,
    )


# =====================================================
# Get All HSN
# =====================================================

@router.get(
    "/",
    response_model=list[HSNResponse],
)
def all_hsn(
    db: Session = Depends(get_db),
):

    return get_all_hsn(db)


# =====================================================
# Search By HSN Code
# =====================================================

@router.get(
    "/search/code/{code}",
    response_model=list[HSNResponse],
)
def find_hsn(
    code: str,
    db: Session = Depends(get_db),
):

    return search_hsn(
        code,
        db,
    )


# =====================================================
# Search By Product Name
# =====================================================

@router.get(
    "/search/product/{product}",
    response_model=list[HSNResponse],
)
def find_product(
    product: str,
    db: Session = Depends(get_db),
):

    return search_product(
        product,
        db,
    )


# =====================================================
# Get HSN By ID
# =====================================================

@router.get(
    "/{hsn_id}",
    response_model=HSNResponse,
)
def single_hsn(
    hsn_id: int,
    db: Session = Depends(get_db),
):

    return get_hsn(
        hsn_id,
        db,
    )


# =====================================================
# Update HSN
# =====================================================

@router.put(
    "/{hsn_id}",
    response_model=HSNResponse,
)
def edit_hsn(
    hsn_id: int,
    hsn: HSNUpdate,
    db: Session = Depends(get_db),
):

    return update_hsn(
        hsn_id,
        hsn,
        db,
    )


# =====================================================
# Delete HSN
# =====================================================

@router.delete(
    "/{hsn_id}",
)
def remove_hsn(
    hsn_id: int,
    db: Session = Depends(get_db),
):

    return delete_hsn(
        hsn_id,
        db,
    )