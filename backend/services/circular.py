from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.circular import Circular
from repositories.circular import CircularRepository
from schemas.circular import (
    CircularCreate,
    CircularUpdate,
)


# =====================================================
# Create Circular
# =====================================================

def create_circular(
    circular: CircularCreate,
    db: Session,
):

    existing = (
        db.query(Circular)
        .filter(
            Circular.circular_no == circular.circular_no
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Circular already exists.",
        )

    new_circular = Circular(
        **circular.model_dump()
    )

    return CircularRepository.create(
        db,
        new_circular,
    )


# =====================================================
# Get All Circulars
# =====================================================

def get_circulars(
    db: Session,
):

    return CircularRepository.get_all(db)


# =====================================================
# Get Circular By ID
# =====================================================

def get_circular(
    circular_id: int,
    db: Session,
):

    circular = CircularRepository.get_by_id(
        db,
        circular_id,
    )

    if not circular:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circular not found.",
        )

    return circular


# =====================================================
# Search Circular
# =====================================================

def search_circular(
    query: str,
    db: Session,
):

    return CircularRepository.search(
        db,
        query,
    )


# =====================================================
# Update Circular
# =====================================================

def update_circular(
    circular_id: int,
    data: CircularUpdate,
    db: Session,
):

    circular = CircularRepository.get_by_id(
        db,
        circular_id,
    )

    if not circular:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circular not found.",
        )

    values = data.model_dump(
        exclude_unset=True,
    )

    for key, value in values.items():

        setattr(
            circular,
            key,
            value,
        )

    return CircularRepository.update(
        db,
        circular,
    )


# =====================================================
# Delete Circular
# =====================================================

def delete_circular(
    circular_id: int,
    db: Session,
):

    circular = CircularRepository.get_by_id(
        db,
        circular_id,
    )

    if not circular:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circular not found.",
        )

    CircularRepository.delete(
        db,
        circular,
    )

    return {
        "message": "Circular deleted successfully."
    }