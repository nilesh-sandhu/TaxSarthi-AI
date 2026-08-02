from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from services.chat import chat_with_ai

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    return chat_with_ai(
        request.message,
        db,
    )