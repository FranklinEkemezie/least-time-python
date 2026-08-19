from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from least_time.models.parameters import RescueParameters
from least_time.models.result import RescueSolution
from ._common import angle_arc


def rescue_figure(parameters: RescueParameters, solution: RescueSolution) -> go.Figure:
    p, s = parameters, solution
    crossing = s.crossing
    fig = go.Figure()
    fig.add_hrect(y0=0, y1=max(8, p.saver.y + 2), fillcolor="#16324f", opacity=0.22, line_width=0)
    fig.add_hrect(y0=min(-7, p.savee.y - 2), y1=0, fillcolor="#0d5c63", opacity=0.18, line_width=0)
    fig.add_hline(y=0, line_color="#f3f4f6", line_width=3)
    fig.add_trace(go.Scatter(x=[p.saver.x, crossing.x, p.savee.x], y=[p.saver.y, 0, p.savee.y],
                             mode="lines+markers", line=dict(color="#fbbf24", width=4),
                             marker=dict(size=[14, 12, 14], color=["#fb7185", "#fbbf24", "#34d399"]),
                             name="Selected path", hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=[p.saver.x, s.optimal_x, p.savee.x], y=[p.saver.y, 0, p.savee.y],
                             mode="lines", line=dict(color="#f8fafc", width=2, dash="dash"),
                             name="Fastest path", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[s.optimal_x], y=[0], mode="markers", marker=dict(size=15, color="#f8fafc", symbol="diamond"), name="Optimal P"))
    fig.add_trace(go.Scatter(x=[crossing.x, crossing.x], y=[-1.15, 1.15], mode="lines", line=dict(color="#cbd5e1", dash="dot", width=1), name="Normal", hoverinfo="skip"))
    for point, label, color, dy in [(p.saver, "S · saver", "#fb7185", 0.35), (p.savee, "R · savee", "#34d399", -0.5)]:
        fig.add_annotation(x=point.x, y=point.y, text=label, showarrow=False, yshift=22 if dy > 0 else -22, font=dict(color=color, size=13))
    fig.add_annotation(x=crossing.x, y=0, text=f"P  x={crossing.x:.2f}", showarrow=False, yshift=18, font=dict(color="#fbbf24", size=12))
    fig.add_annotation(x=(p.saver.x + crossing.x) / 2, y=(p.saver.y) / 2, text=f"d₁={np.hypot(p.saver.x-crossing.x,p.saver.y):.2f}", showarrow=False, font=dict(color="#fde68a", size=11))
    fig.add_annotation(x=(p.savee.x + crossing.x) / 2, y=(p.savee.y) / 2, text=f"d₂={np.hypot(p.savee.x-crossing.x,p.savee.y):.2f}", showarrow=False, font=dict(color="#fde68a", size=11))
    fig.add_annotation(x=p.x_min + 1, y=max(8, p.saver.y + 2) - 0.55, text="REGION 1 · faster/slower medium", showarrow=False, font=dict(color="#93c5fd", size=11))
    fig.add_annotation(x=p.x_min + 1, y=min(-7, p.savee.y - 2) + 0.55, text="REGION 2", showarrow=False, font=dict(color="#99f6e4", size=11))
    arc1 = angle_arc(crossing.x, p.saver, 0.7, "top")
    arc2 = angle_arc(crossing.x, p.savee, 0.7, "bottom")
    fig.add_trace(go.Scatter(x=arc1[0], y=arc1[1], mode="lines", line=dict(color="#fbbf24", width=2), name="θ₁", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=arc2[0], y=arc2[1], mode="lines", line=dict(color="#fbbf24", width=2), name="θ₂", hoverinfo="skip"))
    fig.add_annotation(x=crossing.x + 0.55, y=0.85, text=f"θ₁={np.degrees(np.arcsin(abs(crossing.x-p.saver.x)/np.hypot(crossing.x-p.saver.x,p.saver.y))):.1f}°", showarrow=False, font=dict(color="#fde68a"))
    fig.add_annotation(x=crossing.x + 0.55, y=-0.85, text=f"θ₂={np.degrees(np.arcsin(abs(crossing.x-p.savee.x)/np.hypot(crossing.x-p.savee.x,p.savee.y))):.1f}°", showarrow=False, font=dict(color="#fde68a"))
    fig.update_layout(template="plotly_dark", height=510, margin=dict(l=20, r=20, t=25, b=25),
                      xaxis=dict(range=[p.x_min, p.x_max], title="interface coordinate x"),
                      yaxis=dict(range=[min(-7, p.savee.y - 2), max(8, p.saver.y + 2)], title="height y", scaleanchor="x", scaleratio=1),
                      legend=dict(orientation="h", y=-0.14), hovermode="closest")
    return fig

