from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.compliance import Compliance

from repositories.compliance import (
    ComplianceRepository,
)

from schemas.compliance import (
    ComplianceCreate,
    ComplianceUpdate,
)


# =====================================================
# Create
# =====================================================

def create_compliance(
    compliance: ComplianceCreate,
    db: Session,
):

    existing = (
        db.query(Compliance)
        .filter(
            Compliance.title == compliance.title
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compliance already exists.",
        )

    new_compliance = Compliance(
        **compliance.model_dump()
    )

    return ComplianceRepository.create(
        db,
        new_compliance,
    )


# =====================================================
# Get All
# =====================================================

def get_compliances(
    db: Session,
):

    return ComplianceRepository.get_all(db)


# =====================================================
# Get By ID
# =====================================================

def get_compliance(
    compliance_id: int,
    db: Session,
):

    compliance = ComplianceRepository.get_by_id(
        db,
        compliance_id,
    )

    if not compliance:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance not found.",
        )

    return compliance


# =====================================================
# Search
# =====================================================

def search_compliance(
    query: str,
    db: Session,
):

    return ComplianceRepository.search(
        db,
        query,
    )


# =====================================================
# Update
# =====================================================

def update_compliance(
    compliance_id: int,
    data: ComplianceUpdate,
    db: Session,
):

    compliance = ComplianceRepository.get_by_id(
        db,
        compliance_id,
    )

    if not compliance:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance not found.",
        )

    values = data.model_dump(
        exclude_unset=True,
    )

    for key, value in values.items():

        setattr(
            compliance,
            key,
            value,
        )

    return ComplianceRepository.update(
        db,
        compliance,
    )


# =====================================================
# Delete
# =====================================================

def delete_compliance(
    compliance_id: int,
    db: Session,
):

    compliance = ComplianceRepository.get_by_id(
        db,
        compliance_id,
    )

    if not compliance:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance not found.",
        )

    ComplianceRepository.delete(
        db,
        compliance,
    )

    return {
        "message": "Compliance deleted successfully."
    }