import pygame
import random

# --- (Recursive Backtracking) ---
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    def walk(x, y):
        maze[y][x] = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + (dx * 2), y + (dy * 2)
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                walk(nx, ny)
    walk(0, 0)
    maze[0][0] = 0
    maze[height-1][width-1] = 0
    return maze




class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.tile_size = 25  
        self.width = len(grid[0])
        self.height = len(grid)

    def draw(self, win):
        for row in range(self.height):
            for col in range(self.width):

                if self.grid[row][col] == 1:
                    color = (30, 30, 30) 
                else:
                    color = (220, 220, 220) 
                

                pygame.draw.rect(win, color, (
                    col * self.tile_size, 
                    row * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                ))


        pygame.draw.rect(win, (0, 0, 255), (0, 0, self.tile_size, self.tile_size))
        pygame.draw.rect(win, (0, 255, 0), (
            (self.width-1) * self.tile_size, 
            (self.height-1) * self.tile_size, 
            self.tile_size, 
            self.tile_size
        ))



def main():
    pygame.init()

    COLS, ROWS = 31, 31
    grid = generate_maze(COLS, ROWS)
    maze_display = Maze(grid)

    screen_width = COLS * maze_display.tile_size
    screen_height = ROWS * maze_display.tile_size
    win = pygame.display.set_mode((screen_width, screen_height))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    grid = generate_maze(COLS, ROWS)
                    maze_display.grid = grid

        win.fill((0, 0, 0))
        maze_display.draw(win) 
        pygame.display.update()

    pygame.quit()


main()    