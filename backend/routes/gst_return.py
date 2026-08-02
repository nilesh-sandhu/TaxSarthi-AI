from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.gst_return import (
    GSTReturnCreate,
    GSTReturnUpdate,
    GSTReturnResponse,
)

from services.gst_return import (
    create_return,
    get_returns,
    get_return,
    search_return,
    update_return,
    delete_return,
)

router = APIRouter(
    prefix="/returns",
    tags=["GST Returns"],
)


# Create
@router.post("/", response_model=GSTReturnResponse)
def add_return(
    data: GSTReturnCreate,
    db: Session = Depends(get_db),
):
    return create_return(data, db)


# Get All
@router.get("/", response_model=list[GSTReturnResponse])
def all_returns(
    db: Session = Depends(get_db),
):
    return get_returns(db)


# Search
@router.get("/search/{name}", response_model=GSTReturnResponse)
def find_return(
    name: str,
    db: Session = Depends(get_db),
):
    return search_return(name, db)


# Get By ID
@router.get("/{return_id}", response_model=GSTReturnResponse)
def single_return(
    return_id: int,
    db: Session = Depends(get_db),
):
    return get_return(return_id, db)


# Update
@router.put("/{return_id}", response_model=GSTReturnResponse)
def edit_return(
    return_id: int,
    data: GSTReturnUpdate,
    db: Session = Depends(get_db),
):
    return update_return(return_id, data, db)


# Delete
@router.delete("/{return_id}")
def remove_return(
    return_id: int,
    db: Session = Depends(get_db),
):
    return delete_return(return_id, db)