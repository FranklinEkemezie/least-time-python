from __future__ import annotations

from manim import *


class LeastTimeScene(Scene):
    """A compact, rendered explanation driven by the same equations as the app."""

    def construct(self) -> None:
        title = Text("Least time → refraction", font_size=38, color=BLUE_B).to_edge(UP)
        interface = Line(LEFT * 6, RIGHT * 6, color=WHITE)
        top = Rectangle(width=12, height=3.2, fill_color=BLUE_E, fill_opacity=0.22, stroke_opacity=0).shift(UP * 1.6)
        bottom = Rectangle(width=12, height=3.2, fill_color=TEAL_E, fill_opacity=0.2, stroke_opacity=0).shift(DOWN * 1.6)
        saver = Dot(LEFT * 3.4 + UP * 2.2, color=RED_C)
        savee = Dot(RIGHT * 3.8 + DOWN * 2.0, color=GREEN_C)
        s_label = Text("saver", font_size=22).next_to(saver, UP)
        r_label = Text("savee", font_size=22).next_to(savee, DOWN)
        crossing = Dot(ORIGIN, color=YELLOW)
        selected = VMobject().set_points_as_corners([saver.get_center(), crossing.get_center(), savee.get_center()]).set_color(YELLOW).set_stroke(width=5)
        normal = DashedLine(DOWN * 0.9, UP * 0.9, color=GRAY_B)
        equation = Text("T(x) = d₁ / v₁ + d₂ / v₂", font_size=34).to_edge(DOWN)
        self.play(Write(title), FadeIn(top), FadeIn(bottom), Create(interface))
        self.play(FadeIn(saver), FadeIn(savee), Write(s_label), Write(r_label), FadeIn(crossing), Create(selected))
        self.play(Write(equation), Create(normal))
        moving = Dot(LEFT * 1.7, color=ORANGE)
        route = VMobject().set_points_as_corners([saver.get_center(), moving.get_center(), savee.get_center()]).set_color(ORANGE)
        self.play(FadeIn(moving), Create(route), run_time=1)
        self.play(moving.animate.shift(RIGHT * 3.2), run_time=1.4)
        derivative = Text("T′(x*) = 0   →   sin θ₁ / v₁ = sin θ₂ / v₂", font_size=29).to_edge(DOWN)
        self.play(ReplacementTransform(equation, derivative), FadeOut(route), FadeOut(moving))
        snell = Text("n = c / v   →   n₁ sin θ₁ = n₂ sin θ₂", font_size=31, color=YELLOW).to_edge(DOWN)
        self.play(ReplacementTransform(derivative, snell), run_time=1.5)
        closing = Text("The fastest rescue path and a refracted ray obey the same principle.", font_size=24, color=YELLOW).to_edge(UP).shift(DOWN * 0.55)
        self.play(Write(closing), run_time=1.2)
        self.wait(2)
