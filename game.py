import pygame

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Smart Emotion AI 🧠")

font = pygame.font.SysFont("Segoe UI Emoji", 30)
big_font = pygame.font.SysFont("Segoe UI Emoji", 20)

clock = pygame.time.Clock()

input_text = ""
response = ""
bg_color = (20, 20, 20)

# ----------------- EMOTION KEYWORDS -----------------
happy_words = ["happy", "good", "great", "awesome", "excited", "love", "amazing"]
sad_words = ["sad", "bad", "cry", "depressed", "unhappy", "hate", "upset"]
tired_words = ["tired", "sleepy", "exhausted", "drained", "lazy"]

# ----------------- QUOTES -----------------
quotes = {
    "happy": "Keep shining ✨ You are doing great!",
    "sad": "It's okay to feel low ❤️ better days are coming",
    "tired": "Rest is important 💤 take care of yourself",
    "neutral": "You are doing fine 💪 keep going"
}

def detect_emotion(text):
    text = text.lower()

    happy_score = sum(word in text for word in happy_words)
    sad_score = sum(word in text for word in sad_words)
    tired_score = sum(word in text for word in tired_words)

    # decide emotion based on highest score
    if happy_score > sad_score and happy_score > tired_score:
        return "happy"
    elif sad_score > happy_score and sad_score > tired_score:
        return "sad"
    elif tired_score > 0:
        return "tired"
    else:
        return "neutral"


running = True
while running:
    screen.fill(bg_color)

    # title
    title = big_font.render("Smart Emotion AI 🧠", True, (255, 255, 255))
    screen.blit(title, (120, 20))

    # response
    if response:
        text = font.render(response, True, (255, 255, 255))
        screen.blit(text, (50, 150))

    # input box
    box = pygame.Rect(50, 300, 500, 50)
    pygame.draw.rect(screen, (255, 255, 255), box)

    input_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (60, 310))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                emotion = detect_emotion(input_text)

                response = quotes[emotion]

                # 🎨 change background based on emotion
                if emotion == "happy":
                    bg_color = (40, 180, 90)
                elif emotion == "sad":
                    bg_color = (60, 90, 200)
                elif emotion == "tired":
                    bg_color = (120, 120, 120)
                else:
                    bg_color = (20, 20, 20)

                input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            else:
                input_text += event.unicode

    pygame.display.update()
    clock.tick(60)

pygame.quit()