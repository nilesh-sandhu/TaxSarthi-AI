from sqlalchemy.orm import Session

from engines.search_engine import global_search

from engines.business_engine import (
    business_summary,
)

from engines.registration_engine import (
    registration_summary,
)

from engines.compliance_engine import (
    compliance_summary,
)

from engines.recommendation_engine import (
    generate_recommendations,
)

from engines.notification_engine import (
    latest_notifications,
)

from engines.circular_engine import (
    latest_circulars,
)


# =====================================================
# GST RETURNS KNOWLEDGE
# =====================================================

RETURNS_INFO = {

    "GSTR-1": {

        "name": "GSTR-1",

        "description": (
            "GSTR-1 is a GST return used to report "
            "outward supplies made by a registered taxpayer."
        ),

        "purpose": [

            "Report outward supplies.",

            "Provide invoice-level supply information.",

            "Report taxable and exempt outward supplies.",

        ],

    },

    "GSTR-3B": {

        "name": "GSTR-3B",

        "description": (
            "GSTR-3B is a summary GST return used to "
            "declare tax liability and discharge tax payable."
        ),

        "purpose": [

            "Declare GST liability.",

            "Report eligible Input Tax Credit.",

            "Discharge tax payable.",

        ],

    },

    "GSTR-9": {

        "name": "GSTR-9",

        "description": (
            "GSTR-9 is an annual GST return containing "
            "a consolidated summary of information reported "
            "during the financial year."
        ),

        "purpose": [

            "Provide annual GST information.",

            "Consolidate information reported during the year.",

        ],

    },

}


# =====================================================
# RETURN ALIASES
# =====================================================

RETURN_ALIASES = {

    "GSTR1": "GSTR-1",

    "GSTR 1": "GSTR-1",

    "GSTR-1": "GSTR-1",

    "GSTR3B": "GSTR-3B",

    "GSTR 3B": "GSTR-3B",

    "GSTR-3B": "GSTR-3B",

    "GSTR9": "GSTR-9",

    "GSTR 9": "GSTR-9",

    "GSTR-9": "GSTR-9",

}


# =====================================================
# GET RETURN INFORMATION
# =====================================================

def get_return_info(
    return_name: str,
):

    if not return_name:

        return None

    key = str(
        return_name
    ).upper().strip()

    key = RETURN_ALIASES.get(
        key,
        key,
    )

    return RETURNS_INFO.get(
        key
    )


# =====================================================
# GET ALL RETURNS
# =====================================================

def get_all_returns():

    return list(
        RETURNS_INFO.values()
    )


# =====================================================
# DETECT RETURNS FROM QUERY
# =====================================================

def detect_returns(
    query: str,
):

    if not query:

        return []

    query_upper = (
        query.upper()
    )

    returns = []

    # -------------------------------------------------
    # GSTR-1
    # -------------------------------------------------

    if (
        "GSTR-1" in query_upper
        or "GSTR1" in query_upper
        or "GSTR 1" in query_upper
    ):

        info = get_return_info(
            "GSTR-1"
        )

        if info:

            returns.append(
                info
            )

    # -------------------------------------------------
    # GSTR-3B
    # -------------------------------------------------

    if (
        "GSTR-3B" in query_upper
        or "GSTR3B" in query_upper
        or "GSTR 3B" in query_upper
    ):

        info = get_return_info(
            "GSTR-3B"
        )

        if info:

            returns.append(
                info
            )

    # -------------------------------------------------
    # GSTR-9
    # -------------------------------------------------

    if (
        "GSTR-9" in query_upper
        or "GSTR9" in query_upper
        or "GSTR 9" in query_upper
    ):

        info = get_return_info(
            "GSTR-9"
        )

        if info:

            returns.append(
                info
            )

    return returns


# =====================================================
# SAFE ENGINE EXECUTION
# =====================================================

def safe_call(
    function,
    *args,
    default=None,
    **kwargs,
):

    try:

        result = function(
            *args,
            **kwargs,
        )

        if result is None:

            return (
                default
                if default is not None
                else {}
            )

        return result

    except Exception as e:

        print(
            f"Knowledge Engine Error "
            f"({function.__name__}):",
            e,
        )

        return (
            default
            if default is not None
            else {}
        )


# =====================================================
# BUILD KNOWLEDGE CONTEXT
# =====================================================

def build_context(
    query: str,
    business,
    db: Session,
):

    # =================================================
    # Global Search
    # =================================================

    search = safe_call(

        global_search,

        query=query,

        db=db,

        default={},

    )

    # =================================================
    # Business
    # =================================================

    if business is not None:

        business_data = safe_call(

            business_summary,

            business,

            default={},

        )

    else:

        business_data = {}

    # =================================================
    # Registration
    # =================================================

    if business is not None:

        registration = safe_call(

            registration_summary,

            business,

            default={},

        )

    else:

        registration = {}

    # =================================================
    # Compliance
    # =================================================

    if business is not None:

        compliance = safe_call(

            compliance_summary,

            business,

            default={},

        )

    else:

        compliance = {}

    # =================================================
    # Recommendations
    # =================================================

    if business is not None:

        recommendations = safe_call(

            generate_recommendations,

            business,

            default=[],

        )

    else:

        recommendations = []

    # =================================================
    # Notifications
    # =================================================

    notifications = safe_call(

        latest_notifications,

        db,

        limit=5,

        default=[],

    )

    # =================================================
    # Circulars
    # =================================================

    circulars = safe_call(

        latest_circulars,

        db,

        limit=5,

        default=[],

    )

    # =================================================
    # GST RETURNS
    # =================================================

    returns = detect_returns(
        query
    )

    # =================================================
    # Final Knowledge Context
    # =================================================

    return {

        "query":
            query,

        "business":
            business_data,

        "registration":
            registration,

        "compliance":
            compliance,

        "recommendations":
            recommendations,

        "search":
            search,

        "returns":
            returns,

        "notifications":
            notifications,

        "circulars":
            circulars,

    }