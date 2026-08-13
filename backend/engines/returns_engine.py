# =====================================================
# GST Returns Knowledge Engine
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
            "Report taxable, exempt and other outward supplies.",
        ],
    },

    "GSTR-3B": {
        "name": "GSTR-3B",
        "description": (
            "GSTR-3B is a summary GST return used to "
            "declare tax liability and discharge the tax payable."
        ),
        "purpose": [
            "Declare GST liability.",
            "Report eligible Input Tax Credit.",
            "Discharge the tax payable.",
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


def get_return_info(return_name: str):

    if not return_name:
        return None

    key = return_name.upper().strip()

    aliases = {
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

    key = aliases.get(key, key)

    return RETURNS_INFO.get(key)


def get_all_returns():

    return list(RETURNS_INFO.values())