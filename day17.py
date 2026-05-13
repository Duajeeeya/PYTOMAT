from manim import*

class GeometryLesson(Scene):
    def construct(self):
        circle = Circle(color=RED)
        square = Square(color=BLUE)
        self.play(Create(circle))
        self.wait(2)
        self.play(Transform(circle, square))
        self.wait(1)
        self.play(circle.animate.shift(RIGHT*3))
        self.wait(2)