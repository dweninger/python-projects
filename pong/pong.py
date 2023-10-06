import pygame
import random

# init Pygame
pygame.init()

WIDTH, HEIGHT = 600, 600
BALL_SPEED = 4
PADDLE_SPEED = 10
WHITE = (255, 255, 255)
BALL_RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
FPS = 60

# main window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# paddles and ball
player1_paddle = pygame.Rect(
    50, 
    HEIGHT // 2 - PADDLE_HEIGHT // 2, 
    PADDLE_WIDTH, 
    PADDLE_HEIGHT)
player2_paddle = pygame.Rect(
    WIDTH - 50 - PADDLE_WIDTH, 
    HEIGHT // 2 - PADDLE_HEIGHT // 2, 
    PADDLE_WIDTH,
    PADDLE_HEIGHT)
ball = pygame.Rect(
    WIDTH // 2 - BALL_RADIUS // 2, 
    HEIGHT // 2 - BALL_RADIUS // 2, 
    BALL_RADIUS, 
    BALL_RADIUS)

# init ball direction
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

# init scores
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 36)

# game state
game_started = False

# Start Game button
start_button = pygame.Rect(
    WIDTH // 2 - 100, 
    HEIGHT // 2 - 25, 
    200, 
    50)
start_button_color = (0, 255, 0)

# game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == (
            pygame.MOUSEBUTTONDOWN) and not game_started:
            if start_button.collidepoint(event.pos):
                game_started = True

    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            player1_paddle.y += PADDLE_SPEED

        if keys[pygame.K_UP]:
            player2_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            player2_paddle.y += PADDLE_SPEED

        if player1_paddle.top <= 0:
            player1_paddle.top = 0
        if player1_paddle.bottom >= HEIGHT:
            player1_paddle.bottom = HEIGHT

        if player2_paddle.top <= 0:
            player2_paddle.top = 0
        if player2_paddle.bottom >= HEIGHT:
            player2_paddle.bottom = HEIGHT

        # ball position
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # ball floor or ceiling collision
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # ball paddle collision
        if (
            ball.colliderect(player1_paddle)) or (
                ball.colliderect(player2_paddle)):
            ball_speed_x = -ball_speed_x

        # ball out of bounds
        if ball.left <= 0:
            player2_score += 1
            ball = pygame.Rect(
                WIDTH // 2 - BALL_RADIUS // 2, 
                HEIGHT // 2 - BALL_RADIUS // 2, 
                BALL_RADIUS,
                BALL_RADIUS)
            ball_speed_x = BALL_SPEED * random.choice((1, -1))
            ball_speed_y = BALL_SPEED * random.choice((1, -1))

        if ball.right >= WIDTH:
            player1_score += 1
            ball = pygame.Rect(
                WIDTH // 2 - BALL_RADIUS // 2, 
                HEIGHT // 2 - BALL_RADIUS // 2, 
                BALL_RADIUS, 
                BALL_RADIUS)
            ball_speed_x = BALL_SPEED * random.choice((1, -1))
            ball_speed_y = BALL_SPEED * random.choice((1, -1))

    screen.fill((0, 0, 0))

    # paddles and ball
    pygame.draw.rect(screen, WHITE, player1_paddle)
    pygame.draw.rect(screen, WHITE, player2_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # scores
    player1_text = font.render(f"Player 1: {player1_score}", 
                               True,
                                WHITE)
    player2_text = font.render(f"Player 2: {player2_score}", 
                               True,
                                WHITE)
    screen.blit(player1_text, (50, 50))
    screen.blit(player2_text, (WIDTH - 250, 50))

    # Start Game button
    if not game_started:
        pygame.draw.rect(screen, 
                         start_button_color, 
                         start_button)
        start_text = font.render("Start Game", 
                                 True, 
                                 (0, 0, 0))
        screen.blit(start_text, 
                    (WIDTH // 2 - 60, HEIGHT // 2 - 10))

    # update display
    pygame.display.flip()

    # frame rate
    clock.tick(FPS)

# quit
pygame.quit()
