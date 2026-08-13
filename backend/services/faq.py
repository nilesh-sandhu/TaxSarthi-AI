from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.faq import FAQ
from schemas.faq import FAQCreate, FAQUpdate


# ==========================================================
# Create FAQ
# ==========================================================

def create_faq(
    faq: FAQCreate,
    db: Session,
):

    existing = (
        db.query(FAQ)
        .filter(FAQ.question == faq.question)
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="FAQ already exists.",
        )

    new_faq = FAQ(
        question=faq.question,
        answer=faq.answer,
    )

    db.add(new_faq)

    db.commit()

    db.refresh(new_faq)

    return new_faq


# ==========================================================
# Get All FAQs
# ==========================================================

def get_all_faq(
    db: Session,
):

    return db.query(FAQ).all()


# ==========================================================
# Get FAQ By ID
# ==========================================================

def get_faq(
    faq_id: int,
    db: Session,
):

    faq = (
        db.query(FAQ)
        .filter(FAQ.id == faq_id)
        .first()
    )

    if faq is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found.",
        )

    return faq


# ==========================================================
# Search FAQ
# ==========================================================

def search_faq(
    question: str,
    db: Session,
):

    faq = (
        db.query(FAQ)
        .filter(
            FAQ.question.ilike(f"%{question}%")
        )
        .all()
    )

    return faq


# ==========================================================
# Update FAQ
# ==========================================================

def update_faq(
    faq_id: int,
    faq: FAQUpdate,
    db: Session,
):

    existing = (
        db.query(FAQ)
        .filter(FAQ.id == faq_id)
        .first()
    )

    if existing is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found.",
        )

    update_data = faq.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(existing, key, value)

    db.commit()

    db.refresh(existing)

    return existing


# ==========================================================
# Delete FAQ
# ==========================================================

def delete_faq(
    faq_id: int,
    db: Session,
):

    faq = (
        db.query(FAQ)
        .filter(FAQ.id == faq_id)
        .first()
    )

    if faq is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found.",
        )

    db.delete(faq)

    db.commit()

    return {
        "message": "FAQ deleted successfully."
    }