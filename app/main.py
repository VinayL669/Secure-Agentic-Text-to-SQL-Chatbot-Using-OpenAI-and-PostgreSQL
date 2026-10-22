from fastapi import FastAPI
from app.db import run_query
from app.llm import generate_sql, generate_answer
from app.guardrail import validate_sql, GuardrailError
from app.db import run_readonly_query
from app.analysis import summarize

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