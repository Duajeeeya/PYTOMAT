from flask import Flask, render_template, request

app = Flask(__name__)

# Quiz questions (simple)
quiz = {
    "q1": {
        "question": "What is 2 + 2?",
        "answer": "4"
    },
    "q2": {
        "question": "What is 5 * 3?",
        "answer": "15"
    }
}

@app.route('/')
def home():
    return render_template('quiz.html', quiz=quiz)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0

    # Loop through questions and check answers
    for key in quiz:
        user_answer = request.form.get(key)
        correct_answer = quiz[key]["answer"]

        if user_answer == correct_answer:
            score += 1

    return render_template('result.html', score=score, total=len(quiz))

if __name__ == '__main__':
    app.run(debug=True)