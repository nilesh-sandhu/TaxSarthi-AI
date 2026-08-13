from typing import List, Union, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from pathlib import Path
import json
import re
import pandas as pd

from models.product_master import ProductMaster
from models.product_alias import ProductAlias
from models.hsn import HSNMaster
from models.gst_slab import GSTSlab


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = str(text).lower().strip()

    replacements = {
        "t-shirts": "t shirt",
        "t-shirt": "t shirt",
        "tshirts": "t shirt",
        "tshirt": "t shirt",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return " ".join(text.split())


def clean_product_name(product_name: str) -> str:
    query = normalize_text(product_name)

    prefixes = [
        "what is the gst on ",
        "what is gst on ",
        "what is the gst of ",
        "what is gst of ",
        "what is the gst for ",
        "what is gst for ",
        "gst rate of ",
        "gst rate for ",
        "gst on ",
        "gst for ",
        "gst of ",
        "tax rate of ",
        "tax rate for ",
        "tax on ",
        "tax for ",
        "hsn code of ",
        "hsn code for ",
        "hsn of ",
        "hsn for ",
    ]

    for prefix in prefixes:
        if query.startswith(prefix):
            query = query[len(prefix):]
            break

    return query.strip()


# ============================================================
# PRODUCT MASTER / ALIAS
# ============================================================


# ============================================================
# OFFICIAL LOCAL GST/HSN DATA FILE SEARCH
# ============================================================

_EXTERNAL_DATA_CACHE = {}


def _load_external_data():
    """
    Load the complete HSN CSV + GST Excel from backend/data.

    HSN CSV:
        hsn_code, description

    GST Excel:
        GST rate, HSN heading, Chapter, Description, Sub-codes
    """

    if _EXTERNAL_DATA_CACHE:
        return _EXTERNAL_DATA_CACHE

    data_root = Path(__file__).resolve().parents[1] / "data"

    hsn_path = data_root / "hsn_master.csv"
    gst_path = data_root / "gst-rate-list.xlsx"
    product_path = data_root / "product_master.csv"

    if not hsn_path.exists():
        return {}

    hsn_df = pd.read_csv(
        hsn_path,
        dtype=str,
    ).fillna("")

    gst_df = pd.DataFrame()

    if gst_path.exists():
        # The supplied workbook has 3 title/blank rows.
        gst_df = pd.read_excel(
            gst_path,
            sheet_name="Rate list",
            header=3,
            dtype=str,
        ).fillna("")

        gst_df.columns = [
            str(c).strip()
            for c in gst_df.columns
        ]

    product_df = pd.DataFrame()

    if product_path.exists():
        product_df = pd.read_csv(
            product_path,
            dtype=str,
        ).fillna("")

    _EXTERNAL_DATA_CACHE["hsn"] = hsn_df
    _EXTERNAL_DATA_CACHE["gst"] = gst_df
    _EXTERNAL_DATA_CACHE["products"] = product_df

    return _EXTERNAL_DATA_CACHE


def _normalise_code(value):
    return re.sub(
        r"[^0-9]",
        "",
        str(value or ""),
    )


def _parse_external_rate(value):
    text = str(value or "").strip().lower()

    if not text:
        return None

    if text in {"exempt", "nil", "nil rate", "0", "0%"}:
        return 0.0

    if "varies" in text:
        return None

    try:
        return float(text.replace("%", "").strip())
    except (TypeError, ValueError):
        return None


def _gst_heading_for_hsn(code, gst_df):
    """
    Map an 8/6/4 digit HSN to its 4-digit tariff heading.
    """

    code = _normalise_code(code)

    if len(code) < 4 or gst_df is None or gst_df.empty:
        return []

    heading = code[:4]

    if "HSN heading" not in gst_df.columns:
        return []

    rows = gst_df[
        gst_df["HSN heading"]
        .astype(str)
        .map(_normalise_code)
        == heading
    ]

    results = []

    for _, row in rows.iterrows():

        rate = _parse_external_rate(
            row.get("GST rate", "")
        )

        sub_codes = str(
            row.get("Sub-codes", "")
        ).strip()

        results.append({
            "heading": heading,
            "rate": rate,
            "description": str(
                row.get("Description", "")
            ).strip(),
            "sub_codes": sub_codes,
            "chapter": str(
                row.get("Chapter", "")
            ).strip(),
        })

    return results


def search_external_gst_data(
    product_name: str,
    amount: float = 0,
    interstate: bool = False,
):
    """
    Search ALL HSN records from backend/data/hsn_master.csv
    and map them to GST rates from backend/data/gst-rate-list.xlsx.

    This is the fallback for products that are not present in
    ProductMaster. No product is hard-coded here.
    """

    data = _load_external_data()

    hsn_df = data.get("hsn")
    gst_df = data.get("gst")

    if hsn_df is None or hsn_df.empty:
        return None

    query = normalize_text(product_name)

    if not query:
        return None

    # --------------------------------------------------------
    # 0. Product master CSV
    # --------------------------------------------------------
    # This covers common product names such as:
    # laptop, mobile phone, television, refrigerator, etc.
    # without requiring those rows to already exist in SQLite.

    product_df = data.get("products")

    if product_df is not None and not product_df.empty:

        for _, row in product_df.iterrows():

            product_name_value = normalize_text(
                row.get("product_name", "")
            )

            aliases = [
                normalize_text(x)
                for x in str(
                    row.get("aliases", "")
                ).split("|")
                if normalize_text(x)
            ]

            if (
                query == product_name_value
                or query in aliases
                or (
                    product_name_value
                    and query in product_name_value
                )
            ):

                hsn_code = _normalise_code(
                    row.get("hsn_code", "")
                )

                rate = _parse_external_rate(
                    row.get("gst_rate", "")
                )

                if hsn_code and rate is not None:

                    gst_amount = (
                        float(amount)
                        * rate
                        / 100
                    )

                    tax = calculate_tax(
                        amount,
                        rate,
                        interstate,
                    )

                    return {
                        "success": True,
                        "source": "product_master_csv",
                        "product": str(
                            row.get(
                                "product_name",
                                query,
                            )
                        ),
                        "hsn": hsn_code,
                        "hsn_description": (
                            "Product classification from "
                            "TaxSarthi product master"
                        ),
                        "gst_rate": rate,
                        "taxable_value": float(amount),
                        "gst_amount": round(
                            gst_amount,
                            2,
                        ),
                        "total_invoice_value": round(
                            float(amount) + gst_amount,
                            2,
                        ),
                        **tax,
                        "cess": 0.0,
                        "notification_no": (
                            "TaxSarthi product_master.csv"
                        ),
                        "effective_from": None,
                        "itc_available": True,
                        "recommendation": (
                            "Input Tax Credit may be claimed "
                            "if purchased for business purposes "
                            "and other applicable conditions are satisfied."
                        ),
                    }

    # Detect columns safely.
    hsn_col = next(
        (
            c for c in hsn_df.columns
            if str(c).strip().lower() in {
                "hsn_code",
                "hsn",
                "code",
            }
        ),
        None,
    )

    desc_col = next(
        (
            c for c in hsn_df.columns
            if "description" in str(c).lower()
            or "desc" in str(c).lower()
        ),
        None,
    )

    if not hsn_col or not desc_col:
        return None

    work_df = hsn_df.copy()

    work_df["_code"] = (
        work_df[hsn_col]
        .astype(str)
        .map(_normalise_code)
    )

    work_df["_description"] = (
        work_df[desc_col]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # 1. Exact HSN code
    # --------------------------------------------------------

    exact = work_df[
        work_df["_code"].str.lower() == query.lower()
    ]

    # --------------------------------------------------------
    # 2. Exact phrase
    # --------------------------------------------------------

    if exact.empty:
        exact = work_df[
            work_df["_description"]
            .str.lower()
            .str.contains(
                re.escape(query),
                na=False,
            )
        ]

    # --------------------------------------------------------
    # 3. Word scoring
    # --------------------------------------------------------

    if exact.empty:

        words = [
            w for w in query.split()
            if len(w) > 2
        ]

        if words:

            scored = []

            for _, row in work_df.iterrows():

                description = (
                    str(row["_description"])
                    .lower()
                )

                score = 0

                for word in words:
                    if word in description:
                        score += 1

                if score:
                    scored.append(
                        (score, row)
                    )

            scored.sort(
                key=lambda x: x[0],
                reverse=True,
            )

            if scored:
                exact = pd.DataFrame(
                    [row for _, row in scored[:25]]
                )

    if exact.empty:
        return None

    # --------------------------------------------------------
    # Build unique HSN/GST options
    # --------------------------------------------------------

    options = []

    seen = set()

    for _, row in exact.iterrows():

        code = str(
            row["_code"]
        ).strip()

        if not code:
            continue

        heading_rows = _gst_heading_for_hsn(
            code,
            gst_df,
        )

        # No rate mapping for this HSN.
        if not heading_rows:
            continue

        for mapping in heading_rows:

            rate = mapping["rate"]

            # "varies" / unresolved sub-codes:
            # don't invent a GST rate.
            if rate is None:
                continue

            key = (
                code,
                float(rate),
            )

            if key in seen:
                continue

            seen.add(key)

            options.append({
                "hsn": code,
                "description": str(
                    row["_description"]
                ),
                "gst_rate": float(rate),
                "heading": mapping["heading"],
                "chapter": mapping["chapter"],
                "sub_codes": mapping["sub_codes"],
            })

    if not options:
        return None

    # Keep the best 10 classifications.
    options = options[:10]

    unique_rates = {
        option["gst_rate"]
        for option in options
    }

    # --------------------------------------------------------
    # One clear rate
    # --------------------------------------------------------

    if len(unique_rates) == 1:

        selected = options[0]

        gst_rate = selected["gst_rate"]

        gst_amount = (
            float(amount)
            * gst_rate
            / 100
        )

        tax = calculate_tax(
            amount,
            gst_rate,
            interstate,
        )

        return {
            "success": True,
            "source": "gst_hsn_files",
            "product": query,
            "hsn": selected["hsn"],
            "hsn_description": selected["description"],
            "gst_rate": gst_rate,
            "taxable_value": float(amount),
            "gst_amount": round(
                gst_amount,
                2,
            ),
            "total_invoice_value": round(
                float(amount) + gst_amount,
                2,
            ),
            **tax,
            "cess": 0.0,
            "notification_no": (
                "CBIC GST rate list / local master data"
            ),
            "effective_from": "2025-09-22",
            "itc_available": True,
            "recommendation": (
                "Input Tax Credit may be claimed "
                "if purchased for business purposes "
                "and other applicable conditions are satisfied."
            ),
        }

    # --------------------------------------------------------
    # Multiple possible rates
    # --------------------------------------------------------

    return {
        "success": True,
        "source": "gst_hsn_files",
        "product": query,
        "classification_required": True,
        "message": (
            f"Multiple HSN/GST classifications were "
            f"found for '{query}'. Please provide "
            f"more product details."
        ),
        "hsn_options": options,
    }


def get_product(
    product_name: str,
    db: Session,
):
    """
    Primary source for products present in product_master.csv.

    CSV example:
        Laptop -> 8471 -> 18%
        Mobile Phone -> 8517 -> 18%

    No hard-coded product names are used.
    """

    query = normalize_text(product_name)

    if not query:
        return None

    # 1. Exact product name
    product = (
        db.query(ProductMaster)
        .filter(
            func.lower(
                ProductMaster.product_name
            ) == query
        )
        .first()
    )

    if product:
        return product

    # 2. Exact alias
    alias = (
        db.query(ProductAlias)
        .filter(
            func.lower(
                ProductAlias.alias
            ) == query
        )
        .first()
    )

    if alias:
        return (
            db.query(ProductMaster)
            .filter(
                ProductMaster.id == alias.product_id
            )
            .first()
        )

    # 3. Product name partial match
    product = (
        db.query(ProductMaster)
        .filter(
            ProductMaster.product_name.ilike(
                f"%{query}%"
            )
        )
        .first()
    )

    if product:
        return product

    # 4. Alias partial match
    alias = (
        db.query(ProductAlias)
        .filter(
            ProductAlias.alias.ilike(
                f"%{query}%"
            )
        )
        .first()
    )

    if alias:
        return (
            db.query(ProductMaster)
            .filter(
                ProductMaster.id == alias.product_id
            )
            .first()
        )

    return None


# ============================================================
# HSN LOOKUP
# ============================================================

def get_hsn(
    product,
    db: Session,
):
    if not product:
        return None

    hsn_code = getattr(
        product,
        "hsn_code",
        None,
    )

    if hsn_code is None:
        return None

    clean_code = str(hsn_code).strip()

    # 1) Try exact match
    exact = (
        db.query(HSNMaster)
        .filter(
            HSNMaster.hsn_code == clean_code
        )
        .first()
    )

    if exact:
        return exact

    # 2) Fallback: prefix match (e.g., product.hsn_code=8471 matches 8471.30)
    try:
        prefix_match = (
            db.query(HSNMaster)
            .filter(
                HSNMaster.hsn_code.ilike(f"{clean_code}%")
            )
            .order_by(HSNMaster.hsn_code.asc())
            .first()
        )

        if prefix_match:
            return prefix_match
    except Exception:
        # If DB backend doesn't support ilike, try basic contains
        prefix_match = (
            db.query(HSNMaster)
            .filter(
                HSNMaster.hsn_code.like(f"{clean_code}%")
            )
            .order_by(HSNMaster.hsn_code.asc())
            .first()
        )

        if prefix_match:
            return prefix_match

    return None


def get_gst_slab(
    hsn,
    db: Session,
):
    """
    Returns the latest active GST slab linked to an HSN.
    """

    if not hsn:
        return None

    return (
        db.query(GSTSlab)
        .filter(
            GSTSlab.hsn_id == hsn.id
        )
        .filter(
            GSTSlab.is_active.is_(True)
        )
        .order_by(
            GSTSlab.effective_from.desc()
        )
        .first()
    )


# ============================================================
# DIRECT HSN SEARCH
# ============================================================

def search_hsn_for_product(
    product_name: str,
    db: Session,
):
    """
    Searches only HSN records which have an active GST slab.

    This is important for queries such as "GST on shirt":
    the HSN master may contain many fabric/classification rows,
    but we should not stop at the first 20 rows if those rows
    have no GST mapping.
    """

    query = normalize_text(product_name)

    if not query:
        return []

    # --------------------------------------------------------
    # Search HSN + active GST together
    # --------------------------------------------------------

    base = (
        db.query(HSNMaster)
        .join(
            GSTSlab,
            GSTSlab.hsn_id == HSNMaster.id,
        )
        .filter(
            GSTSlab.is_active.is_(True)
        )
    )

    # --------------------------------------------------------
    # 1. Exact HSN code
    # --------------------------------------------------------

    exact_code = (
        base.filter(
            func.lower(
                HSNMaster.hsn_code
            ) == query
        )
        .all()
    )

    if exact_code:
        return exact_code

    # --------------------------------------------------------
    # 2. Exact phrase in description
    # --------------------------------------------------------

    phrase_results = (
        base.filter(
            HSNMaster.description.ilike(
                f"%{query}%"
            )
        )
        .all()
    )

    if phrase_results:
        return _rank_hsn_results(
            phrase_results,
            query,
        )

    # --------------------------------------------------------
    # 3. Word based search
    # --------------------------------------------------------

    words = [
        word
        for word in query.split()
        if len(word) > 2
    ]

    if not words:
        return []

    conditions = [
        HSNMaster.description.ilike(
            f"%{word}%"
        )
        for word in words
    ]

    results = (
        base.filter(
            or_(*conditions)
        )
        .all()
    )

    return _rank_hsn_results(
        results,
        query,
    )


def _rank_hsn_results(
    results,
    query: str,
):
    """
    Rank finished-product classifications above
    raw fabrics when possible.

    We DO NOT delete fabric records from the database.
    We only rank them lower for natural product queries.
    """

    query = normalize_text(query)

    words = [
        word
        for word in query.split()
        if len(word) > 2
    ]

    def score(row):

        description = (
            getattr(row, "description", "")
            or ""
        ).lower()

        value = 0

        # Exact phrase
        if query in description:
            value += 100

        # Each matching word
        for word in words:
            if word in description:
                value += 10

        # Finished garments/products are preferred
        product_terms = [
            "shirt",
            "shirts",
            "t-shirt",
            "t shirts",
            "trousers",
            "jeans",
            "dress",
            "dresses",
            "footwear",
            "shoes",
            "mobile",
            "telephone",
            "television",
            "refrigerator",
            "computer",
            "laptop",
        ]

        for term in product_terms:
            if term in description:
                value += 8

        # Fabric-only descriptions rank lower
        if "fabric" in description:
            value -= 30

        if "shirting fabrics" in description:
            value -= 50

        return value

    unique = {}

    for row in results:

        code = getattr(
            row,
            "hsn_code",
            None,
        )

        if code is None:
            continue

        if code not in unique:
            unique[code] = row

    ranked = sorted(
        unique.values(),
        key=score,
        reverse=True,
    )

    return ranked


# ============================================================
# TAX CALCULATION
# ============================================================

def calculate_tax(
    amount: float,
    gst_rate: float,
    interstate: bool,
):
    gst_amount = (
        float(amount)
        * float(gst_rate)
        / 100
    )

    if interstate:
        return {
            "cgst": 0,
            "sgst": 0,
            "igst": round(
                gst_amount,
                2,
            ),
        }

    return {
        "cgst": round(
            gst_amount / 2,
            2,
        ),
        "sgst": round(
            gst_amount / 2,
            2,
        ),
        "igst": 0,
    }


# ============================================================
# BUILD RESULT FROM GST SLAB
# ============================================================

def build_gst_result(
    product_name: str,
    hsn,
    slab,
    amount: float,
    interstate: bool,
    source: str,
):
    gst_rate = float(
        slab.gst_rate
    )

    gst_amount = (
        float(amount)
        * gst_rate
        / 100
    )

    tax = calculate_tax(
        amount,
        gst_rate,
        interstate,
    )

    return {
        "success": True,
        "source": source,
        "product": product_name,
        "hsn": hsn.hsn_code,
        "hsn_description": (
            hsn.description
        ),
        "gst_rate": gst_rate,
        "taxable_value": float(amount),
        "gst_amount": round(
            gst_amount,
            2,
        ),
        "total_invoice_value": round(
            float(amount)
            + gst_amount,
            2,
        ),
        **tax,
        "cess": float(
            slab.cess or 0
        ),
        "notification_no": (
            slab.notification_no
        ),
        "effective_from": (
            str(slab.effective_from)
            if slab.effective_from
            else None
        ),
        "effective_to": (
            str(slab.effective_to)
            if slab.effective_to
            else None
        ),
        "itc_available": True,
        "recommendation": (
            "Input Tax Credit may be claimed "
            "if purchased for business purposes "
            "and other CGST Act conditions are satisfied."
        ),
    }


# ============================================================
# BUILD RESULT FROM PRODUCT MASTER CSV
# ============================================================

def build_product_master_result(
    product,
    hsn,
    amount: float,
    interstate: bool,
):
    """
    Uses ProductMaster.gst_rate when available.

    This is the critical fix for product_master.csv.

    Example:
        Laptop -> HSN 8471 -> GST 18%

    Even if GSTSlab for 8471 is not linked,
    the product CSV rate can still be returned.
    """

    gst_rate = getattr(
        product,
        "gst_rate",
        None,
    )

    if gst_rate is None:
        return None

    try:
        gst_rate = float(
            gst_rate
        )
    except (
        TypeError,
        ValueError,
    ):
        return None

    gst_amount = (
        float(amount)
        * gst_rate
        / 100
    )

    tax = calculate_tax(
        amount,
        gst_rate,
        interstate,
    )

    return {
        "success": True,
        "source": "product_master",
        "product": (
            getattr(
                product,
                "product_name",
                None,
            )
            or ""
        ),
        "category": (
            getattr(product.category, "name", None)
            if getattr(product, "category", None)
            else None
        ),
        "hsn": (
            getattr(
                product,
                "hsn_code",
                None,
            )
        ),
        "hsn_description": (
            getattr(
                hsn,
                "description",
                None,
            )
            if hsn
            else None
        ),
        "gst_rate": gst_rate,
        "taxable_value": float(
            amount
        ),
        "gst_amount": round(
            gst_amount,
            2,
        ),
        "total_invoice_value": round(
            float(amount)
            + gst_amount,
            2,
        ),
        **tax,
        "cess": 0.0,
        "notification_no": (
            "product_master.csv"
        ),
        "effective_from": None,
        "effective_to": None,
        "itc_available": True,
        "recommendation": (
            "Input Tax Credit may be claimed "
            "if purchased for business purposes "
            "and other CGST Act conditions are satisfied."
        ),
    }


# ============================================================
# SINGLE PRODUCT GST
# ============================================================

def product_gst(
    product_name: str,
    amount: float = 0,
    interstate: bool = False,
    db: Session = None,
):
    if db is None:
        return {
            "success": False,
            "message": (
                "Database session is required."
            ),
        }

    query = clean_product_name(
        product_name
    )

    if not query:
        return {
            "success": False,
            "message": (
                "Please provide a product name."
            ),
        }

    # ========================================================
    # STEP 1 — PRODUCT MASTER / ALIAS
    # ========================================================

    product = get_product(
        query,
        db,
    )

    if product:

        hsn = get_hsn(
            product,
            db,
        )

        # ----------------------------------------------------
        # 1A. Product CSV rate
        # ----------------------------------------------------

        product_result = (
            build_product_master_result(
                product=product,
                hsn=hsn,
                amount=amount,
                interstate=interstate,
            )
        )

        if product_result:
            return product_result

        # ----------------------------------------------------
        # 1B. GSTSlab fallback
        # ----------------------------------------------------

        if hsn:

            slab = get_gst_slab(
                hsn,
                db,
            )

            if slab:
                return build_gst_result(
                    product_name=(
                        product.product_name
                    ),
                    hsn=hsn,
                    slab=slab,
                    amount=amount,
                    interstate=interstate,
                    source="product_master",
                )

    # ========================================================
    # STEP 2 — COMPLETE CSV + EXCEL GST/HSN SEARCH
    # ========================================================

    external_result = search_external_gst_data(
        product_name=query,
        amount=amount,
        interstate=interstate,
    )

    if external_result:
        return external_result

    # ========================================================
    # STEP 3 — DATABASE HSN + ACTIVE GST SEARCH
    # ========================================================

    hsn_results = (
        search_hsn_for_product(
            query,
            db,
        )
    )

    if not hsn_results:

        return {
            "success": False,
            "source": "hsn_master",
            "product": query,
            "message": (
                f"No HSN/GST information was found "
                f"for '{query}' in the TaxSarthi database."
            ),
        }

    # ========================================================
    # FALLBACK: knowledge_base JSONs
    # ========================================================
    # If HSN/GST not available from DB, consult local knowledge base
    try:
        kb_root = Path(__file__).resolve().parents[2] / "knowledge_base" / "products"

        kb_hsn = kb_root / "hsn_codes.json"
        kb_gst = kb_root / "gst_rates.json"

        kb_data = {}

        # Try to find a KB match by product name
        if kb_hsn.exists():
            with open(kb_hsn, "r", encoding="utf-8") as f:
                entries = json.load(f)

                for e in entries:
                    if (
                        str(e.get("product", "")).lower()
                        == query.lower()
                    ):
                        kb_data.update(e)
                        break

        if not kb_data and kb_gst.exists():
            with open(kb_gst, "r", encoding="utf-8") as f:
                entries = json.load(f)

                for e in entries:
                    if (
                        str(e.get("product", "")).lower()
                        == query.lower()
                    ):
                        kb_data.update(e)
                        break

        if kb_data:
            gst_rate = float(kb_data.get("gst_rate", 0) or 0)

            gst_amount = float(amount) * gst_rate / 100

            tax = calculate_tax(
                amount,
                gst_rate,
                interstate,
            )

            return {
                "success": True,
                "source": "knowledge_base",
                "product": query,
                "hsn": kb_data.get("hsn") or kb_data.get("hsn_code") or None,
                "hsn_description": kb_data.get("description", None),
                "gst_rate": gst_rate,
                "taxable_value": float(amount),
                "gst_amount": round(gst_amount, 2),
                "total_invoice_value": round(float(amount) + gst_amount, 2),
                **tax,
                "cess": 0.0,
                "notification_no": "knowledge_base",
            }
    except Exception:
        pass

    # ========================================================
    # STEP 2b — EXTERNAL CSV / XLSX FILES (hsn_master.csv + gst-rate-list.xlsx)
    # If database and knowledge base miss, consult raw data files
    try:
        data_root = Path(__file__).resolve().parents[1] / "data"

        # cache at module level to avoid repeated reads
        if not hasattr(product_gst, "_external_cache"):
            product_gst._external_cache = {}

        cache = product_gst._external_cache

        hsn_df = cache.get("hsn_df")
        gst_df = cache.get("gst_df")

        if hsn_df is None:
            hsn_path = data_root / "hsn_master.csv"
            if hsn_path.exists():
                hsn_df = pd.read_csv(hsn_path, dtype=str).fillna("")
                cache["hsn_df"] = hsn_df

        if gst_df is None:
            gst_path = data_root / "gst-rate-list.xlsx"
            if gst_path.exists():
                try:
                    gst_df = pd.read_excel(gst_path, dtype=str)
                except Exception:
                    gst_df = pd.read_excel(gst_path, engine="openpyxl", dtype=str)

                gst_df = gst_df.fillna("")
                cache["gst_df"] = gst_df

        # If we have external HSN data, try to match by description or HSN code
        if hsn_df is not None:

            q = query.lower()

            # try exact hsn code match first
            hsn_match = None

            if any("hsn" in c.lower() for c in hsn_df.columns):
                hsn_col = next(c for c in hsn_df.columns if "hsn" in c.lower())
                exact = hsn_df[hsn_df[hsn_col].str.strip().str.lower() == q]
                if not exact.empty:
                    hsn_match = exact.iloc[0].to_dict()

            # description search
            if hsn_match is None and any("desc" in c.lower() or "description" in c.lower() for c in hsn_df.columns):
                desc_col = next(c for c in hsn_df.columns if "desc" in c.lower() or "description" in c.lower())
                candidates = hsn_df[hsn_df[desc_col].str.lower().str.contains(q, na=False)]
                if candidates.shape[0] > 0:
                    hsn_match = candidates.iloc[0].to_dict()

            # word-based fuzzy search
            if hsn_match is None:
                for _, row in hsn_df.iterrows():
                    desc = " ".join([str(x) for x in row.values]).lower()
                    if all(w in desc for w in q.split() if len(w) > 2):
                        hsn_match = row.to_dict()
                        break

            if hsn_match:
                # try to find gst rate by hsn code in gst_df
                gst_rate_val = None

                if gst_df is not None and any("hsn" in c.lower() for c in gst_df.columns):
                    gst_hsn_col = next(c for c in gst_df.columns if "hsn" in c.lower())
                    gst_rate_col = None
                    for c in gst_df.columns:
                        if "rate" in c.lower() or "gst" in c.lower():
                            gst_rate_col = c
                            break

                    if gst_rate_col:
                        code = str(hsn_match.get(hsn_col, "")).strip()
                        matches = gst_df[gst_df[gst_hsn_col].astype(str).str.strip() == code]
                        if not matches.empty:
                            gst_rate_val = matches.iloc[0].get(gst_rate_col)

                # assemble response similar to knowledge_base
                gst_rate = 0.0
                try:
                    gst_rate = float(str(gst_rate_val or hsn_match.get("gst_rate") or hsn_match.get("rate") or 0))
                except Exception:
                    gst_rate = 0.0

                gst_amount = float(amount) * gst_rate / 100

                tax = calculate_tax(amount, gst_rate, interstate)

                return {
                    "success": True,
                    "source": "external_files",
                    "product": query,
                    "hsn": (hsn_match.get(hsn_col) if 'hsn_col' in locals() else None),
                    "hsn_description": (hsn_match.get(desc_col) if 'desc_col' in locals() else None),
                    "gst_rate": gst_rate,
                    "taxable_value": float(amount),
                    "gst_amount": round(gst_amount, 2),
                    "total_invoice_value": round(float(amount) + gst_amount, 2),
                    **tax,
                    "cess": 0.0,
                    "notification_no": "external_files",
                }
    except Exception:
        # do not break main flow on external file errors
        pass

    # ========================================================
    # STEP 3 — GST OPTIONS
    # ========================================================

    gst_options = []

    for hsn in hsn_results:

        slab = get_gst_slab(
            hsn,
            db,
        )

        if not slab:
            continue

        gst_options.append(
            {
                "hsn": hsn.hsn_code,
                "description": hsn.description,
                "gst_rate": float(
                    slab.gst_rate
                ),
                "cgst": float(
                    slab.cgst
                ),
                "sgst": float(
                    slab.sgst
                ),
                "igst": float(
                    slab.igst
                ),
                "cess": float(
                    slab.cess or 0
                ),
                "notification_no": (
                    slab.notification_no
                ),
                "effective_from": (
                    str(slab.effective_from)
                    if slab.effective_from
                    else None
                ),
            }
        )

    if not gst_options:

        return {
            "success": False,
            "source": "hsn_master",
            "product": query,
            "message": (
                "HSN records were found, "
                "but no active GST slab is linked "
                "to them."
            ),
        }

    # ========================================================
    # STEP 4 — UNIQUE RATES
    # ========================================================

    unique_rates = {}

    for option in gst_options:

        rate = option["gst_rate"]

        if rate not in unique_rates:
            unique_rates[rate] = option

    # ========================================================
    # ONE CLEAR RATE
    # ========================================================

    if len(unique_rates) == 1:

        selected = next(
            iter(
                unique_rates.values()
            )
        )

        gst_rate = selected[
            "gst_rate"
        ]

        gst_amount = (
            float(amount)
            * gst_rate
            / 100
        )

        tax = calculate_tax(
            amount,
            gst_rate,
            interstate,
        )

        return {
            "success": True,
            "source": "hsn_master",
            "product": query,
            "hsn": selected["hsn"],
            "hsn_description": (
                selected["description"]
            ),
            "gst_rate": gst_rate,
            "taxable_value": float(
                amount
            ),
            "gst_amount": round(
                gst_amount,
                2,
            ),
            "total_invoice_value": round(
                float(amount)
                + gst_amount,
                2,
            ),
            **tax,
            "cess": selected["cess"],
            "notification_no": (
                selected["notification_no"]
            ),
            "effective_from": (
                selected["effective_from"]
            ),
            "itc_available": True,
            "recommendation": (
                "Input Tax Credit may be claimed "
                "if purchased for business purposes "
                "and other CGST Act conditions are satisfied."
            ),
        }

    # ========================================================
    # MULTIPLE CLASSIFICATIONS
    # ========================================================

    return {
        "success": True,
        "source": "hsn_master",
        "product": query,
        "classification_required": True,
        "message": (
            f"Multiple HSN/GST classifications "
            f"were found for '{query}'. "
            "Please provide more product details "
            "before selecting the applicable rate."
        ),
        "hsn_options": gst_options,
    }


# ============================================================
# EXTRACT MULTIPLE PRODUCTS
# ============================================================

def extract_products(
    message: str,
) -> List[str]:

    if not message:
        return []

    text = normalize_text(
        message
    )

    prefixes = [
        "what is the gst on ",
        "what is gst on ",
        "what is the gst of ",
        "what is gst of ",
        "what is the gst for ",
        "what is gst for ",
        "gst rate for ",
        "gst rate of ",
        "gst on ",
        "gst for ",
        "gst of ",
        "tax rate for ",
        "tax rate of ",
        "tax on ",
        "tax for ",
        "hsn code of ",
        "hsn code for ",
        "hsn of ",
        "hsn for ",
    ]

    for prefix in prefixes:

        if text.startswith(prefix):

            text = text[
                len(prefix):
            ]

            break

    endings = [
        " gst rate",
        " gst",
        " tax",
        " hsn code",
        " hsn",
    ]

    for ending in endings:

        if text.endswith(ending):

            text = text[
                : -len(ending)
            ].strip()

    text = text.replace(
        " and ",
        ",",
    )

    text = text.replace(
        " & ",
        ",",
    )

    products = []

    for item in text.split(","):

        item = item.strip()

        if not item:
            continue

        if item not in products:
            products.append(item)

    return products


# ============================================================
# MULTIPLE PRODUCT GST
# ============================================================

def product_gst_multiple(
    products: Union[str, List[str]],
    amount: float = 0,
    interstate: bool = False,
    db: Session = None,
):
    if db is None:
        return {
            "success": False,
            "message": (
                "Database session is required."
            ),
        }

    if isinstance(
        products,
        str,
    ):
        product_list = extract_products(
            products
        )
    else:
        product_list = products or []

    product_list = [
        clean_product_name(p)
        for p in product_list
        if p
    ]

    # Remove duplicates while preserving order
    product_list = list(
        dict.fromkeys(
            product_list
        )
    )

    if not product_list:
        return {
            "success": False,
            "message": (
                "No product was detected."
            ),
        }

    results = []

    for product_name in product_list:

        result = product_gst(
            product_name=product_name,
            amount=amount,
            interstate=interstate,
            db=db,
        )

        results.append(
            result
        )

    successful = [
        result
        for result in results
        if result.get("success")
    ]

    failed = [
        result
        for result in results
        if not result.get("success")
    ]

    return {
        "success": True,
        "multiple_products": True,
        "total_products": len(
            product_list
        ),
        "successful_products": len(
            successful
        ),
        "failed_products": len(
            failed
        ),
        "products": results,
    }