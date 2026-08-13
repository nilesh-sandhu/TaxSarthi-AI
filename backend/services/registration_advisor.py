from sqlalchemy.orm import Session

from repositories.business_profile import BusinessProfileRepository
from repositories.gst_rule import GSTRuleRepository


def registration_advisor(
    user_id: int,
    business_id: int,
    db: Session,
):

    business = BusinessProfileRepository.get_by_id(
        db,
        business_id,
    )

    if not business:

        raise Exception("Business not found.")

    gst_required = False

    reason = ""

    registration_type = "Not Required"

    returns = []

    next_steps = []

    # ---------------------------------------
    # Interstate Supply
    # ---------------------------------------

    if business.interstate:

        gst_required = True

        registration_type = "Regular"

        reason = (
            "Interstate supply requires GST Registration."
        )

    # ---------------------------------------
    # E-commerce
    # ---------------------------------------

    elif business.ecommerce:

        gst_required = True

        registration_type = "Regular"

        reason = (
            "Selling through E-commerce requires GST."
        )

    # ---------------------------------------
    # Turnover
    # ---------------------------------------

    elif float(business.turnover) >= 4000000:

        gst_required = True

        registration_type = "Regular"

        reason = (
            "Turnover exceeds GST threshold."
        )

    else:

        gst_required = False

        reason = (
            "GST Registration currently not mandatory."
        )

    # ---------------------------------------
    # Returns
    # ---------------------------------------

    if gst_required:

        returns = [

            "GSTR-1",

            "GSTR-3B",

        ]

        next_steps = [

            "Apply for GST Registration",

            "Generate GSTIN",

            "Start filing returns",

        ]

    return {

        "gst_required": gst_required,

        "registration_type": registration_type,

        "reason": reason,

        "recommended_returns": returns,

        "next_steps": next_steps,

    }