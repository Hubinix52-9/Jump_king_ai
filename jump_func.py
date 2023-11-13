import pygame
from platforma import Platforma
from player import Player
from map import Map


def check_collision(hero, list_of_objects):
    hero_rect = hero.get_player_rect()
    flag_if_collision = False
    for x in range(list_of_objects.getNumber()):
        obj_rect = list_of_objects.getObject(x).get_rect()
        cond1 = hero_rect.left >= obj_rect.left and hero_rect.left <= obj_rect.right
        cond2 = hero_rect.right >= obj_rect.left and hero_rect.right <= obj_rect.right
        cond3 = abs(obj_rect.left - hero_rect.right) > abs(obj_rect.top - hero_rect.bottom) #left side for top
        cond4 = abs(obj_rect.left - hero_rect.right) > abs(obj_rect.bottom - hero_rect.top) #left side for bottom
        cond5 = abs(obj_rect.right - hero_rect.left) > abs(obj_rect.top - hero_rect.bottom) #right side for top
        cond6 = abs(obj_rect.right - hero_rect.left) > abs(obj_rect.bottom - hero_rect.top) #right side for bottom
        cond7 = hero_rect.left <= obj_rect.right and hero_rect.right >= obj_rect.right #right wall
        cond8 = hero_rect.right >= obj_rect.left and hero_rect.left <= obj_rect.left #left wall

        if pygame.Rect.colliderect(hero_rect, obj_rect):
            # collision with left wall 
            if cond8:
                hero.set_player_velocity_x(-hero.get_player_velocity_x()/2)
            
            # collision with right wall 
            if cond7:
                hero.set_player_velocity_x(-hero.get_player_velocity_x()/2)

            # collision with upper wall      
            if hero_rect.top <= obj_rect.top and hero_rect.bottom <= obj_rect.bottom and cond3 and cond5:
                hero_rect.bottom = obj_rect.top
                hero.set_landed_flag(True)
                hero.set_player_velocity_x(0)

            # collision with bottom wall
            if hero_rect.bottom >= obj_rect.bottom and cond4 and cond6:
                hero.set_player_velocity_y(-hero.get_player_velocity_y()/2)
                hero.set_player_velocity_x(hero.get_player_velocity_x()/2)
                hero_rect.top = obj_rect.bottom 
                
        if hero_rect.bottom <= obj_rect.top and hero_rect.bottom >= obj_rect.top-45 and (cond1 or cond2):
            flag_if_collision = True
    if not flag_if_collision:
        hero.set_landed_flag(False)

#current map settings
current_map = 1


# initialize pygame
pygame.init()
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680
Map = Map()

# creating objects
down = Platforma(0, SCREEN_HEIGHT, SCREEN_WIDTH, 100)
p1 = Platforma(150, SCREEN_HEIGHT-150, 150, 25)
p2 = Platforma(300, SCREEN_HEIGHT-200, 150, 25)
p3 = Platforma(250, SCREEN_HEIGHT-450, 200, 25)
p4 = Platforma(0, SCREEN_HEIGHT-300, 250, 25)

# adding platforms to list
Map.add(down)
Map.add(p1)
Map.add(p2)
Map.add(p3)
Map.add(p4)


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
character = Player(SCREEN_WIDTH // 2, 100, character_image, SCREEN_WIDTH, SCREEN_HEIGHT, current_map)

# game loop
running = True 
while running:

    clock.tick(FPS)
    character.make_move()
    check_collision(character, Map)

    # map tracing
    if character.get_player_rect().top < 0:
        current_map += 1
        print(f"Przejście do mapy {current_map}")
        character.update_player_y(SCREEN_HEIGHT - character.get_player_height() * 2)  

        if current_map == 2:
            Map.clear()

            new_p1 = Platforma(100, SCREEN_HEIGHT-250, 150, 25)
            new_p2 = Platforma(0, SCREEN_HEIGHT-100, 150, 25)
            new_p3 = Platforma(250, SCREEN_HEIGHT-550, 200, 25)
            new_p4 = Platforma(300, SCREEN_HEIGHT-450, 250, 25)
            
            Map.add(new_p1)
            Map.add(new_p2)
            Map.add(new_p3)
            Map.add(new_p4)

            bg_image = pygame.image.load('assets/test.jpg').convert_alpha()
            bg_image_last = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        if current_map == 3:
            Map.clear()

            new_p1 = Platforma(250, SCREEN_HEIGHT-550, 100, 25)
            new_p2 = Platforma(100, SCREEN_HEIGHT-450, 75, 25)
            new_p3 = Platforma(500, SCREEN_HEIGHT-250, 150, 10)
            new_p4 = Platforma(50, SCREEN_HEIGHT-100, 150, 25)
            
            
            Map.add(new_p1)
            Map.add(new_p2)
            Map.add(new_p3)
            Map.add(new_p4)

            bg_image = pygame.image.load('assets/test2.jpg').convert_alpha()
            bg_image_last = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if character.get_player_rect().bottom > SCREEN_HEIGHT:
        # Zmiana na poprzednią mapę w dół
        if current_map > 1:
            current_map -= 1
            print(f"Przejście do poprzedniej mapy {current_map}")
            character.update_player_y(0)  # Umieść gracza na górze ekranu

            if current_map == 1:

                # Tworzenie nowej mapy
                # Map = Map()
                Map.clear()
                # creating objects
                down = Platforma(0, SCREEN_HEIGHT, SCREEN_WIDTH, 100)
                p1 = Platforma(150, SCREEN_HEIGHT-150, 150, 25)
                p2 = Platforma(300, SCREEN_HEIGHT-200, 150, 25)
                p3 = Platforma(250, SCREEN_HEIGHT-450, 200, 25)
                p4 = Platforma(0, SCREEN_HEIGHT-300, 250, 25)

                # adding platforms to list
                Map.add(down)
                Map.add(p1)
                Map.add(p2)
                Map.add(p3)
                Map.add(p4)

                bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()
                bg_image_last = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

            if current_map == 2:
                Map.clear()

                new_p1 = Platforma(100, SCREEN_HEIGHT-250, 150, 25)
                new_p2 = Platforma(0, SCREEN_HEIGHT-100, 150, 25)
                new_p3 = Platforma(250, SCREEN_HEIGHT-550, 200, 25)
                new_p4 = Platforma(300, SCREEN_HEIGHT-450, 250, 25)
                
                Map.add(new_p1)
                Map.add(new_p2)
                Map.add(new_p3)
                Map.add(new_p4)

                bg_image = pygame.image.load('assets/test.jpg').convert_alpha()
                bg_image_last = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # draw background
    window.blit(bg_image_last, (0, 0))

    # draw sprites
    character.draw(window)
    for x in range(Map.getNumber()):
        obj = Map.getObject(x)
        obj.draw(window)
    
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update display window
    pygame.display.update()

pygame.quit()
