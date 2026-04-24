from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "home works"

@app.route('/quiz')
def quiz():
    quiz_data = {
        "title": "Math Quiz",
        "question": "What is 8 + 4?",
        "options": [10, 11, 12, 13],
        "correct": 12
    }
    return render_template("quiz.html")

if __name__ == '__main__':
    app.run(debug=True)