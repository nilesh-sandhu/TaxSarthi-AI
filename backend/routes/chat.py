from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from core.database import get_db

from dependencies.auth import (
    get_current_user,
)

from models.user import User

from repositories.chat_history import (
    ChatHistoryRepository,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat History"],
)


# ============================================================
# GET CHAT HISTORY
# ============================================================

@router.get("/history")
def get_chat_history(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    history = (
        ChatHistoryRepository.get_history(
            db=db,
            user_id=current_user.id,
            limit=100,
        )
    )

    # Reverse so oldest message appears first
    history.reverse()

    return {
        "success": True,
        "user_id": current_user.id,
        "total": len(history),
        "history": [
            {
                "id": chat.id,
                "role": chat.role,
                "message": chat.message,
                "created_at": chat.created_at,
            }
            for chat in history
        ],
    }


# ============================================================
# CLEAR CHAT HISTORY
# ============================================================

@router.delete("/history")
def clear_chat_history(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    result = (
        ChatHistoryRepository.clear_history(
            db=db,
            user_id=current_user.id,
        )
    )

    return {
        "success": True,
        **result,
    }