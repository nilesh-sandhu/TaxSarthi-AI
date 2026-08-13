from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from services.invoice_analysis import (
    InvoiceAnalysisService,
)

router = APIRouter(

    prefix="/invoice-analysis",

    tags=["Invoice Analysis"],

)


# =====================================================
# Get Analysis
# =====================================================

@router.get("/{document_id}")

def get_invoice_analysis(

    document_id: int,

    db: Session = Depends(get_db),

):

    analysis = InvoiceAnalysisService.get_analysis(

        db=db,

        document_id=document_id,

    )

    if analysis is None:

        return {

            "success": False,

            "message": "Analysis not found."

        }

    return analysis