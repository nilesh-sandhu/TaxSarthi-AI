from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.compliance import (
    ComplianceCreate,
    ComplianceUpdate,
    ComplianceResponse,
)

from services.compliance import (
    create_compliance,
    get_compliances,
    get_compliance,
    search_compliance,
    update_compliance,
    delete_compliance,
)

router = APIRouter(
    prefix="/compliance",
    tags=["Compliance"],
)


# =====================================================
# Create
# =====================================================

@router.post(
    "/",
    response_model=ComplianceResponse,
)
def add_compliance(
    compliance: ComplianceCreate,
    db: Session = Depends(get_db),
):

    return create_compliance(
        compliance,
        db,
    )


# =====================================================
# Get All
# =====================================================

@router.get(
    "/",
    response_model=list[ComplianceResponse],
)
def all_compliances(
    db: Session = Depends(get_db),
):

    return get_compliances(db)


# =====================================================
# Search
# =====================================================

@router.get(
    "/search/{query}",
)
def search(
    query: str,
    db: Session = Depends(get_db),
):

    return search_compliance(
        query,
        db,
    )


# =====================================================
# Get By ID
# =====================================================

@router.get(
    "/{compliance_id}",
    response_model=ComplianceResponse,
)
def single_compliance(
    compliance_id: int,
    db: Session = Depends(get_db),
):

    return get_compliance(
        compliance_id,
        db,
    )


# =====================================================
# Update
# =====================================================

@router.put(
    "/{compliance_id}",
    response_model=ComplianceResponse,
)
def edit_compliance(
    compliance_id: int,
    compliance: ComplianceUpdate,
    db: Session = Depends(get_db),
):

    return update_compliance(
        compliance_id,
        compliance,
        db,
    )


# =====================================================
# Delete
# =====================================================

@router.delete(
    "/{compliance_id}",
)
def remove_compliance(
    compliance_id: int,
    db: Session = Depends(get_db),
):

    return delete_compliance(
        compliance_id,
        db,
    )