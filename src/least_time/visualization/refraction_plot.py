from __future__ import annotations

import plotly.graph_objects as go

from least_time.models.parameters import RescueParameters
from least_time.models.result import RescueSolution


def refraction_figure(parameters: RescueParameters, solution: RescueSolution) -> go.Figure:
    p, s = parameters, solution
    fig = go.Figure()
    fig.add_hrect(y0=0, y1=max(8, p.saver.y + 2), fillcolor="#243b53", opacity=0.3, line_width=0)
    fig.add_hrect(y0=min(-7, p.savee.y - 2), y1=0, fillcolor="#115e59", opacity=0.22, line_width=0)
    fig.add_hline(y=0, line_color="#f8fafc", line_width=3)
    fig.add_trace(go.Scatter(x=[p.saver.x, s.crossing.x, p.savee.x], y=[p.saver.y, 0, p.savee.y], mode="lines+markers",
                             line=dict(color="#fbbf24", width=4), marker=dict(size=11, color="#fbbf24"), name="ray"))
    fig.add_trace(go.Scatter(x=[s.crossing.x, s.crossing.x], y=[-1.35, 1.35], mode="lines", line=dict(color="#cbd5e1", dash="dot"), name="normal"))
    fig.add_annotation(x=p.x_min + 1, y=max(8, p.saver.y + 2)-0.5, text="MEDIUM 1 · n₁=1.00", showarrow=False, font=dict(color="#bfdbfe", size=12))
    fig.add_annotation(x=p.x_min + 1, y=min(-7, p.savee.y - 2)+0.5, text=f"MEDIUM 2 · n₂={p.v1/p.v2:.2f}", showarrow=False, font=dict(color="#99f6e4", size=12))
    fig.add_annotation(x=s.crossing.x, y=0, text="interface", showarrow=False, yshift=18, font=dict(color="#f8fafc"))
    fig.update_layout(template="plotly_dark", height=360, margin=dict(l=20, r=20, t=30, b=25), title="Optical interpretation",
                      xaxis=dict(range=[p.x_min, p.x_max], title="position"), yaxis=dict(range=[min(-7,p.savee.y-2), max(8,p.saver.y+2)], title="height", scaleanchor="x", scaleratio=1),
                      legend=dict(orientation="h", y=-0.18), showlegend=False)
    return fig

