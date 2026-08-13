from sqlalchemy.orm import Session

from repositories.chat_history import ChatHistoryRepository


def save_chat(
    db: Session,
    user_id: int | None,
    role: str,
    message: str,
):

    return ChatHistoryRepository.save_message(
        db,
        user_id,
        role,
        message,
    )


def get_chat_history(
    db: Session,
    user_id: int | None,
):

    return ChatHistoryRepository.get_history(
        db,
        user_id,
    )


def clear_chat_history(
    db: Session,
    user_id: int | None,
):

    return ChatHistoryRepository.clear_history(
        db,
        user_id,
    )