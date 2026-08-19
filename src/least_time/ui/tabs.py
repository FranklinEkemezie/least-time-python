from __future__ import annotations

from pathlib import Path

import streamlit as st

from least_time.mathematics.optimization import solve_rescue
from least_time.mathematics.refraction import normalized_indices
from least_time.mathematics.travel_time import travel_time_derivative
from least_time.models.parameters import RescueParameters
from least_time.visualization.refraction_plot import refraction_figure
from least_time.visualization.rescue_plot import rescue_figure
from least_time.visualization.time_plot import time_figure


def _equations(parameters: RescueParameters, solution) -> None:
    n1, n2 = normalized_indices(parameters.v1, parameters.v2)
    st.latex(r"T(x)=\frac{\sqrt{(x-x_s)^2+y_s^2}}{v_1}+\frac{\sqrt{(x_r-x)^2+y_r^2}}{v_2}")
    st.latex(r"T'(x)=\frac{x-x_s}{v_1d_1}+\frac{x-x_r}{v_2d_2}=0")
    st.latex(r"\frac{\sin\theta_1}{v_1}=\frac{\sin\theta_2}{v_2}")
    st.latex(r"n=\frac{c}{v}\quad\Longrightarrow\quad n_1\sin\theta_1=n_2\sin\theta_2")
    st.caption(f"Normalized indices: n₁={n1:.3f}, n₂={n2:.3f}. The absolute value of c cancels; the ratio n₂/n₁=v₁/v₂ carries the analogy.")


def _animation_tab(media_root: Path) -> None:
    st.subheader("A guided explanation")
    videos = sorted(media_root.rglob("*.mp4")) if media_root.exists() else []
    if videos:
        st.video(str(videos[0]))
        st.caption(f"Rendered Manim scene: {videos[0].relative_to(media_root)}")
    else:
        st.info("No rendered animation is bundled yet. Render it with `uv run manim -pqh src/least_time/manim_scenes/least_time_scene.py LeastTimeScene`, then reload this tab.")
    st.markdown("The animation is deliberately pre-rendered: sliders stay responsive because live interaction is handled by Plotly and the same pure mathematical model.")


def render_tabs(parameters: RescueParameters, media_root: Path) -> None:
    solution, xs, times = solve_rescue(parameters)
    rescue_tab, refraction_tab, math_tab, parameters_tab, animation_tab = st.tabs(["Rescue", "Refraction", "Mathematics", "Parameters", "Manim animation"])
    with rescue_tab:
        st.subheader("Choose where to cross")
        st.plotly_chart(rescue_figure(parameters, solution), width="stretch", config={"displaylogo": False}, key="rescue-diagram")
        st.caption("Gold = your selected route · dashed white = fastest route · diamond = optimal crossing point. The shortest route and fastest route separate when speeds differ.")
        left, right = st.columns(2)
        with left:
            st.plotly_chart(time_figure(parameters, solution, xs, times), width="stretch", config={"displaylogo": False}, key="time-curve")
        with right:
            st.plotly_chart(refraction_figure(parameters, solution), width="stretch", config={"displaylogo": False}, key="rescue-refraction")
        st.info("The fastest path minimizes time, not distance. A slower region makes it worthwhile to change the crossing point.")
    with refraction_tab:
        st.subheader("The same path as a light ray")
        st.plotly_chart(refraction_figure(parameters, solution), width="stretch", config={"displaylogo": False}, key="refraction-focus")
        _equations(parameters, solution)
        st.markdown("Region 1 and Region 2 become optical media. The crossing point is where the ray meets the interface, and least travel time is Fermat's principle.")
    with math_tab:
        st.subheader("From a minimum to Snell's law")
        _equations(parameters, solution)
        st.write(f"At the computed minimum x* = {solution.optimal_x:.5f}, the derivative check gives T′(x*) = {solution.derivative_at_optimum:.3e}.")
        st.write("The two horizontal components have opposite signs at the optimum, so the derivative equation becomes equality of the two positive sine-over-speed terms.")
    with parameters_tab:
        st.subheader("Current source parameters")
        st.json({"saver": {"x": parameters.saver.x, "y": parameters.saver.y}, "savee": {"x": parameters.savee.x, "y": parameters.savee.y}, "v1": parameters.v1, "v2": parameters.v2, "crossing_x": parameters.crossing_x})
        n1, n2 = normalized_indices(parameters.v1, parameters.v2)
        st.markdown(f"**Distance comparison**  \nGeometrically shortest crossing: x = {solution.shortest_x:.3f}, distance = {solution.shortest_distance:.3f}  \nFastest crossing: x = {solution.optimal_x:.3f}, geometric distance = {solution.fastest_distance:.3f}")
        if abs(parameters.v1 - parameters.v2) < 1e-9:
            st.success("Equal-speed check: fastest and shortest-distance paths coincide.")
        else:
            st.warning("Different-speed check: fastest and shortest-distance paths generally differ.")
    with animation_tab:
        _animation_tab(media_root)
