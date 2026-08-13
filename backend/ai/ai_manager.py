import re
from typing import Optional

from sqlalchemy.orm import Session

from ai.gemini import ask_gemini
from ai.prompt_builder import build_prompt
from ai.response_formatter import format_response
from ai.conversation_manager import save_chat
from ai.intent_classifier import detect_intent, extract_entities
from ai.context_manager import context_manager
from ai.fallback import fallback_response

from engines.knowledge_engine import build_context
from engines.registration_engine import registration_summary
from engines.engine_router import EngineRouter

from engines.gst_engine import (
    product_gst,
    product_gst_multiple,
    search_external_gst_data,
)

from repositories.business_profile import (
    BusinessProfileRepository,
)

from services.search import universal_search

# =========================================================
# PRODUCT MASTER
# =========================================================

from models.product_master import ProductMaster


class AIManager:

    # =========================================================
    # HSN QUERY DETECTOR
    # =========================================================

    @staticmethod
    def is_hsn_query(question: str) -> bool:

        q = (question or "").lower().strip()

        keywords = [
            "hsn",
            "hsn code",
            "hsn number",
            "hsn no",
            "classification code",
            "product code",
        ]

        return any(
            keyword in q
            for keyword in keywords
        )

    # =========================================================
    # GST QUERY DETECTOR
    # =========================================================

    @staticmethod
    def is_gst_query(question: str) -> bool:

        q = (question or "").lower().strip()

        keywords = [
            "gst on",
            "gst of",
            "gst for",
            "gst rate",
            "gst percentage",
            "gst %",
            "tax rate",
            "tax on",
            "tax for",

            # HSN + GST
            "hsn and gst",
            "hsn + gst",
            "hsn & gst",
            "hsn with gst",
            "hsn code and gst",
            "hsn code with gst",
        ]

        return any(
            keyword in q
            for keyword in keywords
        )

    # =========================================================
    # EXTRACT PRODUCT FROM HSN QUESTION
    # =========================================================

    @staticmethod
    def extract_hsn_search_term(
        question: str,
    ) -> str:

        q = (
            question or ""
        ).lower().strip()

        patterns = [

            r"\bwhat(?:'s| is)\s+(?:the\s+)?hsn"
            r"(?:\s+code|\s+number|\s+no\.?)?"
            r"\s*(?:of|for|on)?\s*",

            r"\bhsn"
            r"(?:\s+code|\s+number|\s+no\.?)?"
            r"\s+(?:of|for|on)\s+",

            r"\bfind\s+(?:the\s+)?hsn"
            r"(?:\s+code|\s+number|\s+no\.?)?"
            r"\s*(?:of|for|on)?\s*",

            r"\bsearch\s+(?:the\s+)?hsn"
            r"(?:\s+code|\s+number|\s+no\.?)?"
            r"\s*(?:of|for|on)?\s*",

            r"\b(?:give|show|tell)"
            r"\s+(?:me\s+)?(?:the\s+)?hsn"
            r"(?:\s+code|\s+number|\s+no\.?)?"
            r"\s*(?:of|for|on)?\s*",
        ]

        for pattern in patterns:

            q = re.sub(
                pattern,
                "",
                q,
                flags=re.IGNORECASE,
            )

        stop_words = {
            "what",
            "is",
            "the",
            "of",
            "for",
            "on",
            "a",
            "an",
            "please",
            "tell",
            "me",
            "give",
            "show",
            "find",
            "search",
            "hsn",
            "code",
            "number",
            "no",
            "classification",
            "product",
            "gst",
        }

        words = [
            word
            for word in re.findall(
                r"[a-zA-Z0-9._-]+",
                q,
            )
            if word not in stop_words
        ]

        return " ".join(words).strip()

    # =========================================================
    # EXTRACT PRODUCT FROM GST QUESTION
    # =========================================================

    @staticmethod
    def extract_gst_product(
        question: str,
    ) -> str:

        q = (
            question or ""
        ).lower().strip()

        patterns = [

            r"\bwhat(?:'s| is)\s+(?:the\s+)?gst"
            r"(?:\s+rate|\s+percentage|\s+%)?"
            r"\s+(?:of|for|on)\s+",

            r"\bgst"
            r"(?:\s+rate|\s+percentage|\s+%)?"
            r"\s+(?:of|for|on)\s+",

            r"\btax"
            r"(?:\s+rate|\s+percentage|\s+%)?"
            r"\s+(?:of|for|on)\s+",

            r"\bhsn"
            r"(?:\s+code)?"
            r"\s+(?:and|with|\+|&)\s+gst"
            r"\s*(?:of|for|on)?\s*",
        ]

        for pattern in patterns:

            q = re.sub(
                pattern,
                "",
                q,
                flags=re.IGNORECASE,
            )

        stop_words = {
            "what",
            "is",
            "the",
            "of",
            "for",
            "on",
            "a",
            "an",
            "please",
            "tell",
            "me",
            "give",
            "show",
            "gst",
            "rate",
            "percentage",
            "tax",
            "hsn",
            "code",
            "number",
            "and",
            "with",
        }

        words = [
            word
            for word in re.findall(
                r"[a-zA-Z0-9._-]+",
                q,
            )
            if word not in stop_words
        ]

        return " ".join(words).strip()

    # =========================================================
    # DIRECT PRODUCT MASTER SEARCH
    # =========================================================

    @staticmethod
    def direct_product_gst_search(
        product_name: str,
        db: Session,
    ):

        query = (
            product_name or ""
        ).strip().lower()

        if not query:
            return None

        # -----------------------------------------------------
        # EXACT MATCH
        # -----------------------------------------------------

        product = (
            db.query(ProductMaster)
            .filter(
                ProductMaster.product_name.ilike(
                    product_name.strip()
                )
            )
            .first()
        )

        if product:
            return product

        # -----------------------------------------------------
        # CONTAINS MATCH
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # WORD BASED SEARCH
        # -----------------------------------------------------

        words = [
            word
            for word in re.findall(
                r"[a-zA-Z0-9]+",
                query,
            )
            if len(word) >= 2
        ]

        if not words:
            return None

        products = (
            db.query(ProductMaster)
            .filter(
                ProductMaster.is_active == True
            )
            .all()
        )

        best_product = None
        best_score = 0

        for item in products:

            name = (
                item.product_name or ""
            ).lower()

            score = 0

            # Exact query inside product name
            if query in name:
                score += 5

            # Individual words
            for word in words:

                if word in name:
                    score += 2

            if score > best_score:

                best_score = score
                best_product = item

        if best_score > 0:
            return best_product

        return None

    # =========================================================
    # DIRECT PRODUCT RESPONSE
    # =========================================================

    @staticmethod
    def build_direct_product_response(
        product,
    ):

        if product is None:

            return {
                "answer": (
                    "I could not find this product "
                    "in the TaxSarthi Product Master."
                )
            }

        gst_rate = (
            product.gst_rate
            if product.gst_rate is not None
            else 0
        )

        cgst = gst_rate / 2
        sgst = gst_rate / 2

        category_name = "N/A"

        try:

            if product.category:

                category_name = (
                    product.category.name
                )

        except Exception:

            category_name = "N/A"

        lines = [
            (
                f"**{product.product_name} "
                f"— GST & HSN Details**"
            ),
            "",
            f"**HSN Code:** "
            f"{product.hsn_code or 'N/A'}",
            f"**Category:** {category_name}",
            f"**GST Rate:** {gst_rate:g}%",
            f"**CGST:** {cgst:g}%",
            f"**SGST:** {sgst:g}%",
        ]

        if product.description:

            lines.extend([
                "",
                f"**Description:** "
                f"{product.description}",
            ])

        lines.extend([
            "",
            (
                "This information is from the "
                "TaxSarthi Product Master database."
            ),
        ])

        return {
            "answer": "\n".join(lines)
        }

    # =========================================================
    # FORMAT HSN RESULT
    # =========================================================

    @staticmethod
    def build_hsn_response(
        question: str,
        search_result: dict,
    ):

        hsn_results = search_result.get(
            "hsn",
            [],
        )

        if not hsn_results:

            return {
                "answer": (
                    f"I could not find a matching HSN "
                    f"record for '{question}'. "
                    f"Please provide more product details "
                    f"such as material, fabric and product type."
                )
            }

        unique = {}

        for item in hsn_results:

            code = getattr(
                item,
                "hsn_code",
                None,
            )

            description = getattr(
                item,
                "description",
                "",
            )

            if code and code not in unique:

                unique[code] = description

        matches = list(
            unique.items()
        )[:10]

        lines = []

        lines.append(
            "I found the following matching HSN "
            "records in the TaxSarthi HSN database:"
        )

        lines.append("")

        for code, description in matches:

            lines.append(
                f"• {code} — {description}"
            )

        lines.append("")

        lines.append(
            "Important: the exact HSN classification "
            "can depend on factors such as material, "
            "fabric type, whether the product is knitted "
            "or woven, and the specific product type."
        )

        lines.append(
            "Please provide additional product details "
            "if you need a more specific classification."
        )

        return {
            "answer": "\n".join(lines)
        }

    # =========================================================
    # FORMAT GST RESULT
    # =========================================================

    @staticmethod
    def build_gst_response(
        product: str,
        result: dict,
    ):

        if not result.get(
            "success",
            False,
        ):

            return {
                "answer": result.get(
                    "message",
                    (
                        f"No GST information found "
                        f"for '{product}'."
                    ),
                )
            }

        if result.get(
            "classification_required",
            False,
        ):

            lines = [
                (
                    f"I found multiple possible "
                    f"HSN/GST classifications for "
                    f"**{product}**."
                ),
                "",
                (
                    "Please provide more product details "
                    "before selecting the applicable GST rate."
                ),
                "",
                "Possible classifications:",
            ]

            for option in result.get(
                "hsn_options",
                [],
            )[:10]:

                lines.append(
                    f"• HSN {option.get('hsn')} — "
                    f"{option.get('description')} — "
                    f"GST {option.get('gst_rate')}%"
                )

            return {
                "answer": "\n".join(lines)
            }

        hsn = result.get(
            "hsn",
            "N/A",
        )

        description = result.get(
            "hsn_description",
            "",
        )

        gst_rate = result.get(
            "gst_rate",
            0,
        )

        cgst = result.get(
            "cgst",
            0,
        )

        sgst = result.get(
            "sgst",
            0,
        )

        igst = result.get(
            "igst",
            0,
        )

        cess = result.get(
            "cess",
            0,
        )

        notification = result.get(
            "notification_no",
            None,
        )

        effective_from = result.get(
            "effective_from",
            None,
        )

        lines = [
            f"**{product.title()} — GST & HSN Details**",
            "",
            f"**HSN Code:** {hsn}",
            f"**Description:** {description}",
            f"**GST Rate:** {gst_rate}%",
            f"**CGST:** {cgst}%",
            f"**SGST:** {sgst}%",
            f"**IGST:** {igst}%",
        ]

        if cess:

            lines.append(
                f"**Cess:** {cess}%"
            )

        if notification:

            lines.append(
                f"**Source/Notification:** "
                f"{notification}"
            )

        if effective_from:

            lines.append(
                f"**Effective From:** "
                f"{effective_from}"
            )

        lines.append("")

        lines.append(
            "The above information is based on "
            "the HSN and GST records available "
            "in the TaxSarthi database."
        )

        return {
            "answer": "\n".join(lines)
        }

    # =========================================================
    # FORMAT MULTIPLE GST RESULTS
    # =========================================================

    @staticmethod
    def build_multiple_gst_response(
        result: dict,
    ):

        if not result.get(
            "success",
            False,
        ):

            return {
                "answer": result.get(
                    "message",
                    "No GST information found.",
                )
            }

        products = result.get(
            "products",
            [],
        )

        if not products:

            return {
                "answer":
                    "No product GST information was found."
            }

        lines = [
            "**GST & HSN Details**",
            "",
        ]

        for item in products:

            product = item.get(
                "product",
                "Product",
            )

            if not item.get(
                "success",
                False,
            ):

                lines.extend([
                    f"**{product.title()}**",
                    (
                        f"❌ "
                        f"{item.get(
                            'message',
                            'No information found.'
                        )}"
                    ),
                    "",
                ])

                continue

            if item.get(
                "classification_required",
                False,
            ):

                lines.extend([
                    f"**{product.title()}**",
                    "Multiple HSN/GST classifications were found.",
                ])

                for option in item.get(
                    "hsn_options",
                    [],
                )[:5]:

                    lines.append(
                        f"• HSN {option.get('hsn')} — "
                        f"{option.get('description')} — "
                        f"GST {option.get('gst_rate')}%"
                    )

                lines.append("")

                continue

            lines.extend([
                f"**{product.title()}**",
                (
                    f"• HSN Code: "
                    f"{item.get('hsn', 'N/A')}"
                ),
                (
                    f"• Description: "
                    f"{item.get('hsn_description', '')}"
                ),
                (
                    f"• GST Rate: "
                    f"{item.get('gst_rate', 0)}%"
                ),
                (
                    f"• CGST: "
                    f"{item.get('cgst', 0)}%"
                ),
                (
                    f"• SGST: "
                    f"{item.get('sgst', 0)}%"
                ),
                (
                    f"• IGST: "
                    f"{item.get('igst', 0)}%"
                ),
            ])

            if item.get(
                "cess",
                0,
            ):

                lines.append(
                    f"• Cess: "
                    f"{item.get('cess')}%"
                )

            if item.get(
                "notification_no"
            ):

                lines.append(
                    f"• Source/Notification: "
                    f"{item.get('notification_no')}"
                )

            lines.append("")

        lines.append(
            "The above information is based on the "
            "HSN and GST records available in the "
            "TaxSarthi database."
        )

        return {
            "answer": "\n".join(lines)
        }

    # =========================================================
    # FILE HSN RESPONSE
    # =========================================================

    @staticmethod
    def build_file_hsn_response(
        search_term: str,
        result: dict,
    ):

        options = result.get(
            "hsn_options",
            [],
        )

        if not options:

            return {
                "answer": (
                    f"I could not find a matching HSN "
                    f"record for '{search_term}'."
                )
            }

        lines = [
            "I found these HSN/GST classifications "
            "in the TaxSarthi master data:",
            "",
        ]

        for option in options[:10]:

            lines.append(
                f"• HSN {option.get('hsn')} — "
                f"{option.get('description')} — "
                f"GST {option.get('gst_rate')}%"
            )

        lines.extend([
            "",
            (
                "For an exact classification, product "
                "material, composition and product type "
                "may be required."
            ),
        ])

        return {
            "answer": "\n".join(lines)
        }

    # =========================================================
    # MAIN AI FUNCTION
    # =========================================================

    @staticmethod
    def ask(
        user_id: Optional[int],
        question: str,
        db: Session,
    ):

        # =====================================================
        # VALIDATE QUESTION
        # =====================================================

        question = (
            question or ""
        ).strip()

        if not question:

            return {
                "success": False,
                "intent": "general",
                "response": {
                    "answer":
                        "Please enter a question."
                },
            }

        # =====================================================
        # DETECT INTENT
        # =====================================================

        try:

            intent = detect_intent(
                question
            )

        except Exception as e:

            print(
                "Intent Detection Error:",
                e,
            )

            intent = "general"

        # =====================================================
        # UPDATE CONTEXT
        # =====================================================

        try:

            current_context = (
                context_manager.update(
                    question
                )
            )

        except Exception as e:

            print(
                "Context Manager Error:",
                e,
            )

            current_context = {}

        if current_context is None:

            current_context = {}

        # =====================================================
        # EXTRACT ENTITIES
        # =====================================================

        try:

            extracted_entities = (
                extract_entities(
                    question
                )
            )

        except Exception as e:

            print(
                "Entity Extraction Error:",
                e,
            )

            extracted_entities = {
                "question": question,
                "product_names": [],
                "product_name": "",
                "amount": 0,
                "interstate": False,
            }

        if not isinstance(
            current_context,
            dict,
        ):

            current_context = {}

        current_context.update(
            extracted_entities
        )

        current_context["question"] = question

        # =====================================================
        # LOAD BUSINESS PROFILE
        # =====================================================

        business = None

        if user_id is not None:

            try:

                businesses = (
                    BusinessProfileRepository.get_all(
                        db=db,
                        user_id=user_id,
                    )
                )

                business = (
                    businesses[0]
                    if businesses
                    else None
                )

            except Exception as e:

                print(
                    "Business Profile Error:",
                    e,
                )

                business = None

        # =====================================================
        # DIRECT GST SEARCH
        #
        # FIRST:
        # ProductMaster
        #
        # SECOND:
        # Existing GST engine
        #
        # GEMINI IS NOT USED FOR PRODUCT MASTER
        # =====================================================

        if AIManager.is_gst_query(
            question
        ):

            try:

                product_name = (
                    AIManager.extract_gst_product(
                        question
                    )
                )

                print(
                    "🧾 GST Product:",
                    product_name,
                )

                if not product_name:

                    raise ValueError(
                        "No product term found "
                        "in GST question."
                    )

                # -------------------------------------------------
                # PRODUCT NAMES FROM CONTEXT
                # -------------------------------------------------

                product_names = (
                    current_context.get(
                        "product_names",
                        [],
                    )
                )

                if (
                    not product_names
                    and product_name
                ):

                    product_names = [
                        product_name
                    ]

                # -------------------------------------------------
                # MULTIPLE PRODUCTS
                # -------------------------------------------------

                if len(product_names) > 1:

                    direct_results = []

                    for name in product_names:

                        product = (
                            AIManager.direct_product_gst_search(
                                product_name=name,
                                db=db,
                            )
                        )

                        if product:

                            direct_results.append(
                                {
                                    "product":
                                        product.product_name,
                                    "success":
                                        True,
                                    "hsn":
                                        product.hsn_code,
                                    "gst_rate":
                                        product.gst_rate,
                                    "cgst":
                                        (
                                            product.gst_rate / 2
                                            if product.gst_rate
                                            is not None
                                            else 0
                                        ),
                                    "sgst":
                                        (
                                            product.gst_rate / 2
                                            if product.gst_rate
                                            is not None
                                            else 0
                                        ),
                                    "igst":
                                        product.gst_rate or 0,
                                    "hsn_description":
                                        product.description or "",
                                }
                            )

                        else:

                            direct_results.append(
                                {
                                    "product": name,
                                    "success": False,
                                    "message":
                                        "Product not found in Product Master.",
                                }
                            )

                    direct_multi_result = {
                        "success": True,
                        "products": direct_results,
                        "source":
                            "product_master",
                    }

                    response = (
                        AIManager.build_multiple_gst_response(
                            direct_multi_result
                        )
                    )

                    return {
                        "success": True,
                        "intent": "gst",
                        "context": {
                            "source":
                                "product_master",
                            "products":
                                product_names,
                        },
                        "response": response,
                    }

                # -------------------------------------------------
                # SINGLE PRODUCT
                # -------------------------------------------------

                direct_product = (
                    AIManager.direct_product_gst_search(
                        product_name=product_name,
                        db=db,
                    )
                )

                print(
                    "🔎 Direct Product:",
                    (
                        direct_product.product_name
                        if direct_product
                        else "NOT FOUND"
                    ),
                )

                # -------------------------------------------------
                # PRODUCT FOUND
                # -------------------------------------------------

                if direct_product:

                    response = (
                        AIManager.build_direct_product_response(
                            direct_product
                        )
                    )

                    gst_result = {
                        "success": True,
                        "source":
                            "product_master",
                        "product":
                            direct_product.product_name,
                        "hsn":
                            direct_product.hsn_code,
                        "gst_rate":
                            direct_product.gst_rate,
                    }

                    print(
                        "💰 Product Master GST Result:",
                        gst_result,
                    )

                    if user_id is not None:

                        try:

                            save_chat(
                                db=db,
                                user_id=user_id,
                                question=question,
                                answer=response.get(
                                    "answer",
                                    "",
                                ),
                            )

                        except Exception as e:

                            print(
                                "Save Chat Error:",
                                e,
                            )

                    return {
                        "success": True,
                        "intent": "gst",
                        "context": {
                            "product":
                                direct_product.product_name,
                            "gst_result":
                                gst_result,
                            "source":
                                "product_master",
                        },
                        "response": response,
                    }

                # -------------------------------------------------
                # PRODUCT NOT FOUND
                #
                # Try old GST engine
                # -------------------------------------------------

                print(
                    "⚠ Product not found in ProductMaster."
                )

                amount = float(
                    current_context.get(
                        "amount",
                        0,
                    )
                    or 0
                )

                interstate = bool(
                    current_context.get(
                        "interstate",
                        False,
                    )
                )

                gst_result = product_gst(
                    product_name=product_name,
                    amount=amount,
                    interstate=interstate,
                    db=db,
                )

                response = (
                    AIManager.build_gst_response(
                        product=product_name,
                        result=gst_result,
                    )
                )

                return {
                    "success": True,
                    "intent": "gst",
                    "context": {
                        "product":
                            product_name,
                        "gst_result":
                            gst_result,
                    },
                    "response": response,
                }

            except Exception as e:

                print(
                    "Direct GST Search Error:",
                    e,
                )

                # -------------------------------------------------
                # IMPORTANT:
                # Do NOT allow GST query to hang.
                # Return a useful response.
                # -------------------------------------------------

                return {
                    "success": False,
                    "intent": "gst",
                    "context": {},
                    "response": {
                        "answer": (
                            "I could not process the GST "
                            "product lookup right now. "
                            "Please try the product name again."
                        )
                    },
                }

        # =====================================================
        # DIRECT HSN SEARCH
        # =====================================================

        if AIManager.is_hsn_query(
            question
        ):

            try:

                search_term = (
                    AIManager.extract_hsn_search_term(
                        question
                    )
                )

                print(
                    "🔎 Direct HSN Search:",
                    question,
                )

                print(
                    "🔎 HSN Search Term:",
                    search_term,
                )

                if not search_term:

                    raise ValueError(
                        "No product term found "
                        "in HSN question."
                    )

                # -------------------------------------------------
                # SEARCH DATABASE
                # -------------------------------------------------

                search_result = (
                    universal_search(
                        search_term,
                        db,
                    )
                )

                print(
                    "📊 HSN Results:",
                    len(
                        search_result.get(
                            "hsn",
                            [],
                        )
                    ),
                )

                # -------------------------------------------------
                # FALLBACK
                # -------------------------------------------------

                if not search_result.get(
                    "hsn"
                ):

                    file_result = (
                        search_external_gst_data(
                            product_name=search_term,
                            amount=0,
                            interstate=False,
                        )
                    )

                    if file_result:

                        response = (
                            AIManager.build_file_hsn_response(
                                search_term,
                                file_result,
                            )
                        )

                        return {
                            "success": True,
                            "intent": "hsn",
                            "context": {
                                "search": {
                                    "source":
                                        "gst_hsn_files",
                                    "total_results":
                                        len(
                                            file_result.get(
                                                "hsn_options",
                                                [],
                                            )
                                        ),
                                }
                            },
                            "response": response,
                        }

                # -------------------------------------------------
                # FORMAT
                # -------------------------------------------------

                response = (
                    AIManager.build_hsn_response(
                        question=search_term,
                        search_result=search_result,
                    )
                )

                return {
                    "success": True,
                    "intent": "hsn",
                    "context": {
                        "search": {
                            "total_results":
                                search_result.get(
                                    "total_results",
                                    0,
                                ),
                            "hsn_results": [
                                {
                                    "hsn_code":
                                        getattr(
                                            x,
                                            "hsn_code",
                                            "",
                                        ),
                                    "description":
                                        getattr(
                                            x,
                                            "description",
                                            "",
                                        ),
                                }
                                for x in search_result.get(
                                    "hsn",
                                    [],
                                )[:10]
                            ],
                        }
                    },
                    "response": response,
                }

            except Exception as e:

                print(
                    "Direct HSN Search Error:",
                    e,
                )

                # Continue normal AI pipeline

        # =====================================================
        # ENGINE ROUTER
        # =====================================================

        try:

            engine_result = (
                EngineRouter.execute(
                    intent=intent,
                    business=business,
                    db=db,
                    entities=current_context,
                )
            )

        except Exception as e:

            print(
                "Engine Router Error:",
                e,
            )

            engine_result = {}

        if engine_result is None:

            engine_result = {}

        # =====================================================
        # REGISTRATION ADVISOR
        # =====================================================

        if (
            intent == "registration"
            and business is not None
        ):

            try:

                result = registration_summary(
                    business
                )

            except Exception as e:

                print(
                    "Registration Engine Error:",
                    e,
                )

                result = {}

            registration_status = result.get(
                "registration_status",
                "Not Available",
            )

            registration_required = result.get(
                "registration_required",
                False,
            )

            registered = result.get(
                "registered",
                False,
            )

            turnover = result.get(
                "turnover",
                0,
            )

            interstate = result.get(
                "interstate",
                False,
            )

            ecommerce = result.get(
                "ecommerce",
                False,
            )

            composition_eligible = result.get(
                "composition_eligible",
                False,
            )

            reasons = result.get(
                "reasons",
                [],
            )

            recommendations = result.get(
                "recommendations",
                [],
            )

            process = result.get(
                "process",
                [],
            )

            lines = []

            if registration_required:

                lines.append(
                    "Based on your current business profile, "
                    "GST registration is indicated as required."
                )

            elif registered:

                lines.append(
                    "Your business is currently shown as "
                    "GST registered."
                )

            else:

                lines.append(
                    "Based on the current business profile, "
                    "GST registration is not currently indicated "
                    "as mandatory by the implemented rules."
                )

            lines.append("")

            try:

                turnover_text = (
                    f"₹{float(turnover):,.2f}"
                )

            except (
                TypeError,
                ValueError,
            ):

                turnover_text = str(
                    turnover
                )

            lines.append(
                f"Annual turnover: "
                f"{turnover_text}"
            )

            lines.append(
                "Inter-State supply: "
                + (
                    "Yes"
                    if interstate
                    else "No"
                )
            )

            lines.append(
                "E-commerce: "
                + (
                    "Yes"
                    if ecommerce
                    else "No"
                )
            )

            lines.append(
                "Current GST status: "
                + (
                    "Registered"
                    if registered
                    else "Not Registered"
                )
            )

            lines.append("")

            if reasons:

                lines.append("Why:")

                for reason in reasons:

                    lines.append(
                        f"• {reason}"
                    )

                lines.append("")

            if composition_eligible:

                lines.append(
                    "Composition scheme may be considered, "
                    "subject to all applicable statutory conditions."
                )

            elif interstate:

                lines.append(
                    "Composition scheme is not being recommended "
                    "for this profile because inter-State outward "
                    "supplies are marked as applicable."
                )

                lines.append("")

            if recommendations:

                lines.append(
                    "Recommended next steps:"
                )

                for index, recommendation in enumerate(
                    recommendations,
                    start=1,
                ):

                    lines.append(
                        f"{index}. {recommendation}"
                    )

                lines.append("")

            if process:

                lines.append(
                    "GST registration process:"
                )

                for index, step in enumerate(
                    process,
                    start=1,
                ):

                    lines.append(
                        f"{index}. {step}"
                    )

                lines.append("")

            lines.append(
                "Official GST Portal: "
                "https://www.gst.gov.in/"
            )

            answer = "\n".join(
                lines
            )

            if user_id is not None:

                try:

                    save_chat(
                        db=db,
                        user_id=user_id,
                        question=question,
                        answer=answer,
                    )

                except Exception as e:

                    print(
                        "Save Chat Error:",
                        e,
                    )

            return {
                "success": True,
                "intent":
                    "registration",
                "response": {
                    "answer":
                        answer
                },
            }

        # =====================================================
        # KNOWLEDGE CONTEXT
        # =====================================================

        try:

            knowledge = (
                build_context(
                    query=question,
                    business=business,
                    db=db,
                )
            )

        except Exception as e:

            print(
                "Knowledge Engine Error:",
                e,
            )

            knowledge = {}

        if knowledge is None:

            knowledge = {}

        knowledge.setdefault(
            "query",
            question,
        )

        knowledge.setdefault(
            "business",
            current_context,
        )

        knowledge.setdefault(
            "registration",
            {},
        )

        knowledge.setdefault(
            "compliance",
            {},
        )

        knowledge.setdefault(
            "recommendations",
            [],
        )

        knowledge.setdefault(
            "search",
            {},
        )

        knowledge.setdefault(
            "notifications",
            [],
        )

        knowledge.setdefault(
            "circulars",
            [],
        )

        # =====================================================
        # ENGINE RESULT
        # =====================================================

        knowledge[
            "engine_result"
        ] = engine_result

        # =====================================================
        # BUILD PROMPT
        # =====================================================

        try:

            prompt = build_prompt(
                question=question,
                context=knowledge,
            )

        except Exception as e:

            print(
                "Prompt Builder Error:",
                e,
            )

            prompt = question

        # =====================================================
        # GEMINI
        # =====================================================

        gemini = None

        try:

            gemini = ask_gemini(
                prompt
            )

        except Exception as e:

            print(
                "Gemini Exception:",
                e,
            )

            gemini = {
                "success": False
            }

        # =====================================================
        # GEMINI SUCCESS
        # =====================================================

        if (
            gemini
            and gemini.get(
                "success",
                False,
            )
        ):

            try:

                response = (
                    format_response(
                        gemini.get(
                            "response",
                            "",
                        )
                    )
                )

            except Exception as e:

                print(
                    "Response Formatter Error:",
                    e,
                )

                response = {
                    "answer":
                        gemini.get(
                            "response",
                            "",
                        )
                }

            if not response.get(
                "answer"
            ):

                print(
                    "Gemini returned empty response. "
                    "Using fallback."
                )

                fallback_answer = (
                    fallback_response(
                        question=question,
                        intent=intent,
                        engine_result=engine_result,
                        context=knowledge,
                    )
                )

                response = {
                    "answer":
                        fallback_answer
                }

        # =====================================================
        # GEMINI FAILURE
        # =====================================================

        else:

            print(
                "Gemini unavailable. "
                "Using TaxSarthi fallback."
            )

            fallback_answer = (
                fallback_response(
                    question=question,
                    intent=intent,
                    engine_result=engine_result,
                    context=knowledge,
                )
            )

            response = {
                "answer":
                    fallback_answer
            }

        # =====================================================
        # FINAL SAFETY CHECK
        # =====================================================

        if not response.get(
            "answer"
        ):

            response = {
                "answer": (
                    "I could not generate a response "
                    "for this question right now."
                )
            }

        # =====================================================
        # SAVE CONVERSATION
        # =====================================================

        if user_id is not None:

            try:

                save_chat(
                    db=db,
                    user_id=user_id,
                    question=question,
                    answer=response.get(
                        "answer",
                        "",
                    ),
                )

            except Exception as e:

                print(
                    "Save Chat Error:",
                    e,
                )

        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {
            "success": True,
            "intent": intent,
            "context": knowledge,
            "response": response,
        }