from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
import re

from repositories.hsn import HSNRepository
from schemas.hsn import HSNCreate, HSNUpdate

from models.product_master import ProductMaster
from models.hsn import HSNMaster


# ============================================================
# CREATE HSN
# ============================================================

def create_hsn(
    hsn: HSNCreate,
    db: Session,
):
    existing = HSNRepository.get_by_code(
        db,
        hsn.hsn_code,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="HSN Code already exists.",
        )

    return HSNRepository.create(
        db,
        hsn,
    )


# ============================================================
# GET ALL HSN
# ============================================================

def get_all_hsn(db: Session):
    return HSNRepository.get_all(db)


# ============================================================
# GET HSN BY ID
# ============================================================

def get_hsn(
    hsn_id: int,
    db: Session,
):
    hsn = HSNRepository.get_by_id(
        db,
        hsn_id,
    )

    if not hsn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HSN record not found.",
        )

    return hsn


# ============================================================
# NORMALIZE HSN CODE
# ============================================================

def normalize_hsn_code(code: str) -> str:
    """
    Makes these equivalent:

        6105.10.10
        61051010
        6105-10-10

    -> 61051010
    """

    if not code:
        return ""

    return re.sub(
        r"[^0-9]",
        "",
        str(code),
    )


# ============================================================
# NORMALIZE SEARCH QUERY
# ============================================================

def _clean_hsn_query(keyword: str) -> str:

    if not keyword:
        return ""

    query = keyword.lower().strip()

    # Natural-language HSN questions
    patterns = [
        r"what is the hsn code of",
        r"what is the hsn code for",
        r"what is the hsn of",
        r"hsn code of",
        r"hsn code for",
        r"hsn number of",
        r"hsn number for",
        r"hsn no of",
        r"hsn no for",
        r"hsn of",
        r"hsn for",
        r"find hsn code of",
        r"find hsn code for",
        r"give me hsn code of",
        r"give me hsn code for",
    ]

    for pattern in patterns:
        query = re.sub(
            pattern,
            "",
            query,
            flags=re.IGNORECASE,
        )

    query = re.sub(
        r"[?.!,]+$",
        "",
        query,
    )

    return query.strip()


# ============================================================
# PRODUCT ALIASES
# ============================================================

def _get_product_aliases(product: str):

    product = product.lower().strip()

    aliases = {
        "shirt": [
            "shirt",
            "shirts",
            "men's or boys' shirts",
            "women's or girls' shirts",
        ],

        "shirts": [
            "shirt",
            "shirts",
            "men's or boys' shirts",
            "women's or girls' shirts",
        ],

        "tshirt": [
            "t shirt",
            "t-shirt",
            "t shirts",
            "t-shirts",
        ],

        "t shirt": [
            "t shirt",
            "t-shirt",
            "t shirts",
            "t-shirts",
        ],

        "jean": [
            "jean",
            "jeans",
        ],

        "jeans": [
            "jean",
            "jeans",
        ],

        "trouser": [
            "trouser",
            "trousers",
        ],

        "trousers": [
            "trouser",
            "trousers",
        ],
    }

    return aliases.get(
        product,
        [product],
    )


# ============================================================
# SCORE HSN RESULT
# ============================================================

def _score_hsn(
    hsn_code: str,
    description: str,
    product: str,
) -> int:

    desc = description.lower()
    product = product.lower()

    score = 0

    # --------------------------------------------------------
    # Exact product phrase
    # --------------------------------------------------------

    if product in desc:
        score += 100

    # --------------------------------------------------------
    # Product word
    # --------------------------------------------------------

    product_words = product.split()

    for word in product_words:

        if len(word) >= 3 and word in desc:
            score += 30

    # --------------------------------------------------------
    # Product-specific priority
    # --------------------------------------------------------

    if product in {
        "shirt",
        "shirts",
    }:

        # Actual garment descriptions
        if "shirts" in desc:
            score += 150

        if "shirt-blouses" in desc:
            score += 120

        # Fabric should NOT outrank actual shirts
        if "shirting fabrics" in desc:
            score -= 120

        if "fabric" in desc:
            score -= 50

    # --------------------------------------------------------
    # T-shirt
    # --------------------------------------------------------

    if "t shirt" in product or "tshirt" in product:

        if "t-shirts" in desc:
            score += 200

        if "vests" in desc:
            score += 100

    # --------------------------------------------------------
    # Jeans
    # --------------------------------------------------------

    if "jean" in product:

        if "jeans" in desc:
            score += 200

        if "fabric" in desc:
            score -= 50

    # --------------------------------------------------------
    # Exact heading-like code
    # --------------------------------------------------------

    clean_code = normalize_hsn_code(
        hsn_code
    )

    if len(clean_code) == 4:
        score += 20

    return score


# ============================================================
# SEARCH HSN
# ============================================================

def search_hsn(
    keyword: str,
    db: Session,
):

    original_query = (
        keyword or ""
    ).strip()

    query = _clean_hsn_query(
        original_query
    )

    if not query:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Please provide an HSN code "
                "or product name."
            ),
        )

    # ========================================================
    # EXACT HSN CODE SEARCH
    # ========================================================

    normalized_query = normalize_hsn_code(
        query
    )

    if normalized_query:

        all_hsn = (
            db.query(HSNMaster)
            .all()
        )

        exact_matches = []

        for row in all_hsn:

            db_code = normalize_hsn_code(
                row.hsn_code
            )

            if db_code == normalized_query:
                exact_matches.append(row)

        if exact_matches:
            return exact_matches

    # ========================================================
    # PRODUCT SEARCH
    # ========================================================

    aliases = _get_product_aliases(
        query
    )

    candidates = []

    for term in aliases:

        pattern = f"%{term}%"

        rows = (
            db.query(HSNMaster)
            .filter(
                HSNMaster.description.ilike(
                    pattern
                )
            )
            .all()
        )

        candidates.extend(rows)

    # ========================================================
    # FALLBACK TEXT SEARCH
    # ========================================================

    if not candidates:

        words = query.split()

        for word in words:

            if len(word) < 3:
                continue

            rows = (
                db.query(HSNMaster)
                .filter(
                    HSNMaster.description.ilike(
                        f"%{word}%"
                    )
                )
                .all()
            )

            candidates.extend(rows)

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique = {}

    for row in candidates:

        code = row.hsn_code

        if code not in unique:
            unique[code] = row

    # ========================================================
    # SCORE RESULTS
    # ========================================================

    scored = []

    for code, row in unique.items():

        score = _score_hsn(
            code,
            row.description,
            query,
        )

        scored.append(
            (
                score,
                row,
            )
        )

    scored.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    # ========================================================
    # RETURN TOP RESULTS
    # ========================================================

    results = [
        row
        for score, row in scored
        if score > 0
    ][:20]

    if not results:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"No matching HSN found "
                f"for '{original_query}'."
            ),
        )

    return results


# ============================================================
# SEARCH HSN BY PRODUCT NAME
# ============================================================

def search_product(
    product: str,
    db: Session,
):

    if not product or not product.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a product name.",
        )

    query = product.strip()

    # --------------------------------------------------------
    # FIRST: ProductMaster
    # --------------------------------------------------------

    results = (
        db.query(HSNMaster)
        .join(
            ProductMaster,
            ProductMaster.hsn_code
            == HSNMaster.hsn_code,
        )
        .filter(
            ProductMaster.product_name.ilike(
                f"%{query}%"
            )
        )
        .order_by(
            HSNMaster.hsn_code.asc()
        )
        .limit(50)
        .all()
    )

    if results:
        return results

    # --------------------------------------------------------
    # SECOND: Dedicated HSN search
    # --------------------------------------------------------

    return search_hsn(
        query,
        db,
    )


# ============================================================
# UPDATE HSN
# ============================================================

def update_hsn(
    hsn_id: int,
    hsn: HSNUpdate,
    db: Session,
):

    existing = HSNRepository.get_by_id(
        db,
        hsn_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HSN record not found.",
        )

    return HSNRepository.update(
        db,
        existing,
        hsn,
    )


# ============================================================
# DELETE HSN
# ============================================================

def delete_hsn(
    hsn_id: int,
    db: Session,
):

    existing = HSNRepository.get_by_id(
        db,
        hsn_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HSN record not found.",
        )

    return HSNRepository.delete(
        db,
        existing,
    )