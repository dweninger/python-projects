import pygame
import sys
import random

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
MAZE_WIDTH  = WIDTH // GRID_SIZE 
MAZE_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_WIDTH = 1
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)

def generate_maze(width, height):
    maze = [[
        'wall' for _ in range(width)] for _ in range(height)]

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height

    def carve(x, y):
        maze[y][x] = 'path'
        directions = [
            (2, 0), 
            (-2, 0), 
            (0, 2), 
            (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                if maze[ny][nx] == 'wall':
                    maze[ny][nx] = 'path'
                    maze[y + dy // 2][x + dx // 2] = 'path'
                    carve(nx, ny)

    for i in range(height):
        maze[i][0] = 'wall'
        maze[i][width - 1] = 'wall'
    for j in range(width):
        maze[0][j] = 'wall'
        maze[height - 1][j] = 'wall'

    # set top-left corner as 'start'
    maze[1][0] = 'start'  
    # start carving path from (2, 0)
    carve(2, 0)  

    # endpoint at bottom right
    maze[height - 2][width - 1] = 'end'

    return maze

def draw_maze(maze, screen):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 'wall':
                pygame.draw.rect(
                    screen, 
                    BLACK, 
                    (x * GRID_SIZE, 
                     y * GRID_SIZE, 
                     GRID_SIZE, 
                     GRID_SIZE), 
                     LINE_WIDTH)
            elif maze[y][x] == 'path':
                pygame.draw.rect(
                    screen, 
                    WHITE, 
                    (x * GRID_SIZE, 
                     y * GRID_SIZE, 
                     GRID_SIZE, 
                     GRID_SIZE))
    
    # green square for start
    start_x, start_y = 0, 0
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 'start':
                start_x, start_y = x, y
                break
    pygame.draw.rect(
        screen, 
        START_COLOR, 
        (start_x * GRID_SIZE, 
         start_y * GRID_SIZE, 
         GRID_SIZE, 
         GRID_SIZE))
    
    # red square for end
    end_x, end_y = 0, 0
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 'end':
                end_x, end_y = x, y
                break
    pygame.draw.rect(
        screen, 
        END_COLOR, 
        (end_x * GRID_SIZE,
          end_y * GRID_SIZE,
          GRID_SIZE, 
          GRID_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze Generator')

    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_maze(maze, screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
