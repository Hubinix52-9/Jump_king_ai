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
        cond1 = hero.rect.x >= obj_rect.x and hero_rect.x <= obj_rect.x + obj_width
        cond2 = hero.rect.x + hero_width >= obj_rect.x and hero_rect.x + hero_width <= obj_rect.x + obj_width

        if pygame.Rect.colliderect(hero_rect, obj_rect) and hero_rect.bottom >= obj_rect.top and hero_rect.top <= obj_rect.top:
            hero_rect.bottom = obj_rect.top
            hero.set_landed_flag(True)
            hero.set_player_wall_bumped(False)

        if hero_rect.top >= obj_rect.top and pygame.Rect.colliderect(hero_rect, obj_rect) and not hero.get_player_bumped():
            hero_rect.top = obj_rect.bottom+2
            print("bottom collision")
            hero.set_player_bumped(True)
            hero.set_player_velocity_y(1)
            hero.set_player_wall_bumped("bottom")

        if hero_rect.left >= obj_rect.right and pygame.Rect.colliderect(hero_rect, obj_rect):
            hero_rect.left = obj_rect.right
            hero.set_player_bumped(True)
            hero.set_player_wall_bumped("right")

        if hero_rect.right <= obj_rect.left and pygame.Rect.colliderect(hero_rect, obj_rect):
            hero_rect.right = obj_rect.left
            hero.set_player_bumped(True)
            hero.set_player_wall_bumped("left")
        
        if hero.rect.y <= obj_rect.y and hero.rect.y >= (obj_rect.y - 45) and (cond1 or cond2):
            flag_if_collision += 1
    if flag_if_collision == 0:
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
