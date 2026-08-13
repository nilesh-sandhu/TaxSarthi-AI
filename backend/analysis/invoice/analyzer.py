from sqlalchemy.orm import Session

from ai.invoice_ai import InvoiceAI
from ai.invoice_parser import InvoiceParser

from analysis.invoice.extractor import InvoiceExtractor
from analysis.invoice.item_extractor import ItemExtractor
from analysis.invoice.validator import InvoiceValidator
from analysis.invoice.gst_validator import GSTValidator
from analysis.invoice.hsn_validator import HSNValidator
from analysis.invoice.duplicate_detector import DuplicateDetector
from analysis.invoice.report import InvoiceReport


class InvoiceAnalyzer:

    @staticmethod
    def analyze(
        text: str,
        db: Session,
    ):

        print(
            "\n========== INVOICE ANALYZER ==========\n"
        )

        # =====================================================
        # STEP 1 : Regex Extraction
        # =====================================================

        invoice = InvoiceExtractor.extract(
            text
        )

        print(
            "Regex Extraction Completed"
        )

        # =====================================================
        # STEP 2 : Check Extraction Quality
        # =====================================================

        critical_fields = [

            "invoice_number",

            "invoice_date",

            "supplier",

            "supplier_gstin",

            "taxable_amount",

            "total_amount",

        ]

        missing_fields = [

            field

            for field in critical_fields

            if not invoice.get(field)

        ]

        # =====================================================
        # STEP 3 : Financial Consistency Check
        # =====================================================

        financial_data_invalid = False

        try:

            taxable = invoice.get(
                "taxable_amount"
            )

            cgst = invoice.get(
                "cgst"
            ) or 0

            sgst = invoice.get(
                "sgst"
            ) or 0

            igst = invoice.get(
                "igst"
            ) or 0

            total = invoice.get(
                "total_amount"
            )

            if (
                taxable is None
                or total is None
            ):

                financial_data_invalid = True

            else:

                calculated_total = (
                    float(taxable)
                    + float(cgst)
                    + float(sgst)
                    + float(igst)
                )

                difference = abs(
                    calculated_total
                    - float(total)
                )

                # Allow small rounding difference

                if difference > 2:

                    financial_data_invalid = True

                    print(
                        "Financial data mismatch detected."
                    )

                    print(
                        f"Calculated Total : "
                        f"{calculated_total}"
                    )

                    print(
                        f"Extracted Total  : "
                        f"{total}"
                    )

                    print(
                        f"Difference       : "
                        f"{difference}"
                    )

        except Exception as e:

            financial_data_invalid = True

            print(
                "Financial consistency check error:",
                e,
            )

        # =====================================================
        # STEP 4 : GST Data Check
        # =====================================================

        gst_data_invalid = False

        try:

            gst_rate = invoice.get(
                "gst_rate"
            )

            taxable = invoice.get(
                "taxable_amount"
            )

            cgst = invoice.get(
                "cgst"
            ) or 0

            sgst = invoice.get(
                "sgst"
            ) or 0

            igst = invoice.get(
                "igst"
            ) or 0

            # If taxable amount exists but
            # no GST amount exists, ask AI.

            if taxable is not None:

                total_tax = (
                    float(cgst)
                    + float(sgst)
                    + float(igst)
                )

                if (
                    total_tax == 0
                    and float(taxable) > 0
                ):

                    gst_data_invalid = True

            # If GST rate exists, verify it
            # against actual tax amount.

            if (
                gst_rate is not None
                and taxable is not None
            ):

                expected_tax = (
                    float(taxable)
                    * float(gst_rate)
                    / 100
                )

                actual_tax = (
                    float(cgst)
                    + float(sgst)
                    + float(igst)
                )

                if abs(
                    expected_tax
                    - actual_tax
                ) > 2:

                    gst_data_invalid = True

                    print(
                        "GST extraction mismatch detected."
                    )

        except Exception as e:

            gst_data_invalid = True

            print(
                "GST consistency check error:",
                e,
            )

        # =====================================================
        # STEP 5 : AI Fallback
        # =====================================================

        needs_ai_extraction = (

            len(missing_fields) > 0

            or financial_data_invalid

            or gst_data_invalid

        )

        if needs_ai_extraction:

            print(
                "\n========== AI INVOICE EXTRACTION =========="
            )

            print(
                "Missing fields:",
                missing_fields,
            )

            print(
                "Financial data invalid:",
                financial_data_invalid,
            )

            print(
                "GST data invalid:",
                gst_data_invalid,
            )

            try:

                ai_invoice = InvoiceAI.extract(
                    text
                )

                if ai_invoice:

                    print(
                        "\nAI Invoice Data:"
                    )

                    print(
                        ai_invoice
                    )

                    # -----------------------------------------
                    # Smart Merge
                    # -----------------------------------------

                    invoice = InvoiceParser.merge(

                        regex_data=invoice,

                        ai_data=ai_invoice,

                    )

                    print(
                        "\nAI Invoice Extraction Completed"
                    )

                else:

                    print(
                        "AI Invoice Extraction returned no data."
                    )

            except Exception as e:

                print(
                    "AI Invoice Extraction Error:",
                    e,
                )

        # =====================================================
        # STEP 6 : Item Extraction
        # =====================================================

        try:

            invoice["items"] = (
                ItemExtractor.extract(
                    text
                )
            )

        except Exception as e:

            print(
                "Item Extraction Error:",
                e,
            )

            invoice["items"] = []

        print(
            "Item Extraction Completed"
        )

        # =====================================================
        # STEP 7 : Invoice Validation
        # =====================================================

        validation = (
            InvoiceValidator.validate(
                invoice
            )
        )

        print(
            "Invoice Validation Completed"
        )

        # =====================================================
        # STEP 8 : GST Validation
        # =====================================================

        gst_validation = (
            GSTValidator.validate(
                invoice
            )
        )

        # -----------------------------------------------------
        # Avoid duplicate validation messages
        # -----------------------------------------------------

        existing_errors = validation.get(
            "errors",
            []
        )

        gst_errors = gst_validation.get(
            "errors",
            []
        )

        for error in gst_errors:

            if error not in existing_errors:

                existing_errors.append(
                    error
                )

        validation["errors"] = (
            existing_errors
        )

        validation["gst_validation"] = (
            gst_validation
        )

        print(
            "GST Validation Completed"
        )

        # =====================================================
        # STEP 9 : HSN Validation
        # =====================================================

        for item in invoice.get(
            "items",
            [],
        ):

            try:

                hsn_result = (
                    HSNValidator.validate(

                        hsn_code=item.get(
                            "hsn"
                        ),

                        invoice_rate=item.get(
                            "gst_rate",
                            invoice.get(
                                "gst_rate",
                                18,
                            ),
                        ),

                        db=db,

                    )
                )

                item["hsn_validation"] = (
                    hsn_result
                )

            except Exception as e:

                print(
                    "HSN Validation Error:",
                    e,
                )

                item["hsn_validation"] = {

                    "valid": False,

                    "message": str(e),

                }

        print(
            "HSN Validation Completed"
        )

        # =====================================================
        # STEP 10 : Duplicate Detection
        # =====================================================

        try:

            duplicates = (
                DuplicateDetector.check(

                    invoice=invoice,

                    db=db,

                )
            )

        except Exception as e:

            print(
                "Duplicate Detection Error:",
                e,
            )

            duplicates = {

                "duplicate": False,

                "matches": [],

            }

        print(
            "Duplicate Detection Completed"
        )

        # =====================================================
        # STEP 11 : Generate Final Report
        # =====================================================

        report = InvoiceReport.generate(

            invoice=invoice,

            validation=validation,

            duplicates=duplicates,

        )

        print(
            "Report Generated"
        )

        print(
            "\n========== ANALYSIS COMPLETED ==========\n"
        )

        return report