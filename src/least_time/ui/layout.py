from __future__ import annotations

import streamlit as st

from least_time.mathematics.optimization import solve_rescue
from least_time.mathematics.refraction import normalized_indices
from least_time.models.parameters import RescueParameters


def configure_page() -> None:
    st.set_page_config(page_title="Least Time → Refraction", page_icon="〽", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""<style>
    .block-container {padding-top: 2rem; max-width: 1450px;}
    [data-testid="stMetric"] {background: #111827; border: 1px solid #263449; padding: .65rem; border-radius: .6rem;}
    </style>""", unsafe_allow_html=True)


def render_header() -> None:
    st.title("Least time → refraction")
    st.markdown("**One crossing point. Two interpretations.** Find the fastest rescue route through two regions, then see the same condition become Snell's law.")


def render_metric_strip(parameters: RescueParameters) -> None:
    solution, _, _ = solve_rescue(parameters)
    n1, n2 = normalized_indices(parameters.v1, parameters.v2)
    columns = st.columns(5)
    columns[0].metric("Current time T(x)", f"{solution.current_time:.3f} s")
    columns[1].metric("Minimum time", f"{solution.minimum_time:.3f} s")
    columns[2].metric("Optimal x*", f"{solution.optimal_x:.3f}")
    columns[3].metric("Extra time ΔT", f"{solution.current_time - solution.minimum_time:.3f} s")
    columns[4].metric("Normalized n₂ / n₁", f"{n2/n1:.3f}")

