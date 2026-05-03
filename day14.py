from flask import Flask, render_template, request, redirect
import json
import os
import random

app = Flask(__name__)

FILE = "scores.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


# 🎲 Generate random question (like a game)
def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        answer = num1 + num2
    elif op == "-":
        answer = num1 - num2
    else:
        answer = num1 * num2

    question = f"{num1} {op} {num2}"
    return question, answer


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz", methods=["POST"])
def quiz():
    name = request.form["name"]

    question, answer = generate_question()

    return render_template("quiz.html",
                           name=name,
                           question=question,
                           answer=answer)


@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    name = request.form["name"]
    user_answer = request.form["answer"]
    correct_answer = request.form["correct"]

    score = 1 if user_answer == str(correct_answer) else 0

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append({
        "name": name,
        "score": score
    })

    with open(FILE, "w") as f:
        json.dump(data, f)

    return redirect("/result")


@app.route("/result")
def result():
    with open(FILE, "r") as f:
        data = json.load(f)

    return render_template("result.html", scores=data)


if __name__ == "__main__":
    app.run(debug=True)