from sqlalchemy.orm import Session

from models.product_master import ProductMaster


def chat_with_ai(message: str, db: Session):

    message = message.strip()

    if not message:
        return {
            "reply": "Please enter a GST-related question."
        }

    lower_message = message.lower()

    # =====================================================
    # Greetings
    # =====================================================

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if lower_message in greetings:

        return {
            "reply":
            "Hello 👋 How can I help you with GST?"
        }

    # =====================================================
    # Thanks
    # =====================================================

    if (
        "thank" in lower_message
        or "thanks" in lower_message
    ):

        return {
            "reply": "You're welcome."
        }

    # =====================================================
    # Goodbye
    # =====================================================

    if (
        lower_message == "bye"
        or "goodbye" in lower_message
    ):

        return {
            "reply":
            "Thank you for using TaxSarthi AI."
        }

    # =====================================================
    # Product Search
    # =====================================================

    products = (
        db.query(ProductMaster)
        .all()
    )

    for product in products:

        product_name = (
            product.name.lower()
            if product.name
            else ""
        )

        if product_name and product_name in lower_message:

            return {
                "reply":
                (
                    f"**{product.name}**\n\n"
                    f"Category: {product.category}\n"
                    f"GST Rate: {product.gst_rate}%\n"
                    f"HSN Code: {product.hsn_code}\n"
                    f"Description: {product.description or 'Not available'}"
                )
            }

    # =====================================================
    # GST Registration
    # =====================================================

    if (
        "gst registration" in lower_message
        or "register for gst" in lower_message
        or "gst registered" in lower_message
    ):

        return {
            "reply":
            "GST registration is required for businesses that meet the applicable registration criteria. The process involves submitting business and identity details on the GST portal."
        }

    # =====================================================
    # GST Rate
    # =====================================================

    if (
        "gst rate" in lower_message
        or "gst percentage" in lower_message
        or "gst %" in lower_message
    ):

        return {
            "reply":
            "GST rates depend on the product or service. Tell me the product name and I can check its GST rate from the TaxSarthi database."
        }

    # =====================================================
    # HSN
    # =====================================================

    if (
        "hsn" in lower_message
        or "hsn code" in lower_message
    ):

        return {
            "reply":
            "Tell me the product name and I can check its HSN code from the TaxSarthi database."
        }

    # =====================================================
    # Invoice
    # =====================================================

    if (
        "invoice" in lower_message
        or "bill" in lower_message
    ):

        return {
            "reply":
            "You can upload your GST invoice for analysis. TaxSarthi AI can check invoice details, GST information, HSN codes and compliance issues."
        }

    # =====================================================
    # Default
    # =====================================================

    return {
        "reply":
        "I can help with GST registration, GST rates, HSN codes, products and invoice analysis."
    }