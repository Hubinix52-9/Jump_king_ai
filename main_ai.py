import pygame
from platform_class import Platforma
from player_class_ai import Player
from map_class import Map
from ai_managment import Evolutionary_alghoritm
import random


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

# initialize pygame
pygame.init()
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# create game window  
window = pygame.display.set_mode((SCREEN_WIDTH+200, SCREEN_HEIGHT))
pygame.display.set_caption('AI_test')

# maps
Map1 = Map('assets/bg.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
Map2 = Map('assets/test.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
Map3 = Map('assets/test2.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
Map4 = Map('assets/bg.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)

Map_list = [Map1, Map2, Map3, Map4]

# map 1
m1_p1 = Platforma(0, SCREEN_HEIGHT, SCREEN_WIDTH, 100)
m1_p2 = Platforma(130, SCREEN_HEIGHT-150, 100, 25)
m1_p3 = Platforma(330, SCREEN_HEIGHT-200, 100, 25)
m1_p4 = Platforma(350, SCREEN_HEIGHT-400, 200, 25)
m1_p5 = Platforma(30, SCREEN_HEIGHT-300, 150, 25)
m1_p6 = Platforma(100, SCREEN_HEIGHT-500, 100, 25)
m1_p7 = Platforma(320, SCREEN_HEIGHT-600, 100, 25)

Map1.add(m1_p1)
Map1.add(m1_p2)
Map1.add(m1_p3)
Map1.add(m1_p4)
Map1.add(m1_p5)
Map1.add(m1_p6)
Map1.add(m1_p7)

# map 2
m2_p1 = Platforma(100, SCREEN_HEIGHT-250, 150, 25)
m2_p2 = Platforma(0, SCREEN_HEIGHT-100, 150, 25)
m2_p3 = Platforma(250, SCREEN_HEIGHT-550, 200, 25)
m2_p4 = Platforma(430, SCREEN_HEIGHT-340, 50, 25)
m2_p5 = Platforma(550, SCREEN_HEIGHT-450, 120, 25)

Map2.add(m2_p1)
Map2.add(m2_p2)
Map2.add(m2_p3)
Map2.add(m2_p4)
Map2.add(m2_p5)

# map 3
m3_p1 = Platforma(250, SCREEN_HEIGHT-550, 100, 25)
m3_p2 = Platforma(100, SCREEN_HEIGHT-450, 75, 25)
m3_p3 = Platforma(500, SCREEN_HEIGHT-250, 150, 25)
m3_p4 = Platforma(50, SCREEN_HEIGHT-200, 150, 25)
final = Platforma(100, SCREEN_HEIGHT-150, 25, 25)

Map3.add(m3_p1)
Map3.add(m3_p2)
Map3.add(m3_p3)
Map3.add(final) 

# map and image
Actual_map = Map1
current_map = 0
Background_image = Actual_map.get_bg()

#ai algh creation

ev_alg = Evolutionary_alghoritm(5)
ev_alg.create_population(Map1, 0)

# game loop
running = True
while running:
    clock.tick(FPS)
    list_with_characters = ev_alg.get_actual_gen()
    for x in list_with_characters:
        move_list = x.get_player_moves()
        move_to_make, how_long = move_list[x.get_player_did_moves()]
        space, right, left = move_to_make
        x.make_move(move_to_make, how_long)
        check_collision(x, x.get_player_current_map())
        if (x.get_player_landed() and space and not x.get_player_charging()) or (not x.get_player_steping() and (right or left) and not space):
            if len(move_list)-1 > x.get_player_did_moves():
                print(x.get_player_did_moves())
                x.set_player_did_moves(x.get_player_did_moves()+1)
        all_made_moves = ev_alg.all_made_moves()
        if all_made_moves:
            break
    
    

    if all_made_moves:
        ev_alg.fitness_n_selection()
    
    fitness_done = ev_alg.get_fitness_done()

    if fitness_done:
        ev_alg.crossover(Map1, 0)
    
    crossover_done = ev_alg.get_crossover_done()
    
    if crossover_done:
        ev_alg.mutation()

    mutation_done = ev_alg.get_mutation_done()

    if mutation_done:
        ev_alg.prep_for_next_gen()


    # map tracing
    for x in list_with_characters:
        higest_map = []    
      
        if x.get_player_rect().top < 0:
            x.set_player_current_map_id(x.get_player_current_map_id() + 1)  
            x.update_player_y(SCREEN_HEIGHT - x.get_player_height() * 2)

        if x.get_player_rect().bottom > SCREEN_HEIGHT:
            x.set_player_current_map_id(x.get_player_current_map_id() - 1)
            x.update_player_y(0)

        x.set_player_current_map(Map_list[x.get_player_current_map_id()])

        for x in list_with_characters:
            higest_map.append(x.get_player_current_map_id())
        current_map = max(higest_map)
        
        Actual_map = Map_list[current_map]
        Background_image = Actual_map.get_bg()

    # draw background
    window.blit(Background_image, (0, 0))

    # draw sprites
    for x in list_with_characters:
        if Map_list[current_map] == x.get_player_current_map():
            x.draw(window)

    for x in range(Actual_map.getNumber()):
        obj = Actual_map.getObject(x)
        obj.draw(window)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update display window
    pygame.display.update()

pygame.quit()
