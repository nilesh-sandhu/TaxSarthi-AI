import json
import re


class InvoiceParser:

    # =====================================================
    # Parse Gemini Response
    # =====================================================

    @staticmethod
    def parse(response: str) -> dict:

        if not response:
            return {}

        # -------------------------------------------------
        # Clean Markdown JSON
        # -------------------------------------------------

        cleaned = response.strip()

        cleaned = re.sub(
            r"^```json",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"^```",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"```$",
            "",
            cleaned,
        )

        cleaned = cleaned.strip()

        # -------------------------------------------------
        # Direct JSON
        # -------------------------------------------------

        try:

            data = json.loads(
                cleaned
            )

            if isinstance(data, dict):

                return data

        except Exception:

            pass

        # -------------------------------------------------
        # Extract JSON Object
        # -------------------------------------------------

        try:

            match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL,
            )

            if match:

                data = json.loads(
                    match.group()
                )

                if isinstance(data, dict):

                    return data

        except Exception:

            pass

        return {}

    # =====================================================
    # Check Empty Value
    # =====================================================

    @staticmethod
    def is_empty(value):

        return value in [
            None,
            "",
            [],
            {},
        ]

    # =====================================================
    # Numeric Conversion
    # =====================================================

    @staticmethod
    def to_number(value):

        if value is None:
            return None

        if isinstance(
            value,
            (int, float),
        ):

            return float(value)

        try:

            cleaned = (
                str(value)
                .replace(",", "")
                .replace("₹", "")
                .strip()
            )

            return float(cleaned)

        except (
            TypeError,
            ValueError,
        ):

            return None

    # =====================================================
    # Validate GSTIN
    # =====================================================

    @staticmethod
    def valid_gstin(value):

        if not value:
            return False

        value = (
            str(value)
            .strip()
            .upper()
        )

        pattern = (
            r"^\d{2}[A-Z]{5}\d{4}"
            r"[A-Z][A-Z0-9]{3}$"
        )

        return bool(
            re.match(
                pattern,
                value,
            )
        )

    # =====================================================
    # Validate GST Rate
    # =====================================================

    @staticmethod
    def valid_gst_rate(value):

        number = (
            InvoiceParser.to_number(
                value
            )
        )

        if number is None:
            return False

        return any(
            abs(number - rate) < 0.01
            for rate in [
                0,
                3,
                5,
                12,
                18,
                28,
            ]
        )

    # =====================================================
    # Check Financial Consistency
    # =====================================================

    @staticmethod
    def financial_values_valid(data):

        taxable = (
            InvoiceParser.to_number(
                data.get(
                    "taxable_amount"
                )
            )
        )

        total = (
            InvoiceParser.to_number(
                data.get(
                    "total_amount"
                )
            )
        )

        cgst = (
            InvoiceParser.to_number(
                data.get("cgst")
            )
            or 0
        )

        sgst = (
            InvoiceParser.to_number(
                data.get("sgst")
            )
            or 0
        )

        igst = (
            InvoiceParser.to_number(
                data.get("igst")
            )
            or 0
        )

        if (
            taxable is None
            or total is None
        ):

            return False

        calculated_total = (
            taxable
            + cgst
            + sgst
            + igst
        )

        return (
            abs(
                calculated_total - total
            )
            <= 2
        )

    # =====================================================
    # Choose Better Financial Value
    # =====================================================

    @staticmethod
    def choose_financial_value(
        regex_value,
        ai_value,
        regex_data,
        ai_data,
    ):

        regex_number = (
            InvoiceParser.to_number(
                regex_value
            )
        )

        ai_number = (
            InvoiceParser.to_number(
                ai_value
            )
        )

        # Both unavailable
        if (
            regex_number is None
            and ai_number is None
        ):

            return None

        # Only AI available
        if regex_number is None:

            return ai_number

        # Only regex available
        if ai_number is None:

            return regex_number

        # Same value
        if abs(
            regex_number - ai_number
        ) < 0.01:

            return regex_number

        # -------------------------------------------------
        # Check which complete financial set is valid
        # -------------------------------------------------

        regex_test = (
            regex_data.copy()
        )

        regex_test["total_amount"] = (
            regex_number
        )

        ai_test = (
            ai_data.copy()
        )

        ai_test["total_amount"] = (
            ai_number
        )

        # Prefer AI if AI produces
        # financially consistent result
        if InvoiceParser.financial_values_valid(
            ai_test
        ):

            return ai_number

        if InvoiceParser.financial_values_valid(
            regex_test
        ):

            return regex_number

        # If neither is consistent,
        # prefer AI because it understands
        # invoice context better.
        return ai_number

    # =====================================================
    # Merge Regex + AI
    # =====================================================

    @staticmethod
    def merge(
        regex_data: dict,
        ai_data: dict,
    ):

        merged = regex_data.copy()

        if not ai_data:

            return merged

        # =================================================
        # Normal Fields
        # =================================================

        normal_fields = [

            "invoice_number",

            "invoice_date",

            "supplier",

            "supplier_gstin",

            "buyer",

            "buyer_gstin",

        ]

        for key in normal_fields:

            regex_value = (
                regex_data.get(key)
            )

            ai_value = (
                ai_data.get(key)
            )

            # AI fills missing regex data
            if InvoiceParser.is_empty(
                regex_value
            ):

                if not InvoiceParser.is_empty(
                    ai_value
                ):

                    merged[key] = ai_value

        # =================================================
        # GSTIN Validation
        # =================================================

        regex_gstin = (
            regex_data.get(
                "supplier_gstin"
            )
        )

        ai_gstin = (
            ai_data.get(
                "supplier_gstin"
            )
        )

        if (
            not InvoiceParser.valid_gstin(
                regex_gstin
            )
            and InvoiceParser.valid_gstin(
                ai_gstin
            )
        ):

            merged[
                "supplier_gstin"
            ] = ai_gstin

        # =================================================
        # Financial Fields
        # =================================================

        financial_fields = [

            "taxable_amount",

            "cgst",

            "sgst",

            "igst",

            "total_amount",

        ]

        for key in financial_fields:

            regex_value = (
                regex_data.get(key)
            )

            ai_value = (
                ai_data.get(key)
            )

            merged[key] = (
                InvoiceParser.choose_financial_value(
                    regex_value=regex_value,
                    ai_value=ai_value,
                    regex_data=regex_data,
                    ai_data=ai_data,
                )
            )

        # =================================================
        # GST Rate
        # =================================================

        regex_rate = (
            regex_data.get(
                "gst_rate"
            )
        )

        ai_rate = (
            ai_data.get(
                "gst_rate"
            )
        )

        if InvoiceParser.valid_gst_rate(
            regex_rate
        ):

            merged["gst_rate"] = (
                InvoiceParser.to_number(
                    regex_rate
                )
            )

        elif InvoiceParser.valid_gst_rate(
            ai_rate
        ):

            merged["gst_rate"] = (
                InvoiceParser.to_number(
                    ai_rate
                )
            )

        else:

            merged["gst_rate"] = None

        # =================================================
        # Items
        # =================================================

        regex_items = (
            regex_data.get(
                "items"
            )
        )

        ai_items = (
            ai_data.get(
                "items"
            )
        )

        if (
            isinstance(
                regex_items,
                list,
            )
            and len(regex_items) > 0
        ):

            merged["items"] = (
                regex_items
            )

        elif isinstance(
            ai_items,
            list,
        ):

            merged["items"] = (
                ai_items
            )

        return merged