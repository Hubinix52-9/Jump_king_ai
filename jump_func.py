import pygame
from platforma import Platforma

# initialize pygame
pygame.init()

# game window dimensions
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 360
JUMP_HEIGHT = 20
MIN_JUMP_HEIGHT = 10


# creating objects
p1 = Platforma(100,100,50,50)

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
            running = False

    # update display window
    pygame.display.update()

pygame.quit()
