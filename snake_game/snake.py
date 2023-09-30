import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
SNAKE_SIZE = 20
SPEED = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize Snake
snake = [(100, 50), (90, 50), (80, 50)]
snake_direction = "RIGHT"

# Initialize Food
food_position = (random.randrange(1, (WIDTH//SNAKE_SIZE)) * SNAKE_SIZE,
                 random.randrange(1, (HEIGHT//SNAKE_SIZE)) * SNAKE_SIZE)

# Score
score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
state = START

def reset_game():
    global snake, snake_direction, food_position, score, state
    snake = [(100, 50), (90, 50), (80, 50)]
    snake_direction = "RIGHT"
    food_position = (random.randrange(1, (WIDTH//SNAKE_SIZE)) * SNAKE_SIZE,
                     random.randrange(1, (HEIGHT//SNAKE_SIZE)) * SNAKE_SIZE)
    score = 0
    state = PLAYING

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif state == START and event.type == pygame.KEYDOWN:
            reset_game()
        elif state == PLAYING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            if event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            if event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"
        elif state == GAME_OVER and event.type == pygame.KEYDOWN:
            reset_game()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display game state messages
    if state == START:
        start_text = font.render("Press any key to start", True, WHITE)
        screen.blit(start_text, (WIDTH // 4, HEIGHT // 2))
    elif state == GAME_OVER:
        game_over_text = font.render("Game Over. Press any key to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 5, HEIGHT // 2))
    elif state == PLAYING:
        # Move the snake
        if snake_direction == "UP":
            new_head = (snake[0][0], snake[0][1] - SNAKE_SIZE)
        if snake_direction == "DOWN":
            new_head = (snake[0][0], snake[0][1] + SNAKE_SIZE)
        if snake_direction == "LEFT":
            new_head = (snake[0][0] - SNAKE_SIZE, snake[0][1])
        if snake_direction == "RIGHT":
            new_head = (snake[0][0] + SNAKE_SIZE, snake[0][1])

        snake.insert(0, new_head)

        # Check if the snake ate the food
        if abs(snake[0][0] - food_position[0]) < SNAKE_SIZE and abs(snake[0][1] - food_position[1]) < SNAKE_SIZE:
            score += 1
            food_position = (random.randrange(1, (WIDTH//SNAKE_SIZE)) * SNAKE_SIZE,
                             random.randrange(1, (HEIGHT//SNAKE_SIZE)) * SNAKE_SIZE)

        else:
            snake.pop()

        # Check for collisions with walls or itself
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT or
            snake[0] in snake[1:]):
            state = GAME_OVER

        # Draw the food
        pygame.draw.rect(screen, WHITE, pygame.Rect(food_position[0], food_position[1], SNAKE_SIZE, SNAKE_SIZE))

    # Update the display
    pygame.display.flip()

    # Control the game speed
    pygame.time.Clock().tick(SPEED)
