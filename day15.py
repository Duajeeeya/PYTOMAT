from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

def load_quiz():
    with open('data/quizzes.json') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    questions = load_quiz()
    q = random.choice(questions)
    return render_template('quiz.html', question=q)

@app.route('/submit', methods=['POST'])
def submit():
    answer = request.form['answer']
    correct = request.form['correct']
    
    score = 1 if answer == correct else 0
    
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)