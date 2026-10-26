"""Parameterized aggregate queries for an existing SQLAlchemy connection."""

import re

from sqlalchemy import MetaData, Table, func, select
from sqlalchemy.engine import Connection


def grouped_sum(
    connection: Connection, table_name: str, group_column: str, value_column: str
) -> dict[str, float]:
    """Aggregate a numeric column by a dimension using reflected SQL identifiers."""
    identifiers = [table_name, group_column, value_column]
    if any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value) for value in identifiers):
        raise ValueError("table and column names must be simple SQL identifiers")
    table = Table(table_name, MetaData(), autoload_with=connection)
    if group_column not in table.c or value_column not in table.c:
        raise ValueError("requested columns are not present in the table")
    statement = (
        select(table.c[group_column], func.sum(table.c[value_column]))
        .group_by(table.c[group_column])
        .order_by(table.c[group_column])
    )
    return {str(group): float(total or 0) for group, total in connection.execute(statement)}
