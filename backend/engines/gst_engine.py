from typing import List, Union, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from pathlib import Path
import json

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
        "category": getattr(
            product,
            "category",
            None,
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
    # STEP 2 — HSN + ACTIVE GST SEARCH
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