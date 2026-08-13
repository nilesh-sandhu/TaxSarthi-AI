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
from engines.gst_engine import product_gst, product_gst_multiple

from repositories.business_profile import (
    BusinessProfileRepository,
)

from services.search import universal_search


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

            # HSN + GST combined
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

        """
        Examples:

            HSN code of shirt
            -> shirt

            HSN code for shirt
            -> shirt

            HSN on shirt
            -> shirt

            HSN code for cotton shirt
            -> cotton shirt

            What is the HSN of jeans?
            -> jeans
        """

        q = (
            question or ""
        ).lower().strip()

        # -----------------------------------------------------
        # Remove common HSN phrases
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Remove remaining question words
        # -----------------------------------------------------

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

        """
        Examples:

            GST on shirt
            -> shirt

            GST rate for laptop
            -> laptop

            GST of t shirt
            -> t shirt

            HSN and GST of shirt
            -> shirt
        """

        q = (
            question or ""
        ).lower().strip()

        patterns = [

            # What is GST on shirt?
            r"\bwhat(?:'s| is)\s+(?:the\s+)?gst"
            r"(?:\s+rate|\s+percentage|\s+%)?"
            r"\s+(?:of|for|on)\s+",

            # GST on shirt
            r"\bgst"
            r"(?:\s+rate|\s+percentage|\s+%)?"
            r"\s+(?:of|for|on)\s+",

            # Tax on shirt
            r"\btax"
            r"(?:\s+rate|\s+percentage|\s+%)?"
            r"\s+(?:of|for|on)\s+",

            # HSN and GST of shirt
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

        # -----------------------------------------------------
        # Remove remaining words
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # No result
        # -----------------------------------------------------

        if not hsn_results:

            return {
                "answer": (
                    f"I could not find a matching HSN "
                    f"record for '{question}'. "
                    f"Please provide more product details "
                    f"such as material, fabric and product type."
                )
            }

        # -----------------------------------------------------
        # Remove duplicates
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Limit results
        # -----------------------------------------------------

        matches = list(
            unique.items()
        )[:10]

        # -----------------------------------------------------
        # Build response
        # -----------------------------------------------------

        lines = []

        lines.append(
            "I found the following matching HSN records "
            "in the TaxSarthi HSN database:"
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

        # -----------------------------------------------------
        # GST lookup failed
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Multiple classifications
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Single classification
        # -----------------------------------------------------

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

        if not result.get("success", False):
            return {
                "answer": result.get(
                    "message",
                    "No GST information found.",
                )
            }

        products = result.get("products", [])

        if not products:
            return {
                "answer": "No product GST information was found."
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

            if not item.get("success", False):

                lines.extend([
                    f"**{product.title()}**",
                    f"❌ {item.get('message', 'No information found.')}",
                    "",
                ])
                continue

            if item.get("classification_required", False):

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
                f"• HSN Code: {item.get('hsn', 'N/A')}",
                f"• Description: {item.get('hsn_description', '')}",
                f"• GST Rate: {item.get('gst_rate', 0)}%",
                f"• CGST: {item.get('cgst', 0)}%",
                f"• SGST: {item.get('sgst', 0)}%",
                f"• IGST: {item.get('igst', 0)}%",
            ])

            if item.get("cess", 0):
                lines.append(
                    f"• Cess: {item.get('cess')}%"
                )

            if item.get("notification_no"):
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
                    "answer": "Please enter a question."
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
            extracted_entities = extract_entities(
                question
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

        if not isinstance(current_context, dict):
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
        # MUST COME BEFORE HSN SEARCH
        #
        # Example:
        #
        # HSN and GST of shirt
        #
        # contains "HSN", but we want the combined
        # GST engine to handle it.
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
                # GST ENGINE
                # -------------------------------------------------

                product_names = current_context.get(
                    "product_names",
                    [],
                )

                if not product_names and product_name:
                    product_names = [product_name]

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

                if len(product_names) > 1:

                    gst_result = product_gst_multiple(
                        products=product_names,
                        amount=amount,
                        interstate=interstate,
                        db=db,
                    )

                    response = (
                        AIManager.build_multiple_gst_response(
                            gst_result
                        )
                    )

                    print(
                        "💰 Multiple GST Result:",
                        gst_result,
                    )

                else:

                    product_name = (
                        product_names[0]
                        if product_names
                        else product_name
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

                    print(
                        "💰 GST Result:",
                        gst_result,
                    )

                print(
                    "💰 GST Result:",
                    gst_result,
                )

                # -------------------------------------------------
                # Save Chat
                # -------------------------------------------------

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
                        "product": product_name,
                        "gst_result": gst_result,
                    },
                    "response": response,
                }

            except Exception as e:

                print(
                    "Direct GST Search Error:",
                    e,
                )

                # Continue normal AI pipeline

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

                # -------------------------------------------------
                # No product found
                # -------------------------------------------------

                if not search_term:

                    raise ValueError(
                        "No product term found "
                        "in HSN question."
                    )

                # -------------------------------------------------
                # Search HSN database
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
                # Format response
                # -------------------------------------------------

                response = (
                    AIManager.build_hsn_response(
                        question=search_term,
                        search_result=search_result,
                    )
                )

                # -------------------------------------------------
                # Save Chat
                # -------------------------------------------------

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
                    "intent": "hsn",
                    "context": {
                        "search": {
                            "total_results": (
                                search_result.get(
                                    "total_results",
                                    0,
                                )
                            ),
                            "hsn_results": [
                                {
                                    "hsn_code": getattr(
                                        x,
                                        "hsn_code",
                                        "",
                                    ),
                                    "description": getattr(
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

        # =====================================================
        # NORMALIZE ENGINE RESULT
        # =====================================================

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

            # =================================================
            # EXTRACT REGISTRATION RESULT
            # =================================================

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

            # =================================================
            # BUILD USER-FRIENDLY RESPONSE
            # =================================================

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

            # =================================================
            # BUSINESS DETAILS
            # =================================================

            try:
                turnover_text = f"₹{float(turnover):,.2f}"
            except (TypeError, ValueError):
                turnover_text = str(turnover)

            lines.append(
                f"Annual turnover: {turnover_text}"
            )

            lines.append(
                "Inter-State supply: "
                + ("Yes" if interstate else "No")
            )

            lines.append(
                "E-commerce: "
                + ("Yes" if ecommerce else "No")
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

            # =================================================
            # REASONS
            # =================================================

            if reasons:

                lines.append("Why:")

                for reason in reasons:

                    lines.append(
                        f"• {reason}"
                    )

                lines.append("")

            # =================================================
            # COMPOSITION SCHEME
            # =================================================

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

            # =================================================
            # RECOMMENDATIONS
            # =================================================

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

            # =================================================
            # REGISTRATION PROCESS
            # =================================================

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
                "Official GST Portal: https://www.gst.gov.in/"
            )

            answer = "\n".join(lines)

            # =================================================
            # SAVE REGISTRATION CHAT
            # =================================================

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
                "intent": "registration",
                "response": {
                    "answer": answer,
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

        # =====================================================
        # SAFE DEFAULTS
        # =====================================================

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
                    "answer": gemini.get(
                        "response",
                        "",
                    )
                }

            # -------------------------------------------------
            # Empty response fallback
            # -------------------------------------------------

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
                    "answer": fallback_answer
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
                "answer": fallback_answer
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