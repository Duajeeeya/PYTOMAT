import random

# ---------------- DECORATOR ----------------
def track(func):
    def wrapper(*args, **kwargs):
        print("\n--- Quiz Started ---")
        result = func(*args, **kwargs)
        print("--- Quiz Ended ---\n")
        return result
    return wrapper


# ---------------- CLASS (SCOPE) ----------------
class Quiz:
    def __init__(self):
        self.questions = []
        self.score = 0   # scope (instance variable)

    # ---------------- KWARGS ----------------
    def add_question(self, question, answer, **kwargs):
        self.questions.append({
            "q": question,
            "a": answer,
            "info": kwargs   # difficulty, category, etc.
        })

    # ---------------- LAMBDA ----------------
    def sort_questions(self):
        self.questions.sort(
            key=lambda x: x["info"].get("difficulty", "easy")
        )

    # ---------------- *ARGS + DECORATOR ----------------
    @track
    def ask_questions(self, *args):
        random.shuffle(self.questions)

        for q in self.questions:
            user = input(q["q"] + ": ")

            if user.lower() == q["a"].lower():
                print("Correct!\n")
                self.score += 1
            else:
                print("Wrong! Answer:", q["a"], "\n")

    # ---------------- SCOPE ----------------
    def show_score(self):
        print(f"Final Score: {self.score} / {len(self.questions)}")


# ---------------- MAIN PROGRAM ----------------
quiz = Quiz()

while True:
    print("1. Add Question")
    print("2. Start Quiz")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        q = input("Enter question: ")
        a = input("Enter answer: ")
        d = input("Enter difficulty (easy/medium/hard): ")

        quiz.add_question(q, a, difficulty=d)

    elif choice == "2":
        if len(quiz.questions) == 0:
            print("Add questions first!\n")
            continue

        quiz.sort_questions()
        quiz.ask_questions("all")   # *args used here
        quiz.show_score()

    elif choice == "3":
        break

    else:
        print("Invalid choice\n")