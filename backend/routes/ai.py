from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.ai import (
    AIChatRequest,
    AIChatResponse,
)

from ai.ai_manager import AIManager

from dependencies.auth import (
    get_optional_current_user,
)

from models.user import User


router = APIRouter(
    prefix="/ai",
    tags=["AI Copilot"],
)


# ============================================================
# AI CHAT
# Guest + Logged-in users
# ============================================================

@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat(
    request: AIChatRequest,
    current_user: User | None = Depends(
        get_optional_current_user
    ),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Guest = None
    # Logged-in = current user's ID
    # --------------------------------------------------------

    user_id = None

    if current_user is not None:
        user_id = current_user.id

    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    result = AIManager.ask(
        user_id=user_id,
        question=request.question,
        db=db,
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "intent": result.get(
            "intent",
            "general",
        ),
        "response": result.get(
            "response",
            result,
        ),
    }