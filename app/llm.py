import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

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

if __name__ == "__main__":
    print(ask("Say hello in one short sentence."))
    print(route("How many customers do we have?"))
    print(route("Explain what SQL JOIN means."))