import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from app.db import run_query

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"


def ask(question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content

class RouterDecision(BaseModel):
    requires_sql: bool
    reasoning: str


def route(question: str) -> RouterDecision:
    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Decide whether answering the user's question requires querying a database.",
            },
            {"role": "user", "content": question},
        ],
        response_format=RouterDecision,
    )
    return response.choices[0].message.parsed
SCHEMA = """
Table customers(id INTEGER, name TEXT, city TEXT, created_at DATE)
Table orders(id INTEGER, customer_id INTEGER REFERENCES customers.id,
             status TEXT, amount NUMERIC, created_at DATE)
"""

SQL_SYSTEM_PROMPT = f"""You are a PostgreSQL SQL generation engine.

Schema:
{SCHEMA}

Rules:
- Only use the tables and columns listed above. Never invent any.
- Generate read-only SQL: SELECT statements only.
- Always include a LIMIT clause (100 or fewer) unless the question needs a single aggregate value.
- Prefer explicit column names over SELECT *.
"""


class SqlProposal(BaseModel):
    sql: str
    explanation: str
    tables_used: list[str]


def generate_sql(question: str) -> SqlProposal:
    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": SQL_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        response_format=SqlProposal,
    )
    return response.choices[0].message.parsed

if __name__ == "__main__":
    print(ask("Say hello in one short sentence."))
    print(route("How many customers do we have?"))
    print(route("Explain what SQL JOIN means."))
    result = generate_sql("What is the total revenue from completed orders?")
    print(result.sql)
    print(result.explanation)
    print(run_query(result.sql))
