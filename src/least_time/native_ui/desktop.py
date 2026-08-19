from __future__ import annotations

import math
import tkinter as tk
from dataclasses import replace
from tkinter import messagebox, ttk

import numpy as np

from least_time.mathematics.optimization import solve_rescue
from least_time.mathematics.refraction import normalized_indices
from least_time.mathematics.travel_time import angles_from_crossing_point, travel_time
from least_time.models.geometry import Point
from least_time.models.parameters import DEFAULT_PARAMETERS, RescueParameters
from least_time.models.result import RescueSolution


BG = "#0b1220"
PANEL = "#111a2b"
PANEL_2 = "#162237"
TEXT = "#e5edf7"
MUTED = "#8fa5bf"
BOUNDARY = "#f8fafc"
GOLD = "#fbbf24"
FASTEST = "#f8fafc"
SAVER = "#fb7185"
SAVEE = "#34d399"
BLUE = "#60a5fa"
TEAL = "#2dd4bf"


class LeastTimeDesktop(tk.Tk):
    """Responsive native desktop view backed by the shared least-time model."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Least time → refraction")
        self.geometry("1440x920")
        self.minsize(1080, 720)
        self.configure(bg=BG)
        self._updating = False
        self.parameters = DEFAULT_PARAMETERS
        self.solution, self.xs, self.times = solve_rescue(self.parameters)
        self._make_styles()
        self._make_variables()
        self._build_layout()
        self._bind_redraws()
        self._update_metrics()
        self._redraw_all()

    def _make_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 23, "bold"))
        style.configure("Subtitle.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 11))
        style.configure("Section.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 12, "bold"))
        style.configure("Card.TFrame", background=PANEL_2)
        style.configure("CardLabel.TLabel", background=PANEL_2, foreground=MUTED, font=("Segoe UI", 8))
        style.configure("CardValue.TLabel", background=PANEL_2, foreground=TEXT, font=("Segoe UI", 12, "bold"))
        style.configure("TButton", background=PANEL_2, foreground=TEXT, padding=(8, 5))
        style.map("TButton", background=[("active", "#243653")])
        style.configure("TCombobox", fieldbackground=PANEL_2, background=PANEL_2, foreground=TEXT)

    def _make_variables(self) -> None:
        p = self.parameters
        self.saver_x = tk.DoubleVar(value=p.saver.x)
        self.saver_y = tk.DoubleVar(value=p.saver.y)
        self.savee_x = tk.DoubleVar(value=p.savee.x)
        self.savee_y = tk.DoubleVar(value=p.savee.y)
        self.v1 = tk.DoubleVar(value=p.v1)
        self.v2 = tk.DoubleVar(value=p.v2)
        self.crossing_x = tk.DoubleVar(value=p.crossing_x)
        self.preset = tk.StringVar(value="Custom")
        self.metric_current = tk.StringVar()
        self.metric_minimum = tk.StringVar()
        self.metric_optimal = tk.StringVar()
        self.metric_delta = tk.StringVar()
        self.metric_indices = tk.StringVar()
        self.status = tk.StringVar()

    def _build_layout(self) -> None:
        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True, padx=18, pady=15)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Least time → refraction", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="One crossing point. Two interpretations. Move the controls and watch the model respond locally.", style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)
        sidebar = ttk.Frame(body, style="Panel.TFrame", width=260)
        sidebar.pack(side="left", fill="y", padx=(0, 14))
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        content = ttk.Frame(body)
        content.pack(side="left", fill="both", expand=True)
        self._build_metrics(content)
        ttk.Label(content, text="Interactive rescue route", style="Section.TLabel").pack(anchor="w", pady=(14, 5))
        self.rescue_canvas = tk.Canvas(content, bg=PANEL, highlightthickness=0, height=460)
        self.rescue_canvas.pack(fill="both", expand=True)

        lower = ttk.Frame(content)
        lower.pack(fill="both", expand=True, pady=(12, 0))
        graph_frame = ttk.Frame(lower, style="Panel.TFrame")
        graph_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))
        ray_frame = ttk.Frame(lower, style="Panel.TFrame")
        ray_frame.pack(side="left", fill="both", expand=True, padx=(6, 0))
        ttk.Label(graph_frame, text="Total travel time T(x)", style="Section.TLabel").pack(anchor="w", padx=12, pady=(10, 0))
        ttk.Label(ray_frame, text="Optical interpretation", style="Section.TLabel").pack(anchor="w", padx=12, pady=(10, 0))
        self.graph_canvas = tk.Canvas(graph_frame, bg=PANEL, highlightthickness=0, height=265)
        self.graph_canvas.pack(fill="both", expand=True, padx=4, pady=4)
        self.ray_canvas = tk.Canvas(ray_frame, bg=PANEL, highlightthickness=0, height=265)
        self.ray_canvas.pack(fill="both", expand=True, padx=4, pady=4)
        ttk.Label(content, textvariable=self.status, style="Muted.TLabel").pack(anchor="w", pady=(7, 0))

    def _build_metrics(self, parent: ttk.Frame) -> None:
        metrics = ttk.Frame(parent)
        metrics.pack(fill="x")
        cards = [("Current T(x)", self.metric_current), ("Minimum time", self.metric_minimum), ("Optimal x*", self.metric_optimal), ("Extra time ΔT", self.metric_delta), ("n₂ / n₁", self.metric_indices)]
        for title, variable in cards:
            card = ttk.Frame(metrics, style="Card.TFrame")
            card.pack(side="left", fill="x", expand=True, padx=(0, 7))
            ttk.Label(card, text=title, style="CardLabel.TLabel").pack(anchor="w", padx=10, pady=(7, 0))
            ttk.Label(card, textvariable=variable, style="CardValue.TLabel").pack(anchor="w", padx=10, pady=(1, 7))

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Experiment controls", style="Section.TLabel").pack(anchor="w", padx=14, pady=(16, 3))
        ttk.Label(parent, text="Native controls update the canvases on every drag event.", style="Muted.TLabel", wraplength=225).pack(anchor="w", padx=14, pady=(0, 14))
        ttk.Label(parent, text="Speed preset", style="TLabel").pack(anchor="w", padx=14)
        preset = ttk.Combobox(parent, textvariable=self.preset, values=["Custom", "Equal speeds", "Water slightly slower", "Water much slower", "Water much faster"], state="readonly")
        preset.pack(fill="x", padx=14, pady=(4, 12))
        preset.bind("<<ComboboxSelected>>", self._preset_changed)

        self._add_scale(parent, "Region 1 speed · v₁", self.v1, 0.2, 10.0, "%.1f m/s")
        self._add_scale(parent, "Region 2 speed · v₂", self.v2, 0.2, 10.0, "%.1f m/s")
        ttk.Separator(parent).pack(fill="x", padx=14, pady=8)
        ttk.Label(parent, text="Geometry", style="TLabel").pack(anchor="w", padx=14, pady=(0, 2))
        self._add_scale(parent, "Saver xₛ", self.saver_x, -8.0, 8.0, "%.1f")
        self._add_scale(parent, "Saver height yₛ", self.saver_y, 0.25, 8.0, "%.1f")
        self._add_scale(parent, "Savee xᵣ", self.savee_x, -8.0, 8.0, "%.1f")
        self._add_scale(parent, "Savee height yᵣ", self.savee_y, -8.0, -0.25, "%.1f")
        ttk.Separator(parent).pack(fill="x", padx=14, pady=8)
        ttk.Label(parent, text="Crossing point", style="TLabel").pack(anchor="w", padx=14, pady=(0, 2))
        self.crossing_scale = self._add_scale(parent, "x", self.crossing_x, -10.0, 10.0, "%.2f", crossing=True)
        ttk.Label(parent, text="θ₁ and θ₂ are measured from the normal, not the interface.", style="Muted.TLabel", wraplength=225).pack(anchor="w", padx=14, pady=(4, 8))
        ttk.Button(parent, text="Reset example", command=self._reset).pack(fill="x", padx=14, pady=(2, 5))
        ttk.Label(parent, text="Backend: least_time.mathematics + models", style="Muted.TLabel", wraplength=225).pack(anchor="w", padx=14, pady=(8, 0))

    def _add_scale(self, parent: ttk.Frame, label: str, variable: tk.DoubleVar, minimum: float, maximum: float, fmt: str, crossing: bool = False) -> tk.Scale:
        row = ttk.Frame(parent, style="Panel.TFrame")
        row.pack(fill="x", padx=14, pady=(3, 0))
        value_label = ttk.Label(row, text=label, style="Muted.TLabel")
        value_label.pack(anchor="w")
        scale = tk.Scale(row, variable=variable, from_=minimum, to=maximum, resolution=0.05 if crossing else 0.1, orient="horizontal", showvalue=False, highlightthickness=0, bd=0, bg=PANEL, troughcolor="#2a3b59", activebackground=GOLD, fg=TEXT, command=self._crossing_changed if crossing else self._source_changed)
        scale.pack(fill="x")
        readout = ttk.Label(row, text=fmt % variable.get(), style="Muted.TLabel")
        readout.pack(anchor="e")
        variable.trace_add("write", lambda *_args, var=variable, target=readout, template=fmt: target.configure(text=template % var.get()))
        return scale

    def _bind_redraws(self) -> None:
        self.rescue_canvas.bind("<Configure>", lambda _event: self._draw_rescue())
        self.graph_canvas.bind("<Configure>", lambda _event: self._draw_graph())
        self.ray_canvas.bind("<Configure>", lambda _event: self._draw_ray())

    def _preset_changed(self, _event=None) -> None:
        values = {"Equal speeds": (4.0, 4.0), "Water slightly slower": (4.0, 3.0), "Water much slower": (4.0, 1.4), "Water much faster": (2.0, 5.0)}
        if self.preset.get() in values:
            v1, v2 = values[self.preset.get()]
            self.v1.set(v1)
            self.v2.set(v2)
            self._source_changed()

    def _reset(self) -> None:
        self.preset.set("Custom")
        for variable, value in [(self.saver_x, -4.0), (self.saver_y, 4.0), (self.savee_x, 5.0), (self.savee_y, -3.0), (self.v1, 4.0), (self.v2, 2.0), (self.crossing_x, 0.0)]:
            variable.set(value)
        self._source_changed()

    def _build_parameters(self) -> RescueParameters:
        return RescueParameters.from_values(saver_x=self.saver_x.get(), saver_y=self.saver_y.get(), savee_x=self.savee_x.get(), savee_y=self.savee_y.get(), v1=self.v1.get(), v2=self.v2.get(), crossing_x=self.crossing_x.get())

    def _source_changed(self, _value=None) -> None:
        if self._updating:
            return
        self._updating = True
        try:
            self.parameters = self._build_parameters()
            self.solution, self.xs, self.times = solve_rescue(self.parameters)
            theta1, theta2 = angles_from_crossing_point(self.parameters.crossing_x, self.parameters.saver, self.parameters.savee)
            self.solution = replace(self.solution, theta1=theta1, theta2=theta2)
            self._update_metrics()
            self._redraw_all()
        except ValueError as exc:
            self.status.set(str(exc))
        finally:
            self._updating = False

    def _crossing_changed(self, _value=None) -> None:
        if self._updating:
            return
        self._updating = True
        try:
            self.parameters = self._build_parameters()
            current = float(travel_time(self.parameters.crossing_x, self.parameters.saver, self.parameters.savee, self.parameters.v1, self.parameters.v2))
            theta1, theta2 = angles_from_crossing_point(self.parameters.crossing_x, self.parameters.saver, self.parameters.savee)
            self.solution = replace(self.solution, crossing=Point(self.parameters.crossing_x, 0.0), current_time=current, theta1=theta1, theta2=theta2)
            self._update_metrics()
            self._redraw_all()
        finally:
            self._updating = False

    def _update_metrics(self) -> None:
        n1, n2 = normalized_indices(self.parameters.v1, self.parameters.v2)
        self.metric_current.set(f"{self.solution.current_time:.3f} s")
        self.metric_minimum.set(f"{self.solution.minimum_time:.3f} s")
        self.metric_optimal.set(f"{self.solution.optimal_x:.3f}")
        self.metric_delta.set(f"{self.solution.current_time - self.solution.minimum_time:.3f} s")
        self.metric_indices.set(f"{n2 / n1:.3f}")
        self.status.set(f"x = {self.parameters.crossing_x:.2f}   ·   θ₁ = {math.degrees(self.solution.theta1):.1f}°   ·   θ₂ = {math.degrees(self.solution.theta2):.1f}°   ·   T′(x*) = {self.solution.derivative_at_optimum:.2e}")

    def _redraw_all(self) -> None:
        self._draw_rescue()
        self._draw_graph()
        self._draw_ray()

    @staticmethod
    def _plot_bounds(parameters: RescueParameters) -> tuple[float, float, float, float]:
        return parameters.x_min, parameters.x_max, min(-7.0, parameters.savee.y - 2), max(8.0, parameters.saver.y + 2)

    @staticmethod
    def _map_point(canvas: tk.Canvas, x: float, y: float, bounds: tuple[float, float, float, float], margin: float = 35.0) -> tuple[float, float]:
        width = max(canvas.winfo_width(), 10)
        height = max(canvas.winfo_height(), 10)
        xmin, xmax, ymin, ymax = bounds
        return margin + (x - xmin) / (xmax - xmin) * (width - 2 * margin), margin + (ymax - y) / (ymax - ymin) * (height - 2 * margin)

    def _draw_rescue(self) -> None:
        c = self.rescue_canvas
        c.delete("all")
        p, s = self.parameters, self.solution
        bounds = self._plot_bounds(p)
        _, _, ymin, ymax = bounds
        left, right = self._map_point(c, p.x_min, 0, bounds)[0], self._map_point(c, p.x_max, 0, bounds)[0]
        _, ytop = self._map_point(c, 0, ymax, bounds)
        _, yzero = self._map_point(c, 0, 0, bounds)
        _, ybottom = self._map_point(c, 0, ymin, bounds)
        c.create_rectangle(left, ytop, right, yzero, fill="#16324f", outline="")
        c.create_rectangle(left, yzero, right, ybottom, fill="#0d5c63", outline="")
        c.create_line(left, yzero, right, yzero, fill=BOUNDARY, width=3)
        c.create_text(left + 12, ytop + 14, text="REGION 1", anchor="nw", fill="#93c5fd", font=("Segoe UI", 10, "bold"))
        c.create_text(left + 12, ybottom - 14, text="REGION 2", anchor="sw", fill="#99f6e4", font=("Segoe UI", 10, "bold"))
        saver = self._map_point(c, p.saver.x, p.saver.y, bounds)
        savee = self._map_point(c, p.savee.x, p.savee.y, bounds)
        crossing = self._map_point(c, p.crossing_x, 0, bounds)
        optimum = self._map_point(c, s.optimal_x, 0, bounds)
        c.create_line(saver, crossing, fill=GOLD, width=4, arrow=tk.LAST)
        c.create_line(crossing, savee, fill=GOLD, width=4, arrow=tk.LAST)
        opt_a = self._map_point(c, p.saver.x, p.saver.y, bounds)
        opt_b = self._map_point(c, s.optimal_x, 0, bounds)
        c.create_line(opt_a, opt_b, fill=FASTEST, width=2, dash=(7, 5))
        c.create_line(optimum, savee, fill=FASTEST, width=2, dash=(7, 5))
        c.create_line(crossing[0], yzero - 45, crossing[0], yzero + 45, fill="#cbd5e1", width=1, dash=(3, 4))
        self._point(c, saver, SAVER, "S · saver", 14)
        self._point(c, savee, SAVEE, "R · savee", -14)
        self._point(c, crossing, GOLD, f"P  x={p.crossing_x:.2f}", -15)
        self._point(c, optimum, FASTEST, "x*", 16)
        c.create_text((saver[0] + crossing[0]) / 2, (saver[1] + crossing[1]) / 2 - 13, text=f"d₁={math.hypot(p.saver.x-p.crossing_x,p.saver.y):.2f}", fill="#fde68a", font=("Segoe UI", 9))
        c.create_text((savee[0] + crossing[0]) / 2, (savee[1] + crossing[1]) / 2 + 13, text=f"d₂={math.hypot(p.savee.x-p.crossing_x,p.savee.y):.2f}", fill="#fde68a", font=("Segoe UI", 9))
        c.create_text(crossing[0] + 35, crossing[1] - 30, text=f"θ₁ {math.degrees(s.theta1):.1f}°", fill=GOLD, anchor="w", font=("Segoe UI", 9))
        c.create_text(crossing[0] + 35, crossing[1] + 30, text=f"θ₂ {math.degrees(s.theta2):.1f}°", fill=GOLD, anchor="w", font=("Segoe UI", 9))
        c.create_text(right - 10, ytop + 14, text=f"v₁={p.v1:.1f} m/s", anchor="ne", fill=TEXT, font=("Segoe UI", 9))
        c.create_text(right - 10, ybottom - 14, text=f"v₂={p.v2:.1f} m/s", anchor="se", fill=TEXT, font=("Segoe UI", 9))

    @staticmethod
    def _point(canvas: tk.Canvas, point: tuple[float, float], color: str, label: str, offset: int) -> None:
        x, y = point
        canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill=color, outline=BOUNDARY, width=1)
        canvas.create_text(x, y + offset, text=label, fill=color, font=("Segoe UI", 9, "bold"))

    def _draw_graph(self) -> None:
        c = self.graph_canvas
        c.delete("all")
        width, height = max(c.winfo_width(), 10), max(c.winfo_height(), 10)
        margin = 42
        tmin, tmax = float(np.min(self.times)), float(np.max(self.times))
        tpad = max((tmax - tmin) * 0.12, 0.05)
        tmin -= tpad
        tmax += tpad
        def point(x: float, t: float) -> tuple[float, float]:
            return margin + (x - self.parameters.x_min) / (self.parameters.x_max - self.parameters.x_min) * (width - 2 * margin), margin + (tmax - t) / (tmax - tmin) * (height - 2 * margin)
        c.create_line(margin, height - margin, width - margin, height - margin, fill=MUTED)
        c.create_line(margin, margin, margin, height - margin, fill=MUTED)
        c.create_text(width / 2, height - 13, text="crossing coordinate x", fill=MUTED, font=("Segoe UI", 9))
        c.create_text(13, height / 2, text="T", fill=MUTED, angle=90, font=("Segoe UI", 9))
        coords = [point(float(x), float(t)) for x, t in zip(self.xs, self.times)]
        flat = [value for pair in coords for value in pair]
        c.create_line(*flat, fill=BLUE, width=2, smooth=True)
        opt = point(self.solution.optimal_x, self.solution.minimum_time)
        current = point(self.parameters.crossing_x, self.solution.current_time)
        c.create_oval(opt[0]-6, opt[1]-6, opt[0]+6, opt[1]+6, fill=SAVEE, outline="")
        c.create_text(opt[0], opt[1]-13, text="minimum", fill=SAVEE, font=("Segoe UI", 9))
        c.create_oval(current[0]-6, current[1]-6, current[0]+6, current[1]+6, fill=GOLD, outline="")
        c.create_text(current[0], current[1]+14, text="current", fill=GOLD, font=("Segoe UI", 9))
        c.create_text(margin - 5, height - margin + 14, text=f"{self.parameters.x_min:g}", anchor="e", fill=MUTED, font=("Segoe UI", 8))
        c.create_text(width - margin + 5, height - margin + 14, text=f"{self.parameters.x_max:g}", anchor="w", fill=MUTED, font=("Segoe UI", 8))

    def _draw_ray(self) -> None:
        c = self.ray_canvas
        c.delete("all")
        p, s = self.parameters, self.solution
        bounds = self._plot_bounds(p)
        _, _, ymin, ymax = bounds
        left = self._map_point(c, p.x_min, 0, bounds)[0]
        right = self._map_point(c, p.x_max, 0, bounds)[0]
        _, ytop = self._map_point(c, 0, ymax, bounds)
        _, yzero = self._map_point(c, 0, 0, bounds)
        _, ybottom = self._map_point(c, 0, ymin, bounds)
        c.create_rectangle(left, ytop, right, yzero, fill="#243b53", outline="")
        c.create_rectangle(left, yzero, right, ybottom, fill="#115e59", outline="")
        c.create_line(left, yzero, right, yzero, fill=BOUNDARY, width=3)
        start = self._map_point(c, p.saver.x, p.saver.y, bounds)
        cross = self._map_point(c, p.crossing_x, 0, bounds)
        end = self._map_point(c, p.savee.x, p.savee.y, bounds)
        c.create_line(start, cross, fill=GOLD, width=4, arrow=tk.LAST)
        c.create_line(cross, end, fill=GOLD, width=4, arrow=tk.LAST)
        c.create_line(cross[0], yzero - 42, cross[0], yzero + 42, fill="#cbd5e1", width=1, dash=(3, 4))
        c.create_text(left + 10, ytop + 15, text="MEDIUM 1 · n₁=1.00", anchor="nw", fill="#bfdbfe", font=("Segoe UI", 9, "bold"))
        c.create_text(left + 10, ybottom - 15, text=f"MEDIUM 2 · n₂={p.v1/p.v2:.2f}", anchor="sw", fill="#99f6e4", font=("Segoe UI", 9, "bold"))
        c.create_text(cross[0] + 35, cross[1] - 25, text=f"θ₁={math.degrees(s.theta1):.1f}°", anchor="w", fill=GOLD, font=("Segoe UI", 9))
        c.create_text(cross[0] + 35, cross[1] + 25, text=f"θ₂={math.degrees(s.theta2):.1f}°", anchor="w", fill=GOLD, font=("Segoe UI", 9))
        c.create_text((left + right) / 2, ybottom - 7, text="n₁ sin θ₁ = n₂ sin θ₂", fill=TEXT, font=("Segoe UI", 10, "bold"))


def main() -> None:
    app = LeastTimeDesktop()
    app.mainloop()
