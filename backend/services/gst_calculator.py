def calculate_gst(
    amount: float,
    gst_rate: float,
    calculation_type: str,
    interstate: bool = False,
):

    gst_rate = float(gst_rate)

    if calculation_type == "exclusive":

        taxable = amount

        gst = taxable * gst_rate / 100

        total = taxable + gst

    else:

        total = amount

        taxable = total / (1 + gst_rate / 100)

        gst = total - taxable

    if interstate:

        igst = gst
        cgst = 0
        sgst = 0

    else:

        cgst = gst / 2
        sgst = gst / 2
        igst = 0

    return {

        "taxable_amount": round(taxable, 2),

        "gst_amount": round(gst, 2),

        "cgst": round(cgst, 2),

        "sgst": round(sgst, 2),

        "igst": round(igst, 2),

        "total_amount": round(total, 2),
    }