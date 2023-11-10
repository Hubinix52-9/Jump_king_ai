import pygame
from platforma import Platforma
from player import Player
from list_of_platforms import List_of_objects


def check_collision(hero, list_of_objects):
    hero_rect = hero.get_player_rect()
    flag_if_collision = False
    for x in range(list_of_platforms.getNumber()):
        obj_rect = list_of_objects.getObject(x).get_rect()
        cond1 = hero_rect.left >= obj_rect.left and hero_rect.left <= obj_rect.right
        cond2 = hero_rect.right >= obj_rect.left and hero_rect.right <= obj_rect.right
        cond3 = abs(obj_rect.left - hero_rect.right) > abs(obj_rect.top - hero_rect.bottom)
        cond4 = abs(obj_rect.left - hero_rect.right) > abs(obj_rect.bottom - hero_rect.top)
        cond5 = abs(obj_rect.right - hero_rect.left) < abs(obj_rect.top - hero_rect.bottom)
        cond6 = abs(obj_rect.right - hero_rect.left) < abs(obj_rect.bottom - hero_rect.top)

        if pygame.Rect.colliderect(hero_rect, obj_rect):
            # collision with left wall 
            if hero_rect.right >= obj_rect.left and hero_rect.left <= obj_rect.left:
                hero_rect.right = obj_rect.left
                hero.set_player_velocity_x(-hero.get_player_velocity_x()/2)
                print("left")
            
            # collision with right wall 
            if hero_rect.left <= obj_rect.right and hero_rect.right >= obj_rect.right:
                hero_rect.left = obj_rect.right
                hero.set_player_velocity_x(-hero.get_player_velocity_x()/2)
                print("right")

            # collision with upper wall
            if hero_rect.top <= obj_rect.top and hero_rect.bottom <= obj_rect.bottom and (cond3 or cond5):
                hero_rect.bottom = obj_rect.top
                hero.set_landed_flag(True)
                hero.set_player_velocity_x(0)

            # collision with bottom wall
            if hero_rect.bottom >= obj_rect.bottom and (cond4 or cond6):   
                hero.set_player_velocity_y(-hero.get_player_velocity_y()/2)
                hero.set_player_velocity_x(hero.get_player_velocity_x()/2)
                hero_rect.top = obj_rect.bottom
                print("bottom")
                
        if hero_rect.bottom <= obj_rect.top and hero_rect.bottom >= obj_rect.top-45 and (cond1 or cond2):
            flag_if_collision = True
    if not flag_if_collision:
        hero.set_landed_flag(False)
    
# initialize pygame
pygame.init()
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680
list_of_platforms = List_of_objects()

# creating objects
down = Platforma(0, SCREEN_HEIGHT, SCREEN_WIDTH, 100)
#p1 = Platforma(150, SCREEN_HEIGHT-150, 150, 25)
p2 = Platforma(300, SCREEN_HEIGHT-200, 150, 25)
p3 = Platforma(250, SCREEN_HEIGHT-450, 200, 25)
p4 = Platforma(0, SCREEN_HEIGHT-300, 250, 25)

# adding platforms to list
list_of_platforms.add(down)
#list_of_platforms.add(p1)
list_of_platforms.add(p2)
list_of_platforms.add(p3)
list_of_platforms.add(p4)


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
