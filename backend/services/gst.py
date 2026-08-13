from schemas.gst import (
    GSTCalculationRequest,
    GSTCalculationResponse,
)


def calculate_gst(
    request: GSTCalculationRequest,
) -> GSTCalculationResponse:
    """
    Calculate GST for an exclusive or inclusive amount.

    Intra-State:
        CGST = half of GST
        SGST = half of GST
        IGST = 0

    Inter-State:
        IGST = full GST
        CGST = 0
        SGST = 0
    """

    amount = float(request.amount)
    rate = float(request.gst_rate)

    if request.calculation_type == "exclusive":
        base_amount = amount
        gst_amount = (
            base_amount * rate
        ) / 100
        total_amount = (
            base_amount + gst_amount
        )

    else:
        total_amount = amount
        base_amount = (
            total_amount
            / (1 + rate / 100)
        )
        gst_amount = (
            total_amount - base_amount
        )

    if request.interstate:
        cgst = 0.0
        sgst = 0.0
        igst = gst_amount

    else:
        cgst = gst_amount / 2
        sgst = gst_amount / 2
        igst = 0.0

    return GSTCalculationResponse(
        calculation_type=request.calculation_type,
        interstate=request.interstate,
        base_amount=round(base_amount, 2),
        gst_rate=rate,
        gst_amount=round(gst_amount, 2),
        cgst=round(cgst, 2),
        sgst=round(sgst, 2),
        igst=round(igst, 2),
        total_amount=round(total_amount, 2),
    )