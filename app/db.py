import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)


def run_query(sql: str) -> list[dict]:
    with engine.connect() as connection:
        result = connection.execute(text(sql))
        return [dict(row._mapping) for row in result]


if __name__ == "__main__":
    rows = run_query("SELECT name, city FROM customers ORDER BY name")
    for row in rows:
        print(row)