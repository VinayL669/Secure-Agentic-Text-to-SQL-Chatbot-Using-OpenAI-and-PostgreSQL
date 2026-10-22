from fastapi import FastAPI
from app.db import run_query
from app.llm import generate_sql, generate_answer
from app.guardrail import validate_sql, GuardrailError
from app.db import run_readonly_query
from app.analysis import summarize
from app.schemas import ChatRequest, ChatResponse, new_conversation_id
from app.memory import get_history, add_turn

app = FastAPI(title="SQL Chatbot")


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/db-check")
def db_check():
    return run_query("SELECT COUNT(*) AS customers FROM customers")

@app.get("/ask")
def ask(question: str):
    proposal = generate_sql(question)

    try:
        safe_sql = validate_sql(proposal.sql)
    except GuardrailError as e:
        return {"error": str(e), "attempted_sql": proposal.sql}

    try:
        rows = run_readonly_query(safe_sql)
    except Exception:
        return {"error": "I couldn't access the database right now. Please try again."}

    facts = summarize(rows)
    answer = generate_answer(question, rows, facts)

    return {"answer": answer, "facts": facts, "sql": safe_sql}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation_id = request.conversation_id or new_conversation_id()
    history = get_history(conversation_id)

    proposal = generate_sql(request.message, history)

    try:
        safe_sql = validate_sql(proposal.sql)
    except GuardrailError as e:
        answer = f"I can't run that query: {e}"
        add_turn(conversation_id, request.message, answer, None)
        return ChatResponse(conversation_id=conversation_id, answer=answer, facts={})

    try:
        rows = run_readonly_query(safe_sql)
    except Exception as e:
        print("Database error:", e)
        answer = "I couldn't access the database right now. Please try again."
        add_turn(conversation_id, request.message, answer, safe_sql)
        return ChatResponse(conversation_id=conversation_id, answer=answer, facts={})

    facts = summarize(rows)
    answer = generate_answer(request.message, rows, facts)
    add_turn(conversation_id, request.message, answer, safe_sql)

    return ChatResponse(conversation_id=conversation_id, answer=answer, sql=safe_sql, facts=facts)