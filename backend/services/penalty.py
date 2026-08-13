from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.penalty import Penalty

from repositories.penalty import (
    PenaltyRepository,
)

from schemas.penalty import (
    PenaltyCreate,
    PenaltyUpdate,
)


# =====================================================
# Create Penalty
# =====================================================

def create_penalty(
    penalty: PenaltyCreate,
    db: Session,
):

    existing = (
        db.query(Penalty)
        .filter(
            Penalty.title == penalty.title
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Penalty already exists.",
        )

    new_penalty = Penalty(
        **penalty.model_dump()
    )

    return PenaltyRepository.create(
        db,
        new_penalty,
    )


# =====================================================
# Get All Penalties
# =====================================================

def get_penalties(
    db: Session,
):

    return PenaltyRepository.get_all(db)


# =====================================================
# Get Penalty By ID
# =====================================================

def get_penalty(
    penalty_id: int,
    db: Session,
):

    penalty = PenaltyRepository.get_by_id(
        db,
        penalty_id,
    )

    if not penalty:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penalty not found.",
        )

    return penalty


# =====================================================
# Search Penalty
# =====================================================

def search_penalty(
    query: str,
    db: Session,
):

    return PenaltyRepository.search(
        db,
        query,
    )


# =====================================================
# Update Penalty
# =====================================================

def update_penalty(
    penalty_id: int,
    data: PenaltyUpdate,
    db: Session,
):

    penalty = PenaltyRepository.get_by_id(
        db,
        penalty_id,
    )

    if not penalty:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penalty not found.",
        )

    values = data.model_dump(
        exclude_unset=True,
    )

    for key, value in values.items():

        setattr(
            penalty,
            key,
            value,
        )

    return PenaltyRepository.update(
        db,
        penalty,
    )


# =====================================================
# Delete Penalty
# =====================================================

def delete_penalty(
    penalty_id: int,
    db: Session,
):

    penalty = PenaltyRepository.get_by_id(
        db,
        penalty_id,
    )

    if not penalty:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penalty not found.",
        )

    PenaltyRepository.delete(
        db,
        penalty,
    )

    return {
        "message": "Penalty deleted successfully."
    }