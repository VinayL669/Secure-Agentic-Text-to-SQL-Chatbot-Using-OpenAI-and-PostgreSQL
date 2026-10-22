from types import SimpleNamespace

from fastapi.testclient import TestClient

import app.main as main
from app.memory import conversations


def test_chat_replays_history_on_follow_up(monkeypatch):
    conversations.clear()
    seen_histories = []

    def fake_generate_sql(question, history=None):
        seen_histories.append(list(history or []))
        return SimpleNamespace(sql="SELECT COUNT(*) AS n FROM customers")

    monkeypatch.setattr(main, "generate_sql", fake_generate_sql)
    monkeypatch.setattr(main, "run_readonly_query", lambda sql: [{"n": 5}])
    monkeypatch.setattr(main, "generate_answer", lambda q, rows, facts: "There are 5 customers.")

    client = TestClient(main.app)
    first = client.post("/chat", json={"message": "how many customers"}).json()
    client.post("/chat", json={"conversation_id": first["conversation_id"], "message": "again"})

    assert first["answer"] == "There are 5 customers."
    assert len(seen_histories[0]) == 0
    assert len(seen_histories[1]) == 1


def test_chat_blocks_dangerous_sql(monkeypatch):
    conversations.clear()
    ran = []

    monkeypatch.setattr(main, "generate_sql", lambda q, history=None: SimpleNamespace(sql="DROP TABLE customers"))
    monkeypatch.setattr(main, "run_readonly_query", lambda sql: ran.append(sql))

    client = TestClient(main.app)
    body = client.post("/chat", json={"message": "delete everything"}).json()

    assert body["answer"].startswith("I can't run that query")
    assert ran == []


def test_chat_rejects_empty_message():
    client = TestClient(main.app)
    assert client.post("/chat", json={"message": ""}).status_code == 422