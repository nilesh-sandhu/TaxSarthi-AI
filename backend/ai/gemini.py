import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =====================================================
# ENV FILE
# =====================================================

ENV_PATH = PROJECT_ROOT / ".env"

# Load .env explicitly
load_dotenv(
    dotenv_path=ENV_PATH,
    override=True,
)

# =====================================================
# API KEY
# =====================================================

API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("TaxSarthi AI - Gemini Configuration")
print("=" * 60)
print("Project Root :", PROJECT_ROOT)
print(".env Path    :", ENV_PATH)
print(".env Exists  :", ENV_PATH.exists())
print("API Loaded   :", "YES" if API_KEY else "NO")
print("=" * 60)


# =====================================================
# GEMINI CLIENT
# =====================================================

client = None

if API_KEY:

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        print(
            "Gemini client initialized successfully."
        )

    except Exception as e:

        print(
            "Gemini initialization failed:"
        )

        print(e)

        client = None

else:

    print(
        "Gemini API Key Missing."
    )


# =====================================================
# ASK GEMINI
# =====================================================

def ask_gemini(prompt: str):

    # -------------------------------------------------
    # Gemini unavailable
    # -------------------------------------------------

    if client is None:

        return {

            "success": False,

            "available": False,

            "response": "",

            "error_type": "unavailable",

        }

    # -------------------------------------------------
    # Empty prompt
    # -------------------------------------------------

    if not prompt or not prompt.strip():

        return {

            "success": False,

            "available": True,

            "response": "",

            "error_type": "invalid_prompt",

        }

    # -------------------------------------------------
    # Generate response
    # -------------------------------------------------

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

        )

        text = getattr(
            response,
            "text",
            None,
        )

        if not text:

            return {

                "success": False,

                "available": True,

                "response": "",

                "error_type": "empty_response",

            }

        return {

            "success": True,

            "available": True,

            "response": text,

            "error_type": None,

        }

    # -------------------------------------------------
    # Any Gemini/API error
    # -------------------------------------------------

    except Exception as e:

        print(
            "Gemini request failed:"
        )

        print(e)

        return {

            "success": False,

            "available": True,

            "response": "",

            "error_type": "api_error",

        }