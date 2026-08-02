from schemas.registration import (
    RegistrationRequest,
    RegistrationResponse,
)


def check_registration(
    request: RegistrationRequest,
) -> RegistrationResponse:

    threshold = 4000000  # ₹40 Lakhs

    if request.business_type.lower() == "service":
        threshold = 2000000  # ₹20 Lakhs

    if request.interstate_supply:
        return RegistrationResponse(
            gst_required=True,
            reason="Interstate supply requires GST registration.",
            threshold_limit=threshold,
        )

    if request.annual_turnover >= threshold:
        return RegistrationResponse(
            gst_required=True,
            reason="Annual turnover exceeds GST threshold.",
            threshold_limit=threshold,
        )

    return RegistrationResponse(
        gst_required=False,
        reason="GST registration is currently not mandatory.",
        threshold_limit=threshold,
    )