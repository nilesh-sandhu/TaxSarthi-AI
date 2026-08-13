from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.gst_return import GSTReturn
from schemas.gst_return import (
    GSTReturnCreate,
    GSTReturnUpdate,
)


# -----------------------------
# Create Return
# -----------------------------
def create_return(data: GSTReturnCreate, db: Session):

    new_return = GSTReturn(
        return_name=data.return_name,
        description=data.description,
        due_date=data.due_date,
        frequency=data.frequency,
        late_fee=data.late_fee,
    )

    db.add(new_return)
    db.commit()
    db.refresh(new_return)

    return new_return


# -----------------------------
# Get All Returns
# -----------------------------
def get_returns(db: Session):

    return db.query(GSTReturn).all()


# -----------------------------
# Get Return By ID
# -----------------------------
def get_return(return_id: int, db: Session):

    gst_return = (
        db.query(GSTReturn)
        .filter(GSTReturn.id == return_id)
        .first()
    )

    if not gst_return:
        raise HTTPException(
            status_code=404,
            detail="GST Return not found."
        )

    return gst_return


# -----------------------------
# Search Return
# -----------------------------
def search_return(name: str, db: Session):

    gst_return = (
        db.query(GSTReturn)
        .filter(GSTReturn.return_name.ilike(f"%{name}%"))
        .first()
    )

    if not gst_return:
        raise HTTPException(
            status_code=404,
            detail="GST Return not found."
        )

    return gst_return


# -----------------------------
# Update Return
# -----------------------------
def update_return(
    return_id: int,
    data: GSTReturnUpdate,
    db: Session,
):

    gst_return = (
        db.query(GSTReturn)
        .filter(GSTReturn.id == return_id)
        .first()
    )

    if not gst_return:
        raise HTTPException(
            status_code=404,
            detail="GST Return not found."
        )

    gst_return.return_name = data.return_name
    gst_return.description = data.description
    gst_return.due_date = data.due_date
    gst_return.frequency = data.frequency
    gst_return.late_fee = data.late_fee

    db.commit()
    db.refresh(gst_return)

    return gst_return


# -----------------------------
# Delete Return
# -----------------------------
def delete_return(return_id: int, db: Session):

    gst_return = (
        db.query(GSTReturn)
        .filter(GSTReturn.id == return_id)
        .first()
    )

    if not gst_return:
        raise HTTPException(
            status_code=404,
            detail="GST Return not found."
        )

    db.delete(gst_return)
    db.commit()

    return {
        "message": "GST Return deleted successfully."
    }