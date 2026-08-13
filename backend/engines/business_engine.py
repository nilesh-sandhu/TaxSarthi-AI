from decimal import Decimal, InvalidOperation


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


def get_business_type(business):

    value = getattr(
        business,
        "business_type",
        None,
    )

    if not value:
        return "Unknown"

    return str(
        value
    ).strip()


def get_state(business):

    value = getattr(
        business,
        "state",
        None,
    )

    if not value:
        return "Not Available"

    return str(
        value
    ).strip()


def get_gstin(business):

    value = getattr(
        business,
        "gstin",
        None,
    )

    if not value:
        return None

    value = str(
        value
    ).strip()

    if not value:
        return None

    return value


def get_registration_type(business):

    value = getattr(
        business,
        "registration_type",
        None,
    )

    if not value:
        return "Not Available"

    return str(
        value
    ).strip()


def has_gstin(business):

    gstin = get_gstin(
        business
    )

    return bool(
        gstin
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


def is_composition_scheme(business):

    return bool(
        getattr(
            business,
            "composition_scheme",
            False,
        )
    )


def get_business_status(business):

    value = getattr(
        business,
        "business_status",
        None,
    )

    if not value:
        return "Active"

    return str(
        value
    ).strip()


# =====================================================
# BUSINESS CATEGORY
# =====================================================

def business_category(
    business,
):

    return get_business_type(
        business
    )


# =====================================================
# BUSINESS SIZE
# =====================================================

def business_size(
    business,
):

    turnover = get_turnover(
        business
    )

    if turnover < Decimal("2000000"):

        return "Micro"

    elif turnover < Decimal("50000000"):

        return "Small"

    elif turnover < Decimal("250000000"):

        return "Medium"

    return "Large"


# =====================================================
# GST REGISTRATION STATUS
# =====================================================

def gst_status(
    business,
):

    if has_gstin(
        business
    ):

        return "Registered"

    return "Not Registered"


# =====================================================
# RISK ANALYSIS
# =====================================================

def risk_level(
    business,
):

    score = 0

    turnover = get_turnover(
        business
    )

    # -------------------------------------------------
    # Interstate
    # -------------------------------------------------

    if is_interstate(
        business
    ):

        score += 30

    # -------------------------------------------------
    # E-Commerce
    # -------------------------------------------------

    if is_ecommerce(
        business
    ):

        score += 20

    # -------------------------------------------------
    # Turnover
    # -------------------------------------------------

    if turnover > Decimal("4000000"):

        score += 20

    # -------------------------------------------------
    # GST Registration
    # -------------------------------------------------

    if has_gstin(
        business
    ):

        score += 10

    # -------------------------------------------------
    # Risk Level
    # -------------------------------------------------

    if score >= 60:

        return "High"

    elif score >= 30:

        return "Medium"

    return "Low"


# =====================================================
# COMPLIANCE SCORE
# =====================================================

def compliance_score(
    business,
):

    score = 100

    turnover = get_turnover(
        business
    )

    registered = has_gstin(
        business
    )

    # -------------------------------------------------
    # GST Registration
    # -------------------------------------------------

    if not registered:

        score -= 30

    # -------------------------------------------------
    # Turnover Threshold
    # -------------------------------------------------

    if (
        turnover >= Decimal("4000000")
        and not registered
    ):

        score -= 40

    # -------------------------------------------------
    # Interstate
    # -------------------------------------------------

    if is_interstate(
        business
    ):

        score -= 10

    # -------------------------------------------------
    # E-Commerce
    # -------------------------------------------------

    if is_ecommerce(
        business
    ):

        score -= 10

    return max(
        score,
        0,
    )


# =====================================================
# BUSINESS SUMMARY
# =====================================================

def business_summary(
    business,
):

    turnover = get_turnover(
        business
    )

    return {

        # -------------------------------------------------
        # Basic Business Information
        # -------------------------------------------------

        "business_name":
            getattr(
                business,
                "business_name",
                "Not Available",
            ),

        "owner":
            getattr(
                business,
                "owner_name",
                "Not Available",
            ),

        "business_type":
            business_category(
                business
            ),

        "state":
            get_state(
                business
            ),

        # -------------------------------------------------
        # Financial Information
        # -------------------------------------------------

        "turnover":
            float(
                turnover
            ),

        # -------------------------------------------------
        # GST Information
        # -------------------------------------------------

        "gstin":
            get_gstin(
                business
            ),

        "gst_status":
            gst_status(
                business
            ),

        "registration_type":
            get_registration_type(
                business
            ),

        # -------------------------------------------------
        # Business Configuration
        # -------------------------------------------------

        "interstate":
            is_interstate(
                business
            ),

        "ecommerce":
            is_ecommerce(
                business
            ),

        "composition_scheme":
            is_composition_scheme(
                business
            ),

        "business_status":
            get_business_status(
                business
            ),

        # -------------------------------------------------
        # Analysis
        # -------------------------------------------------

        "business_size":
            business_size(
                business
            ),

        "risk_level":
            risk_level(
                business
            ),

        "compliance_score":
            compliance_score(
                business
            ),
    }