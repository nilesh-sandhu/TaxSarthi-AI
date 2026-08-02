from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.faq import FAQ
from schemas.faq import FAQCreate, FAQUpdate


# -----------------------------
# Create FAQ
# -----------------------------
def create_faq(faq: FAQCreate, db: Session):

    new_faq = FAQ(
        question=faq.question,
        answer=faq.answer,
        category=faq.category,
    )

    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)

    return new_faq


# -----------------------------
# Get All FAQ
# -----------------------------
def get_all_faq(db: Session):

    return db.query(FAQ).all()


# -----------------------------
# Get FAQ By ID
# -----------------------------
def get_faq(faq_id: int, db: Session):

    faq = db.query(FAQ).filter(
        FAQ.id == faq_id
    ).first()

    if not faq:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found."
        )

    return faq


# -----------------------------
# Search FAQ
# -----------------------------
def search_faq(question: str, db: Session):

    faq = (
        db.query(FAQ)
        .filter(FAQ.question.ilike(f"%{question}%"))
        .first()
    )

    if not faq:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found."
        )

    return faq


# -----------------------------
# Update FAQ
# -----------------------------
def update_faq(
    faq_id: int,
    faq: FAQUpdate,
    db: Session,
):

    existing = db.query(FAQ).filter(
        FAQ.id == faq_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found."
        )

    existing.question = faq.question
    existing.answer = faq.answer
    existing.category = faq.category

    db.commit()
    db.refresh(existing)

    return existing


# -----------------------------
# Delete FAQ
# -----------------------------
def delete_faq(
    faq_id: int,
    db: Session,
):

    faq = db.query(FAQ).filter(
        FAQ.id == faq_id
    ).first()

    if not faq:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found."
        )

    db.delete(faq)
    db.commit()

    return {
        "message": "FAQ deleted successfully."
    }