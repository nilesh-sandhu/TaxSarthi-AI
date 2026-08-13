from decimal import Decimal, InvalidOperation


# =====================================================
# CONSTANTS
# =====================================================

COMPOSITION_LIMIT = Decimal("15000000")   # ₹1.5 Crore


# =====================================================
# SAFE HELPERS
# =====================================================

def get_turnover(business):

    try:

        value = getattr(
            business,
            "turnover",
            0,
        )

        if value is None:
            return Decimal("0")

        return Decimal(
            str(value)
        )

    except (
        InvalidOperation,
        ValueError,
        TypeError,
    ):

        return Decimal("0")


def has_gstin(business):

    gstin = getattr(
        business,
        "gstin",
        None,
    )

    return bool(
        gstin
        and str(gstin).strip()
    )


def is_interstate(business):

    return bool(
        getattr(
            business,
            "interstate",
            False,
        )
    )


def is_ecommerce(business):

    return bool(
        getattr(
            business,
            "ecommerce",
            False,
        )
    )


def get_business_type(business):

    business_type = getattr(
        business,
        "business_type",
        "",
    )

    if not business_type:
        return "Unknown"

    return str(
        business_type
    ).strip()


# =====================================================
# GENERATE BUSINESS RECOMMENDATIONS
# =====================================================

def generate_recommendations(
    business,
):

    recommendations = []

    turnover = get_turnover(
        business
    )

    registered = has_gstin(
        business
    )

    interstate = is_interstate(
        business
    )

    ecommerce = is_ecommerce(
        business
    )

    business_type = (
        get_business_type(
            business
        )
    )


    # =================================================
    # GST REGISTRATION
    # =================================================

    if not registered:

        recommendations.append(
            "Review GST registration applicability "
            "for your business."
        )


    # =================================================
    # ITC
    # =================================================

    recommendations.append(
        "Claim Input Tax Credit only on eligible "
        "business purchases and maintain the required "
        "supporting records."
    )


    # =================================================
    # DIGITAL RECORDS
    # =================================================

    recommendations.append(
        "Maintain digital invoices, purchase records "
        "and supporting GST documents."
    )


    # =================================================
    # HSN / SAC
    # =================================================

    recommendations.append(
        "Use the appropriate HSN or SAC code while "
        "generating GST invoices."
    )


    # =================================================
    # COMPOSITION SCHEME
    # =================================================

    if turnover <= COMPOSITION_LIMIT:

        recommendations.append(
            "Evaluate whether the Composition Scheme "
            "is suitable for your business model and "
            "eligibility conditions."
        )


    # =================================================
    # INTERSTATE TRANSACTIONS
    # =================================================

    if interstate:

        recommendations.append(
            "Review IGST applicability for interstate "
            "transactions."
        )


    # =================================================
    # E-COMMERCE
    # =================================================

    if ecommerce:

        recommendations.append(
            "Reconcile GST-related sales and transaction "
            "data received from e-commerce operators."
        )


    # =================================================
    # RETURN FILING
    # =================================================

    if registered:

        recommendations.append(
            "File applicable GST returns such as "
            "GSTR-1 and GSTR-3B within the applicable "
            "filing timelines."
        )

    else:

        recommendations.append(
            "After GST registration, review the applicable "
            "GST return filing obligations."
        )


    # =================================================
    # ANNUAL RECONCILIATION
    # =================================================

    recommendations.append(
        "Review annual GST reconciliation and "
        "transaction records before applicable "
        "annual compliance filings."
    )


    # =================================================
    # BUSINESS-SPECIFIC
    # =================================================

    if business_type != "Unknown":

        recommendations.append(
            f"Keep GST records and tax documentation "
            f"organized according to the requirements "
            f"applicable to your {business_type} business."
        )


    # =================================================
    # RETURN
    # =================================================

    return recommendations