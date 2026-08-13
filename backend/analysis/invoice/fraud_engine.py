from datetime import datetime


class FraudEngine:

    @staticmethod
    def detect(invoice):

        frauds = []

        # =====================================================
        # Supplier GSTIN
        # =====================================================

        if not invoice.get("supplier_gstin"):

            frauds.append({

                "severity": "HIGH",

                "type": "GSTIN",

                "issue": "Supplier GSTIN Missing",

                "recommendation": "Verify supplier GSTIN before claiming ITC."

            })

        # =====================================================
        # Buyer GSTIN
        # =====================================================

        if not invoice.get("buyer_gstin"):

            frauds.append({

                "severity": "MEDIUM",

                "type": "GSTIN",

                "issue": "Buyer GSTIN Missing",

                "recommendation": "Buyer GSTIN should be present for B2B invoices."

            })

        # =====================================================
        # Invoice Number
        # =====================================================

        if not invoice.get("invoice_number"):

            frauds.append({

                "severity": "HIGH",

                "type": "Invoice",

                "issue": "Invoice Number Missing",

                "recommendation": "Every GST invoice must have a unique invoice number."

            })

        # =====================================================
        # Invoice Date
        # =====================================================

        invoice_date = invoice.get("invoice_date")

        if invoice_date:

            try:

                year = int(str(invoice_date).split("/")[-1])

                current_year = datetime.now().year

                if year < current_year - 3:

                    frauds.append({

                        "severity": "MEDIUM",

                        "type": "Invoice Date",

                        "issue": "Invoice appears to be very old.",

                        "recommendation": "Verify invoice date before processing."

                    })

            except Exception:

                pass

        # =====================================================
        # Total Amount
        # =====================================================

        total = invoice.get("total_amount")

        if total is None:

            frauds.append({

                "severity": "HIGH",

                "type": "Amount",

                "issue": "Invoice Amount Missing",

                "recommendation": "Verify total invoice value."

            })

        elif total > 1000000:

            frauds.append({

                "severity": "LOW",

                "type": "Amount",

                "issue": "High Value Invoice",

                "recommendation": "Review invoice before claiming ITC."

            })

        # =====================================================
        # HSN Validation
        # =====================================================

        items = invoice.get("items", [])

        for index, item in enumerate(items):

            if not item.get("hsn"):

                frauds.append({

                    "severity": "MEDIUM",

                    "type": "HSN",

                    "issue": f"Missing HSN in Item {index+1}",

                    "recommendation": "Provide HSN code."

                })

        # =====================================================
        # GST Calculation
        # =====================================================

        taxable = invoice.get("taxable_amount")

        cgst = invoice.get("cgst") or 0

        sgst = invoice.get("sgst") or 0

        igst = invoice.get("igst") or 0

        gst_rate = invoice.get("gst_rate", 18)

        if taxable:

            expected = taxable * gst_rate / 100

            actual = cgst + sgst + igst

            if abs(expected - actual) > 2:

                frauds.append({

                    "severity": "HIGH",

                    "type": "GST",

                    "issue": "GST Calculation Mismatch",

                    "recommendation": "Verify CGST/SGST/IGST calculations."

                })

        # =====================================================
        # Overall Status
        # =====================================================

        if not frauds:

            frauds.append({

                "severity": "NONE",

                "type": "Audit",

                "issue": "No fraud indicators detected.",

                "recommendation": "Invoice appears compliant."

            })

        return frauds