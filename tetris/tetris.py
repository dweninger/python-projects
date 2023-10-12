import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]
SHAPES_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
    (255, 128, 0),  # Orange
]

SCORE_FONT = pygame.font.Font(None, 36)
SCORE_COLOR = BLACK
score = 0

# Initialize screen
screen = pygame.display.set_mode((
    SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Initialize clock
clock = pygame.time.Clock()

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(
                screen, 
                BLACK, 
                (x * GRID_SIZE, 
                 y * GRID_SIZE, 
                 GRID_SIZE, 
                 GRID_SIZE), 1)

def draw_shape(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(
                    screen, 
                    color, 
                    (x + col * GRID_SIZE,
                      y + row * GRID_SIZE, 
                      GRID_SIZE, 
                      GRID_SIZE))

def check_collision(shape, x, y, grid):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if (x + col < 0 
                    or x + col >= GRID_WIDTH 
                    or y + row >= GRID_HEIGHT 
                    or grid[y + row][x + col]):
                    return True
    return False

def rotate_shape(shape):
    return [[shape[j][i] 
             for j in range(len(shape))] 
             for i in range(len(shape[0]) - 1, -1, -1)]

def clear_rows(grid, color_grid):
    full_rows = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            full_rows.append(row)

    for row in full_rows:
        grid.pop(row)
        grid.insert(0, [0] * GRID_WIDTH)
        color_grid.pop(row)
        color_grid.insert(0, [(0, 0, 0)] * GRID_WIDTH)

    return len(full_rows)  # Return number of cleared rows

def calculate_score(cleared_rows):
    if cleared_rows == 1:
        return 40
    elif cleared_rows == 2:
        return 100
    elif cleared_rows == 3:
        return 300
    elif cleared_rows == 4:
        return 1200
    else:
        return 0

def is_game_over(grid):
    # Check if top row of middle column is filled
    return any(
        grid[0][GRID_WIDTH // 2 - 1:GRID_WIDTH // 2 + 1])

def main():
    global score

    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    color_grid = [
        [(0, 0, 0)] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    shape = random.choice(SHAPES)
    shape_color = SHAPES_COLORS[SHAPES.index(shape)]
    x, y = GRID_WIDTH // 2 - len(shape[0]) // 2, 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(
                        shape, x - 1, y, grid):
                        x -= 1
                if event.key == pygame.K_RIGHT:
                    if not check_collision(
                        shape, x + 1, y, grid):
                        x += 1
                if event.key == pygame.K_DOWN:
                    if not check_collision(
                        shape, x, y + 1, grid):
                        y += 1
                if event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(shape)
                    if not check_collision(
                        rotated_shape, x, y, grid):
                        shape = rotated_shape

        if not check_collision(shape, x, y + 1, grid):
            y += 1
        else:
            for row in range(len(shape)):
                for col in range(len(shape[row])):
                    if shape[row][col]:
                        grid[y + row][x + col] = 1
                        color_grid[
                            y + row][
                                x + col] = shape_color
            cleared_rows = clear_rows(grid, color_grid)
            score += calculate_score(cleared_rows)
            shape = random.choice(SHAPES)
            shape_color = SHAPES_COLORS[
                SHAPES.index(shape)]
            x, y = GRID_WIDTH // 2 - len(shape[0]) // 2, 0

        screen.fill(WHITE)
        draw_grid()

        # Draw filled blocks on grid
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col]:
                    draw_shape(
                        [[1]], 
                        col * GRID_SIZE, 
                        row * GRID_SIZE, 
                        color_grid[row][col])

        draw_shape(
            shape, 
            x * GRID_SIZE, 
            y * GRID_SIZE, 
            shape_color)

        # Display score
        score_text = SCORE_FONT.render(
            f"Score: {score}", True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(4)

        if is_game_over(grid):
            game_over = True
            game_over_text = SCORE_FONT.render(
                "Game Over!", True, SCORE_COLOR)
            restart_text = SCORE_FONT.render(
                "Press R to Restart", True, SCORE_COLOR)
            game_over_text_rect = game_over_text.get_rect(
                center=(
                    SCREEN_WIDTH // 2, 
                    SCREEN_HEIGHT // 2 - 20))
            restart_text_rect = restart_text.get_rect(
                center=(
                    SCREEN_WIDTH // 2, 
                    SCREEN_HEIGHT // 2 + 20))
            screen.blit(
                game_over_text, 
                game_over_text_rect)
            screen.blit(
                restart_text, 
                restart_text_rect)
            pygame.display.update()

            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()

if __name__ == "__main__":
    main()
