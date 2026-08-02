from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.gst_form import GSTForm
from schemas.gst_form import (
    GSTFormCreate,
    GSTFormUpdate,
)


def create_form(data: GSTFormCreate, db: Session):

    form = GSTForm(
        form_name=data.form_name,
        purpose=data.purpose,
        applicability=data.applicability,
        description=data.description,
    )

    db.add(form)
    db.commit()
    db.refresh(form)

    return form


def get_forms(db: Session):

    return db.query(GSTForm).all()


def get_form(form_id: int, db: Session):

    form = db.query(GSTForm).filter(
        GSTForm.id == form_id
    ).first()

    if not form:
        raise HTTPException(
            status_code=404,
            detail="GST Form not found."
        )

    return form


def search_form(name: str, db: Session):

    form = (
        db.query(GSTForm)
        .filter(GSTForm.form_name.ilike(f"%{name}%"))
        .first()
    )

    if not form:
        raise HTTPException(
            status_code=404,
            detail="GST Form not found."
        )

    return form


def update_form(
    form_id: int,
    data: GSTFormUpdate,
    db: Session,
):

    form = db.query(GSTForm).filter(
        GSTForm.id == form_id
    ).first()

    if not form:
        raise HTTPException(
            status_code=404,
            detail="GST Form not found."
        )

    form.form_name = data.form_name
    form.purpose = data.purpose
    form.applicability = data.applicability
    form.description = data.description

    db.commit()
    db.refresh(form)

    return form


def delete_form(form_id: int, db: Session):

    form = db.query(GSTForm).filter(
        GSTForm.id == form_id
    ).first()

    if not form:
        raise HTTPException(
            status_code=404,
            detail="GST Form not found."
        )

    db.delete(form)
    db.commit()

    return {
        "message": "GST Form deleted successfully."
    }