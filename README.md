# Text-to-SQL Chatbot

Ask questions about a PostgreSQL database in plain English. An LLM proposes the SQL,
a guardrail validates it, a read-only database user runs it, and the answer is written
from verified numbers.

## How it works
question → OpenAI writes SQL → guardrail checks → read-only DB runs → Python summarizes → OpenAI explains

## Setup
1. Install Python 3.10+ and PostgreSQL.
2. `python -m venv .venv` then activate it.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your values.
5. Create the database and load `db/demo.sql`, then `db/readonly.sql`.
6. `uvicorn app.main:app --reload` and open http://127.0.0.1:8000/docs

## Tests
`pytest`

## Safety
- Only SELECT statements and allowed tables pass the guardrail.
- Queries run as a read-only database user with a 5-second timeout.
- Row limit added automatically.

## Known limitations
- The guardrail checks words, not full SQL grammar, so some valid queries are rejected.
- Conversation memory is in RAM and resets on restart.
- No login yet.
