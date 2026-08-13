from repositories.chat_history import ChatHistoryRepository


def save_chat(
    db,
    user_id,
    question,
    answer,
):
    """
    Save chat conversation for logged-in users.

    Guest users:
        user_id = None
        Chat history is not saved.

    Logged-in users:
        user_id = actual database user ID
        Both user and assistant messages are saved.
    """

    # =====================================================
    # GUEST USER
    # =====================================================

    if user_id is None:
        return

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    ChatHistoryRepository.save_message(
        db=db,
        user_id=user_id,
        role="user",
        message=question,
    )

    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    ChatHistoryRepository.save_message(
        db=db,
        user_id=user_id,
        role="assistant",
        message=answer,
    )