import pygame
import random

WIN_WIDTH = 800
WIN_HEIGHT = 600

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.5
        self.velocity = 0

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity
    def jump(self):
        self.velocity = -9
    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 30, 30))
    def getRect(self):
        return (self.x, self.y, 30, 30)

class Pipe:
    def __init__(self, x, gapStart):
        self.x = x
        self.height = WIN_HEIGHT
        self.width = 50
        self.gap = 150
        self.gapStart = gapStart

    def move(self):
        self.x -= 5
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, 0, self.width, self.gapStart))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.gapStart + self.gap, self.width, self.height - self.gapStart - self.gap))
    def getRect(self):
        return (self.x, 0, self.width, self.gapStart), (self.x, self.gapStart + self.gap, self.width, self.height - self.gapStart - self.gap)


win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bird = Bird(100, 300)
pipes = []
while True:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    bird.move()

    randomNum = random.randint(0, WIN_HEIGHT-150)
    if len(pipes) == 0 or pipes[-1].x < WIN_WIDTH - 300:
        pipes.append(Pipe(WIN_WIDTH, randomNum))

    for pipe in pipes:
        pipe.move()

    win.fill((0,0,0))
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    #check for collision
    birdRect = pygame.Rect(bird.getRect())
    for pipe in pipes:
        pipeRects = top, bottom = pipe.getRect()
        if birdRect.colliderect(pygame.Rect(top)) or birdRect.colliderect(pygame.Rect(bottom)) or bird.y > WIN_HEIGHT or bird.y < 0:
            print("Game Over")
            pygame.quit()
            exit()

    pipes = [p for p in pipes if p.x > -50]
    pygame.display.update()
