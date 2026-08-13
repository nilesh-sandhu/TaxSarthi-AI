import re


# =====================================================
# Business Types
# =====================================================

BUSINESS_TYPES = {

    "electronics": "Electronics",
    "electronic": "Electronics",

    "restaurant": "Restaurant",
    "hotel": "Restaurant",

    "medical": "Medical",
    "pharmacy": "Medical",

    "grocery": "Food & Grocery",
    "kirana": "Food & Grocery",

    "cloth": "Clothing",
    "clothing": "Clothing",
    "textile": "Clothing",

    "car": "Automobile",
    "automobile": "Automobile",

    "education": "Education",

    "service": "Services",
    "consultant": "Services",
    "freelancer": "Services",
}


# =====================================================
# Products
# =====================================================

PRODUCTS = [

    "laptop",
    "mobile",
    "phone",
    "television",
    "tv",
    "refrigerator",
    "washing machine",
    "shirt",
    "tshirt",
    "jeans",
    "rice",
    "wheat",
    "cement",
    "steel",
    "computer",
    "printer",

]


# =====================================================
# GST Returns
# =====================================================

RETURNS = [

    "gstr-1",
    "gstr1",

    "gstr-3b",
    "gstr3b",

    "gstr-9",
    "gstr9",

]


# =====================================================
# States
# =====================================================

STATES = [

    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal",
    "delhi",

]


# =====================================================
# Notification / Circular Stop Words
# =====================================================

UPDATE_STOP_WORDS = {

    "latest",
    "new",
    "recent",
    "government",
    "govt",
    "gst",
    "notification",
    "notifications",
    "circular",
    "circulars",
    "show",
    "tell",
    "give",
    "find",
    "search",
    "about",
    "regarding",
    "related",
    "on",
    "for",
    "the",
    "a",
    "an",
    "me",
    "please",
    "what",
    "are",
    "is",

}


# =====================================================
# Notification / Circular Topics
# =====================================================

UPDATE_TOPICS = [

    "input tax credit",
    "itc",
    "reverse charge",
    "rcm",
    "e-commerce",
    "ecommerce",
    "invoice",
    "invoicing",
    "registration",
    "gst registration",
    "gst rate",
    "gst rates",
    "hsn",
    "sac",
    "returns",
    "gstr-1",
    "gstr1",
    "gstr-3b",
    "gstr3b",
    "gstr-9",
    "gstr9",
    "composition",
    "composition scheme",
    "late fee",
    "penalty",
    "interest",
    "refund",
    "export",
    "import",
    "igst",
    "cgst",
    "sgst",
    "tax invoice",
    "credit note",
    "debit note",

]


# =====================================================
# Amount
# =====================================================

def extract_amount(text):

    text = text.lower()

    lakh = re.search(
        r"(\d+(\.\d+)?)\s*lakh",
        text
    )

    if lakh:

        return (
            float(lakh.group(1))
            * 100000
        )

    crore = re.search(
        r"(\d+(\.\d+)?)\s*crore",
        text
    )

    if crore:

        return (
            float(crore.group(1))
            * 10000000
        )

    amount = re.search(
        r"₹?\s*([\d,]+)",
        text
    )

    if amount:

        return float(
            amount.group(1)
            .replace(",", "")
        )

    return None


# =====================================================
# GSTIN
# =====================================================

def extract_gstin(text):

    match = re.search(

        r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b",

        text.upper()

    )

    if match:

        return match.group()

    return None


# =====================================================
# Extract Notification / Circular Keyword
# =====================================================

def extract_update_keyword(text):

    text_lower = text.lower().strip()

    # -------------------------------------------------
    # First check known multi-word topics
    # -------------------------------------------------

    for topic in sorted(
        UPDATE_TOPICS,
        key=len,
        reverse=True,
    ):

        if topic in text_lower:

            return topic


    # -------------------------------------------------
    # Remove notification/circular related words
    # -------------------------------------------------

    words = re.findall(
        r"[a-zA-Z0-9-]+",
        text_lower
    )

    filtered_words = []

    for word in words:

        if word in UPDATE_STOP_WORDS:

            continue

        if word in {
            "notification",
            "notifications",
            "circular",
            "circulars",
        }:

            continue

        filtered_words.append(
            word
        )


    # -------------------------------------------------
    # If something meaningful remains
    # -------------------------------------------------

    if filtered_words:

        return " ".join(
            filtered_words
        )

    return ""


# =====================================================
# Entity Extraction
# =====================================================

def extract_business_information(text):

    text_lower = text.lower()

    business_type = None

    state = None

    product = None

    gst_return = None

    amount = extract_amount(
        text
    )

    gstin = extract_gstin(
        text
    )

    interstate = False

    ecommerce = False

    composition = False

    notification_keyword = ""

    circular_keyword = ""


    # =================================================
    # Business
    # =================================================

    for k, v in BUSINESS_TYPES.items():

        if k in text_lower:

            business_type = v

            break


    # =================================================
    # Product
    # =================================================

    for p in PRODUCTS:

        if p in text_lower:

            product = p.title()

            break


    # =================================================
    # GST Return
    # =================================================

    for r in RETURNS:

        if r in text_lower:

            gst_return = r.upper()

            break


    # =================================================
    # State
    # =================================================

    for s in STATES:

        if s in text_lower:

            state = s.title()

            break


    # =================================================
    # Interstate
    # =================================================

    interstate = any(

        word in text_lower

        for word in [

            "interstate",
            "inter state",
            "outside state",
            "other states",
            "across india",

        ]

    )


    # =================================================
    # Ecommerce
    # =================================================

    ecommerce = any(

        word in text_lower

        for word in [

            "amazon",
            "flipkart",
            "meesho",
            "online",
            "ecommerce",
            "e-commerce",

        ]

    )


    # =================================================
    # Composition
    # =================================================

    if "composition" in text_lower:

        composition = True


    # =================================================
    # Notification Keyword
    # =================================================

    if (
        "notification" in text_lower
        or "notifications" in text_lower
    ):

        notification_keyword = (
            extract_update_keyword(
                text
            )
        )


    # =================================================
    # Circular Keyword
    # =================================================

    if (
        "circular" in text_lower
        or "circulars" in text_lower
    ):

        circular_keyword = (
            extract_update_keyword(
                text
            )
        )


    # =================================================
    # Final Entities
    # =================================================

    return {

        "business_type":
            business_type,

        "product_name":
            product,

        "gst_return":
            gst_return,

        "state":
            state,

        "amount":
            amount,

        "turnover":
            amount,

        "gstin":
            gstin,

        "interstate":
            interstate,

        "ecommerce":
            ecommerce,

        "composition_scheme":
            composition,

        "notification_keyword":
            notification_keyword,

        "circular_keyword":
            circular_keyword,

    }


# =====================================================
# Demo
# =====================================================

if __name__ == "__main__":

    test_queries = [

        "Latest GST notification",

        "Latest GST notification about ITC",

        "GST notification regarding e-commerce",

        "Latest GST circular",

        "GST circular about input tax credit",

        "GST circular regarding invoice",

        (
            "I have an electronics shop in Delhi "
            "with annual turnover of 55 lakh. "
            "GST on Laptop worth ₹50000. "
            "My GSTIN is 07ABCDE1234F1Z5 "
            "and I need to file GSTR-3B."
        ),

    ]


    for query in test_queries:

        print(
            "\nQuery:",
            query
        )

        print(
            extract_business_information(
                query
            )
        )