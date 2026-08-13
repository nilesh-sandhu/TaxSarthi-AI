from sqlalchemy.orm import Session

from models.chat_history import ChatHistory


class ChatHistoryRepository:

    # -----------------------------
    # Save Message
    # -----------------------------
    @staticmethod
    def save_message(
        db: Session,
        user_id: int | None,
        role: str,
        message: str,
    ):

        chat = ChatHistory(
            user_id=user_id,
            role=role,
            message=message,
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat

    # -----------------------------
    # Get Chat History
    # -----------------------------
    @staticmethod
    def get_history(
        db: Session,
        user_id: int | None,
        limit: int = 20,
    ):

        return (
            db.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
            .all()
        )

    # -----------------------------
    # Clear Chat
    # -----------------------------
    @staticmethod
    def clear_history(
        db: Session,
        user_id: int | None,
    ):

        (
            db.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id)
            .delete()
        )

        db.commit()

        return {
            "message": "Chat history cleared."
        }