from typing import Dict


def check_registration(profile) -> Dict:

    # ----------------------------------
    # Assumption:
    # Turnover is stored in Rupees
    # ----------------------------------

    THRESHOLD_LIMIT = 4000000  # ₹40 Lakh

    registration_required = False
    reason = ""
    recommendation = ""

    # ----------------------------------
    # Already Registered
    # ----------------------------------
    if profile.gstin:

        return {
            "registration_required": True,
            "reason": "Business is already registered under GST.",
            "threshold_limit": THRESHOLD_LIMIT,
            "recommendation": "Continue filing GST returns on time.",
            "documents": [],
            "next_steps": [
                "File GSTR-1",
                "File GSTR-3B",
                "Maintain GST compliance",
            ],
        }

    # ----------------------------------
    # Interstate Supply
    # ----------------------------------
    if bool(getattr(profile, "interstate", False)):

        registration_required = True

        reason = (
            "The business profile is marked for inter-State supply; review compulsory-registration applicability for the actual nature of those supplies."
        )

    # ----------------------------------
    # E-Commerce
    # ----------------------------------
    elif profile.business_type.lower() == "e-commerce":

        registration_required = True

        reason = (
            "E-commerce businesses generally require GST registration."
        )

    # ----------------------------------
    # Turnover Rule
    # ----------------------------------
    elif profile.turnover >= THRESHOLD_LIMIT:

        registration_required = True

        reason = (
            f"Annual turnover exceeds ₹{THRESHOLD_LIMIT:,}."
        )

    # ----------------------------------
    # Not Required
    # ----------------------------------
    else:

        registration_required = False

        reason = (
            "Based on the available business information, GST registration is not mandatory at this stage."
        )

    # ----------------------------------
    # Recommendation
    # ----------------------------------
    if registration_required:

        recommendation = (
            "Apply for GST registration as soon as possible."
        )

    else:

        recommendation = (
            "Registration is currently optional unless your business circumstances change."
        )

    # ----------------------------------
    # Final Response
    # ----------------------------------
    return {

        "registration_required": registration_required,

        "reason": reason,

        "threshold_limit": THRESHOLD_LIMIT,

        "recommendation": recommendation,

        "documents": [
            "PAN Card",
            "Aadhaar Card",
            "Business Address Proof",
            "Bank Account Details",
            "Passport Size Photograph",
        ],

        "next_steps": [

            "Create GST account",

            "Fill GST REG-01",

            "Upload required documents",

            "Complete Aadhaar / OTP verification",

            "Receive GSTIN",

        ],
    }