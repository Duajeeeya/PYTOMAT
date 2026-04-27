from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def quiz():
    # dynamic quiz data
    question = "What is 5 + 3?"
    options = [6, 7, 8, 9]

    return render_template("day12_quiz.html", question=question, options=options)

if __name__ == "__main__":
    app.run(debug=True)