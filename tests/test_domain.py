import pytest
from sqlalchemy import create_engine, text

from erp.kpis import completion_rate, grouped_totals
from erp.sql_analytics import grouped_sum


def test_completion_rate_handles_empty_denominator():
    assert completion_rate(0, 0) == 0

def test_grouped_totals():
    assert grouped_totals([{"team": "A", "hours": 2}, {"team": "A", "hours": 3}], "team", "hours") == {"A": 5.0}

def test_completion_rate_rejects_impossible_values():
    with pytest.raises(ValueError):
        completion_rate(3, 2)


def test_grouped_sum_uses_reflected_table_columns():
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE sales (team TEXT, amount REAL)"))
        connection.execute(text("INSERT INTO sales VALUES ('A', 4), ('A', 6), ('B', 3)"))
        assert grouped_sum(connection, "sales", "team", "amount") == {"A": 10.0, "B": 3.0}
