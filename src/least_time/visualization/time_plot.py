from __future__ import annotations

import plotly.graph_objects as go

from least_time.models.parameters import RescueParameters
from least_time.models.result import RescueSolution


def time_figure(parameters: RescueParameters, solution: RescueSolution, xs, times) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=times, mode="lines", line=dict(color="#60a5fa", width=3), name="T(x)"))
    fig.add_trace(go.Scatter(x=[solution.optimal_x], y=[solution.minimum_time], mode="markers+text",
                             text=["minimum"], textposition="top center", marker=dict(size=12, color="#34d399"), name="x*"))
    fig.add_trace(go.Scatter(x=[parameters.crossing_x], y=[solution.current_time], mode="markers+text",
                             text=["current"], textposition="bottom center", marker=dict(size=12, color="#fbbf24"), name="selected x"))
    fig.update_layout(template="plotly_dark", height=360, margin=dict(l=35, r=20, t=30, b=35),
                      title="Total travel time T(x)", xaxis_title="crossing coordinate x", yaxis_title="time (s)",
                      hovermode="x unified", legend=dict(orientation="h", y=-0.22))
    return fig

