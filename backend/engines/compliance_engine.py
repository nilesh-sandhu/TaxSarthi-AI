from datetime import datetime
from decimal import Decimal, InvalidOperation


# =====================================================
# GST RETURN DUE-DAY REFERENCES
# =====================================================

GSTR1_DUE_DAY = 11
GSTR3B_DUE_DAY = 20


# =====================================================
# GST THRESHOLDS
# =====================================================

GOODS_THRESHOLD = Decimal("4000000")      # ₹40 Lakh
SERVICE_THRESHOLD = Decimal("2000000")    # ₹20 Lakh


# =====================================================
# SAFE VALUE HELPERS
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


def get_business_status(business):

    status = getattr(
        business,
        "business_status",
        "active",
    )

    if not status:
        return "active"

    return str(status).strip().lower()


def get_business_type(business):

    business_type = getattr(
        business,
        "business_type",
        "",
    )

    if not business_type:
        return ""

    return str(
        business_type
    ).strip().lower()


# =====================================================
# DETERMINE GST THRESHOLD
# =====================================================

def get_threshold(business):

    business_type = get_business_type(
        business
    )

    service_types = [

        "service",
        "services",
        "consultant",
        "consulting",
        "freelancer",

    ]

    if business_type in service_types:

        return (
            SERVICE_THRESHOLD,
            "₹20 Lakh",
        )

    return (
        GOODS_THRESHOLD,
        "₹40 Lakh",
    )


# =====================================================
# COMPLIANCE SCORE
# =====================================================

def compliance_score(
    business,
):

    score = 100

    reasons = []

    turnover = get_turnover(
        business
    )

    registered = has_gstin(
        business
    )

    status = get_business_status(
        business
    )

    threshold, threshold_label = (
        get_threshold(
            business
        )
    )

    # =================================================
    # GST REGISTRATION
    # =================================================

    if not registered:

        score -= 30

        reasons.append(
            "Business is not GST registered."
        )

        # ---------------------------------------------
        # Turnover Threshold
        # ---------------------------------------------

        if turnover >= threshold:

            score -= 40

            reasons.append(
                "Turnover has reached or exceeded "
                f"the applicable {threshold_label} "
                "GST registration threshold."
            )

    # =================================================
    # BUSINESS STATUS
    # =================================================

    if status != "active":

        score -= 20

        reasons.append(
            "Business is not marked as active."
        )

    # =================================================
    # SCORE LIMIT
    # =================================================

    score = max(
        0,
        min(
            score,
            100,
        ),
    )

    return (
        score,
        reasons,
    )


# =====================================================
# PENDING RETURNS
# =====================================================

def pending_returns():

    today = datetime.today()

    pending = []

    # =================================================
    # GSTR-1
    # =================================================

    if today.day > GSTR1_DUE_DAY:

        pending.append(
            "GSTR-1"
        )

    # =================================================
    # GSTR-3B
    # =================================================

    if today.day > GSTR3B_DUE_DAY:

        pending.append(
            "GSTR-3B"
        )

    return pending


# =====================================================
# RISK LEVEL
# =====================================================

def risk_level(
    score,
):

    if score >= 90:

        return "Low"

    if score >= 70:

        return "Medium"

    return "High"


# =====================================================
# RECOMMENDATIONS
# =====================================================

def recommendations(
    score,
    reasons=None,
):

    recommendations_list = []

    reasons = reasons or []

    # =================================================
    # Registration
    # =================================================

    if any(
        "not GST registered"
        in reason
        for reason in reasons
    ):

        recommendations_list.append(
            "Review GST registration applicability."
        )

    # =================================================
    # Threshold
    # =================================================

    if any(
        "threshold"
        in reason.lower()
        for reason in reasons
    ):

        recommendations_list.append(
            "GST registration should be reviewed "
            "because the applicable turnover threshold "
            "has been reached or exceeded."
        )

    # =================================================
    # Records
    # =================================================

    if score < 100:

        recommendations_list.append(
            "Maintain updated GST records and "
            "supporting business documents."
        )

    # =================================================
    # Compliance Review
    # =================================================

    if score < 80:

        recommendations_list.append(
            "Review GST compliance requirements "
            "and pending obligations."
        )

    # =================================================
    # High Risk
    # =================================================

    if score < 60:

        recommendations_list.append(
            "Professional tax advice may be appropriate "
            "for unresolved compliance issues."
        )

    # =================================================
    # No Issues
    # =================================================

    if not recommendations_list:

        recommendations_list.append(
            "Continue maintaining accurate GST records "
            "and monitor applicable filing obligations."
        )

    return recommendations_list


# =====================================================
# COMPLIANCE SUMMARY
# =====================================================

def compliance_summary(
    business,
):

    # =================================================
    # Calculate Score
    # =================================================

    score, reasons = (
        compliance_score(
            business
        )
    )

    # =================================================
    # Pending Returns
    # =================================================

    pending = pending_returns()

    # =================================================
    # Risk
    # =================================================

    risk = risk_level(
        score
    )

    # =================================================
    # Recommendations
    # =================================================

    recs = recommendations(
        score,
        reasons,
    )

    # =================================================
    # Registration Status
    # =================================================

    registered = has_gstin(
        business
    )

    turnover = get_turnover(
        business
    )

    threshold, threshold_label = (
        get_threshold(
            business
        )
    )

    registration_required = (

        not registered
        and turnover >= threshold

    )

    # =================================================
    # Final Result
    # =================================================

    return {

        "success":
            True,

        "compliance_score":
            score,

        "risk":
            risk,

        "gst_registered":
            registered,

        "registration_required":
            registration_required,

        "turnover":
            float(turnover),

        "applicable_threshold":
            float(threshold),

        "threshold_label":
            threshold_label,

        "pending_returns":
            pending,

        "reasons":
            reasons,

        "recommendations":
            recs,

    }