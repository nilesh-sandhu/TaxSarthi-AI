import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from models.document import Document
from repositories.document import DocumentRepository

from ocr.pdf_reader import PDFReader
from analysis.dispatcher import analyze_document
from services.invoice_analysis import InvoiceAnalysisService

from schemas.document import DocumentResponse


UPLOAD_FOLDER = "uploads/documents"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)


class DocumentService:

    # =====================================================
    # Upload Document
    # =====================================================

    @staticmethod
    def upload_document(
        db: Session,
        user_id: int,
        business_id: int | None,
        document_type: str,
        file: UploadFile,
    ):

        # -------------------------------------------------
        # Validate File
        # -------------------------------------------------

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="Invalid file.",
            )

        # -------------------------------------------------
        # Validate Document Type
        # -------------------------------------------------

        if not document_type:

            raise HTTPException(
                status_code=400,
                detail="Document type is required.",
            )

        # -------------------------------------------------
        # Generate Unique File Name
        # -------------------------------------------------

        extension = os.path.splitext(
            file.filename
        )[1]

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        save_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename,
        )

        # -------------------------------------------------
        # Save File
        # -------------------------------------------------

        try:

            with open(
                save_path,
                "wb",
            ) as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"File upload failed: {str(e)}",
            )

        # -------------------------------------------------
        # Save Document
        # -------------------------------------------------

        document = Document(

            user_id=user_id,

            business_id=business_id,

            document_name=file.filename,

            document_type=document_type,

            file_path=save_path,

            status="Uploaded",

        )

        saved_document = (
            DocumentRepository.create(
                db=db,
                document=document,
            )
        )

        # -------------------------------------------------
        # Analysis Result
        # -------------------------------------------------

        analysis_result = None

        # -------------------------------------------------
        # Extract PDF Text
        # -------------------------------------------------

        extracted_text = ""

        try:

            extracted_text = (
                PDFReader.extract(
                    save_path
                )
            )

            saved_document.extracted_text = (
                extracted_text
            )

            saved_document.status = (
                "Processed"
            )

            DocumentRepository.update(
                db=db,
                document=saved_document,
            )

            print(
                "\n========== PDF TEXT =========="
            )

            print(
                extracted_text[:500]
            )

            print(
                "==============================\n"
            )

        except Exception as e:

            print(
                "\nPDF Extraction Error"
            )

            print(e)

            saved_document.status = (
                "Failed"
            )

            DocumentRepository.update(
                db=db,
                document=saved_document,
            )

            # Return document with error
            response = (
                DocumentResponse.model_validate(
                    saved_document
                ).model_dump()
            )

            response["analysis"] = {
                "success": False,
                "error": "Unable to extract text from document.",
            }

            return response

        # -------------------------------------------------
        # Invoice Analysis
        # -------------------------------------------------

        try:

            analysis_result = (
                analyze_document(

                    document=saved_document,

                    text=extracted_text,

                    db=db,

                )
            )

            print(
                "\n========== ANALYSIS RESULT =========="
            )

            print(
                analysis_result
            )

            print(
                "=====================================\n"
            )

            # -------------------------------------------------
            # Save Invoice Analysis
            # -------------------------------------------------

            if analysis_result.get(
                "success",
                False,
            ):

                if (
                    saved_document
                    .document_type
                    .lower()
                    == "invoice"
                ):

                    InvoiceAnalysisService.save_analysis(

                        db=db,

                        document_id=saved_document.id,

                        report=analysis_result,

                    )

                    print(
                        "Invoice Analysis Saved Successfully"
                    )

                else:

                    print(
                        "Document is not an invoice."
                    )

            else:

                print(
                    "Analysis Failed"
                )

        except Exception as e:

            print(
                "\nInvoice Analysis Error"
            )

            print(e)

            analysis_result = {

                "success": False,

                "error": str(e),

            }

        # -------------------------------------------------
        # Build API Response
        # -------------------------------------------------

        response = (
            DocumentResponse.model_validate(
                saved_document
            ).model_dump()
        )

        response["analysis"] = (
            analysis_result
        )

        return response


    # =====================================================
    # Get Document
    # =====================================================

    @staticmethod
    def get_document(
        db: Session,
        document_id: int,
    ):

        document = (
            DocumentRepository.get_by_id(

                db=db,

                document_id=document_id,

            )
        )

        if document is None:

            raise HTTPException(

                status_code=404,

                detail="Document not found.",

            )

        return document


    # =====================================================
    # Get Documents
    # =====================================================

    @staticmethod
    def get_documents(
        db: Session,
        user_id: int,
    ):

        return (
            DocumentRepository.get_all(

                db=db,

                user_id=user_id,

            )
        )


    # =====================================================
    # Delete Document
    # =====================================================

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int,
    ):

        document = (
            DocumentRepository.get_by_id(

                db=db,

                document_id=document_id,

            )
        )

        if document is None:

            raise HTTPException(

                status_code=404,

                detail="Document not found.",

            )

        if os.path.exists(
            document.file_path
        ):

            os.remove(
                document.file_path
            )

        DocumentRepository.delete(

            db=db,

            document=document,

        )

        return {

            "success": True,

            "message":
                "Document deleted successfully.",

        }