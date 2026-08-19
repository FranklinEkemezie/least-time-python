# Least Time: Rescue to Refraction

An educational Streamlit + Plotly application showing how a rescue path through two regions with different speeds leads to the same mathematics as light refraction.

The live dashboard uses one mathematical model for the rescue diagram, the total-time curve, and the optical interpretation. A separate Manim scene provides a polished, linear explanation of the same idea.

## Setup with uv

Requires Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

```bash
uv venv
uv sync --dev --extra animation
```

Activate the environment if desired:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Run the dashboard:

```bash
uv run streamlit run app.py
```

For Streamlit Community Cloud, select `app.py` as the main file. The included `requirements.txt` contains the lightweight dashboard runtime dependencies; the full `pyproject.toml` remains available for local Manim/native development.

Run the native desktop application (Tkinter):

```bash
uv run python native_app.py
# or, after the editable install:
uv run least-time-native
```

The native app uses the same `least_time` mathematical backend, but draws the rescue diagram, time curve, and optical interpretation on native Tkinter canvases. The crossing slider is handled directly by the desktop event loop, so it updates continuously without Streamlit reruns or browser/server round trips.

Run the tests:

```bash
uv run pytest
```

Render the explanatory animation:

```bash
uv run --extra animation manim -pqh src/least_time/manim_scenes/least_time_scene.py LeastTimeScene
```

The Streamlit app looks for rendered video files under `media/`. Manim's output is intentionally ignored by Git; after rendering, the app's Manim Animation tab will embed the available MP4.

## Model

For saver `S=(x_s,y_s)`, savee `R=(x_r,y_r)`, and interface crossing `P=(x,0)`:

```text
T(x) = sqrt((x-xs)^2 + ys^2)/v1
     + sqrt((xr-x)^2 + yr^2)/v2
```

The bounded numerical minimum is checked against the derivative and displayed as the velocity form of Snell's law:

```text
sin(theta1)/v1 = sin(theta2)/v2
```

Using the normalized relationship `n ∝ 1/v` gives `n1 sin(theta1) = n2 sin(theta2)`.

## Project layout

`src/least_time/mathematics` contains pure numerical functions; `models` contains validated domain objects; `visualization` contains Plotly figures; `ui` contains Streamlit presentation helpers; and `manim_scenes` contains the independent Manim explanation.
