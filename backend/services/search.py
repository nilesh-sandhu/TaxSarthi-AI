from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String

from models.product_master import ProductMaster
from models.hsn import HSNMaster
from models.faq import FAQ
from models.gst_return import GSTReturn


def universal_search(query: str, db: Session):

    query = query.strip()

    if not query:
        return {
            "query": query,
            "products": [],
            "hsn": [],
            "faq": [],
            "gst_returns": [],
            "total_results": 0,
        }

    search_pattern = f"%{query}%"

    # =====================================================
    # PRODUCT SEARCH
    # =====================================================

    products = (
        db.query(ProductMaster)
        .filter(
            or_(
                ProductMaster.product_name.ilike(
                    search_pattern
                ),

                ProductMaster.hsn_code.ilike(
                    search_pattern
                ),

                ProductMaster.description.ilike(
                    search_pattern
                ),
            )
        )
        .all()
    )

    # =====================================================
    # HSN SEARCH
    # =====================================================

    hsn = (
        db.query(HSNMaster)
        .filter(
            or_(
                HSNMaster.hsn_code.ilike(
                    search_pattern
                ),

                HSNMaster.description.ilike(
                    search_pattern
                ),
            )
        )
        .all()
    )

    # =====================================================
    # FAQ SEARCH
    # =====================================================

    faq = (
        db.query(FAQ)
        .filter(
            or_(
                FAQ.question.ilike(
                    search_pattern
                ),

                FAQ.answer.ilike(
                    search_pattern
                ),
            )
        )
        .all()
    )

    # =====================================================
    # GST RETURN SEARCH
    # =====================================================

    gst_returns = (
        db.query(GSTReturn)
        .filter(
            or_(
                GSTReturn.return_name.ilike(
                    search_pattern
                ),

                GSTReturn.description.ilike(
                    search_pattern
                ),

                GSTReturn.frequency.ilike(
                    search_pattern
                ),

                # due_date may be a Date field,
                # so convert it to string before ilike.
                cast(
                    GSTReturn.due_date,
                    String
                ).ilike(
                    search_pattern
                ),
            )
        )
        .all()
    )

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {
        "query": query,

        "products": products,

        "hsn": hsn,

        "faq": faq,

        "gst_returns": gst_returns,

        "total_results": (
            len(products)
            + len(hsn)
            + len(faq)
            + len(gst_returns)
        ),
    }