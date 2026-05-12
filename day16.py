from manim import *

class RationalizeScene(Scene):
    def construct(self):
        # ── colour palette ──────────────────────────────────────────────
        C_GOLD   = "#F5B700"
        C_TEAL   = "#1DC9A4"
        C_CORAL  = "#E8572A"
        C_WHITE  = WHITE
        C_MUTED  = "#AAAAAA"

        # ── helpers ─────────────────────────────────────────────────────
        def frac(num_tex, den_tex, color=C_WHITE):
            num = MathTex(num_tex, color=color).scale(0.85)
            line = Line(LEFT * 0.6, RIGHT * 0.6, color=color, stroke_width=2)
            den = MathTex(den_tex, color=color).scale(0.85)
            line.next_to(num, DOWN, buff=0.15)
            den.next_to(line, DOWN, buff=0.15)
            return VGroup(num, line, den)

        def step_label(n, text, color=C_MUTED):
            return (
                Text(f"Step {n}  —  {text}", font_size=22, color=color)
                .to_edge(UP, buff=0.4)
            )

        # ═══════════════════════════════════════════════════════════════
        # TITLE
        # ═══════════════════════════════════════════════════════════════
        title = Text("Rationalising a Surd", font_size=48, color=C_GOLD,
                     weight=BOLD)
        subtitle = Text("Removing √ from the denominator", font_size=24,
                        color=C_MUTED)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ═══════════════════════════════════════════════════════════════
        # STEP 0  – show the problem
        # ═══════════════════════════════════════════════════════════════
        label0 = step_label(0, "The expression")
        expr0 = frac(r"1", r"1 + \sqrt{2}", color=C_WHITE)
        expr0.scale(1.5).move_to(ORIGIN)

        self.play(FadeIn(label0))
        self.play(Write(expr0), run_time=1.2)
        self.wait(1.5)

        # ═══════════════════════════════════════════════════════════════
        # STEP 1  – conjugate hint
        # ═══════════════════════════════════════════════════════════════
        label1 = step_label(1, "Multiply by the conjugate")

        conj_box = MathTex(r"1 - \sqrt{2}", color=C_TEAL).scale(1.3)
        conj_box.shift(DOWN * 2.2)
        conj_label = Text("conjugate", font_size=20, color=C_TEAL)
        conj_label.next_to(conj_box, DOWN, buff=0.2)
        arrow = Arrow(conj_box.get_top(), expr0[2].get_bottom() + DOWN * 0.1,
                      color=C_TEAL, stroke_width=2, max_tip_length_to_length_ratio=0.15)

        self.play(Transform(label0, label1))
        self.play(GrowArrow(arrow), Write(conj_box), FadeIn(conj_label))
        self.wait(2)
        self.play(FadeOut(conj_box), FadeOut(conj_label), FadeOut(arrow))

        # ═══════════════════════════════════════════════════════════════
        # STEP 2  – multiply top & bottom
        # ═══════════════════════════════════════════════════════════════
        label2 = step_label(2, "Write the multiplication out")

        expr2 = VGroup(
            frac(r"1 \cdot (1 - \sqrt{2})",
                 r"(1 + \sqrt{2})(1 - \sqrt{2})"),
        ).scale(1.2).move_to(ORIGIN)

        self.play(Transform(label0, label2))
        self.play(ReplacementTransform(expr0, expr2), run_time=1.2)
        self.wait(2)

        # ═══════════════════════════════════════════════════════════════
        # STEP 3  – difference of squares on denominator
        # ═══════════════════════════════════════════════════════════════
        label3 = step_label(3, "Difference of two squares: (a+b)(a−b) = a²−b²")

        dos_rule = MathTex(
            r"(1 + \sqrt{2})(1 - \sqrt{2})",
            r"= 1^2 - (\sqrt{2})^2",
            r"= 1 - 2",
            r"= -1",
            color=C_TEAL,
        ).scale(0.75).to_edge(DOWN, buff=0.6)

        self.play(Transform(label0, label3))
        self.play(Write(dos_rule), run_time=2)
        self.wait(2)

        expr3 = frac(r"1 - \sqrt{2}", r"-1").scale(1.5).move_to(ORIGIN)
        self.play(ReplacementTransform(expr2, expr3),
                  FadeOut(dos_rule), run_time=1.2)
        self.wait(1.5)

        # ═══════════════════════════════════════════════════════════════
        # STEP 4  – simplify sign
        # ═══════════════════════════════════════════════════════════════
        label4 = step_label(4, "Divide through by −1")

        expr4 = MathTex(r"\sqrt{2} - 1", color=C_CORAL).scale(2.4)
        expr4.move_to(ORIGIN)

        box = SurroundingRectangle(expr4, color=C_GOLD, buff=0.3, corner_radius=0.15,
                                   stroke_width=2.5)

        self.play(Transform(label0, label4))
        self.play(ReplacementTransform(expr3, expr4), run_time=1.2)
        self.play(Create(box))
        self.wait(0.5)

        tag = Text("Rationalised!", font_size=26, color=C_GOLD)
        tag.next_to(box, DOWN, buff=0.35)
        self.play(FadeIn(tag, shift=UP * 0.15))
        self.wait(2.5)

        # ═══════════════════════════════════════════════════════════════
        # SUMMARY  – side-by-side before / after
        # ═══════════════════════════════════════════════════════════════
        self.play(FadeOut(label0), FadeOut(box), FadeOut(tag),
                  FadeOut(expr4))

        before_title = Text("Before", font_size=22, color=C_MUTED).shift(LEFT * 3 + UP * 1.2)
        after_title  = Text("After",  font_size=22, color=C_MUTED).shift(RIGHT * 3 + UP * 1.2)

        before_expr = frac(r"1", r"1 + \sqrt{2}").scale(1.3).shift(LEFT * 3)
        after_expr  = MathTex(r"\sqrt{2} - 1", color=C_CORAL).scale(1.8).shift(RIGHT * 3)

        arrow_mid = Arrow(LEFT * 0.9, RIGHT * 0.9, color=C_GOLD, stroke_width=2.5,
                          max_tip_length_to_length_ratio=0.18)

        self.play(
            FadeIn(before_title), Write(before_expr),
            FadeIn(after_title),  Write(after_expr),
            GrowArrow(arrow_mid),
            run_time=1.5,
        )
        self.wait(3)