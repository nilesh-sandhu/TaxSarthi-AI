from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.circular import (
    CircularCreate,
    CircularUpdate,
    CircularResponse,
)

from services.circular import (
    create_circular,
    get_circulars,
    get_circular,
    search_circular,
    update_circular,
    delete_circular,
)

router = APIRouter(
    prefix="/circulars",
    tags=["GST Circulars"],
)


# =====================================================
# Create
# =====================================================

@router.post(
    "/",
    response_model=CircularResponse,
)
def add_circular(
    circular: CircularCreate,
    db: Session = Depends(get_db),
):

    return create_circular(
        circular,
        db,
    )


# =====================================================
# Get All
# =====================================================

@router.get(
    "/",
    response_model=list[CircularResponse],
)
def all_circulars(
    db: Session = Depends(get_db),
):

    return get_circulars(db)


# =====================================================
# Search
# =====================================================

@router.get(
    "/search/{query}",
)
def search(
    query: str,
    db: Session = Depends(get_db),
):

    return search_circular(
        query,
        db,
    )


# =====================================================
# Get By ID
# =====================================================

@router.get(
    "/{circular_id}",
    response_model=CircularResponse,
)
def single_circular(
    circular_id: int,
    db: Session = Depends(get_db),
):

    return get_circular(
        circular_id,
        db,
    )


# =====================================================
# Update
# =====================================================

@router.put(
    "/{circular_id}",
    response_model=CircularResponse,
)
def edit_circular(
    circular_id: int,
    circular: CircularUpdate,
    db: Session = Depends(get_db),
):

    return update_circular(
        circular_id,
        circular,
        db,
    )


# =====================================================
# Delete
# =====================================================

@router.delete(
    "/{circular_id}",
)
def remove_circular(
    circular_id: int,
    db: Session = Depends(get_db),
):

    return delete_circular(
        circular_id,
        db,
    )