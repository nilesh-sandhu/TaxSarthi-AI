import re


# ============================================================
# INTENT KEYWORDS
# ============================================================

INTENTS = {

    "registration": [
        "register",
        "registration",
        "gst registration",
        "new business",
        "gst number",
        "gstin",
    ],

    "gst_calculation": [
        "calculate gst",
        "calculate tax",
        "gst calculation",
        "tax calculation",
        "cgst",
        "sgst",
        "igst",
        "gst on price",
        "tax on price",
    ],

    "hsn_search": [
        "hsn",
        "hsn code",
        "hsn number",
        "sac",
        "sac code",
    ],

    "product_search": [
        "product",
        "gst rate",
        "gst on",
        "gst for",
        "gst of",
        "tax rate",
        "tax on",
        "tax for",
    ],

    "returns": [
        "gstr",
        "gstr1",
        "gstr-1",
        "gstr 1",

        "gstr3b",
        "gstr-3b",
        "gstr 3b",

        "gstr9",
        "gstr-9",
        "gstr 9",

        "return",
        "returns",
    ],

    "notification": [
        "notification",
        "latest notification",
        "cbic",
        "update",
    ],

    "circular": [
        "circular",
        "clarification",
    ],

    "penalty": [
        "penalty",
        "late fee",
        "fine",
        "interest",
    ],

    "compliance": [
        "compliance",
        "due date",
        "due",
        "deadline",
        "filing",
    ],

    "business_advice": [
        "business",
        "advice",
        "startup",
        "firm",
        "company",
    ],
}


# ============================================================
# NORMALIZE QUERY
# ============================================================

def normalize_query(query: str) -> str:

    if not query:
        return ""

    query = query.lower().strip()

    query = re.sub(
        r"\s+",
        " ",
        query,
    )

    return query


# ============================================================
# CHECK HSN QUERY
# ============================================================

def is_hsn_query(query: str) -> bool:

    return bool(
        re.search(
            r"\b(hsn|sac)\b",
            query,
            re.IGNORECASE,
        )
    )


# ============================================================
# CHECK GST PRODUCT QUERY
# ============================================================

def is_gst_product_query(query: str) -> bool:

    patterns = [

        r"\bgst\s+on\b",
        r"\bgst\s+for\b",
        r"\bgst\s+of\b",

        r"\bgst\s+rate\b",
        r"\btax\s+on\b",
        r"\btax\s+for\b",
        r"\btax\s+rate\b",

        r"\bhsn\b.*\bgst\b",
        r"\bgst\b.*\bhsn\b",
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            query,
            re.IGNORECASE,
        ):

            return True

    return False


# ============================================================
# CHECK GST CALCULATION QUERY
# ============================================================

def is_calculation_query(query: str) -> bool:

    patterns = [

        r"\bcalculate\b.*\bgst\b",
        r"\bcalculate\b.*\btax\b",

        r"\bgst\s+calculation\b",
        r"\btax\s+calculation\b",

        r"\bhow\s+much\s+gst\b",

        r"\bcalculate\b.*\d+",
        r"\bgst\b.*\d+",
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            query,
            re.IGNORECASE,
        ):

            return True

    return False


# ============================================================
# DETECT INTENT
# ============================================================

def detect_intent(
    query: str,
):

    if not query:

        return "general"

    query = normalize_query(
        query
    )

    # ========================================================
    # 1. REGISTRATION PRIORITY
    # ========================================================

    if (
        "gst registration" in query
        or "gstin" in query
        or "register for gst" in query
        or "gst number" in query
    ):

        return "registration"

    # ========================================================
    # 2. GST PRODUCT PRIORITY
    #
    # IMPORTANT:
    #
    # GST on shirt
    # GST on laptop
    # GST on laptop and mobile
    # HSN and GST of shirt
    #
    # All should reach product GST engine.
    # ========================================================

    if is_gst_product_query(
        query
    ):

        # Do not treat pure calculation
        # queries as product search.

        if not is_calculation_query(
            query
        ):

            return "product_search"

    # ========================================================
    # 3. PURE GST CALCULATION
    # ========================================================

    if is_calculation_query(
        query
    ):

        return "gst_calculation"

    # ========================================================
    # 4. PURE HSN SEARCH
    # ========================================================

    if is_hsn_query(
        query
    ):

        return "hsn_search"

    # ========================================================
    # 5. SCORE NORMAL INTENTS
    # ========================================================

    scores = {}

    for intent, keywords in INTENTS.items():

        score = 0

        for keyword in keywords:

            if " " in keyword:

                if keyword in query:

                    score += 2

            else:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    query,
                ):

                    score += 1

        scores[intent] = score

    # ========================================================
    # 6. BEST INTENT
    # ========================================================

    best_intent = max(
        scores,
        key=scores.get,
    )

    if scores[best_intent] == 0:

        return "general"

    return best_intent


# ============================================================
# EXTRACT PRODUCT LIST
# ============================================================

def extract_product_names(
    query: str,
):

    """
    Extract multiple product names from a natural
    GST/HSN query.

    Examples:

        GST on laptop
        -> ["laptop"]

        GST on laptop and mobile
        -> ["laptop", "mobile"]

        GST on shirt, jeans and shoes
        -> ["shirt", "jeans", "shoes"]

        HSN and GST of laptop and mobile
        -> ["laptop", "mobile"]
    """

    if not query:

        return []

    text = normalize_query(
        query
    )

    # ========================================================
    # REMOVE QUESTION PREFIX
    # ========================================================

    patterns = [

        r"^what\s+is\s+the\s+gst\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^what\s+is\s+gst\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^gst\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^tax\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^hsn\s+(?:code\s+)?(?:and\s+)?gst\s+(?:on|of|for)?\s*",

        r"^gst\s+(?:and\s+)?hsn\s+(?:on|of|for)?\s*",

        r"^what\s+is\s+the\s+hsn\s+(?:code\s+)?(?:of|for|on)\s+",

        r"^what\s+is\s+the\s+hsn\s+(?:of|for|on)\s+",

        r"^hsn\s+(?:code\s+)?(?:of|for|on)\s+",
    ]

    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE,
        )

    # ========================================================
    # REMOVE QUESTION MARKS
    # ========================================================

    text = re.sub(
        r"[?!.]+$",
        "",
        text,
    )

    # ========================================================
    # NORMALIZE SEPARATORS
    # ========================================================

    text = re.sub(
        r"\s+and\s+",
        ",",
        text,
    )

    text = re.sub(
        r"\s*&\s*",
        ",",
        text,
    )

    # ========================================================
    # SPLIT PRODUCTS
    # ========================================================

    raw_products = (
        text.split(",")
    )

    products = []

    for product in raw_products:

        product = product.strip()

        if not product:
            continue

        # ----------------------------------------------------
        # Remove trailing GST/HSN words
        # ----------------------------------------------------

        product = re.sub(
            r"\b(?:gst|hsn|hsn code|tax|rate)\b",
            "",
            product,
            flags=re.IGNORECASE,
        )

        product = product.strip()

        if not product:
            continue

        if product not in products:

            products.append(
                product
            )

    return products


# ============================================================
# EXTRACT AMOUNT
# ============================================================

def extract_amount(
    query: str,
) -> float:
    """Extract the transaction amount, not the GST percentage."""

    if not query:
        return 0.0

    # Prefer values explicitly marked as currency.
    currency_matches = re.findall(
        r"(?:₹|rs\\.?|inr)\\s*([0-9][0-9,]*(?:\\.[0-9]+)?)",
        query,
        flags=re.IGNORECASE,
    )

    if currency_matches:
        try:
            return float(
                currency_matches[-1].replace(",", "")
            )
        except (TypeError, ValueError):
            pass

    # Otherwise find numeric values, excluding values followed by %.
    matches = re.findall(
        r"(?<![A-Za-z])([0-9][0-9,]*(?:\\.[0-9]+)?)(?!\\s*%)",
        query,
        flags=re.IGNORECASE,
    )

    if not matches:
        return 0.0

    try:
        return float(matches[0].replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


# ============================================================
# DETECT INTERSTATE
# ============================================================

def detect_interstate(
    query: str,
) -> bool:

    if not query:

        return False

    interstate_words = [
        "interstate",
        "inter state",
        "different state",
        "another state",
        "outside state",
        "outside my state",
    ]

    return any(
        word in query
        for word in interstate_words
    )


# ============================================================
# BUILD ENTITIES
# ============================================================

def extract_entities(
    query: str,
):

    intent = detect_intent(
        query
    )

    products = []

    if intent in {
        "product_search",
        "gst_calculation",
        "hsn_search",
    }:

        products = extract_product_names(
            query
        )

    amount = extract_amount(
        query
    )

    interstate = detect_interstate(
        query
    )

    entities = {
        "question": query,

        "product_names": products,

        "product_name": (
            products[0]
            if products
            else ""
        ),

        "amount": amount,

        "interstate": interstate,
    }

    return entities


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    test_queries = [

        "What is GST registration?",

        "GST rate of laptop",

        "GST on laptop and mobile",

        "GST on shirt, jeans and t shirt",

        "HSN code of laptop",

        "HSN and GST of shirt",

        "HSN and GST of laptop and mobile",

        "Calculate GST on 50000",

        "GST on laptop ₹50000",

        "GST on laptop ₹50000 interstate",

        "How do I file GSTR 3B?",

        "What is the late fee for GST?",
    ]

    for query in test_queries:

        print(
            "\nQUERY:",
            query,
        )

        print(
            "INTENT:",
            detect_intent(
                query
            ),
        )

        print(
            "PRODUCTS:",
            extract_product_names(
                query
            ),
        )

        print(
            "AMOUNT:",
            extract_amount(
                query
            ),
        )

        print(
            "INTERSTATE:",
            detect_interstate(
                query
            ),
        )
        import re


# ============================================================
# INTENT KEYWORDS
# ============================================================

INTENTS = {

    "registration": [
        "register",
        "registration",
        "gst registration",
        "new business",
        "gst number",
        "gstin",
    ],

    "gst_calculation": [
        "calculate gst",
        "calculate tax",
        "gst calculation",
        "tax calculation",
        "cgst",
        "sgst",
        "igst",
        "gst on price",
        "tax on price",
    ],

    "hsn_search": [
        "hsn",
        "hsn code",
        "hsn number",
        "sac",
        "sac code",
    ],

    "product_search": [
        "product",
        "gst rate",
        "gst on",
        "gst for",
        "gst of",
        "tax rate",
        "tax on",
        "tax for",
    ],

    "returns": [
        "gstr",
        "gstr1",
        "gstr-1",
        "gstr 1",

        "gstr3b",
        "gstr-3b",
        "gstr 3b",

        "gstr9",
        "gstr-9",
        "gstr 9",

        "return",
        "returns",
    ],

    "notification": [
        "notification",
        "latest notification",
        "cbic",
        "update",
    ],

    "circular": [
        "circular",
        "clarification",
    ],

    "penalty": [
        "penalty",
        "late fee",
        "fine",
        "interest",
    ],

    "compliance": [
        "compliance",
        "due date",
        "due",
        "deadline",
        "filing",
    ],

    "business_advice": [
        "business",
        "advice",
        "startup",
        "firm",
        "company",
    ],
}


# ============================================================
# NORMALIZE QUERY
# ============================================================

def normalize_query(query: str) -> str:

    if not query:
        return ""

    query = query.lower().strip()

    query = re.sub(
        r"\s+",
        " ",
        query,
    )

    return query


# ============================================================
# CHECK HSN QUERY
# ============================================================

def is_hsn_query(query: str) -> bool:

    return bool(
        re.search(
            r"\b(hsn|sac)\b",
            query,
            re.IGNORECASE,
        )
    )


# ============================================================
# CHECK GST PRODUCT QUERY
# ============================================================

def is_gst_product_query(query: str) -> bool:

    patterns = [

        r"\bgst\s+on\b",
        r"\bgst\s+for\b",
        r"\bgst\s+of\b",

        r"\bgst\s+rate\b",
        r"\btax\s+on\b",
        r"\btax\s+for\b",
        r"\btax\s+rate\b",

        r"\bhsn\b.*\bgst\b",
        r"\bgst\b.*\bhsn\b",
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            query,
            re.IGNORECASE,
        ):

            return True

    return False


# ============================================================
# CHECK GST CALCULATION QUERY
# ============================================================

def is_calculation_query(query: str) -> bool:

    patterns = [

        r"\bcalculate\b.*\bgst\b",
        r"\bcalculate\b.*\btax\b",

        r"\bgst\s+calculation\b",
        r"\btax\s+calculation\b",

        r"\bhow\s+much\s+gst\b",

        r"\bcalculate\b.*\d+",
        r"\bgst\b.*\d+",
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            query,
            re.IGNORECASE,
        ):

            return True

    return False


# ============================================================
# DETECT INTENT
# ============================================================

def detect_intent(
    query: str,
):

    if not query:

        return "general"

    query = normalize_query(
        query
    )

    # ========================================================
    # 1. REGISTRATION PRIORITY
    # ========================================================

    if (
        "gst registration" in query
        or "gstin" in query
        or "register for gst" in query
        or "gst number" in query
    ):

        return "registration"

    # ========================================================
    # 2. GST PRODUCT PRIORITY
    #
    # IMPORTANT:
    #
    # GST on shirt
    # GST on laptop
    # GST on laptop and mobile
    # HSN and GST of shirt
    #
    # All should reach product GST engine.
    # ========================================================

    if is_gst_product_query(
        query
    ):

        # Do not treat pure calculation
        # queries as product search.

        if not is_calculation_query(
            query
        ):

            return "product_search"

    # ========================================================
    # 3. PURE GST CALCULATION
    # ========================================================

    if is_calculation_query(
        query
    ):

        return "gst_calculation"

    # ========================================================
    # 4. PURE HSN SEARCH
    # ========================================================

    if is_hsn_query(
        query
    ):

        return "hsn_search"

    # ========================================================
    # 5. SCORE NORMAL INTENTS
    # ========================================================

    scores = {}

    for intent, keywords in INTENTS.items():

        score = 0

        for keyword in keywords:

            if " " in keyword:

                if keyword in query:

                    score += 2

            else:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    query,
                ):

                    score += 1

        scores[intent] = score

    # ========================================================
    # 6. BEST INTENT
    # ========================================================

    best_intent = max(
        scores,
        key=scores.get,
    )

    if scores[best_intent] == 0:

        return "general"

    return best_intent


# ============================================================
# EXTRACT PRODUCT LIST
# ============================================================

def extract_product_names(
    query: str,
):

    """
    Extract multiple product names from a natural
    GST/HSN query.

    Examples:

        GST on laptop
        -> ["laptop"]

        GST on laptop and mobile
        -> ["laptop", "mobile"]

        GST on shirt, jeans and shoes
        -> ["shirt", "jeans", "shoes"]

        HSN and GST of laptop and mobile
        -> ["laptop", "mobile"]
    """

    if not query:

        return []

    text = normalize_query(
        query
    )

    # ========================================================
    # REMOVE QUESTION PREFIX
    # ========================================================

    patterns = [

        r"^what\s+is\s+the\s+gst\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^what\s+is\s+gst\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^gst\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^tax\s+(?:rate\s+)?(?:on|of|for)\s+",

        r"^hsn\s+(?:code\s+)?(?:and\s+)?gst\s+(?:on|of|for)?\s*",

        r"^gst\s+(?:and\s+)?hsn\s+(?:on|of|for)?\s*",

        r"^what\s+is\s+the\s+hsn\s+(?:code\s+)?(?:of|for|on)\s+",

        r"^what\s+is\s+the\s+hsn\s+(?:of|for|on)\s+",

        r"^hsn\s+(?:code\s+)?(?:of|for|on)\s+",
    ]

    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE,
        )

    # ========================================================
    # REMOVE QUESTION MARKS
    # ========================================================

    text = re.sub(
        r"[?!.]+$",
        "",
        text,
    )

    # ========================================================
    # NORMALIZE SEPARATORS
    # ========================================================

    text = re.sub(
        r"\s+and\s+",
        ",",
        text,
    )

    text = re.sub(
        r"\s*&\s*",
        ",",
        text,
    )

    # ========================================================
    # SPLIT PRODUCTS
    # ========================================================

    raw_products = (
        text.split(",")
    )

    products = []

    for product in raw_products:

        product = product.strip()

        if not product:
            continue

        # ----------------------------------------------------
        # Remove trailing GST/HSN words
        # ----------------------------------------------------

        product = re.sub(
            r"\b(?:gst|hsn|hsn code|tax|rate)\b",
            "",
            product,
            flags=re.IGNORECASE,
        )

        product = product.strip()

        if not product:
            continue

        if product not in products:

            products.append(
                product
            )

    return products


# ============================================================
# EXTRACT AMOUNT
# ============================================================

def extract_amount(
    query: str,
) -> float:
    """Extract the transaction amount, not the GST percentage."""

    if not query:
        return 0.0

    # Prefer values explicitly marked as currency.
    currency_matches = re.findall(
        r"(?:₹|rs\\.?|inr)\\s*([0-9][0-9,]*(?:\\.[0-9]+)?)",
        query,
        flags=re.IGNORECASE,
    )

    if currency_matches:
        try:
            return float(
                currency_matches[-1].replace(",", "")
            )
        except (TypeError, ValueError):
            pass

    # Otherwise find numeric values, excluding values followed by %.
    matches = re.findall(
        r"(?<![A-Za-z])([0-9][0-9,]*(?:\\.[0-9]+)?)(?!\\s*%)",
        query,
        flags=re.IGNORECASE,
    )

    if not matches:
        return 0.0

    try:
        return float(matches[0].replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


# ============================================================
# DETECT INTERSTATE
# ============================================================

def detect_interstate(
    query: str,
) -> bool:

    if not query:

        return False

    interstate_words = [
        "interstate",
        "inter state",
        "different state",
        "another state",
        "outside state",
        "outside my state",
    ]

    return any(
        word in query
        for word in interstate_words
    )


# ============================================================
# BUILD ENTITIES
# ============================================================

def extract_entities(
    query: str,
):

    intent = detect_intent(
        query
    )

    products = []

    if intent in {
        "product_search",
        "gst_calculation",
        "hsn_search",
    }:

        products = extract_product_names(
            query
        )

    amount = extract_amount(
        query
    )

    interstate = detect_interstate(
        query
    )

    entities = {
        "question": query,

        "product_names": products,

        "product_name": (
            products[0]
            if products
            else ""
        ),

        "amount": amount,

        "interstate": interstate,
    }

    return entities


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    test_queries = [

        "What is GST registration?",

        "GST rate of laptop",

        "GST on laptop and mobile",

        "GST on shirt, jeans and t shirt",

        "HSN code of laptop",

        "HSN and GST of shirt",

        "HSN and GST of laptop and mobile",

        "Calculate GST on 50000",

        "GST on laptop ₹50000",

        "GST on laptop ₹50000 interstate",

        "How do I file GSTR 3B?",

        "What is the late fee for GST?",
    ]

    for query in test_queries:

        print(
            "\nQUERY:",
            query,
        )

        print(
            "INTENT:",
            detect_intent(
                query
            ),
        )

        print(
            "PRODUCTS:",
            extract_product_names(
                query
            ),
        )

        print(
            "AMOUNT:",
            extract_amount(
                query
            ),
        )

        print(
            "INTERSTATE:",
            detect_interstate(
                query
            ),
        )