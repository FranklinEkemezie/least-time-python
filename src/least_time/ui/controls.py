from __future__ import annotations

import streamlit as st

from least_time.models.parameters import RescueParameters


def render_controls(defaults: RescueParameters) -> dict[str, float]:
    """Render controls and return only source parameters."""

    st.sidebar.header("Experiment controls")
    st.sidebar.caption("Move the crossing point and watch the path, time, and ray update together.")
    if "preset" not in st.session_state:
        st.session_state.preset = "Custom"
    preset = st.sidebar.selectbox("Speed preset", ["Custom", "Equal speeds", "Water slightly slower", "Water much slower", "Water much faster"], key="preset")
    presets = {"Equal speeds": (4.0, 4.0), "Water slightly slower": (4.0, 3.0), "Water much slower": (4.0, 1.4), "Water much faster": (2.0, 5.0)}
    if preset != "Custom":
        v1, v2 = presets[preset]
        st.sidebar.info(f"Preset: v₁={v1:g}, v₂={v2:g}")
    else:
        v1 = st.sidebar.slider("Region 1 speed · v₁", 0.2, 10.0, float(defaults.v1), 0.1, format="%.1f m/s")
        v2 = st.sidebar.slider("Region 2 speed · v₂", 0.2, 10.0, float(defaults.v2), 0.1, format="%.1f m/s")
    st.sidebar.subheader("Geometry")
    saver_x = st.sidebar.slider("Saver xₛ", -8.0, 8.0, float(defaults.saver.x), 0.1)
    saver_y = st.sidebar.slider("Saver height yₛ", 0.25, 8.0, float(defaults.saver.y), 0.1)
    savee_x = st.sidebar.slider("Savee xᵣ", -8.0, 8.0, float(defaults.savee.x), 0.1)
    savee_y = st.sidebar.slider("Savee height yᵣ", -8.0, -0.25, float(defaults.savee.y), 0.1)
    st.sidebar.subheader("Crossing")
    crossing_x = st.sidebar.slider("Crossing coordinate x", -10.0, 10.0, float(defaults.crossing_x), 0.05)
    st.sidebar.caption("The normal is perpendicular to the interface, so θ₁ and θ₂ are measured from vertical.")
    if st.sidebar.button("Reset geometry"):
        for key, value in {"preset": "Custom"}.items():
            st.session_state[key] = value
        st.rerun()
    return dict(saver_x=saver_x, saver_y=saver_y, savee_x=savee_x, savee_y=savee_y,
                v1=v1, v2=v2, crossing_x=crossing_x, x_min=-10.0, x_max=10.0)

