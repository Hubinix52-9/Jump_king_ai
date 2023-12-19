import player_class_ai
from map_class import Map
from platform_class import Platforma
from ai_managment import Evolutionary_alghoritm as ev_alg
import pygame
class Game_organization_ai():
    def __init__(self, scr_w, scr_h) -> None:
        self.screen_w = scr_w
        self.screen_h = scr_h
        self.stop_flag = False
        self.last_gen_flag = False
        self.checkout_flag = False
        self.destination = None
        self.map_list = []
        self.button_list = []
        self.b_functions_list = []
        self.b_names = []
        self.b_names_cord = []
        self.font = pygame.font.Font(None, 35)
        self.bfont = pygame.font.Font(None, 60)
        self.maps()

    def render(self, window):
        text_render = self.bfont.render("Validating", True, (255,255,255))
        window.blit(text_render, (235, 715))

    def render_ui(self, window, clock, ev):
        text_render = self.font.render("Generacja: "+str(ev.get_generation()), True, (255,255,255))
        window.blit(text_render, (20, 715))
        if len(ev.get_elite()) == 0:
            text_render = self.font.render("Best score: "+str(0), True, (255,255,255))
            window.blit(text_render, (215, 715))
            text_render = self.font.render("Moves: "+str(0), True, (255,255,255))
            window.blit(text_render, (410, 715))
        else:
            text_render = self.font.render("Best score: "+str(ev.get_elite()[0].get_value()), True, (255,255,255))
            window.blit(text_render, (215, 715))
            text_render = self.font.render("Moves: "+str(len(ev.get_elite()[0].get_parent_moves())), True, (255,255,255))
            window.blit(text_render, (410, 715))
        
        fps = int(clock.get_fps())
        fps_text = self.font.render("Fps : "+str(fps), True, (255,255,255))
        window.blit(fps_text, (550, 715))

        for x in self.button_list:
            pygame.draw.rect(window, (255,255,255), x) 
        
        for x in range(len(self.b_names)):
            window.blit(self.b_names[x], self.b_names_cord[x] )


    def maps(self):
        # maps defining
        Map1 = Map('assets/block.png', self.screen_w, self.screen_h)
        Map2 = Map('assets/block3.png', self.screen_w, self.screen_h)
        Map3 = Map('assets/block5.png', self.screen_w, self.screen_h)
        Map4 = Map('assets/block7.png', self.screen_w, self.screen_h)

        # map 1
        m1_p1 = Platforma(0, self.screen_h, self.screen_w, 100)
        m1_p2 = Platforma(130, self.screen_h-150, 100, 25)
        m1_p3 = Platforma(330, self.screen_h-180, 100, 25)
        m1_p4 = Platforma(350, self.screen_h-380, 200, 25)
        m1_p5 = Platforma(30, self.screen_h-300, 150, 25)
        m1_p6 = Platforma(0, self.screen_h-480, 200, 25)
        m1_p7 = Platforma(340, self.screen_h-580, 150, 25)


        Map1.add(m1_p1)
        Map1.add(m1_p2)
        Map1.add(m1_p3)
        Map1.add(m1_p4)
        Map1.add(m1_p5)
        Map1.add(m1_p6)
        Map1.add(m1_p7)

        # map 2
        m2_p1 = Platforma(100, self.screen_h-250, 150, 25)
        m2_p2 = Platforma(0, self.screen_h-100, 150, 25)
        m2_p3 = Platforma(250, self.screen_h-550, 200, 25)
        m2_p4 = Platforma(380, self.screen_h-340, 120, 25)
        m2_p5 = Platforma(550, self.screen_h-450, 120, 25)


        Map2.add(m2_p1)
        Map2.add(m2_p2)
        Map2.add(m2_p3)
        Map2.add(m2_p4)
        Map2.add(m2_p5)

        # map 3
        m3_p1 = Platforma(0, self.screen_h-100, 200, 25)
        m3_p2 = Platforma(450, self.screen_h-250, 200, 25)
        m3_p3 = Platforma(50, self.screen_h-350, 200, 25)
        m3_p4 = Platforma(320, self.screen_h-490, 130, 25)
        m3_p5 = Platforma(320, self.screen_h-490, 130, 25)

        Map3.add(m3_p1)
        Map3.add(m3_p2)
        Map3.add(m3_p3)
        Map3.add(m3_p4)
        Map3.add(m3_p5)

        # map 4

        m4_p1 = Platforma(550, self.screen_h-5, 100, 25)
        m4_p2 = Platforma(400, self.screen_h-150, 50, 25)
        m4_p3 = Platforma(150, self.screen_h-200, 150, 25)
        m4_p4 = Platforma(20, self.screen_h-250, 50, 25)
        m4_p5 = Platforma(200, self.screen_h-350, 100, 25)
        m4_p6 = Platforma(450, self.screen_h-450, 140, 25)
        m4_p7 = Platforma(220, self.screen_h-550, 130, 25)
        final = Platforma(270, self.screen_h-555, 40, 25)


        Map4.add(m4_p1)
        Map4.add(m4_p2)
        Map4.add(m4_p3)
        Map4.add(m4_p4)
        Map4.add(m4_p5)
        Map4.add(m4_p6)
        Map4.add(m4_p7) 

        Map_list = [Map1, Map2, Map3, Map4]

        self.map_list = Map_list
        self.destination = final