import pygame

# initialize pygame
pygame.init()

# game widnow dimensions
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 360
JUMP_HEIGHT = 20

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# create game window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AI_test')

# load images
character_image = pygame.image.load('assets/ch.png').convert_alpha()
bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()

# game variables
GRAVITY = 1

# define colors
WHITE = (255, 255, 255)


# player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(character_image, (45, 45))
        self.width = 45
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        # reset variables
        dx = 0
        dy = 0

        # process keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -5
            self.flip = True
        if key[pygame.K_d]:
            dx = 5
            self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player dosen't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # check collision with ground
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            # self.vel_y = -20
        # Jump logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.jumping:
                self.y_velocity = -JUMP_HEIGHT
                self.jumping = True
        else:
            self.jumping = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))
        pygame.draw.rect(window, WHITE, self.rect, 2)


character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25)

# game loop
running = True
while running:

    clock.tick(FPS)

    character.move()

    # draw background
    window.blit(bg_image, (0, 0))

    # draw sprites
    character.draw()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.update()

pygame.quit()
