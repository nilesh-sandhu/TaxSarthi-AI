import re


class GSTValidator:

    # =====================================================
    # GSTIN Validation
    # =====================================================

    @staticmethod
    def validate_gstin(gstin):

        if not gstin:
            return False

        gstin = str(gstin).strip().upper()

        pattern = (
            r"^\d{2}[A-Z]{5}\d{4}"
            r"[A-Z][A-Z0-9]{3}$"
        )

        return bool(
            re.match(
                pattern,
                gstin,
            )
        )

    # =====================================================
    # GST Rate Validation
    # =====================================================

    @staticmethod
    def validate_gst_rate(rate):

        valid_rates = {
            0,
            3,
            5,
            12,
            18,
            28,
        }

        if rate is None:
            return False

        try:

            rate = float(rate)

        except (
            TypeError,
            ValueError,
        ):

            return False

        return any(
            abs(rate - valid_rate) < 0.01
            for valid_rate in valid_rates
        )

    # =====================================================
    # Normalize Rate
    # =====================================================

    @staticmethod
    def normalize_rate(rate):

        if rate is None:
            return None

        try:

            rate = float(rate)

        except (
            TypeError,
            ValueError,
        ):

            return None

        return round(rate, 2)

    # =====================================================
    # Derive GST Rate From Tax Amount
    # =====================================================

    @staticmethod
    def derive_gst_rate(
        taxable,
        cgst,
        sgst,
        igst,
    ):

        if taxable is None:
            return None

        try:

            taxable = float(taxable)

        except (
            TypeError,
            ValueError,
        ):

            return None

        if taxable <= 0:
            return None

        cgst = float(cgst or 0)
        sgst = float(sgst or 0)
        igst = float(igst or 0)

        total_tax = (
            cgst
            + sgst
            + igst
        )

        if total_tax <= 0:
            return 0.0

        return round(
            (total_tax / taxable) * 100,
            2,
        )

    # =====================================================
    # GST Calculation Validation
    # =====================================================

    @staticmethod
    def validate_tax(
        taxable,
        cgst,
        sgst,
        igst,
        gst_rate,
    ):

        if taxable is None:
            return False

        try:

            taxable = float(taxable)

        except (
            TypeError,
            ValueError,
        ):

            return False

        if taxable < 0:
            return False

        cgst = float(cgst or 0)
        sgst = float(sgst or 0)
        igst = float(igst or 0)

        gst_rate = (
            GSTValidator.normalize_rate(
                gst_rate
            )
        )

        # -------------------------------------------------
        # If no GST rate is available,
        # derive it from actual tax.
        # -------------------------------------------------

        if gst_rate is None:

            gst_rate = (
                GSTValidator.derive_gst_rate(
                    taxable=taxable,
                    cgst=cgst,
                    sgst=sgst,
                    igst=igst,
                )
            )

        if gst_rate is None:
            return False

        expected_tax = (
            taxable
            * gst_rate
            / 100
        )

        # =================================================
        # Interstate Supply
        # =================================================

        if igst > 0:

            return abs(
                igst - expected_tax
            ) <= 1.0

        # =================================================
        # Intra-state Supply
        # CGST + SGST
        # =================================================

        total_tax = (
            cgst
            + sgst
        )

        return abs(
            total_tax - expected_tax
        ) <= 1.0

    # =====================================================
    # Overall Validation
    # =====================================================

    @staticmethod
    def validate(invoice):

        result = {

            "gstin_valid": False,

            "gst_rate_valid": False,

            "tax_valid": False,

            "errors": [],

        }

        # =================================================
        # GSTIN
        # =================================================

        result["gstin_valid"] = (
            GSTValidator.validate_gstin(
                invoice.get(
                    "supplier_gstin"
                )
            )
        )

        if not result["gstin_valid"]:

            result["errors"].append(
                "Supplier GSTIN is invalid."
            )

        # =================================================
        # Extract GST Values
        # =================================================

        taxable = invoice.get(
            "taxable_amount"
        )

        cgst = invoice.get(
            "cgst"
        )

        sgst = invoice.get(
            "sgst"
        )

        igst = invoice.get(
            "igst"
        )

        gst_rate = (
            invoice.get(
                "gst_rate"
            )
        )

        # =================================================
        # Normalize GST Rate
        # =================================================

        gst_rate = (
            GSTValidator.normalize_rate(
                gst_rate
            )
        )

        # =================================================
        # Derive GST Rate If Missing
        # =================================================

        if gst_rate is None:

            gst_rate = (
                GSTValidator.derive_gst_rate(
                    taxable=taxable,
                    cgst=cgst,
                    sgst=sgst,
                    igst=igst,
                )
            )

        # =================================================
        # GST Rate Validation
        # =================================================

        result["gst_rate_valid"] = (
            GSTValidator.validate_gst_rate(
                gst_rate
            )
        )

        if not result["gst_rate_valid"]:

            result["errors"].append(
                "GST Rate is invalid."
            )

        # =================================================
        # Tax Calculation
        # =================================================

        result["tax_valid"] = (
            GSTValidator.validate_tax(
                taxable=taxable,
                cgst=cgst,
                sgst=sgst,
                igst=igst,
                gst_rate=gst_rate,
            )
        )

        if not result["tax_valid"]:

            result["errors"].append(
                "GST calculation mismatch."
            )

        # =================================================
        # Final Result
        # =================================================

        result["gst_rate"] = gst_rate

        result["valid"] = (
            result["gstin_valid"]
            and result["gst_rate_valid"]
            and result["tax_valid"]
        )

        return result