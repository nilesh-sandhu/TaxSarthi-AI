import re


class InvoiceExtractor:

    @staticmethod
    def extract(text: str):

        invoice = {

            "invoice_number": None,

            "invoice_date": None,

            "supplier": None,

            "buyer": None,

            "supplier_gstin": None,

            "buyer_gstin": None,

            "gstin": None,

            "items": [],

            "taxable_amount": None,

            "gst_rate": None,

            "cgst": None,

            "sgst": None,

            "igst": None,

            "total_amount": None,

        }

        # =====================================================
        # Invoice Number
        # =====================================================

        patterns = [

            r"Invoice\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\/\-]+)",

            r"Invoice\s*Number\s*[:\-]?\s*([A-Za-z0-9\/\-]+)",

            r"Inv\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\/\-]+)",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                invoice["invoice_number"] = match.group(1)

                break

        # =====================================================
        # Invoice Date
        # =====================================================

        date = re.search(

            r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",

            text,

        )

        if date:

            invoice["invoice_date"] = date.group()

        else:

            # Support formats such as 09-Aug-2026
            date = re.search(

                r"\b\d{1,2}[-/][A-Za-z]{3,9}[-/]\d{4}\b",

                text,

                re.IGNORECASE,

            )

            if date:

                invoice["invoice_date"] = date.group()

        # =====================================================
        # GSTINs
        # =====================================================

        gstins = re.findall(

            r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]{3}\b",

            text,

        )

        if len(gstins) >= 1:

            invoice["supplier_gstin"] = gstins[0]

            invoice["gstin"] = gstins[0]

        if len(gstins) >= 2:

            invoice["buyer_gstin"] = gstins[1]

        # =====================================================
        # Supplier Name
        # =====================================================

        supplier = re.search(

            r"Supplier\s*[:\-]?\s*(.+)",

            text,

            re.IGNORECASE,

        )

        if supplier:

            invoice["supplier"] = supplier.group(1).strip()

        # =====================================================
        # Buyer Name
        # =====================================================

        buyer = re.search(

            r"(Buyer|Bill To|Customer)\s*[:\-]?\s*(.+)",

            text,

            re.IGNORECASE,

        )

        if buyer:

            invoice["buyer"] = buyer.group(2).strip()

        # =====================================================
        # Taxable Amount
        # =====================================================

        taxable = re.search(

            r"Taxable\s*(?:Value|Amount)"
            r"\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

            text,

            re.IGNORECASE,

        )

        if taxable:

            invoice["taxable_amount"] = float(

                taxable.group(1).replace(",", "")

            )

        # =====================================================
        # GST Rate
        # =====================================================

        gst_rate = re.search(

            r"GST\s*(?:Rate)?\s*[:@\-]?\s*"
            r"(\d+(?:\.\d+)?)\s*%",

            text,

            re.IGNORECASE,

        )

        if gst_rate:

            invoice["gst_rate"] = float(

                gst_rate.group(1)

            )

        # =====================================================
        # CGST
        # =====================================================
        #
        # Important:
        #
        # CGST @ 9%     11025.00
        #
        # We need 11025, NOT 9.
        #
        # =====================================================

        cgst = re.search(

            r"CGST\s*(?:@\s*\d+(?:\.\d+)?\s*%)?"
            r"\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

            text,

            re.IGNORECASE,

        )

        if cgst:

            invoice["cgst"] = float(

                cgst.group(1).replace(",", "")

            )

        # =====================================================
        # SGST
        # =====================================================

        sgst = re.search(

            r"SGST\s*(?:@\s*\d+(?:\.\d+)?\s*%)?"
            r"\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

            text,

            re.IGNORECASE,

        )

        if sgst:

            invoice["sgst"] = float(

                sgst.group(1).replace(",", "")

            )

        # =====================================================
        # IGST
        # =====================================================

        igst = re.search(

            r"IGST\s*(?:@\s*\d+(?:\.\d+)?\s*%)?"
            r"\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

            text,

            re.IGNORECASE,

        )

        if igst:

            invoice["igst"] = float(

                igst.group(1).replace(",", "")

            )

        # =====================================================
        # Grand Total
        # =====================================================

        total_patterns = [

            r"Grand\s*Total\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

            r"Invoice\s*Total\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

            r"Total\s*Amount\s*[:\-]?\s*[₹]?\s*"
            r"([\d,]+\.\d+|[\d,]+)",

        ]

        for pattern in total_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE,

            )

            if match:

                invoice["total_amount"] = float(

                    match.group(1).replace(",", "")

                )

                break

        # =====================================================
        # Calculate GST Rate if not explicitly extracted
        # =====================================================

        if (
            invoice["gst_rate"] is None
            and invoice["taxable_amount"]
        ):

            taxable_amount = invoice["taxable_amount"]

            total_tax = (
                (invoice["cgst"] or 0)
                + (invoice["sgst"] or 0)
                + (invoice["igst"] or 0)
            )

            if taxable_amount > 0 and total_tax > 0:

                invoice["gst_rate"] = round(

                    (total_tax / taxable_amount) * 100,

                    2,

                )

        return invoice