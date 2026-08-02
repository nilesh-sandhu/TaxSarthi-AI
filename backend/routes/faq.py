from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.faq import (
    FAQCreate,
    FAQUpdate,
    FAQResponse,
)

from services.faq import (
    create_faq,
    get_all_faq,
    get_faq,
    search_faq,
    update_faq,
    delete_faq,
)

router = APIRouter(
    prefix="/faq",
    tags=["FAQ"],
)


# -----------------------------
# Create FAQ
# -----------------------------
@router.post("/", response_model=FAQResponse)
def add_faq(
    faq: FAQCreate,
    db: Session = Depends(get_db),
):
    return create_faq(faq, db)


# -----------------------------
# Get All FAQ
# -----------------------------
@router.get("/", response_model=list[FAQResponse])
def all_faq(
    db: Session = Depends(get_db),
):
    return get_all_faq(db)


# -----------------------------
# Search FAQ
# -----------------------------
@router.get(
    "/search/{question}",
    response_model=FAQResponse,
)
def find_faq(
    question: str,
    db: Session = Depends(get_db),
):
    return search_faq(question, db)


# -----------------------------
# Get FAQ By ID
# -----------------------------
@router.get(
    "/{faq_id}",
    response_model=FAQResponse,
)
def single_faq(
    faq_id: int,
    db: Session = Depends(get_db),
):
    return get_faq(faq_id, db)


# -----------------------------
# Update FAQ
# -----------------------------
@router.put(
    "/{faq_id}",
    response_model=FAQResponse,
)
def edit_faq(
    faq_id: int,
    faq: FAQUpdate,
    db: Session = Depends(get_db),
):
    return update_faq(faq_id, faq, db)


# -----------------------------
# Delete FAQ
# -----------------------------
@router.delete("/{faq_id}")
def remove_faq(
    faq_id: int,
    db: Session = Depends(get_db),
):
    return delete_faq(faq_id, db)