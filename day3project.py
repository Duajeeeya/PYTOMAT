x = 2
y = 3
correct = 0

while x < 10:

    answer = int(input("What is " + str(x) + " * " + str(y) + "? "))

    if answer == x * y:
        print("Correct!")
        x += 1
        correct += 1
    else:
        print("Try again")

    if correct == 5:
        print("Level 1 Complete!")
    