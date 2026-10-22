from app.guardrail import validate_sql, GuardrailError

good = [
    "SELECT SUM(amount) FROM orders WHERE status = 'completed'",
    "SELECT name FROM customers WHERE created_at >= '2026-02-01';",
]
bad = [
    "DROP TABLE customers",
    "DELETE FROM orders",
    "SELECT 1; DROP TABLE orders",
    "SELECT * FROM users",
    "SELECT * FROM customers /* sneaky */",
]

for sql in good:
    print("OK     ", validate_sql(sql))
for sql in bad:
    try:
        validate_sql(sql)
        print("PASSED?!", sql)
    except GuardrailError as e:
        print("blocked:", e)