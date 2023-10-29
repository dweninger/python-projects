import pygame
import random
from pygame.locals import *

pygame.font.init()
# Constants
ROWS = 7
COLS = 8
GEM_SIZE = 60
GEMS = ['A', 'B', 'C', 'D', 'E']
MARGIN = 50
SCREEN_WIDTH = COLS * GEM_SIZE
SCREEN_HEIGHT = ROWS * GEM_SIZE + MARGIN
MESSAGE_FONT = pygame.font.Font(None, 48)
MESSAGE_COLOR = (0, 0, 0)

# Colors
WHITE = (255, 255, 255)
GEM_COLORS = {
    'A': (255, 0, 0),   # Red
    'B': (0, 100, 0),   # Green
    'C': (0, 0, 255),   # Blue
    'D': (255, 140, 0),    # Orange
    'E': (139, 0, 139),   # Purple
    '-': (200, 200, 200),
    'A_flash': (255, 100, 100),  # Light Red
    'B_flash': (100, 255, 100),  # Light Green
    'C_flash': (100, 100, 255),  # Light Blue
    'D_flash': (255, 204, 102),  # Light Orange
    'E_flash': (255, 100, 255),  # Light Purple
}

score = 0
swaps = 20
rounds = 1
round_scores = [200, 300, 400, 500]
round_swaps = [5, 7, 10, 12]

# Create a label using Pygame
pygame.init()
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Match-3 Game")
font = pygame.font.Font(None, 36)
score_text = font.render(
    f"Score: {score}/{round_scores[rounds - 1]}", 
    True, (0, 0, 0))
swaps_text = font.render(
    f"Swaps: {swaps}", True, (0, 0, 0))
round_text = font.render(
    f"Round: {rounds}", True, (0, 0, 0))

game_won = False
game_lost = False

# Initialize the game board
def initialize_board():
    global score, swaps, rounds
    board = [
        [random.choice(GEMS) 
         for _ in range(COLS)] 
         for _ in range(ROWS)]
    while check_matches(board, True, None):
        board = [
            [random.choice(GEMS) 
             for _ in range(COLS)] 
             for _ in range(ROWS)]
    score = 0
    swaps = round_swaps[rounds - 1]
    return board

# Modify the gem rendering position
def draw_board(board, selected_gem):
    screen.fill(WHITE)  # Clear the screen
    for row in range(ROWS):
        for col in range(COLS):
            gem = board[row][col]
            gem_color = GEM_COLORS[gem]
            gem_rect = pygame.Rect(
                col * GEM_SIZE, 
                (row * GEM_SIZE) + MARGIN, 
                GEM_SIZE, GEM_SIZE)
            pygame.draw.circle(
                screen, gem_color, gem_rect.center, 
                GEM_SIZE // 2)

            if (selected_gem is not None and 
                (row, col) == selected_gem):
                pygame.draw.circle(
                    screen, (0, 0, 0), gem_rect.center, 
                    GEM_SIZE // 2, 3)

    # Update the score, swaps, and round text
    score_text = font.render(
        f"Score: {score}/{round_scores[rounds - 1]}", 
        True, (0, 0, 0))
    swaps_text = font.render(
        f"Swaps: {swaps}", True, (0, 0, 0))
    round_text = font.render(
        f"Round: {rounds}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(swaps_text, (200, 10))
    screen.blit(round_text, (340, 10))

# Swap two gems on the board
def swap(board, row1, col1, row2, col2):
    global swaps
    if swaps > 0:
        swaps -= 1
        board[row1][col1], board[row2][col2] = board[
            row2][col2], board[row1][col1]
    else:
        pass

def check_matches(board, game_start, selected_gem):
    global score, rounds, swaps, game_won, game_lost
    matches = False
    matching_gems = set() 

    for row in range(ROWS):
        for col in range(COLS):
            gem = board[row][col]
            if gem == ' ':
                continue

            # Check horizontally
            for c in range(col, COLS):
                if board[row][c] != gem:
                    break
                if c - col + 1 >= 3:
                    for i in range(col, c + 1):
                        matching_gems.add(
                            ((row, i),
                              GEM_COLORS[board
                                         [row][i]]))
                    matches = True

            # Check vertically
            for r in range(row, ROWS):
                if board[r][col] != gem:
                    break
                if r - row + 1 >= 3:
                    for i in range(row, r + 1):
                        matching_gems.add(
                            ((i, col), 
                             GEM_COLORS[board[i][col]]))
                    matches = True

    # Highlight matching gems
    for (r, c), color in matching_gems:
        if not game_start:
            score = score + 10
        color_names = [key for key, value in 
                       GEM_COLORS.items() if 
                       value == color]
        board[r][c] = f"{color_names[0]}_flash"

    draw_board(board, selected_gem)
    pygame.display.flip()
    if not game_start:
        pygame.time.wait(500)

    # Restore original colors
    for (r, c), color in matching_gems:
        board[r][c] = ' '

    # Check if player has reached required score for round
    if score >= round_scores[rounds - 1]:
        if rounds < len(round_scores):
            rounds += 1
            swaps = round_swaps[rounds - 1]
            score = 0
            initialize_board()
        else:
            # The player has completed all rounds
            game_won = True
        
    if swaps <= 0 and not game_won:
        # loss
        game_lost = True
    
    return matches

# Move gems down after matches are cleared
def apply_gravity(board):
    for col in range(COLS):
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                for above_row in range(row - 1, -1, -1):
                    if board[above_row][col] != ' ':
                        board[row][col], board[
                            above_row][col] = board[
                                above_row][col], board[
                                    row][col]
                        break

# Refill the top rows with new gems
def refill_top_rows(board):
    for col in range(COLS):
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = random.choice(GEMS)

def play_match3():
    global score, swaps, game_won, game_lost, rounds
    board = initialize_board()

    selected_gem = None  # Store the selected gem position
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                col = event.pos[0] // GEM_SIZE
                row = (event.pos[1] - MARGIN) // GEM_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if selected_gem is None:
                        selected_gem = (row, col)
                    else:
                        # Check if clicked gem is adjacent
                        if (
                            abs(row - selected_gem[0]) + 
                            abs(col - selected_gem[1]) 
                            == 1):
                            swap(board, row, col, 
                                 selected_gem[0], 
                                 selected_gem[1])
                            selected_gem = None
                        else:
                            selected_gem = None
                            selected_gem = (row, col)
            if event.type == KEYDOWN:
                if event.key == K_r:
                    if game_won or game_lost:
                        # Reset game state
                        game_won = False
                        game_lost = False
                        score = 0
                        rounds = 1
                        swaps = round_swaps[rounds - 1]
                        board = initialize_board()

        # Check matches and increment rounds
        if not game_won and not game_lost:
            if check_matches(board, False, selected_gem):
                apply_gravity(board)
                refill_top_rows(board)

        draw_board(board, selected_gem)
        
        if game_won:
            message = MESSAGE_FONT.render(
                "You Win!", True, MESSAGE_COLOR)
            screen.blit(
                message, (SCREEN_WIDTH // 2 - 100, 
                          SCREEN_HEIGHT // 2 - 50))
            press_r_message = MESSAGE_FONT.render(
                "Press R key to restart", True, 
                MESSAGE_COLOR)
            screen.blit(press_r_message, (
                SCREEN_WIDTH // 2 - 200, 
                SCREEN_HEIGHT // 2 + 50))

        if game_lost:
            message = MESSAGE_FONT.render(
                "Game Over!", True, MESSAGE_COLOR)
            screen.blit(message, 
                        (SCREEN_WIDTH // 2 - 100, 
                         SCREEN_HEIGHT // 2 - 50))
            press_r_message = MESSAGE_FONT.render(
                "Press R key to restart", True, 
                MESSAGE_COLOR)
            screen.blit(press_r_message, (
                SCREEN_WIDTH // 2 - 200, 
                SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    play_match3()
