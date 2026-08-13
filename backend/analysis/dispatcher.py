from sqlalchemy.orm import Session

from analysis.invoice.analyzer import InvoiceAnalyzer
from analysis.notice_analyzer import analyze_notice
from analysis.return_analyzer import analyze_return

from ocr.pdf_reader import PDFReader


# =====================================================
# Document Dispatcher
# =====================================================

def analyze_document(
    document,
    text: str = "",
    db: Session = None,
):

    print("\n========== DOCUMENT DISPATCHER ==========")
    print(f"Document Type : {document.document_type}")
    print("=========================================\n")

    document_type = document.document_type.lower()

    # =====================================================
    # Invoice
    # =====================================================

    if document_type == "invoice":

        if not text:

            return {
                "success": False,
                "message": "Invoice text not found.",
            }

        if db is None:

            return {
                "success": False,
                "message": "Database session missing.",
            }

        try:

            # =================================================
            # PAGE-WISE PDF PROCESSING
            # =================================================

            pages = PDFReader.extract_pages(
                document.file_path
            )

            print(
                f"\nInvoice PDF Pages Found : {len(pages)}"
            )

            # -------------------------------------------------
            # If page extraction fails, fallback to old method
            # -------------------------------------------------

            if not pages:

                result = InvoiceAnalyzer.analyze(
                    text=text,
                    db=db,
                )

                return result

            invoice_results = []

            # =================================================
            # Analyze Each Page Separately
            # =================================================

            for page_data in pages:

                page_number = page_data["page"]

                page_text = page_data["text"]

                print(
                    f"\n========== ANALYZING PAGE {page_number} =========="
                )

                print(
                    page_text[:500]
                )

                print(
                    "==============================================\n"
                )

                # -------------------------------------------------
                # Skip empty pages
                # -------------------------------------------------

                if not page_text.strip():

                    print(
                        f"Page {page_number} is empty. Skipping."
                    )

                    continue

                try:

                    result = InvoiceAnalyzer.analyze(

                        text=page_text,

                        db=db,

                    )

                    # Add page number to result

                    if isinstance(result, dict):

                        result["page"] = page_number

                    invoice_results.append(
                        result
                    )

                except Exception as e:

                    print(
                        f"Page {page_number} Analysis Error:"
                    )

                    print(e)

                    invoice_results.append({

                        "success": False,

                        "page": page_number,

                        "message": str(e),

                    })

            # =================================================
            # No Invoice Result
            # =================================================

            if not invoice_results:

                return {

                    "success": False,

                    "message": (
                        "No invoice could be detected "
                        "in the document."
                    ),

                    "invoices": [],

                }

            # =================================================
            # Single Invoice
            # =================================================
            #
            # Keep old response structure so existing
            # frontend/backend code does not break.
            #
            # =================================================

            if len(invoice_results) == 1:

                result = invoice_results[0]

                print(
                    "\n========== SINGLE INVOICE ANALYZED =========="
                )

                print(result)

                print(
                    "=============================================\n"
                )

                return result

            # =================================================
            # Multiple Invoices
            # =================================================

            successful_results = [

                result

                for result in invoice_results

                if result.get(
                    "success",
                    False,
                )

            ]

            overall_success = (
                len(successful_results) > 0
            )

            result = {

                "success": overall_success,

                "invoice_count": len(
                    invoice_results
                ),

                "successful_invoices": len(
                    successful_results
                ),

                "invoices": invoice_results,

            }

            print(
                "\n========== MULTIPLE INVOICES ANALYZED =========="
            )

            print(
                f"Total Invoices : {len(invoice_results)}"
            )

            print(
                f"Successful     : {len(successful_results)}"
            )

            print(
                "=================================================\n"
            )

            return result

        except Exception as e:

            print(
                "\n========== INVOICE ANALYSIS ERROR =========="
            )

            print(e)

            print(
                "============================================\n"
            )

            return {

                "success": False,

                "message": str(e),

            }

    # =====================================================
    # Notice
    # =====================================================

    elif document_type == "notice":

        try:

            return analyze_notice(
                document
            )

        except Exception as e:

            return {

                "success": False,

                "message": str(e),

            }

    # =====================================================
    # Return
    # =====================================================

    elif document_type == "return":

        try:

            return analyze_return(
                document
            )

        except Exception as e:

            return {

                "success": False,

                "message": str(e),

            }

    # =====================================================
    # Unsupported
    # =====================================================

    return {

        "success": False,

        "message": (
            f"Unsupported document type: "
            f"{document.document_type}"
        ),

    }