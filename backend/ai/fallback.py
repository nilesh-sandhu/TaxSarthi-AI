# ai/fallback.py


def _safe_number(value, default=0.0):
    """
    Safely convert a possibly-None/string/invalid numeric value
    into a number so fallback responses never crash.
    """
    try:
        if value is None:
            return default

        number = float(value)

        if number != number:  # NaN
            return default

        return number

    except (TypeError, ValueError):
        return default


def fallback_response(
    question: str,
    intent: str,
    engine_result=None,
    context=None,
):

    question_lower = question.lower()

    engine_result = engine_result or {}
    context = context or {}

    # =====================================================
    # GST CALCULATION
    # =====================================================

    if intent == "gst_calculation":

        if engine_result.get("success"):

            product = engine_result.get(
                "product",
                "Product",
            )

            hsn = engine_result.get(
                "hsn"
            )

            gst_rate = engine_result.get(
                "gst_rate"
            )

            taxable = _safe_number(
                engine_result.get(
                    "taxable_value"
                )
            )

            gst_amount = _safe_number(
                engine_result.get(
                    "gst_amount"
                )
            )

            total = _safe_number(
                engine_result.get(
                    "total_invoice_value"
                )
            )

            cgst = _safe_number(
                engine_result.get(
                    "cgst",
                    0,
                )
            )

            sgst = _safe_number(
                engine_result.get(
                    "sgst",
                    0,
                )
            )

            igst = _safe_number(
                engine_result.get(
                    "igst",
                    0,
                )
            )

            gst_rate = _safe_number(
                gst_rate
            )

            answer = (
                f"GST calculation for {product}\n\n"
            )

            if hsn:
                answer += f"HSN: {hsn}\n"

            answer += (
                f"GST Rate: {gst_rate:g}%\n"
                f"Taxable Value: ₹{taxable:,.2f}\n"
                f"GST Amount: ₹{gst_amount:,.2f}\n"
            )

            if igst:

                answer += (
                    f"IGST: ₹{igst:,.2f}\n"
                )

            else:

                answer += (
                    f"CGST: ₹{cgst:,.2f}\n"
                    f"SGST: ₹{sgst:,.2f}\n"
                )

            answer += (
                f"Total Invoice Value: "
                f"₹{total:,.2f}\n\n"
                "The calculation is based on the "
                "available TaxSarthi GST data."
            )

            return answer

        return (
            "I could not calculate the GST for this "
            "product because the required GST information "
            "is currently unavailable."
        )

    # =====================================================
    # HSN
    # =====================================================

    if intent == "hsn_search":

        if engine_result.get("success"):

            product = engine_result.get(
                "product",
                "Product",
            )

            hsn = engine_result.get(
                "hsn"
            )

            gst_rate = engine_result.get(
                "gst_rate"
            )

            answer = (
                f"GST information for {product}\n\n"
            )

            if hsn:
                answer += (
                    f"HSN Code: {hsn}\n"
                )

            if gst_rate is not None:
                answer += (
                    f"GST Rate: {gst_rate}%\n"
                )

            return answer

        return (
            "I could not find reliable HSN information "
            "for the requested product."
        )

    # =====================================================
    # PRODUCT SEARCH
    # =====================================================

    if intent == "product_search":

        if engine_result.get("success"):

            product = engine_result.get(
                "product"
            )

            hsn = engine_result.get(
                "hsn"
            )

            gst_rate = engine_result.get(
                "gst_rate"
            )

            return (
                f"Product: {product}\n"
                f"HSN Code: {hsn}\n"
                f"GST Rate: {gst_rate}%"
            )

        return (
            "I could not find reliable information "
            "for that product."
        )

    # =====================================================
    # REGISTRATION
    # =====================================================

    if intent == "registration":

        if engine_result:

            return registration_fallback(
                engine_result
            )

        return (
            "GST registration is the process of "
            "obtaining a GSTIN for a business that is "
            "required or eligible to register under GST.\n\n"
            "The application is submitted online through "
            "the official GST Portal.\n\n"
            "Official GST Portal:\n"
            "https://www.gst.gov.in/"
        )

    # =====================================================
    # COMPLIANCE
    # =====================================================

    if intent == "compliance":

        if engine_result:

            return compliance_fallback(
                engine_result
            )

        return (
            "GST compliance includes maintaining proper "
            "records and filing applicable GST returns "
            "within the prescribed timelines."
        )

    # =====================================================
    # NOTIFICATION
    # =====================================================

    if intent == "notification":

        if engine_result:

            return simple_list_response(
                engine_result,
                "Latest GST Notifications",
            )

        return (
            "No notification information is currently "
            "available."
        )

    # =====================================================
    # CIRCULAR
    # =====================================================

    if intent == "circular":

        if engine_result:

            return simple_list_response(
                engine_result,
                "Latest GST Circulars",
            )

        return (
            "No circular information is currently "
            "available."
        )

    # =====================================================
    # GENERAL
    # =====================================================

    return (
        "I can help you with GST registration, GST "
        "calculations, HSN codes, GST rates, returns, "
        "compliance, notifications and circulars."
    )


# =====================================================
# REGISTRATION FALLBACK
# =====================================================

def registration_fallback(result):

    answer = (
        "GST Registration\n\n"
        "GST registration provides a business with a "
        "GSTIN and enables it to comply with applicable "
        "GST requirements.\n\n"
    )

    if result.get("mandatory") is not None:

        if result.get("mandatory"):

            answer += (
                "Based on the available business "
                "information, registration may be "
                "required.\n\n"
            )

        else:

            answer += (
                "Based on the available business "
                "information, mandatory registration "
                "may not currently apply.\n\n"
            )

    if result.get("threshold"):

        answer += (
            f"Applicable threshold information: "
            f"{result.get('threshold')}\n\n"
        )

    answer += (
        "Registration is completed through the official "
        "GST Portal:\n"
        "https://www.gst.gov.in/"
    )

    return answer


# =====================================================
# COMPLIANCE FALLBACK
# =====================================================

def compliance_fallback(result):

    answer = "GST Compliance Status\n\n"

    score = result.get(
        "compliance_score"
    )

    risk = result.get(
        "risk"
    )

    if score is not None:

        answer += (
            f"Compliance Score: {score}/100\n"
        )

    if risk:

        answer += (
            f"Risk Level: {risk}\n"
        )

    pending = result.get(
        "pending_returns",
        [],
    )

    if pending:

        answer += (
            "\nPending Returns:\n"
        )

        for item in pending:

            answer += (
                f"- {item}\n"
            )

    reasons = result.get(
        "reasons",
        [],
    )

    if reasons:

        answer += "\nPoints to Review:\n"

        for reason in reasons:

            answer += (
                f"- {reason}\n"
            )

    recommendations = result.get(
        "recommendations",
        [],
    )

    if recommendations:

        answer += "\nRecommendations:\n"

        for recommendation in recommendations:

            answer += (
                f"- {recommendation}\n"
            )

    return answer


# =====================================================
# LIST RESPONSE
# =====================================================

def simple_list_response(
    result,
    title,
):

    if isinstance(result, list):

        items = result

    elif isinstance(result, dict):

        items = (
            result.get("notifications")
            or result.get("circulars")
            or result.get("data")
            or result.get("results")
            or []
        )

    else:

        items = []

    if not items:

        return (
            f"{title}\n\n"
            "No information is currently available."
        )

    answer = f"{title}\n\n"

    for index, item in enumerate(
        items[:5],
        start=1,
    ):

        if isinstance(item, dict):

            text = (
                item.get("title")
                or item.get("subject")
                or item.get("description")
                or str(item)
            )

        else:

            text = str(item)

        answer += (
            f"{index}. {text}\n"
        )

    return answer