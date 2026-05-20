from manim import *

class QuadraticGraph(Scene):
    def construct(self):

        title = Text("Graph Animation", font_size=40)

        self.play(Write(title))
        self.wait(1)

        self.play(title.animate.to_edge(UL))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": BLUE}
        )

        labels = axes.get_axis_labels(
            x_label="x",
            y_label="y"
        )

        self.play(Create(axes))
        self.play(Write(labels))

        graph = axes.plot(
            lambda x: 2*x**3,
            color=YELLOW
        )

        graph_label = MathTex("y = 2*x^3")
        graph_label.to_corner(UR)

        self.play(Create(graph))
        self.play(Write(graph_label))

        dot = Dot(
            axes.coords_to_point(2,4),
            color=RED
        )

        self.play(FadeIn(dot))

        self.wait(3)