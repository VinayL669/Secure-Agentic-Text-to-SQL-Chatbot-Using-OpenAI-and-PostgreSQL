from decimal import Decimal

from app.analysis import summarize


def test_empty_result():
    assert summarize([]) == {"row_count": 0}


def test_decimal_values_are_summed_exactly():
    rows = [{"amount": Decimal("500.00")}, {"amount": Decimal("300.00")}]
    facts = summarize(rows)
    assert facts["row_count"] == 2
    assert facts["amount_sum"] == Decimal("800.00")
    assert facts["amount_avg"] == Decimal("400.00")
    assert facts["amount_min"] == Decimal("300.00")
    assert facts["amount_max"] == Decimal("500.00")


def test_text_columns_are_ignored():
    facts = summarize([{"city": "Mumbai", "n": 2}, {"city": "Delhi", "n": 3}])
    assert "city_sum" not in facts
    assert facts["n_sum"] == 5


def test_null_in_first_row_does_not_hide_the_column():
    facts = summarize([{"amount": None}, {"amount": Decimal("5")}])
    assert facts["amount_sum"] == Decimal("5")


def test_booleans_are_not_treated_as_numbers():
    facts = summarize([{"active": True}, {"active": False}])
    assert "active_sum" not in facts