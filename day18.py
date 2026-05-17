from manim import *

class BoxMethod(Scene):
    def construct(self):

        title = Text("Box Method Multiplication", font_size=40)
        self.play(Write(title))
        self.wait(1)

        self.play(title.animate.to_edge(UP))

        equation = MathTex("123 \\times 45")
        equation.scale(1.3)
        self.play(equation.animate.to_edge(UP))

        self.play(Write(equation))
        self.wait(1)

        # Create table
        table = MathTable(
            [
                ["4000", "500"],
                ["800", "100"],
                ["120", "15"]
            ],
            row_labels=[
                MathTex("100"),
                MathTex("20"),
                MathTex("3")
            ],
            col_labels=[
                MathTex("40"),
                MathTex("5")
            ],
            include_outer_lines=True
        )

        table.scale(0.8)
        table.move_to(DOWN)

        self.play(Create(table))
        self.wait(2)

        #add all

        explain = Text("Add All The Values \n Inside The Blocks",font_size=10)
        explain.next_to(table, LEFT,0.2)     
        explain.scale(2.9) 
        self.play(Write(explain))
        self.wait(2)

        # Final answer
        answer = MathTex("5535")
        answer.scale(1.5)
        answer.set_color(YELLOW)

        answer.next_to(table, DOWN)

        self.play(Write(answer))
        self.wait(2)