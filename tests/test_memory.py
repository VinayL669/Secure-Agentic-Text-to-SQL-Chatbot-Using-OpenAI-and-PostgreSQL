from app.memory import MAX_HISTORY_TURNS, add_turn, conversations, get_history


def test_unknown_conversation_has_empty_history():
    conversations.clear()
    assert get_history("never-seen") == []


def test_turns_are_stored_in_order():
    conversations.clear()
    add_turn("c1", "first", "a1", "SELECT 1")
    add_turn("c1", "second", "a2", None)
    history = get_history("c1")
    assert [turn["question"] for turn in history] == ["first", "second"]
    assert history[1]["sql"] is None


def test_history_is_capped_and_oldest_is_dropped():
    conversations.clear()
    for i in range(MAX_HISTORY_TURNS + 2):
        add_turn("c1", f"q{i}", f"a{i}", f"SELECT {i}")
    history = get_history("c1")
    assert len(history) == MAX_HISTORY_TURNS
    assert history[0]["question"] == "q2"


def test_conversations_do_not_mix():
    conversations.clear()
    add_turn("alice", "hello", "hi", None)
    assert get_history("bob") == []