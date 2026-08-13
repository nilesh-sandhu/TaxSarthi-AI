import json

from ai.gemini import ask_gemini
from ai.invoice_prompt import INVOICE_EXTRACTION_PROMPT
from ai.invoice_parser import InvoiceParser


class InvoiceAI:

    @staticmethod
    def extract(text: str):

        prompt = f"""
{INVOICE_EXTRACTION_PROMPT}

Invoice Text:

{text}
"""

        response = ask_gemini(prompt)

        if not response.get("success"):

            return {}

        return InvoiceParser.parse(
            response.get("response", "")
        )