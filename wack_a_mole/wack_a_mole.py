import pygame
import random
import sys

WIDTH, HEIGHT = 400, 450
GRID_SIZE = 3
MOLE_SIZE = WIDTH // GRID_SIZE
MARGIN = 50
FPS = 30
GAME_DURATION = 30 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRID_COLOR = (150, 150, 150) 

pygame.init()

# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

clock = pygame.time.Clock()

moles = []

class Mole:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.up = False
        self.timer = 0
        self.hit = False
        self.hit_timer = 0

score = 0
font = pygame.font.Font(None, 36)

# Mole images
mole_image = pygame.image.load(
    "./mole.png")
mole_image = pygame.transform.scale(
    mole_image, (MOLE_SIZE, 
                 int(MOLE_SIZE * (
                     mole_image.get_height() / 
                     mole_image.get_width()))))

mole_hit_image = pygame.image.load(
    "./mole_hit.png")
mole_hit_image = pygame.transform.scale(
    mole_hit_image, (MOLE_SIZE, MOLE_SIZE))

hit_sound = pygame.mixer.Sound(
    "./hit.wav")

def draw_grid():
    for mole in moles:
        x = mole.col * MOLE_SIZE
        y = mole.row * MOLE_SIZE + MARGIN
        pygame.draw.rect(screen, GRID_COLOR, 
                    (x, y, MOLE_SIZE, MOLE_SIZE), 1)
        if mole.up:
            screen.blit(mole_image, (x, y))
        if mole.hit:
            screen.blit(mole_hit_image, (x, y))

def draw_score():
    score_text = font.render(
        f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_timer(seconds):
    timer_text = font.render(
        f"Time: {seconds} s", True, BLACK)
    screen.blit(timer_text, (WIDTH - 120, 10))

def draw_start_screen():
    start_text = font.render(
        "Press 'r' to start", True, BLACK)
    screen.blit(start_text, 
                (WIDTH // 2 - 100, HEIGHT // 2 - 18))

def main():
    global score, moles
    game_over = True
    game_start_time = 0
    game_duration = GAME_DURATION * 1000
    remaining_time = 0

    start_screen = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if game_over:
                        score = 0
                        game_start_time = (pygame.
                                    time.get_ticks())
                        moles = ([Mole(row, col) 
                            for row in range(GRID_SIZE) 
                            for col in range(GRID_SIZE)])
                        game_over = False
                        start_screen = False
                        remaining_time = GAME_DURATION
            if (event.type == pygame.MOUSEBUTTONDOWN and 
                not game_over):
                x, y = event.pos
                for mole in moles:
                    mole_x = mole.col * MOLE_SIZE
                    mole_y = mole.row * MOLE_SIZE + MARGIN
                    if (mole.up and 
                        mole_x <= x < mole_x + MOLE_SIZE 
                        and mole_y <= y < mole_y + 
                                            MOLE_SIZE):
                        mole.up = False
                        score += 1
                        hit_sound.play()
                        mole.hit = True
                        mole.hit_timer = 15

        if not game_over:
            elapsed_time = (pygame.time.get_ticks() 
                            - game_start_time)
            remaining_time = max(
                0, (game_duration - elapsed_time) 
                // 1000)

            for mole in moles:
                if mole.up:
                    mole.timer += 1
                    if mole.timer >= FPS:
                        mole.up = False
                        mole.timer = 0
                elif mole.hit:
                    mole.hit_timer -= 1
                    if mole.hit_timer <= 0:
                        mole.hit = False
                elif random.random() < 0.005:
                    mole.up = True
                    mole.timer = 0

        screen.fill(BROWN)
        draw_grid()
        draw_score()
        draw_timer(remaining_time)

        if start_screen or game_over:
            draw_start_screen()
        else:
            pygame.display.set_caption("Whack-a-Mole")

        if remaining_time == 0:
            game_over = True

        clock.tick(FPS)
        pygame.display.flip()

if __name__ == "__main__":
    main()
