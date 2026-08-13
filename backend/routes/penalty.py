from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.penalty import (
    PenaltyCreate,
    PenaltyUpdate,
    PenaltyResponse,
)

from services.penalty import (
    create_penalty,
    get_penalties,
    get_penalty,
    search_penalty,
    update_penalty,
    delete_penalty,
)

router = APIRouter(
    prefix="/penalties",
    tags=["Penalties"],
)


# =====================================================
# Create
# =====================================================

@router.post(
    "/",
    response_model=PenaltyResponse,
)
def add_penalty(
    penalty: PenaltyCreate,
    db: Session = Depends(get_db),
):

    return create_penalty(
        penalty,
        db,
    )


# =====================================================
# Get All
# =====================================================

@router.get(
    "/",
    response_model=list[PenaltyResponse],
)
def all_penalties(
    db: Session = Depends(get_db),
):

    return get_penalties(db)


# =====================================================
# Search
# =====================================================

@router.get("/search/{query}")
def search(
    query: str,
    db: Session = Depends(get_db),
):

    return search_penalty(
        query,
        db,
    )


# =====================================================
# Get By ID
# =====================================================

@router.get(
    "/{penalty_id}",
    response_model=PenaltyResponse,
)
def single_penalty(
    penalty_id: int,
    db: Session = Depends(get_db),
):

    return get_penalty(
        penalty_id,
        db,
    )


# =====================================================
# Update
# =====================================================

@router.put(
    "/{penalty_id}",
    response_model=PenaltyResponse,
)
def edit_penalty(
    penalty_id: int,
    penalty: PenaltyUpdate,
    db: Session = Depends(get_db),
):

    return update_penalty(
        penalty_id,
        penalty,
        db,
    )


# =====================================================
# Delete
# =====================================================

@router.delete(
    "/{penalty_id}",
)
def remove_penalty(
    penalty_id: int,
    db: Session = Depends(get_db),
):

    return delete_penalty(
        penalty_id,
        db,
    )