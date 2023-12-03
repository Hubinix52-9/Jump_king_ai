import pygame
from platform_class import Platforma
from player_class_ai import Player
from map_class import Map
from ai_managment import Evolutionary_alghoritm
import time

def check_collision(hero, list_of_objects):
    hero_rect = hero.rect
    flag_if_collision = False
    for x in range(len(list_of_objects.list)):
        obj_rect = list_of_objects.getObject(x).rect
        cond = hero_rect.right > obj_rect.left and hero_rect.left < obj_rect.right
        
        if pygame.Rect.colliderect(hero_rect, obj_rect):
            cond3 = abs(obj_rect.left - hero_rect.right) > abs(obj_rect.top - hero_rect.bottom) #left side for top
            cond4 = abs(obj_rect.left - hero_rect.right) > abs(obj_rect.bottom - hero_rect.top) #left side for bottom
            cond5 = abs(obj_rect.right - hero_rect.left) > abs(obj_rect.top - hero_rect.bottom) #right side for top
            cond6 = abs(obj_rect.right - hero_rect.left) > abs(obj_rect.bottom - hero_rect.top) #right side for bottom
            cond7 = hero_rect.left <= obj_rect.right and hero_rect.right >= obj_rect.right #right wall
            cond8 = hero_rect.right >= obj_rect.left and hero_rect.left <= obj_rect.left #left wall

            # collision with left and right wall 
            if cond8 or cond7:
                hero.vel_x = -hero.vel_x/2

            # collision with upper wall      
            if hero_rect.top <= obj_rect.top and hero_rect.bottom <= obj_rect.bottom and cond3 and cond5:
                hero_rect.bottom = obj_rect.top
                hero.landed = True
                hero.vel_x = 0

            # collision with bottom wall
            if hero_rect.bottom >= obj_rect.bottom and cond4 and cond6:
                hero.vel_y = -hero.vel_y/2
                hero.vel_x = hero.vel_x/2
                hero_rect.top = obj_rect.bottom 
                
        if hero_rect.bottom <= obj_rect.top and hero_rect.bottom >= obj_rect.top-45 and cond:
            flag_if_collision = True
    if not flag_if_collision:
        hero.landed = False

# initialize pygame
pygame.init()
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680

# set frame rate
clock = pygame.time.Clock()
FPS = 50

# create game window  
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+100))
pygame.display.set_caption('AI Solving Platform Game')

# maps defining
Map1 = Map('assets/block.png', SCREEN_WIDTH, SCREEN_HEIGHT)
Map2 = Map('assets/block3.png', SCREEN_WIDTH, SCREEN_HEIGHT)
Map3 = Map('assets/block5.png', SCREEN_WIDTH, SCREEN_HEIGHT)
Map4 = Map('assets/block7.png', SCREEN_WIDTH, SCREEN_HEIGHT)

Map_list = [Map1, Map2, Map3, Map4]

# map 1
m1_p1 = Platforma(0, SCREEN_HEIGHT, SCREEN_WIDTH, 100)
m1_p2 = Platforma(130, SCREEN_HEIGHT-150, 100, 25)
m1_p3 = Platforma(330, SCREEN_HEIGHT-180, 100, 25)
m1_p4 = Platforma(350, SCREEN_HEIGHT-380, 200, 25)
m1_p5 = Platforma(30, SCREEN_HEIGHT-300, 150, 25)
m1_p6 = Platforma(0, SCREEN_HEIGHT-480, 200, 25)
m1_p7 = Platforma(340, SCREEN_HEIGHT-580, 150, 25)


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
m2_p4 = Platforma(380, SCREEN_HEIGHT-340, 120, 25)
m2_p5 = Platforma(550, SCREEN_HEIGHT-450, 120, 25)


Map2.add(m2_p1)
Map2.add(m2_p2)
Map2.add(m2_p3)
Map2.add(m2_p4)
Map2.add(m2_p5)

# map 3
m3_p1 = Platforma(0, SCREEN_HEIGHT-100, 200, 25)
m3_p2 = Platforma(450, SCREEN_HEIGHT-250, 200, 25)
m3_p3 = Platforma(50, SCREEN_HEIGHT-350, 200, 25)
m3_p4 = Platforma(320, SCREEN_HEIGHT-490, 130, 25)
m3_p5 = Platforma(320, SCREEN_HEIGHT-490, 130, 25)

Map3.add(m3_p1)
Map3.add(m3_p2)
Map3.add(m3_p3)
Map3.add(m3_p4)
Map3.add(m3_p5)

# map 4

m4_p1 = Platforma(550, SCREEN_HEIGHT-5, 100, 25)
m4_p2 = Platforma(400, SCREEN_HEIGHT-150, 50, 25)
m4_p3 = Platforma(150, SCREEN_HEIGHT-200, 150, 25)
m4_p4 = Platforma(20, SCREEN_HEIGHT-250, 50, 25)
m4_p5 = Platforma(200, SCREEN_HEIGHT-350, 100, 25)
m4_p6 = Platforma(450, SCREEN_HEIGHT-450, 140, 25)
m4_p7 = Platforma(220, SCREEN_HEIGHT-550, 130, 25)
final = Platforma(270, SCREEN_HEIGHT-555, 40, 25)


Map4.add(m4_p1)
Map4.add(m4_p2)
Map4.add(m4_p3)
Map4.add(m4_p4)
Map4.add(m4_p5)
Map4.add(m4_p6)
Map4.add(m4_p7) 

# ui
font = pygame.font.Font(None, 35)

# map and image
Actual_map = Map1
current_map = 0
Background_image = Actual_map.get_bg()

# ai alghoritm creation
ev_alg = Evolutionary_alghoritm(30)

ev_alg.create_population(Map1, 0)
#ev_alg.create_from_file(Map1, 0)

# game loop
running = True
while running:
    
    window.fill((0,0,0))
    clock.tick(FPS)
    list_with_characters = ev_alg.get_actual_gen()
    for x in list_with_characters:
        if not x.get_go_next():
            move_list = x.get_player_moves()
            #print(len(move_list))
            move_to_make, how_long = move_list[x.get_player_did_moves()]
            space, right, left = move_to_make
            x.make_move(move_to_make, how_long)
            check_collision(x, x.get_player_current_map())
            if (x.get_player_landed() and space and not x.get_player_charging()) or (not x.get_player_steping() and (right or left) and not space):
                if len(ev_alg.actual_generation) < 30:
                    print(move_to_make, how_long)
                    print(x.get_player_did_moves())
                if len(move_list)-1 > x.get_player_did_moves():
                    x.set_player_did_moves(x.get_player_did_moves()+1)
                else:
                    x.set_go_next()
                    if ev_alg.testing:
                        time.sleep(2)
                        ev_alg.testing_done_func()
        
    if not ev_alg.get_showout() and not ev_alg.testing:
        if ev_alg.get_go_next() :
            ev_alg.fitness_n_selection()
        
        if ev_alg.get_fitness_done() and not ev_alg.testing_done:
            ev_alg.testing_if(Map1, 0)
        
        if ev_alg.testing_done:
            ev_alg.crossover(Map1, 0)
        # else:
        #     ev_alg.get_information()
        
        if ev_alg.get_crossover_done():
            ev_alg.mutation()

        if ev_alg.get_mutation_done():
            ev_alg.prep_for_next_gen()

        ev_alg.alghoritm_end(Map4, final)

        if ev_alg.get_showout():
            ev_alg.ultimate_indyvidual(Map1, 0)
    
    # map tracing
    for x in list_with_characters:
        higest_map = []    
      
        if x.rect.top < 0 and x.current_map_id < len(Map_list)-1:
            x.current_map_id += 1  
            x.rect.y = SCREEN_HEIGHT - x.height * 2

        if x.rect.bottom > SCREEN_HEIGHT:
            x.current_map_id -= 1 
            x.rect.y = 0

        x.current_map = Map_list[x.current_map_id]

        for x in list_with_characters:
            higest_map.append(x.current_map_id)
        current_map = max(higest_map)
        
        Actual_map = Map_list[current_map]
        Background_image = Actual_map.get_bg()

    # draw background
    window.blit(Background_image, (0, 0))

    # draw sprites
    for x in list_with_characters:
        if Map_list[current_map] == x.current_map:
            x.draw(window)

    for x in range(Map_list[current_map].getNumber()):
        Map_list[current_map].getObject(x).draw(window)


    # drawing ui
    text_render = font.render("Generacja: "+str(ev_alg.get_generation()), True, (255,255,255))
    window.blit(text_render, (20, 715))
    if len(ev_alg.get_elite()) == 0:
        text_render = font.render("Best score: "+str(0), True, (255,255,255))
        window.blit(text_render, (215, 715))
        text_render = font.render("Moves: "+str(0), True, (255,255,255))
        window.blit(text_render, (410, 715))
    else:
        text_render = font.render("Best score: "+str(ev_alg.get_elite()[0].get_value()), True, (255,255,255))
        window.blit(text_render, (215, 715))
        text_render = font.render("Moves: "+str(len(ev_alg.get_elite()[0].get_parent_moves())), True, (255,255,255))
        window.blit(text_render, (410, 715))
    
    fps = int(clock.get_fps())
    fps_text = font.render("Fps : "+str(fps), True, (255,255,255))
    window.blit(fps_text, (550, 715))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update display window
    pygame.display.update()

pygame.quit()
