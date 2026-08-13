from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)

from sqlalchemy.orm import Session

from core.database import get_db

from schemas.document import (
    DocumentResponse,
)

from services.document import (
    DocumentService,
)

router = APIRouter(

    prefix="/documents",

    tags=["Documents"],

)


# =====================================================
# Upload Document
# =====================================================

@router.post(

    "/upload",

    response_model=DocumentResponse,

    status_code=201,

)

def upload_document(

    document_type: str = Form(...),

    business_id: int | None = Form(None),

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

):

    # Temporary User
    # JWT Integration Later

    user_id = 1

    return DocumentService.upload_document(

        db=db,

        user_id=user_id,

        business_id=business_id,

        document_type=document_type,

        file=file,

    )


# =====================================================
# Get All Documents
# =====================================================

@router.get(

    "/",

    response_model=list[DocumentResponse],

)

def get_documents(

    db: Session = Depends(get_db),

):

    user_id = 1

    return DocumentService.get_documents(

        db=db,

        user_id=user_id,

    )


# =====================================================
# Get Single Document
# =====================================================

@router.get(

    "/{document_id}",

    response_model=DocumentResponse,

)

def get_document(

    document_id: int,

    db: Session = Depends(get_db),

):

    return DocumentService.get_document(

        db=db,

        document_id=document_id,

    )


# =====================================================
# Delete Document
# =====================================================

@router.delete(

    "/{document_id}",

)

def delete_document(

    document_id: int,

    db: Session = Depends(get_db),

):

    return DocumentService.delete_document(

        db=db,

        document_id=document_id,

    )