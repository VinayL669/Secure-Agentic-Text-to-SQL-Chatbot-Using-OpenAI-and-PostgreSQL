from fastapi import FastAPI
from app.db import run_query

app = FastAPI(title="SQL Chatbot")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/db-check")
def db_check():
    return run_query("SELECT COUNT(*) AS customers FROM customers")