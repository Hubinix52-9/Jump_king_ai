import pygame
from platforma import Platforma
from player import Player
from list_of_platforms import List_of_objects


def check_collision(hero, list_of_objects):
    hero_rect = hero.get_player_rect()
    hero_width = hero.get_player_width()
    flag_if_collision = 0
    for x in range(list_of_platforms.getNumber()):
        obj = list_of_objects.getObject(x)
        obj_rect = obj.get_rect()
        obj_width = obj.get_width()
        obj_height = obj.get_height()
        cond1 = hero.rect.x >= obj_rect.x and hero_rect.x <= obj_rect.x + obj_width
        cond2 = hero.rect.x + hero_width >= obj_rect.x and hero_rect.x + hero_width <= obj_rect.x + obj_width

        if pygame.Rect.colliderect(hero_rect, obj_rect) and hero.rect.y <= (obj_rect.y + 5):
            if cond1 or cond2:
                hero.update_player_y(obj_rect.y - 45)
                hero.set_landed_flag(True)

        if hero.rect.y == (obj_rect.y + obj_height):
            if cond1 or cond2:
                hero.update_player_y(obj_rect.y  + obj_height + 10)
                hero.set_player_gravity(30)
                hero.set_landed_flag(False)
        
        if hero.rect.y <= obj_rect.y and hero.rect.y >= (obj_rect.y - 45) and (cond1 or cond2):
            flag_if_collision += 1
    if flag_if_collision == 0:
        hero.set_player_gravity(0.5)
        hero.set_landed_flag(False)
        

# initialize pygame
pygame.init()
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680
list_of_platforms = List_of_objects()

# creating objects
down = Platforma(5, SCREEN_HEIGHT-5, SCREEN_WIDTH-5, 100)
p1 = Platforma(100, SCREEN_HEIGHT-222, 150, 25)
p2 = Platforma(400, SCREEN_HEIGHT-300, 150, 25)

# adding platforms to list
list_of_platforms.add(down)
list_of_platforms.add(p1)
list_of_platforms.add(p2)


# set frame rate
clock = pygame.time.Clock()
FPS = 60

# create game window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AI_test')

# load images
character_image = pygame.image.load('assets/ch.png').convert_alpha()
bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()

bg_image_last = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# define colors
WHITE = (255, 255, 255)


# player class
character = Player(SCREEN_WIDTH // 2, 100, character_image, SCREEN_WIDTH, SCREEN_HEIGHT)

# game loop
running = True 
while running:

    clock.tick(FPS)
    character.make_move()
    check_collision(character, list_of_platforms)

    # draw background
    window.blit(bg_image_last, (0, 0))

    # draw sprites
    character.draw(window)
    for x in range(list_of_platforms.getNumber()):
        obj = list_of_platforms.getObject(x)
        obj.draw(window)
    
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update display window
    pygame.display.update()

pygame.quit()
