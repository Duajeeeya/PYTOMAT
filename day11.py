from flask import Flask

app = Flask(__name__)

## create routes in the browser... while searching for different pages dont forget to ##
@app.route('/')
def home():
    return "Welcome to my learning website!"

@app.route('/about')
def about():
    return "this is my return page"

@app.route('/lesson')
def lesson():
    return "this is my lesson quiz"

if __name__ == '__main__':
    app.run(debug=True)