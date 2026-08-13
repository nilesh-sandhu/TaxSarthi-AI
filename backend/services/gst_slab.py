from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.gst_slab import GSTSlabRepository
from schemas.gst_slab import (
    GSTSlabCreate,
    GSTSlabUpdate,
)


def create_gst_slab(
    slab: GSTSlabCreate,
    db: Session,
):

    existing = GSTSlabRepository.get_by_hsn(
        db,
        slab.hsn_id,
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GST Slab already exists for this HSN.",
        )

    return GSTSlabRepository.create(
        db,
        slab,
    )


def get_gst_slabs(db: Session):

    return GSTSlabRepository.get_all(db)


def get_gst_slab(
    slab_id: int,
    db: Session,
):

    slab = GSTSlabRepository.get_by_id(
        db,
        slab_id,
    )

    if not slab:

        raise HTTPException(
            status_code=404,
            detail="GST Slab not found.",
        )

    return slab


def update_gst_slab(
    slab_id: int,
    slab: GSTSlabUpdate,
    db: Session,
):

    existing = GSTSlabRepository.get_by_id(
        db,
        slab_id,
    )

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="GST Slab not found.",
        )

    return GSTSlabRepository.update(
        db,
        existing,
        slab,
    )


def delete_gst_slab(
    slab_id: int,
    db: Session,
):

    existing = GSTSlabRepository.get_by_id(
        db,
        slab_id,
    )

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="GST Slab not found.",
        )

    return GSTSlabRepository.delete(
        db,
        existing,
    )