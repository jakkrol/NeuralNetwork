import pygame
import random
from network import Network

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


class Prisoner:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.fitness = 0
        self.steps = 0
        self.alive = True
        self.brain = Network()
    
    def move(self, choice):
        if choice == "UP": self.grid_y -= 1
        elif choice == "DOWN": self.grid_y += 1
        elif choice == "LEFT": self.grid_x -= 1
        elif choice == "RIGHT": self.grid_x += 1
        self.steps += 1

    def draw(self, window, size):
        color = (255, 0, 0, 100)
        pygame.draw.circle(window, color, (self.grid_x * size + size//2, self.grid_y * size + size//2), size//3)



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

def get_inputs(p: Prisoner, grid):
    x, y = p.grid_x, p.grid_y
    rows = len(grid)
    cols = len(grid[0])

    up    = grid[y-1][x] if y > 0 else 1
    down  = grid[y+1][x] if y < rows-1 else 1
    left  = grid[y][x-1] if x > 0 else 1
    right = grid[y][x+1] if x < cols-1 else 1



    dist_x = (cols - 1 - x) / cols
    dist_y = (rows - 1 - y) / rows

    return [up, down, left, right, dist_x, dist_y]



number_of_prisoners = 50
prisoners = [Prisoner(0,0) for _ in range(number_of_prisoners)]
prisoner = Prisoner(0,0)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    COLS, ROWS = 31, 31
    grid = generate_maze(COLS, ROWS)
    maze_display = Maze(grid)

    screen_width = COLS * maze_display.tile_size
    screen_height = ROWS * maze_display.tile_size
    win = pygame.display.set_mode((screen_width, screen_height))
    

    run = True
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    grid = generate_maze(COLS, ROWS)
                    maze_display.grid = grid

        ######DECISON#######
        for p in prisoners:
            if p.alive:
                inputs = get_inputs(p, grid)
                output = p.brain.predict(inputs)

                choice = output.index(max(output))
                directions = ["UP", "DOWN", "LEFT", "RIGHT"]
                p.move(directions[choice])
        ####################

        for p in prisoners:
            if p.alive:
                if p.steps > 200:
                    p.alive = False
                if p.grid_x < 0 or p.grid_x >= COLS or p.grid_y < 0 or p.grid_y >= ROWS:
                    p.alive = False
                    p.fitness -= 200 
                elif grid[p.grid_y][p.grid_x] == 1:
                    p.alive = False
                    p.fitness -= 100


        # 1. Czyścimy tło
        win.fill((0, 0, 0))
        
        # 2. Rysujemy labirynt
        maze_display.draw(win) 
        
        # 3. Rysujemy więźnia (na wierzchu labiryntu)
        for p in prisoners:
            if p.alive:
                p.draw(win, maze_display.tile_size)
        
        pygame.display.update()

    pygame.quit()


main()    