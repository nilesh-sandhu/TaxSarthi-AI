from ai.entity_extractor import extract_business_information


class ContextManager:
    """
    Maintains short-term conversation context
    for the current user session.
    """

    def __init__(self):

        self.context = {

            # Business information
            "business_type": None,
            "state": None,
            "turnover": None,
            "interstate": None,
            "ecommerce": None,
            "composition_scheme": None,

            # Query information
            "product_name": None,
            "amount": None,
            "gst_return": None,
            "gstin": None,

        }

    # =====================================================
    # Update Context
    # =====================================================

    def update(self, user_message: str):

        extracted = extract_business_information(
            user_message
        )

        for key, value in extracted.items():

            if value is not None:

                self.context[key] = value

        return self.context

    # =====================================================
    # Get Context
    # =====================================================

    def get(self):

        return self.context

    # =====================================================
    # Reset Context
    # =====================================================

    def reset(self):

        self.context = {

            "business_type": None,
            "state": None,
            "turnover": None,
            "interstate": None,
            "ecommerce": None,
            "composition_scheme": None,

            "product_name": None,
            "amount": None,
            "gst_return": None,
            "gstin": None,

        }

    # =====================================================
    # Missing Information
    # =====================================================

    def missing_fields(self):

        missing = []

        for key, value in self.context.items():

            if value is None:

                missing.append(key)

        return missing

    # =====================================================
    # Context Complete?
    # =====================================================

    def is_complete(self):

        return len(
            self.missing_fields()
        ) == 0


# =====================================================
# Singleton Instance
# =====================================================

context_manager = ContextManager()


# =====================================================
# Demo
# =====================================================

if __name__ == "__main__":

    context_manager.update(
        "GST rate of laptop worth 50000"
    )

    print(
        context_manager.get()
    )