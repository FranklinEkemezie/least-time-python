"""Streamlit entry point for the least-time/refraction demonstration."""

from pathlib import Path

import streamlit as st

from least_time.models.parameters import DEFAULT_PARAMETERS, RescueParameters
from least_time.ui.controls import render_controls
from least_time.ui.layout import configure_page, render_header, render_metric_strip
from least_time.ui.tabs import render_tabs


@st.cache_data(show_spinner=False)
def _validated_parameters(
    saver_x: float,
    saver_y: float,
    savee_x: float,
    savee_y: float,
    v1: float,
    v2: float,
    crossing_x: float,
    x_min: float,
    x_max: float,
) -> RescueParameters:
    return RescueParameters.from_values(
        saver_x=saver_x,
        saver_y=saver_y,
        savee_x=savee_x,
        savee_y=savee_y,
        v1=v1,
        v2=v2,
        crossing_x=crossing_x,
        x_min=x_min,
        x_max=x_max,
    )


def main() -> None:
    configure_page()
    render_header()
    values = render_controls(DEFAULT_PARAMETERS)
    try:
        parameters = _validated_parameters(**values)
    except ValueError as exc:
        st.error(f"Please check the parameters: {exc}")
        return

    render_metric_strip(parameters)
    render_tabs(parameters, media_root=Path(__file__).parent / "media")


if __name__ == "__main__":
    main()

