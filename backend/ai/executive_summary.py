from ai.gemini import ask_gemini


class ExecutiveSummary:

    @staticmethod
    def generate(stats: dict):

        prompt = f"""
You are a Chartered Accountant.

Generate a professional business GST summary.

Dashboard Statistics:

{stats}

Rules:
- Maximum 120 words.
- Professional tone.
- Mention risks.
- Mention compliance.
- Mention recommendations.
"""

        response = ask_gemini(prompt)

        if response.get("success"):

            return response["response"]

        return "Unable to generate executive summary."