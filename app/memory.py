MAX_HISTORY_TURNS = 5

conversations: dict[str, list[dict]] = {}


def get_history(conversation_id: str) -> list[dict]:
    return conversations.get(conversation_id, [])


def add_turn(conversation_id: str, question: str, answer: str, sql: str | None) -> None:
    history = conversations.setdefault(conversation_id, [])
    history.append({"question": question, "answer": answer, "sql": sql})
    if len(history) > MAX_HISTORY_TURNS:
        del history[0]