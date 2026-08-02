from sqlalchemy.orm import Session

from models.product import Product


def chat_with_ai(message: str, db: Session):

    message = message.lower().strip()

    # -----------------------------
    # Greetings
    # -----------------------------
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening"
    ]

    if message in greetings:
        return {
            "reply":
            "Hello 👋 Welcome to TaxSarthi AI.\nHow can I help you regarding GST today?"
        }

    # -----------------------------
    # Thanks
    # -----------------------------
    if "thank" in message:
        return {
            "reply":
            "You're welcome 😊"
        }

    # -----------------------------
    # Bye
    # -----------------------------
    if "bye" in message:
        return {
            "reply":
            "Thank you for using TaxSarthi AI. Have a great day!"
        }

    # -----------------------------
    # Product Search
    # -----------------------------
    products = db.query(Product).all()

    for product in products:

        if product.name.lower() in message:

            return {
                "reply":
                f"""
Product : {product.name}

Category : {product.category}

GST Rate : {product.gst_rate}%

HSN Code : {product.hsn_code}

Description : {product.description}
"""
            }

    return {
        "reply":
        "Sorry, I couldn't find this product in the database."
    }