from decimal import Decimal, InvalidOperation


GST_THRESHOLD_SERVICE = Decimal("2000000")   # ₹20 lakh
GST_THRESHOLD_GOODS = Decimal("4000000")     # ₹40 lakh


def get_turnover(business):
    try:
        value = getattr(
            business,
            "turnover",
            0,
        )

        if value is None:
            return Decimal("0")

        return Decimal(str(value))

    except (
        InvalidOperation,
        ValueError,
        TypeError,
    ):
        return Decimal("0")


def get_business_type(business):
    value = getattr(
        business,
        "business_type",
        "",
    )

    return str(value).strip().lower()


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


def is_goods_business(business):
    business_type = get_business_type(
        business
    )

    goods_keywords = [
        "goods",
        "proprietorship",
        "trader",
        "retail",
        "wholesale",
        "manufacturing",
        "manufacturer",
        "trading",
    ]

    return any(
        keyword in business_type
        for keyword in goods_keywords
    )


def gst_registration_required(business):
    """
    Determine whether the profile contains a
    compulsory-registration trigger.

    This is an advisory engine; exceptions under
    GST law/notified categories may require
    case-specific review.
    """

    if has_gstin(business):
        return False

    turnover = get_turnover(
        business
    )

    # -------------------------------------------------
    # Compulsory registration trigger:
    # Inter-State taxable supply
    # -------------------------------------------------

    if is_interstate(business):
        return True

    # -------------------------------------------------
    # E-commerce flag
    # -------------------------------------------------

    if is_ecommerce(business):
        return True

    # -------------------------------------------------
    # Threshold
    # -------------------------------------------------

    if is_goods_business(business):
        return turnover >= GST_THRESHOLD_GOODS

    return turnover >= GST_THRESHOLD_SERVICE


def composition_eligible(business):
    """
    Conservative composition eligibility check.

    Inter-State outward supplies of goods are
    not treated as composition-eligible here.
    """

    if has_gstin(business) is False:
        return False

    if is_interstate(business):
        return False

    if is_ecommerce(business):
        return False

    turnover = get_turnover(
        business
    )

    # Composition threshold for this product's
    # advisory logic.
    if turnover > Decimal("5000000"):
        return False

    return True


def registration_summary(business):

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

    registration_required = (
        gst_registration_required(
            business
        )
    )

    composition = (
        composition_eligible(
            business
        )
    )

    reasons = []

    if interstate:
        reasons.append(
            "Inter-State taxable supplies can trigger compulsory GST registration irrespective of the normal turnover threshold."
        )

    if ecommerce:
        reasons.append(
            "The business is marked as operating through e-commerce, which can create additional registration requirements depending on the applicable provisions."
        )

    if not registered and not interstate and not ecommerce:
        if is_goods_business(business):
            if turnover >= GST_THRESHOLD_GOODS:
                reasons.append(
                    "Turnover has reached the applicable goods threshold used by this advisory engine."
                )
        else:
            if turnover >= GST_THRESHOLD_SERVICE:
                reasons.append(
                    "Turnover has reached the applicable services threshold used by this advisory engine."
                )

    if not reasons and not registered:
        reasons.append(
            "The current business profile does not show a compulsory-registration trigger from the rules currently implemented."
        )

    if registered:
        registration_status = "Registered"

    elif registration_required:
        registration_status = "Registration Required"

    else:
        registration_status = "Not Currently Required Based On Profile"

    recommendations = []

    if registration_required and not registered:
        recommendations.extend([
            "Review GST registration applicability for the actual nature of your supplies.",
            "Complete GST registration through the official GST Portal if registration is applicable.",
            "Maintain proper sales and purchase records.",
        ])

    elif not registered:
        recommendations.append(
            "Continue monitoring turnover and the nature of supplies because GST registration obligations can change."
        )

    if composition:
        recommendations.append(
            "Composition eligibility may be considered, subject to all statutory conditions."
        )
    else:
        if interstate:
            recommendations.append(
                "Composition scheme should not be suggested for a business making inter-State outward supplies of goods."
            )

    return {
        "success": True,

        "registration_status":
            registration_status,

        "registration_required":
            registration_required,

        "registered":
            registered,

        "turnover":
            float(turnover),

        "interstate":
            interstate,

        "ecommerce":
            ecommerce,

        "composition_eligible":
            composition,

        "reasons":
            reasons,

        "recommendations":
            recommendations,

        "process": [
            "Visit GST Portal",
            "Fill GST REG-01",
            "Submit required business and identity details",
            "Complete verification",
            "GSTIN issued after approval",
        ],
    }