import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 360, 600
BIRD_WIDTH, BIRD_HEIGHT = 40, 40
PIPE_WIDTH = 75
PIPE_HEIGHT = 100 
PIPE_GAP = 130  
GRAVITY = 0.008
BIRD_JUMP = -1
BACKGROUND_COLOR = (135, 206, 235)
BIRD_COLOR = (255, 215, 0)
PIPE_COLOR = (0, 128, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load bird image
bird_image = pygame.image.load(
    "./flappy_bird/assets/images/bird1.png")

bird_image = pygame.transform.scale(
    bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Load background image
background_image = pygame.image.load(
    "./flappy_bird/assets/images/bg.png")

# Load pipe image
pipe_image = pygame.image.load(
    "./flappy_bird/assets/images/pipe.png")

pipe_image = pygame.transform.scale(
    pipe_image, (PIPE_WIDTH, HEIGHT))
flipped_pipe_image = pygame.transform.flip(
    pipe_image, False, True)

# Load sounds
hit_sound = pygame.mixer.Sound(
    "./flappy_bird/assets/sounds/hit.wav")
point_sound = pygame.mixer.Sound(
    "./flappy_bird/assets/sounds/point.wav")
flap_sound = pygame.mixer.Sound(
    "./flappy_bird/assets/sounds/swoosh.wav")

# Bird attributes
bird_x = WIDTH // 4
bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
bird_velocity = 0

# Pipe attributes
pipes = []
pipe_velocity = -1 
pipe_spawn_timer = time.time()

MAX_PIPES = 3

# Define fixed time step parameters
FPS = 60
fixed_time_step = 1 / FPS
accumulated_time = 0

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 48)

game_started = False
game_over = False
previous_time = time.time()

score = 0

def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

def draw_score():
    score_display = font.render(
        f"{score}", True, (255, 255, 255))
    score_rect = score_display.get_rect()
    score_rect.topleft = (
        WIDTH // 2 - score_rect.width // 2, 10)

    # Score outline
    outline_thickness = 2
    score_outline = font.render(
        f"{score}", True, (0, 0, 0))
    screen.blit(score_outline, (
        score_rect.left - outline_thickness, 
        score_rect.top))
    screen.blit(score_outline, (
        score_rect.left + outline_thickness, 
        score_rect.top))
    screen.blit(score_outline, (
        score_rect.left, score_rect.top - 
        outline_thickness))
    screen.blit(score_outline, (
        score_rect.left, score_rect.top + 
        outline_thickness))

    screen.blit(score_display, score_rect)

def start_screen():
    screen.blit(background_image, (0, 0))
    text = font.render(
        "Press space to start", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 6, HEIGHT // 3))
    bird_x = WIDTH // 4
    bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
    draw_bird(bird_x, bird_y)
    draw_score()
    pygame.display.update()

def reset_game():
    global bird_y, bird_velocity
    global pipes, score, game_started
    bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_started = True

# Game Start
start_screen()

bird_falling = False
bird_fall_timer = 0
ready_to_jump = False 

# Game loop
while True:
    current_time = time.time()
    elapsed_time = current_time - previous_time
    previous_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
        if (event.type == pygame.KEYDOWN and 
            event.key == pygame.K_SPACE):
            if not game_started:
                game_over = False
                game_started = True
                reset_game()
                ready_to_jump = True
                flap_sound.play()
        if (event.type == pygame.KEYDOWN and 
            event.key == pygame.K_SPACE and 
            ready_to_jump):
            bird_velocity = BIRD_JUMP

    if not game_started or game_over:
        continue

    # Update bird falling
    if ready_to_jump:
        bird_velocity += GRAVITY
        bird_y += bird_velocity

    # Check if the bird goes below the screen
    if bird_y > HEIGHT:
        hit_sound.play()
        game_over = True
        game_started = False

    # Spawn pipes
    if current_time - pipe_spawn_timer >= 2:
        if len(pipes) < MAX_PIPES:
            pipe_x = WIDTH
            gap = random.randint(
                100, HEIGHT - PIPE_GAP - 100)
            pipes.append((pipe_x, gap))
        pipe_spawn_timer = current_time

    # Update pipes
    for i, (pipe_x, gap) in enumerate(pipes):
        pipes[i] = (pipe_x + pipe_velocity, gap)
        # Score point
        if bird_x == pipe_x:
            point_sound.play()
            score += 1
        if pipe_x < -PIPE_WIDTH:
            pipes.pop(i)

        # Check for collision
        if (bird_x < pipe_x + PIPE_WIDTH and 
            bird_x + BIRD_WIDTH > pipe_x):
            if (bird_y < gap or 
                bird_y + BIRD_HEIGHT > gap + PIPE_GAP):
                hit_sound.play()
                game_over = True
                game_started = False
                ready_to_jump = False

    # Draw everything
    screen.blit(background_image, (0, 0))
    draw_bird(bird_x, bird_y)
    for pipe_x, gap in pipes:
        screen.blit(
            flipped_pipe_image, 
            (pipe_x, gap - pipe_image.get_height()))
        screen.blit(
            pipe_image,
            (pipe_x, gap + PIPE_GAP))

    draw_score()

    if game_over:
        start_screen()
        ready_to_jump = False

    pygame.display.update()
