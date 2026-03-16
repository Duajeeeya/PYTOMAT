import random

with open("story.txt", "r", encoding="utf-8") as file:
    text = file.read()

words = text.split()

clean_words = []

for word in words:
    
    # keep only alphabet words
    if word.isalpha() and len(word) > 4:
        clean_words.append(word.lower())

quiz_words = random.sample(clean_words, 5)

print("Vocabulary Practice\n")

for word in quiz_words:
    meaning = input(f"What does '{word}' mean? ")
    print("Your answer:", meaning)
    print()