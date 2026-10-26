"""Plotly chart builder for already-aggregated ERP KPI values."""

from collections.abc import Mapping

import plotly.graph_objects as go


def kpi_bar_chart(values: Mapping[str, float], *, title: str = "Operational KPI") -> go.Figure:
    if not values or any(not isinstance(value, (int, float)) for value in values.values()):
        raise ValueError("provide a non-empty mapping of numeric aggregate values")
    figure = go.Figure(go.Bar(x=list(values), y=list(values.values()), marker_color="#258f86"))
    figure.update_layout(title=title, xaxis_title="Group", yaxis_title="Value", template="plotly_white")
    return figure
