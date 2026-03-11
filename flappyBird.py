import pygame
import random
from mutate import mutate_network
from network import Network
from neuron import Neuron
import copy

WIN_WIDTH = 800
WIN_HEIGHT = 600

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.5
        self.velocity = 0
        self.fitness = 0
        self.brain = Network()

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
        self.passed = False

    def move(self):
        self.x -= 5
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, 0, self.width, self.gapStart))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.gapStart + self.gap, self.width, self.height - self.gapStart - self.gap))
    def getRect(self):
        return (self.x, 0, self.width, self.gapStart), (self.x, self.gapStart + self.gap, self.width, self.height - self.gapStart - self.gap)


# win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# bird = Bird(100, 300)
# pipes = []
# while True:
#     pygame.time.Clock().tick(30)
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 bird.jump()



#     #NEURON DECISION
#     pipe_index = 0
#     if len(pipes) > 0:
#         if pipes[0].x + pipes[0].width < bird.x and len(pipes) > 1:
#             pipe_index = 1
        
#         target_pipe = pipes[pipe_index]

#         inputs = [
#             bird.y,
#             target_pipe.gapStart,
#             target_pipe.x
#         ]

#         output = bird.brain.predict(inputs)
#         if output > 0:
#             bird.jump()
#     ################
#     bird.move()

#     randomNum = random.randint(0, WIN_HEIGHT-150)
#     if len(pipes) == 0 or pipes[-1].x < WIN_WIDTH - 300:
#         pipes.append(Pipe(WIN_WIDTH, randomNum))

#     for pipe in pipes:
#         pipe.move()

#     win.fill((0,0,0))
#     bird.draw(win)
#     for pipe in pipes:
#         pipe.draw(win)

#     #check for collision
#     birdRect = pygame.Rect(bird.getRect())
#     for pipe in pipes:
#         pipeRects = top, bottom = pipe.getRect()
#         if birdRect.colliderect(pygame.Rect(top)) or birdRect.colliderect(pygame.Rect(bottom)) or bird.y > WIN_HEIGHT or bird.y < 0:
#             print("Game Over")
#             pygame.quit()
#             exit()

#     pipes = [p for p in pipes if p.x > -50]
#     pygame.display.update()


number_of_birds = 250
number_of_generations = 0

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
birds = [Bird(100, 300) for _ in range(number_of_birds)]
pipes = []
dead_birds = []

global_best_brain = None
global_best_fitness = 0

while True:
    pygame.time.Clock().tick(30)

    ############# NEURON DECISION ##################
    for bird in birds:
        pipe_index = 0
        if len(pipes) > 0:
            if pipes[0].x + pipes[0].width < bird.x and len(pipes) > 1:
                pipe_index = 1
            
            target_pipe = pipes[pipe_index]

            inputs = [
                (target_pipe.gapStart + (target_pipe.gap / 2) - bird.y) / WIN_HEIGHT, # Dystans pionowy do środka dziury
                (target_pipe.x - bird.x) / WIN_WIDTH, # Dystans poziomy do rury
                bird.velocity / 10 # Prędkość
            ]

            output = bird.brain.predict(inputs)
            if output > 0:
                bird.jump()
        bird.move()
        bird.fitness += 0.1
    ##############################################

    randomNum = random.randint(0, WIN_HEIGHT-150)
    if len(pipes) == 0 or pipes[-1].x < WIN_WIDTH - 300:
        pipes.append(Pipe(WIN_WIDTH, randomNum))

    for pipe in pipes:
        pipe.move()
        if not pipe.passed and pipe.x < 100: 
            pipe.passed = True
            for bird in birds:
                bird.fitness += 1

    win.fill((0,0,0))

    for bird in birds:
        bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    #check for collision
    # check for collision
    for bird in birds[:]:
        birdRect = pygame.Rect(bird.getRect())
        collision = False

        for pipe in pipes:
            top, bottom = pipe.getRect()
            if birdRect.colliderect(pygame.Rect(top)) or birdRect.colliderect(pygame.Rect(bottom)):
                collision = True
                break
        
        if birdRect.bottom >= WIN_HEIGHT or birdRect.top <= 0:
            collision = True

        if collision:
            # --- DODAJEMY KOMPAS DLA EWOLUCJI ---
            if len(pipes) > 0:
                # Szukamy rury, w którą ptak właśnie uderzył lub którą mijał
                # Najczęściej jest to pipes[0]
                target = pipes[0]
                gap_center = target.gapStart + (target.gap / 2)
                
                # Obliczamy dystans od środka dziury (0.0 - 1.0)
                # Im mniejszy dystans, tym większa nagroda
                dist = abs(bird.y - gap_center)
                fitness_bonus = (1 - (dist / WIN_HEIGHT)) * 2 
                bird.fitness += fitness_bonus
            
            dead_birds.append(bird)
            birds.remove(bird)

    if len(birds) == 0:
            dead_birds.sort(key=lambda b: b.fitness, reverse=True)
            current_best_bird = dead_birds[0]

            if current_best_bird.fitness > global_best_fitness:
                global_best_fitness = current_best_bird.fitness
                global_best_brain = copy.deepcopy(current_best_bird.brain)
            
            #5 najlepszych 
            top_birds = dead_birds[:5]
            best_bird = top_birds[0] 

            birds = []

            if global_best_brain:
                leader = Bird(100, 300)
                leader.brain = copy.deepcopy(global_best_brain)
                birds.append(leader)
            
            for parent in top_birds[:4]:
                leader = Bird(100, 300)
                leader.brain = copy.deepcopy(parent.brain)
                birds.append(leader)

            potential_parents = [copy.deepcopy(p.brain) for p in top_birds]
            if global_best_brain:
                potential_parents.append(copy.deepcopy(global_best_brain))
            for _ in range(number_of_birds - len(birds)):
                random_parent_brain = random.choice(potential_parents)
                new_bird = Bird(100, 300)
                new_bird.brain = mutate_network(random_parent_brain)
                birds.append(new_bird)
            
            dead_birds = []
            pipes = []
            number_of_generations += 1
            print(f"--- Generacja: {number_of_generations} ---")
            print(f"Najlepszy fitness: {best_bird.fitness:.2f}")
            continue
        # print("All birds died :(")
        # pygame.quit()
        # exit()

    pipes = [p for p in pipes if p.x > -50]
    pygame.display.update()