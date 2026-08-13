from sqlalchemy.orm import Session

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
    search_notification,
)

from engines.circular_engine import (
    latest_circulars,
    search_circular,
)

from engines.gst_engine import (
    product_gst,
    product_gst_multiple,
)


# ============================================================
# ENGINE ROUTER
# ============================================================

class EngineRouter:

    @staticmethod
    def execute(
        intent: str,
        business,
        db: Session,
        entities: dict,
    ):

        try:

            entities = entities or {}

            # =================================================
            # GST REGISTRATION
            # =================================================

            if intent == "registration":

                if business:

                    return registration_summary(
                        business
                    )

                return {
                    "success": True,
                    "message": (
                        "Business profile is required "
                        "for personalized GST registration "
                        "guidance."
                    ),
                }

            # =================================================
            # COMPLIANCE
            # =================================================

            elif intent == "compliance":

                if business:

                    return compliance_summary(
                        business
                    )

                return {
                    "success": True,
                    "message": (
                        "Business profile is required "
                        "for personalized compliance guidance."
                    ),
                }

            # =================================================
            # GST RETURNS
            # =================================================

            elif intent == "returns":

                if business:

                    compliance = compliance_summary(
                        business
                    )

                    return {
                        "success": True,
                        "type": "returns",

                        "pending_returns":
                            compliance.get(
                                "pending_returns",
                                [],
                            ),

                        "compliance_score":
                            compliance.get(
                                "compliance_score"
                            ),

                        "risk":
                            compliance.get(
                                "risk"
                            ),

                        "reasons":
                            compliance.get(
                                "reasons",
                                [],
                            ),

                        "recommendations":
                            compliance.get(
                                "recommendations",
                                [],
                            ),
                    }

                return {
                    "success": True,
                    "type": "returns",
                    "pending_returns": [],
                    "message": (
                        "Business profile is not available. "
                        "General GST return information can "
                        "still be provided."
                    ),
                }

            # =================================================
            # RECOMMENDATIONS
            # =================================================

            elif intent == "recommendation":

                if business:

                    return generate_recommendations(
                        business
                    )

                return {
                    "success": True,
                    "recommendations": [],
                }

            # =================================================
            # NOTIFICATIONS
            # =================================================

            elif intent == "notification":

                keyword = entities.get(
                    "notification_keyword",
                    "",
                )

                if keyword:

                    results = search_notification(
                        keyword=keyword,
                        db=db,
                        limit=5,
                    )

                    if results:

                        return {
                            "success": True,
                            "type":
                                "notification_search",

                            "keyword":
                                keyword,

                            "count":
                                len(results),

                            "notifications":
                                results,
                        }

                results = latest_notifications(
                    db=db,
                    limit=5,
                )

                return {
                    "success": True,
                    "type":
                        "latest_notifications",

                    "count":
                        len(results),

                    "notifications":
                        results,
                }

            # =================================================
            # CIRCULARS
            # =================================================

            elif intent == "circular":

                keyword = entities.get(
                    "circular_keyword",
                    "",
                )

                if keyword:

                    results = search_circular(
                        keyword=keyword,
                        db=db,
                        limit=5,
                    )

                    if results:

                        return {
                            "success": True,
                            "type":
                                "circular_search",

                            "keyword":
                                keyword,

                            "count":
                                len(results),

                            "circulars":
                                results,
                        }

                results = latest_circulars(
                    db=db,
                    limit=5,
                )

                return {
                    "success": True,
                    "type":
                        "latest_circulars",

                    "count":
                        len(results),

                    "circulars":
                        results,
                }

            # =================================================
            # GST CALCULATION
            # =================================================

            elif intent == "gst_calculation":

                # -------------------------------------------------
                # MULTIPLE PRODUCTS
                # -------------------------------------------------

                product_names = entities.get(
                    "product_names"
                )

                if (
                    isinstance(product_names, list)
                    and len(product_names) > 0
                ):

                    return product_gst_multiple(
                        products=product_names,
                        amount=float(
                            entities.get(
                                "amount",
                                0,
                            )
                            or 0
                        ),
                        interstate=entities.get(
                            "interstate",
                            False,
                        ),
                        db=db,
                    )

                # -------------------------------------------------
                # RAW USER QUERY FALLBACK
                # -------------------------------------------------

                question = entities.get(
                    "question",
                    "",
                )

                if question:

                    return product_gst_multiple(
                        products=question,
                        amount=float(
                            entities.get(
                                "amount",
                                0,
                            )
                            or 0
                        ),
                        interstate=entities.get(
                            "interstate",
                            False,
                        ),
                        db=db,
                    )

                # -------------------------------------------------
                # SINGLE PRODUCT
                # -------------------------------------------------

                return product_gst(
                    product_name=entities.get(
                        "product_name",
                        "",
                    ),

                    amount=float(
                        entities.get(
                            "amount",
                            0,
                        )
                        or 0
                    ),

                    interstate=entities.get(
                        "interstate",
                        False,
                    ),

                    db=db,
                )

            # =================================================
            # PRODUCT SEARCH
            # =================================================

            elif intent == "product_search":

                product_names = entities.get(
                    "product_names"
                )

                if (
                    isinstance(product_names, list)
                    and len(product_names) > 0
                ):

                    return product_gst_multiple(
                        products=product_names,
                        amount=float(
                            entities.get(
                                "amount",
                                0,
                            )
                            or 0
                        ),
                        interstate=entities.get(
                            "interstate",
                            False,
                        ),
                        db=db,
                    )

                question = entities.get(
                    "question",
                    "",
                )

                if question:

                    return product_gst_multiple(
                        products=question,
                        amount=float(
                            entities.get(
                                "amount",
                                0,
                            )
                            or 0
                        ),
                        interstate=entities.get(
                            "interstate",
                            False,
                        ),
                        db=db,
                    )

                product_name = entities.get(
                    "product_name",
                    "",
                )

                return product_gst(
                    product_name=product_name,

                    amount=float(
                        entities.get(
                            "amount",
                            0,
                        )
                        or 0
                    ),

                    interstate=entities.get(
                        "interstate",
                        False,
                    ),

                    db=db,
                )

            # =================================================
            # HSN SEARCH
            # =================================================

            elif intent == "hsn_search":

                product_names = entities.get(
                    "product_names"
                )

                if (
                    isinstance(product_names, list)
                    and len(product_names) > 0
                ):

                    return product_gst_multiple(
                        products=product_names,
                        amount=0,
                        interstate=False,
                        db=db,
                    )

                question = entities.get(
                    "question",
                    "",
                )

                if question:

                    return product_gst_multiple(
                        products=question,
                        amount=0,
                        interstate=False,
                        db=db,
                    )

                return product_gst(
                    product_name=entities.get(
                        "product_name",
                        "",
                    ),

                    amount=0,

                    interstate=False,

                    db=db,
                )

            # =================================================
            # UNKNOWN INTENT
            # =================================================

            return {
                "success": False,
                "message": (
                    f"No engine available for intent "
                    f"'{intent}'."
                ),
            }

        except Exception as e:

            print(
                "Engine Router Error:",
                repr(e),
            )

            return {
                "success": False,
                "error": str(e),
                "message": (
                    "An error occurred while processing "
                    "your request."
                ),
            }