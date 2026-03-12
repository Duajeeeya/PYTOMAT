print("Mini Dictionary")
print("1 Search word")
print("2 Add new word")
print("3 Exit")

choice = input("Enter choice: ")

file = open("dictionary.txt", "r")

if choice == "1":
    word = input("Enter word: ")
    
    text = file.read()
    dictionary = {}
    for line in text.split("\n"):
        if ":" in line:
            w, m = line.split(":", 1)
            dictionary[w] = m

    if word in dictionary:
        print(dictionary[word])
    else:
        print("Word not found")

    file.close()

elif choice == "2":
    
    file.close()
    
    new_word = input("Enter new word: ")
    meaning = input("Enter meaning: ")

    file = open("dictionary.txt", "a")
    file.write("\n" + new_word + ":" + meaning)
    
    print("Word added successfully")

    file.close()

elif choice == "3":
    print("Program ended")
    file.close()

else:
    print("Invalid choice")
    file.close()