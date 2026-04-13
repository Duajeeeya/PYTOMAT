import pygame
import random
import time

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Learning Game")

# Fonts
font = pygame.font.SysFont(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Game variables
score = 0
level = 1
time_limit = 10
start_time = time.time()

# Generate question
def new_question():
    num1 = random.randint(1, 10 * level)
    num2 = random.randint(1, 10 * level)
    return num1, num2, num1 + num2

num1, num2, correct_answer = new_question()
user_answer = ""

running = True

# 🎮 MAIN GAME LOOP
while running:

    screen.fill(WHITE)

    # 1. EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_answer != "":
                    if int(user_answer) == correct_answer:
                        score += 1
                        feedback = "Correct!"
                        color = GREEN
                    else:
                        feedback = "Wrong!"
                        color = RED

                    # Level up every 5 points
                    if score % 5 == 0:
                        level += 1

                    num1, num2, correct_answer = new_question()
                    user_answer = ""
                    start_time = time.time()

            elif event.key == pygame.K_BACKSPACE:
                user_answer = user_answer[:-1]

            else:
                if event.unicode.isdigit():
                    user_answer += event.unicode

    # 2. GAME LOGIC (Timer)
    elapsed_time = time.time() - start_time
    remaining_time = int(time_limit - elapsed_time)

    if remaining_time <= 0:
        feedback = "Time Up!"
        color = RED
        num1, num2, correct_answer = new_question()
        user_answer = ""
        start_time = time.time()

    # 3. DRAW EVERYTHING
    question_text = font.render(f"{num1} + {num2} = ?", True, BLACK)
    answer_text = font.render(user_answer, True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    timer_text = font.render(f"Time: {remaining_time}", True, BLACK)

    screen.blit(question_text, (200, 100))
    screen.blit(answer_text, (250, 150))
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))
    screen.blit(timer_text, (450, 20))

    # Feedback (if exists)
    if 'feedback' in locals():
        feedback_text = font.render(feedback, True, color)
        screen.blit(feedback_text, (230, 200))

    pygame.display.update()

pygame.quit()