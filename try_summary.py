from app.db import run_readonly_query
from app.analysis import summarize

rows = run_readonly_query("SELECT status, amount FROM orders")
print(summarize(rows))