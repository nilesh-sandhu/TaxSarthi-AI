from schemas.gst import (
    GSTCalculationRequest,
    GSTCalculationResponse,
)


def calculate_gst(
    request: GSTCalculationRequest,
) -> GSTCalculationResponse:

    if request.calculation_type == "exclusive":
        base_amount = request.amount
        gst_amount = (base_amount * request.gst_rate) / 100
        total_amount = base_amount + gst_amount

    else:
        total_amount = request.amount
        base_amount = total_amount / (1 + request.gst_rate / 100)
        gst_amount = total_amount - base_amount

    cgst = gst_amount / 2
    sgst = gst_amount / 2
    igst = gst_amount

    return GSTCalculationResponse(
        calculation_type=request.calculation_type,
        base_amount=round(base_amount, 2),
        gst_rate=request.gst_rate,
        gst_amount=round(gst_amount, 2),
        cgst=round(cgst, 2),
        sgst=round(sgst, 2),
        igst=round(igst, 2),
        total_amount=round(total_amount, 2),
    )