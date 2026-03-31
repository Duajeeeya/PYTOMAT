"""
Day 9 – Catch the Answer!
=========================
A Pygame game where math questions appear at the top of the screen
and three answer bubbles fall down. Move the basket left/right with
the arrow keys to catch the CORRECT answer. Wrong catches or missing
the correct bubble costs a life. You have 3 lives total.

Controls:
  LEFT / RIGHT arrow keys  →  move basket
  R                        →  restart after game over
  ESC                      →  quit
"""

import pygame   # main game library – handles window, drawing, input, timing
import random   # used to shuffle questions, randomise positions and speeds
import sys      # used to exit the program cleanly


# ---------------------------------------------------------------------------
# 1. PYGAME INITIALISATION
#    Must be called before using any pygame feature.
# ---------------------------------------------------------------------------
pygame.init()

# Window size in pixels
WIDTH, HEIGHT = 700, 550

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 9 – Catch the Answer!")

# Clock controls how fast the game loop runs (frames per second)
clock = pygame.time.Clock()
FPS = 60   # target 60 frames every second → smooth animation


# ---------------------------------------------------------------------------
# 2. COLOUR PALETTE
#    All colours are RGB tuples (red, green, blue), each value 0–255.
# ---------------------------------------------------------------------------
BG          = (15,  17,  26)    # dark navy background
BASKET_COL  = (83, 186, 166)    # teal basket body
CORRECT_COL = (99, 195, 99)     # green – shown on correct objects after catch
WRONG_COL   = (220, 80,  70)    # red   – shown on wrong objects after catch
NEUTRAL_COL = (130, 140, 200)   # soft purple-blue – normal falling object colour
TEXT_COL    = (230, 230, 235)   # near-white for most text
DIM_COL     = (100, 105, 120)   # muted grey for HUD labels
FLASH_GREEN = (60,  210, 140)   # bright green flash when correct
FLASH_RED   = (230, 70,  70)    # bright red flash when wrong / missed


# ---------------------------------------------------------------------------
# 3. FONTS
#    SysFont looks up a system font by name; bold=True makes it heavier.
#    Three sizes: big for the question, medium for answer numbers, small for HUD.
# ---------------------------------------------------------------------------
font_big   = pygame.font.SysFont("Arial", 36, bold=True)   # question text
font_med   = pygame.font.SysFont("Arial", 26, bold=True)   # answer numbers
font_small = pygame.font.SysFont("Arial", 20)               # score / lives


# ---------------------------------------------------------------------------
# 4. QUESTION BANK
#    Each entry is a tuple:
#      (question_string,  correct_answer_int,  list_of_three_wrong_answers)
#    Two wrong answers are picked randomly each round for variety.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 4. RANDOM QUESTION SYSTEM (REPLACES FIXED QUESTION BANK)
# ---------------------------------------------------------------------------
OBJ_W, OBJ_H = 70, 42          # width and height of each falling answer bubble
def generate_question():
    """
    Creates a random math question every round.
    Replaces the fixed QUESTIONS list.
    """

    # Random numbers
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)

    # Random operation
    op = random.choice(["+", "-", "*", "/"])

    # ---------------- CREATE QUESTION ----------------
    if op == "+":
        question = f"{num1} + {num2}"
        correct = num1 + num2

    elif op == "-":
        question = f"{num1} - {num2}"
        correct = num1 - num2

    elif op == "*":
        question = f"{num1} × {num2}"
        correct = num1 * num2

    else:
        # clean division (no decimals)
        num1 = num1 * num2
        question = f"{num1} ÷ {num2}"
        correct = num1 // num2

    # ---------------- WRONG ANSWERS ----------------
    wrong1 = correct + random.randint(1, 5)
    wrong2 = correct - random.randint(1, 5)

    # avoid duplicate wrong answer
    if wrong2 == correct:
        wrong2 += 2

    # mix answers
    answers = [correct, wrong1, wrong2]
    random.shuffle(answers)

    # ---------------- POSITION OBJECTS ----------------
    xs = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
    random.shuffle(xs)

    objects = []

    for i, val in enumerate(answers):
        objects.append({
            "x": xs[i] - OBJ_W // 2,
            "y": -OBJ_H - i * 90,
            "speed": random.uniform(2.2, 3.5),
            "value": val,
            "correct": val == correct,
        })

    # return same format as before (IMPORTANT!)
    return question, correct, objects


# ---------------------------------------------------------------------------
# 5. BASKET & OBJECT SIZES
#    Defined once here so every function uses the same values.
# ---------------------------------------------------------------------------
BASKET_W, BASKET_H = 110, 22   # width and height of the basket rectangle
BASKET_SPEED = 7                # pixels the basket moves per frame when a key is held




# ---------------------------------------------------------------------------
# 6. NEW ROUND – build the state dictionary for one question
#
#    The entire game state lives in a single dictionary so resetting is easy:
#    just call new_round() and replace the old dict with the fresh one.
#
#    Parameters:
#      score – carry the current score forward into the new round
#      lives – carry the remaining lives forward
#
#    Returns a dict with keys:
#      question   – string shown at the top ("3 + 5 = ?")
#      correct    – the integer correct answer
#      objects    – list of falling-object dicts (see below)
#      score      – current score
#      lives      – remaining lives
#      basket_x   – left edge of basket in pixels (starts centred)
#      flash      – None, or (colour, frames_remaining) during the result flash
#      flash_msg  – string shown during the flash ("Correct! +10" etc.)
#      state      – "playing", "flash", or "gameover"
# ---------------------------------------------------------------------------
def new_round(score, lives):
    # Generate FULL question system (already includes objects)
    question, correct, objects = generate_question()

    return {
        "question":  question,
        "correct":   correct,
        "objects":   objects,
        "score":     score,
        "lives":     lives,
        "basket_x":  WIDTH // 2 - BASKET_W // 2,
        "flash":     None,
        "flash_msg": "",
        "state":     "playing",
    }

# ---------------------------------------------------------------------------
# 7. DRAWING HELPERS
# ---------------------------------------------------------------------------

def draw_basket(surf, bx, by):
    """
    Draw the player's basket at position (bx, by).
      bx = left edge x
      by = top edge y

    Made of three shapes:
      1. Filled rounded rectangle – the body
      2. Thin highlight strip along the top rim
      3. Two vertical lines for the side walls
    """
    # Main body
    body = pygame.Rect(bx, by, BASKET_W, BASKET_H)
    pygame.draw.rect(surf, BASKET_COL, body, border_radius=6)

    # Top rim highlight – slightly lighter colour, 5 px tall
    pygame.draw.rect(surf, (140, 220, 200), (bx, by, BASKET_W, 5), border_radius=3)

    # Side walls – a darker teal line on each edge for depth
    pygame.draw.line(surf, (60, 140, 120), (bx, by), (bx, by + BASKET_H), 3)
    pygame.draw.line(surf, (60, 140, 120), (bx + BASKET_W, by), (bx + BASKET_W, by + BASKET_H), 3)


def draw_object(surf, obj, highlight=None):
    """
    Draw a single falling answer bubble.

    surf      – the surface to draw on (main screen)
    obj       – object dict containing x, y, value
    highlight – optional colour override used during the flash phase
                to reveal correct (green) / wrong (red) bubbles
    """
    # Build a Rect from the object's current position
    # int(obj["y"]) converts the float y position to an integer pixel coordinate
    r = pygame.Rect(obj["x"], int(obj["y"]), OBJ_W, OBJ_H)

    # Choose fill colour
    col = NEUTRAL_COL if highlight is None else highlight

    # Filled rounded bubble
    pygame.draw.rect(surf, col, r, border_radius=10)

    # Thin light border so the bubble stands out from the dark background
    pygame.draw.rect(surf, (200, 205, 220), r, 2, border_radius=10)

    # Answer number centred inside the bubble
    txt = font_med.render(str(obj["value"]), True, TEXT_COL)
    surf.blit(txt, txt.get_rect(center=r.center))


# ---------------------------------------------------------------------------
# 8. MAIN GAME LOOP
#    Everything that happens each frame lives here:
#      a) Event handling  – quit / key presses
#      b) Update          – move objects, detect collisions, count lives
#      c) Draw            – render the scene to the screen
# ---------------------------------------------------------------------------
def main():
    # Initialise the first round with score=0 and lives=3
    state = new_round(0, 3)
    flash_timer = 0   # counts down frames during the result flash

    running = True
    while running:
        # Limit the loop to FPS frames per second.
        # tick() also returns elapsed milliseconds since the last call (not used here).
        clock.tick(FPS)

        # --------------------------------------------------------------------
        # 8a. EVENT HANDLING
        #     pygame.event.get() drains the event queue built up since last frame.
        # --------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User clicked the window's X button
                running = False

            if event.type == pygame.KEYDOWN:
                # R restarts the game after game over
                if event.key == pygame.K_r and state["state"] == "gameover":
                    state = new_round(0, 3)

                # ESC quits at any time
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --------------------------------------------------------------------
        # 8b. UPDATE – only runs during active gameplay
        # --------------------------------------------------------------------
        if state["state"] == "playing":

            # ----------------------------------------------------------------
            # PLAYER MOVEMENT
            #
            # pygame.key.get_pressed() returns a snapshot of ALL keys right now.
            # This is different from KEYDOWN (which fires only once on initial press).
            # get_pressed() fires every frame while the key is held → smooth movement.
            # ----------------------------------------------------------------
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                state["basket_x"] -= BASKET_SPEED   # move left: decrease x

            if keys[pygame.K_RIGHT]:
                state["basket_x"] += BASKET_SPEED   # move right: increase x

            # CLAMPING – keep the basket fully on screen
            #   max(0, ...)            → left wall: basket_x never goes below 0
            #   min(WIDTH - BASKET_W, ...) → right wall: right edge never past WIDTH
            state["basket_x"] = max(0, min(WIDTH - BASKET_W, state["basket_x"]))

            # Basket sits 60 px above the bottom of the window
            basket_by   = HEIGHT - 60
            basket_rect = pygame.Rect(state["basket_x"], basket_by, BASKET_W, BASKET_H)

            # ----------------------------------------------------------------
            # FALLING OBJECTS – move down and check for catches / misses
            # ----------------------------------------------------------------
            for obj in state["objects"]:
                # Move the object downward by its speed (pixels per frame)
                obj["y"] += obj["speed"]

                # Build the object's collision rect at its new position
                obj_rect = pygame.Rect(obj["x"], int(obj["y"]), OBJ_W, OBJ_H)

                # COLLISION DETECTION
                # colliderect() returns True when the two rectangles overlap.
                # This is the moment the basket "catches" a falling bubble.
                if obj_rect.colliderect(basket_rect):
                    if obj["correct"]:
                        # Correct answer caught – award 10 points
                        state["score"] += 10
                        state["flash"]     = (FLASH_GREEN, 40)
                        state["flash_msg"] = "+10  Correct!"
                    else:
                        # Wrong answer caught – lose a life
                        state["lives"] -= 1
                        state["flash"]     = (FLASH_RED, 40)
                        state["flash_msg"] = f"Wrong!  Answer was {state['correct']}"

                    # Freeze gameplay for 40 frames (~0.67 s) to show the result
                    state["state"] = "flash"
                    flash_timer    = 40
                    break   # stop checking other objects this frame

            # ----------------------------------------------------------------
            # MISSED CORRECT ANSWER
            # If the correct bubble fell below the screen without being caught,
            # deduct a life and flash red.
            # ----------------------------------------------------------------
            if state["state"] == "playing":
                # List comprehension: find correct objects whose y is below HEIGHT
                fallen_correct = [
                    o for o in state["objects"]
                    if o["correct"] and int(o["y"]) > HEIGHT
                ]
                if fallen_correct:
                    state["lives"] -= 1
                    state["flash"]     = (FLASH_RED, 40)
                    state["flash_msg"] = f"Missed!  Answer was {state['correct']}"
                    state["state"]     = "flash"
                    flash_timer        = 40

        # --------------------------------------------------------------------
        # 8c. FLASH STATE – brief pause to show the result, then advance
        # --------------------------------------------------------------------
        elif state["state"] == "flash":
            flash_timer -= 1           # tick down one frame

            if flash_timer <= 0:       # flash period over
                if state["lives"] <= 0:
                    # No lives remaining → game over screen
                    state["state"] = "gameover"
                else:
                    # Still alive → start a fresh round, carrying score and lives
                    state = new_round(state["score"], state["lives"])

        # --------------------------------------------------------------------
        # 8d. DRAW – render the entire scene every frame
        # --------------------------------------------------------------------

        # Fill the screen with the background colour (clears previous frame)
        screen.fill(BG)

        # STARFIELD – static background decoration.
        # Using a fixed seed (42) makes random produce the same coordinates
        # every frame, so the stars appear stationary.
        random.seed(42)
        for _ in range(60):
            sx    = random.randint(0, WIDTH)
            sy    = random.randint(0, HEIGHT - 100)   # keep stars above the ground
            r     = random.choice([1, 1, 1, 2])       # mostly 1 px, occasionally 2 px
            alpha = random.randint(80, 200)            # varying brightness
            pygame.draw.circle(screen, (alpha, alpha, alpha + 10), (sx, sy), r)
        random.seed()   # reset seed so game randomness is unaffected afterwards

        # ---- Draw the PLAYING and FLASH states (same scene, extra overlay for flash) ---
        if state["state"] in ("playing", "flash"):

            # Question banner centred at the top
            q_surf = font_big.render(state["question"] + " = ?", True, TEXT_COL)
            screen.blit(q_surf, q_surf.get_rect(centerx=WIDTH // 2, y=18))

            # HUD: score top-left
            score_txt = font_small.render(f"Score: {state['score']}", True, DIM_COL)
            screen.blit(score_txt, (14, 20))

            # HUD: lives as heart characters top-right
            # ♥ = filled heart (life remaining),  ♡ = empty heart (lost life)
            hearts    = "♥ " * state["lives"] + "♡ " * (3 - state["lives"])
            lives_txt = font_small.render(hearts, True, FLASH_RED)
            screen.blit(lives_txt, (WIDTH - lives_txt.get_width() - 14, 20))

            # Draw each falling answer bubble
            basket_by = HEIGHT - 60
            for obj in state["objects"]:
                if state["state"] == "flash":
                    # After a catch/miss: colour-code each bubble to reveal the answer
                    hi = CORRECT_COL if obj["correct"] else WRONG_COL
                    draw_object(screen, obj, highlight=hi)
                else:
                    # Normal falling state: neutral colour
                    draw_object(screen, obj)

            # Draw the player's basket
            draw_basket(screen, state["basket_x"], basket_by)

            # Ground line – a subtle horizontal separator near the bottom
            pygame.draw.line(screen, (60, 65, 80), (0, HEIGHT - 30), (WIDTH, HEIGHT - 30), 2)

            # FLASH OVERLAY – semi-transparent tint + centred result message
            if state["state"] == "flash" and state["flash"]:
                col, _ = state["flash"]

                # pygame.SRCALPHA lets us create a surface with an alpha channel
                # so we can draw a translucent colour wash over the whole scene
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((*col, 35))   # very low alpha (35/255) → gentle tint
                screen.blit(overlay, (0, 0))

                # Dark pill behind the message text for legibility
                msg = font_big.render(state["flash_msg"], True, col)
                pygame.draw.rect(
                    screen, (20, 22, 35),
                    msg.get_rect(centerx=WIDTH // 2, centery=HEIGHT // 2).inflate(24, 14),
                    border_radius=10
                )
                # Blit the message on top of the pill
                screen.blit(msg, msg.get_rect(centerx=WIDTH // 2, centery=HEIGHT // 2))

        # ---- GAME OVER screen -----------------------------------------------
        elif state["state"] == "gameover":
            go_txt = font_big.render("Game Over", True, FLASH_RED)
            sc_txt = font_med.render(f"Final score: {state['score']}", True, TEXT_COL)
            re_txt = font_small.render("Press  R  to restart  |  ESC to quit", True, DIM_COL)

            screen.blit(go_txt, go_txt.get_rect(centerx=WIDTH // 2, centery=HEIGHT // 2 - 50))
            screen.blit(sc_txt, sc_txt.get_rect(centerx=WIDTH // 2, centery=HEIGHT // 2 + 10))
            screen.blit(re_txt, re_txt.get_rect(centerx=WIDTH // 2, centery=HEIGHT // 2 + 56))

        # FLIP the display buffer.
        # Pygame uses double-buffering: you draw to an invisible back buffer,
        # then flip() swaps it to the screen all at once. This prevents flickering.
        pygame.display.flip()

    # Clean up pygame resources and exit when the loop ends
    pygame.quit()
    sys.exit()


# ---------------------------------------------------------------------------
# 9. ENTRY POINT
#    if __name__ == "__main__" ensures main() only runs when this file is
#    executed directly (e.g. python day9_catch_game.py), not when imported
#    as a module by another script.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()