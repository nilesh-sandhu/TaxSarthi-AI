from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.gst_slab import (
    GSTSlabCreate,
    GSTSlabUpdate,
    GSTSlabResponse,
)

from services.gst_slab import (
    create_gst_slab,
    get_gst_slabs,
    get_gst_slab,
    update_gst_slab,
    delete_gst_slab,
)

router = APIRouter(
    prefix="/gst-slabs",
    tags=["GST Slabs"],
)


@router.post("/", response_model=GSTSlabResponse, status_code=201)
def add_slab(
    slab: GSTSlabCreate,
    db: Session = Depends(get_db),
):
    return create_gst_slab(slab, db)


@router.get("/", response_model=list[GSTSlabResponse])
def all_slabs(
    db: Session = Depends(get_db),
):
    return get_gst_slabs(db)


@router.get("/{slab_id}", response_model=GSTSlabResponse)
def single_slab(
    slab_id: int,
    db: Session = Depends(get_db),
):
    return get_gst_slab(slab_id, db)


@router.put("/{slab_id}", response_model=GSTSlabResponse)
def edit_slab(
    slab_id: int,
    slab: GSTSlabUpdate,
    db: Session = Depends(get_db),
):
    return update_gst_slab(slab_id, slab, db)


@router.delete("/{slab_id}")
def remove_slab(
    slab_id: int,
    db: Session = Depends(get_db),
):
    return delete_gst_slab(slab_id, db)