import pytest

from app.guardrail import GuardrailError, MAX_ROWS, validate_sql


def assert_blocked(sql, expected_text=None):
    with pytest.raises(GuardrailError) as error:
        validate_sql(sql)
    if expected_text:
        assert expected_text in str(error.value)


def test_limit_is_added_when_missing():
    result = validate_sql("SELECT name FROM customers")
    assert result == f"SELECT name FROM customers LIMIT {MAX_ROWS}"


def test_existing_limit_is_kept():
    result = validate_sql("SELECT name FROM customers LIMIT 3")
    assert result == "SELECT name FROM customers LIMIT 3"


def test_trailing_semicolon_is_removed():
    result = validate_sql("SELECT name FROM customers;")
    assert ";" not in result


def test_created_at_column_is_allowed():
    # Regression: "create" used to match inside "created_at".
    validate_sql("SELECT name FROM customers WHERE created_at >= '2026-02-01'")


def test_extract_year_is_allowed():
    # Regression: the FROM inside EXTRACT(...) was mistaken for a table name.
    validate_sql("SELECT id FROM orders WHERE EXTRACT(YEAR FROM created_at) = 2030")


def test_join_between_allowed_tables_is_allowed():
    validate_sql(
        "SELECT c.name, o.amount FROM orders o JOIN customers c ON c.id = o.customer_id"
    )


def test_destructive_statements_are_blocked():
    for sql in [
        "DROP TABLE customers",
        "drop table customers",
        "DELETE FROM orders",
        "UPDATE orders SET amount = 0",
        "INSERT INTO orders (amount) VALUES (1)",
        "TRUNCATE orders",
        "ALTER TABLE orders ADD COLUMN x int",
        "CREATE TABLE x (a int)",
        "GRANT ALL ON orders TO public",
    ]:
        assert_blocked(sql)


def test_non_select_statements_are_blocked():
    # None of these contain a forbidden keyword, so only the "must start with SELECT" rule stops them.
    for sql in ["SHOW ALL", "SET ROLE postgres", "EXPLAIN SELECT * FROM orders", "VACUUM orders", "BEGIN"]:
        assert_blocked(sql, "Only SELECT")


def test_stacked_statements_are_blocked():
    assert_blocked("SELECT 1 FROM orders; DROP TABLE orders", "Multiple statements")


def test_comments_are_blocked():
    assert_blocked("SELECT name FROM customers -- hi", "comments")
    assert_blocked("SELECT name FROM customers /* sneaky */", "comments")


def test_unknown_tables_are_blocked():
    for sql in [
        "SELECT * FROM users",
        "SELECT id FROM orders JOIN secrets ON 1 = 1",
        "SELECT id FROM orders WHERE id IN (SELECT id FROM secrets)",
        "SELECT id FROM orders UNION SELECT id FROM secrets",
    ]:
        assert_blocked(sql, "Table not allowed")


def test_extract_does_not_hide_a_bad_table():
    assert_blocked("SELECT EXTRACT(year FROM created_at) FROM users", "Table not allowed")


def test_empty_sql_is_blocked():
    assert_blocked("")
    assert_blocked("   ")