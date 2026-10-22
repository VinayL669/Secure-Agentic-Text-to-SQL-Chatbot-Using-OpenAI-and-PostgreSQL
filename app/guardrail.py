import re

ALLOWED_TABLES = {"customers", "orders"}
FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter", "truncate",
    "create", "grant", "revoke", "copy", "execute", "call",
}
MAX_ROWS = 100


class GuardrailError(Exception):
    pass


def validate_sql(sql: str) -> str:
    """Return safe SQL to execute, or raise GuardrailError."""
    cleaned = sql.strip().rstrip(";").strip()
    lowered = cleaned.lower()

    if not lowered:
        raise GuardrailError("Empty SQL.")

    if not lowered.startswith("select"):
        raise GuardrailError("Only SELECT statements are allowed.")

    if ";" in lowered:
        raise GuardrailError("Multiple statements are not allowed.")

    if "--" in lowered or "/*" in lowered:
        raise GuardrailError("SQL comments are not allowed.")

    for word in re.findall(r"[a-z_]+", lowered):
        if word in FORBIDDEN_KEYWORDS:
            raise GuardrailError(f"Forbidden keyword found: '{word}'")

        # EXTRACT(year FROM created_at) and "IS DISTINCT FROM" use the word FROM
        # without naming a table, so hide them before looking for table names.
    for_tables = re.sub(r"extract\s*\(\s*[a-z_]+\s+from\s", "extract(x ", lowered)
    for_tables = re.sub(r"distinct\s+from\s", "distinct_from ", for_tables)

    for table in re.findall(r"\b(?:from|join)\s+([a-z_][a-z0-9_]*)", for_tables):
        if table not in ALLOWED_TABLES:
            raise GuardrailError(f"Table not allowed: '{table}'")

    if not re.search(r"\blimit\b", lowered):
        cleaned = f"{cleaned} LIMIT {MAX_ROWS}"

    return cleaned