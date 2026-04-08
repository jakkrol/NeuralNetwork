import pygame

WIN_WIDTH = 1400
WIN_HEIGHT = 800

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.gravity = 0.5
        self.velocity = 0
        self.velocity_x = 0
        self.on_ground = False
        self.jump_strength = 0
        self.dir = 0

    def moveRight(self):
        self.rect.x += 5
    def moveLeft(self):
        self.rect.x -= 5
    def jump(self):
        self.velocity = self.jump_strength
    
    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.rect)
    def getRect(self):
        return self.rect



win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
player = Player(100, 300)
floor_rect = pygame.Rect(0, WIN_HEIGHT - 50, WIN_WIDTH, 50)
wall_rect = pygame.Rect(0, 0, 50, WIN_HEIGHT)

platforms = [
    pygame.Rect(0, WIN_HEIGHT - 50, WIN_WIDTH, 50), # Podłoga
    pygame.Rect(0, 0, 50, WIN_HEIGHT),              # Lewa ściana
    pygame.Rect(WIN_WIDTH - 50, 0, 50, WIN_HEIGHT), # Prawa ściana
    pygame.Rect(400, 600, 200, 20)                  # Przykładowa platforma
]

last_dir = 0
while True:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.on_ground:
                player.velocity = player.jump_strength
                player.velocity_x = player.dir * abs(player.jump_strength) * 0.5
                player.on_ground = False
                player.jump_strength = 0
                player.dir = 0


    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if player.on_ground:
            #player.on_ground = False
            if player.jump_strength > -15:
                player.jump_strength += -1

    last_dir = player.velocity_x
    if keys[pygame.K_RIGHT]:
        if player.on_ground and player.jump_strength == 0:
            player.moveRight()
        player.dir = 1
        last_dir = 1
    if keys[pygame.K_LEFT]:
        if player.on_ground and player.jump_strength == 0:
            player.moveLeft()
        player.dir = -1
        last_dir = -1

    player.velocity += player.gravity
    player.rect.x += player.velocity_x


    for plat in platforms:
        if player.rect.colliderect(plat):
            if player.velocity_x == 0:
                if last_dir > 0:
                    player.rect.right = plat.left
                elif last_dir < 0:
                    player.rect.left = plat.right
                

            if player.velocity_x > 0: # Moving right
                player.rect.right = plat.left
            elif player.velocity_x < 0: # Moving left
                player.rect.left = plat.right

            player.velocity_x *= -0.7

    player.rect.y += player.velocity
    for plat in platforms:
        if player.rect.colliderect(plat):
            if player.velocity > 0: # Falling down
                player.rect.bottom = plat.top
                player.velocity = 0
                player.velocity_x = 0
                player.on_ground = True
            elif player.velocity < 0: # Moving up
                player.rect.top = plat.bottom
                player.velocity = 0


    # if player.rect.colliderect(floor_rect):
    #     player.rect.bottom = floor_rect.top
    #     player.on_ground = True
    #     player.velocity = 0
    #     player.velocity_x = 0

    
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (0, 255, 0), floor_rect)
    pygame.draw.rect(win, (0, 255, 0), wall_rect)
    for plat in platforms:
        pygame.draw.rect(win, (0, 255, 0), plat)
    player.draw(win)
    pygame.display.update()