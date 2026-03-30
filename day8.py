import pygame      # Import pygame library for creating game window, graphics, and handling input
import random      # Import random to generate random math questions
import time        # Import time to handle the countdown timer
import os          # Import os to work with files (for saving high score)

pygame.init()      # Initialize all pygame modules (required before using pygame)

# ---------------- SCREEN SETUP ----------------
WIDTH, HEIGHT = 700, 500   # Define width and height of game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game window with given size
pygame.display.set_caption("Speed Math Challenge")  # Set title of the window

# ---------------- COLORS ----------------
WHITE = (255,255,255)   # White color (background)
BLACK = (0,0,0)         # Black color (text/borders)
GREEN = (0,200,0)       # Green color (user input text)
RED = (200,0,0)         # Red color (timer and alerts)

# ---------------- FONTS ----------------
font = pygame.font.Font(None, 50)        # Main font with size 50
small_font = pygame.font.Font(None, 35)  # Smaller font for score and info

# ---------------- SOUND EFFECTS ----------------
try:
    correct_sound = pygame.mixer.Sound("ding.wav")  
    # Load sound file for correct answer

    wrong_sound = pygame.mixer.Sound("buzz.wav")  
    # Load sound file for wrong answer

except:
    correct_sound = None  
    wrong_sound = None  
    # If sound files not found, set to None so game doesn't crash

# ---------------- GAME VARIABLES ----------------
input_text = ""   # Stores what user types (like "12")
score = 0         # Player score starts at 0
combo = 0         # Counts consecutive correct answers
time_limit = 30   # Total game time in seconds
start_time = time.time()  
# Store starting time to calculate countdown later

difficulty = "easy"  
# Change to "hard" if you want harder questions

# ---------------- LEADERBOARD FILE ----------------
HIGH_SCORE_FILE = "highscore.txt"  
# File name where high score will be stored

def load_high_score():
    # Function to load saved high score from file

    if os.path.exists(HIGH_SCORE_FILE):  
        # Check if file already exists

        with open(HIGH_SCORE_FILE, "r") as f:  
            # Open file in read mode

            return int(f.read())  
            # Read number from file and convert to integer

    return 0  
    # If file doesn't exist, return 0 as default high score

def save_high_score(new_score):
    # Function to save new high score

    with open(HIGH_SCORE_FILE, "w") as f:  
        # Open file in write mode (overwrite old value)

        f.write(str(new_score))  
        # Convert score to string and save in file

high_score = load_high_score()  
# Load high score at start of game

# ---------------- QUESTION GENERATOR ----------------
def generate_question():

    if difficulty == "easy":
        # Easy mode: smaller numbers, simple operations

        num1 = random.randint(1, 10)  
        num2 = random.randint(1, 10)  
        op = random.choice(["+", "-"])  

    else:
        # Hard mode: larger numbers + multiplication + division

        num1 = random.randint(1, 20)  
        num2 = random.randint(1, 20)  
        op = random.choice(["+", "-", "*", "/"])  

    if op == "/":
        num1 = num1 * num2  
        # Ensures division gives whole number (no decimals)

    question = f"{num1} {op} {num2}"  
    # Create question as string (example: "8 * 3")

    answer = int(eval(question))  
    # eval() solves the math expression
    # int() ensures answer is integer

    return question, answer  
    # Return both question and correct answer

# Generate first question
question, correct_answer = generate_question()

running = True   # Controls game loop (keeps game running)
feedback = ""    # Stores feedback message like "Correct!" or "Wrong!"

# ---------------- MAIN GAME LOOP ----------------
while running:

    screen.fill(WHITE)  
    # Clear screen every frame

    # -------- TIMER --------
    elapsed_time = int(time.time() - start_time)  
    # Calculate how many seconds have passed

    remaining_time = max(0, time_limit - elapsed_time)  
    # Prevent negative time

    if remaining_time == 0:
        running = False  
        # Stop game when time ends

    # -------- DRAW QUESTION --------
    screen.blit(font.render(f"Q: {question}", True, BLACK), (50, 50))  
    # Display current math question

    # -------- INPUT BOX --------
    pygame.draw.rect(screen, BLACK, (50,150,300,50), 2)  
    # Draw rectangle for input box

    screen.blit(font.render(input_text, True, GREEN), (60,160))  
    # Display user input text inside box

    # -------- SCORE + COMBO --------
    screen.blit(small_font.render(f"Score: {score}", True, BLACK), (50,230))  
    # Display score

    screen.blit(small_font.render(f"Combo: {combo}", True, BLACK), (50,270))  
    # Display combo count

    # -------- TIMER DISPLAY --------
    screen.blit(small_font.render(f"Time: {remaining_time}s", True, RED), (500,50))  
    # Display remaining time

    # -------- FEEDBACK --------
    screen.blit(small_font.render(feedback, True, BLACK), (50,320))  
    # Show feedback message

    # -------- EVENTS --------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False  
            # Close game window

        if event.type == pygame.KEYDOWN:
            # Detect key press

            if event.key == pygame.K_RETURN:
                # If Enter key is pressed

                try:
                    if int(input_text) == correct_answer:
                        score += 1  
                        # Increase score for correct answer

                        combo += 1  
                        # Increase combo streak

                        if combo == 3:
                            score += 5  
                            # Bonus points for 3 correct in a row

                            feedback = "🔥 Combo! +5 bonus!"  
                            combo = 0  
                            # Reset combo after bonus

                        else:
                            feedback = "Correct!"  

                        if correct_sound:
                            correct_sound.play()  
                            # Play correct sound

                    else:
                        score -= 1  
                        # Decrease score for wrong answer

                        combo = 0  
                        # Reset combo if wrong

                        feedback = "Wrong!"  

                        if wrong_sound:
                            wrong_sound.play()  
                            # Play wrong sound

                except:
                    feedback = "Invalid input!"  
                    # Handle case where input is not a number

                input_text = ""  
                # Clear input after submission

                question, correct_answer = generate_question()  
                # Generate new question

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  
                # Remove last character

            else:
                input_text += event.unicode  
                # Add typed character to input
                # event.unicode gives actual character (e.g., "5", "a")

    pygame.display.flip()  
    # Update screen with new frame

# ---------------- GAME OVER SCREEN ----------------
screen.fill(WHITE)  
# Clear screen

if score > high_score:
    save_high_score(score)  
    # Save new high score

    high_score = score  
    # Update high score variable

# -------- SMART FEEDBACK --------
if score < 5:
    message = "Keep going, you're learning!"  
elif score < 15:
    message = "Nice work, keep improving!"  
else:
    message = "You're a math machine!"  

# -------- DISPLAY FINAL SCREEN --------
screen.blit(font.render("Time's Up!", True, RED), (230,120))  
# Show game over message

screen.blit(font.render(f"Score: {score}", True, BLACK), (250,180))  
# Show final score

screen.blit(font.render(f"High Score: {high_score}", True, BLACK), (200,240))  
# Show high score

screen.blit(small_font.render(message, True, BLACK), (180,300))  
# Show motivational message

pygame.display.flip()  
# Update final screen

pygame.time.delay(5000)  
# Wait 5 seconds before closing

pygame.quit()  
# Properly close pygame