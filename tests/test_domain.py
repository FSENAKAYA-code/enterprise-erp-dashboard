import pytest

from erp.kpis import completion_rate, grouped_totals


def test_completion_rate_handles_empty_denominator():
    assert completion_rate(0, 0) == 0

def test_grouped_totals():
    assert grouped_totals([{"team": "A", "hours": 2}, {"team": "A", "hours": 3}], "team", "hours") == {"A": 5.0}

def test_completion_rate_rejects_impossible_values():
    with pytest.raises(ValueError):
        completion_rate(3, 2)
