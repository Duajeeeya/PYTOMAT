import random

print("Welcome to the Random Math Quiz!")

difficulty = input("Choose difficulty (easy / medium / hard): ")

score = 0

for i in range(10):

    if difficulty == "easy":
        a = random.randint(1,10)
        b = random.randint(1,10)

    elif difficulty == "medium":
        a = random.randint(5,10)
        b = random.randint(5,10)

    else:
        a = random.randint(5,15)
        b = random.randint(5,15)

    op = random.choice(["+","-","*"])

    if op == "+":
        answer = a + b
    elif op == "-":
        answer = a - b
    else:
        answer = a * b

    user = int(input(f"Question {i+1}: {a} {op} {b} = "))

    if user == answer:
        print("Correct!")
        score += 1
    else:
        print("Wrong! Correct answer:", answer)

print("\nGame Over")
print("Your Score:", score, "/10")

if score == 10:
    print("Perfect score! 🎉")
elif score >= 7:
    print("Great job! 👍")
else:
    print("Keep practicing! 💪")