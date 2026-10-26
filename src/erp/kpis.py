"""Small pure-function KPI helpers over already-authorized aggregate values."""

from collections.abc import Iterable


def completion_rate(completed: int, total: int) -> float:
    if completed < 0 or total < 0 or completed > total:
        raise ValueError("expected 0 <= completed <= total")
    return completed / total if total else 0.0


def grouped_totals(rows: Iterable[dict[str, object]], group_key: str, value_key: str) -> dict[str, float]:
    totals: dict[str, float] = {}
    for row in rows:
        group = str(row[group_key])
        value = float(row[value_key])
        totals[group] = totals.get(group, 0.0) + value
    return totals
