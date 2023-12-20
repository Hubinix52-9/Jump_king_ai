import pygame
from ai_managment import Evolutionary_alghoritm
from game_organization_ai import Game_organization_ai

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

# game managment class
g_m = Game_organization_ai(SCREEN_WIDTH, SCREEN_HEIGHT)
Map_list = g_m.map_list

# map and image
Actual_map = Map_list[0]
current_map = 0
Background_image = Actual_map.get_bg()

# ai alghoritm creation
ev_alg = Evolutionary_alghoritm(30)

ev_alg.create_population(Map_list[0], 0)
#ev_alg.create_from_file(Map_list[0], 0)

# game loop
running = True
while running:
    if not ev_alg.testing:
        window.fill((0,0,0)) 
        
    clock.tick(FPS)
    list_with_characters = ev_alg.get_actual_gen()
    for x in list_with_characters:
        if not x.get_go_next():
            
            move_list = x.get_player_moves()
            move_to_make, how_long = move_list[x.get_player_did_moves()]
            space, right, left = move_to_make
            if not ev_alg.testing:
                x.make_move(move_to_make, how_long)
            else:
                x.move(move_to_make, how_long)
            check_collision(x, x.current_map)
            if (x.get_player_landed() and space and not x.get_player_charging()) or (not x.get_player_steping() and (right or left) and not space):
                if len(move_list)-1 > x.get_player_did_moves():
                    x.set_player_did_moves(x.get_player_did_moves()+1)
                else:
                    x.set_go_next()
                    if ev_alg.testing and ev_alg.get_go_next():
                        ev_alg.testing_check()
    
    if ev_alg.get_go_next() :
        ev_alg.fitness_n_selection()

    if ev_alg.get_fitness_done() and not ev_alg.testing and not ev_alg.testing_done:
        ev_alg.create_best(Map_list[0], 0)

    if ev_alg.testing_done:
        ev_alg.crossover(Map_list[0], 0)

    if ev_alg.get_crossover_done():
        ev_alg.mutation()

    if ev_alg.get_mutation_done():
        ev_alg.prep_for_next_gen()
        do_checkout = False

    ev_alg.alghoritm_end(Map_list[3], g_m.destination)

    if ev_alg.get_showout():
        ev_alg.ultimate_indyvidual(Map_list[0], 0)


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
    if ev_alg.testing:
        Actual_map = Map_list[ev_alg.best_individuals[0].current_map_id]
        Background_image = Actual_map.get_bg()
    window.blit(Background_image, (0, 0))

    if not ev_alg.testing: 
        for x in list_with_characters:
            if Map_list[current_map] == x.current_map:
                x.draw(window)
        
        # rendering ui
        g_m.render_ui(window, clock, ev_alg)

    else:
        list_with_characters = ev_alg.next_generation
        for x in list_with_characters:
            if Map_list[ev_alg.best_individuals[0].current_map_id] == x.current_map:
                x.draw(window)

        g_m.render(window)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update display window
    pygame.display.update()

pygame.quit()
