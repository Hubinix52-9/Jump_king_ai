import pygame
import keyboard
import time


class Player():
    def __init__(self, x, y, image, scr_width, scr_height):
        self.width = 45
        self.height = 45
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.flip = False
        self.jumping = False
        self.is_jumping = False
        self.landed = True
        self.jump_height = 20
        self.jump_max_height = 15
        self.jump_min_height = 10
        self.gravity = 0.5
        self.lockkey = False
        self.charging_jump = False
        self.duration = 0
        self.bumped = False
        self.wall_bumped = ""

    def get_player_bumped(self):
        return self.bumped
    
    def set_player_bumped(self, wart):
        self.bumped = wart
    
    def set_player_wall_bumped(self, wart):
        self.bumped = wart

    def get_player_jump_height(self):
        return self.jump_height
    
    def set_player_height(self, wart):
        self.jump_height = wart

    def get_player_gravity(self):
        return self.gravity
    
    def set_player_gravity(self, wart):
        self.gravity = wart

    def set_player_jumping(self, wart):
        self.is_jumping = wart

    def get_player_width(self):
        return self.height
    
    def get_player_rect(self):
        return self.rect
    
    def update_player_y(self, y):
        self.rect.y = y

    def set_landed_flag(self, wart):
        self.landed = wart
        
    def make_move(self):
        key = pygame.key.get_pressed()
        space_pressed_time = None
        space_released_time = None 

        def on_key_event(e):
            nonlocal space_pressed_time, space_released_time
            if e.name == "space" and space_pressed_time is None and space_released_time is None and e.event_type == "down" and not self.charging_jump: 
                space_pressed_time = time.time()
                self.charging_jump = True
            elif e.name == "space" and space_released_time is None and space_pressed_time is not None and e.event_type == "up" and self.charging_jump:
                space_released_time = time.time()
                if space_pressed_time is not None:
                    self.duration = int((space_released_time - space_pressed_time)*1000)
                    self.charging_jump = False
                    space_pressed_time = None
                    space_released_time = None
                        

        keyboard.hook(on_key_event)
        if not self.charging_jump:
            self.move(key, self.duration)
    
    

    def move(self, key, time):
        # reset variables
        dx = 0
        dy = 0
        self.jump_height = 0
        # process keypress
        
        if key[pygame.K_a] and not key[pygame.K_SPACE] and self.landed:
            dx = -3
            self.flip = True
            
        if key[pygame.K_d] and not key[pygame.K_SPACE] and self.landed:
            dx = 3
            self.flip = False

        if not self.landed:
            self.vel_y += self.gravity
            dy += self.vel_y

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > self.scr_width:
            dx = self.scr_width - self.rect.right


        if time < 1000:  # Less than 1 second          
            self.jump_height = self.jump_min_height
        elif time > 1000 and time < 1500:  # 1 to 1.5 seconds
            self.jump_height = self.jump_min_height + (self.duration / 1500) * (self.jump_max_height - self.jump_min_height)
        else:  # 1.5 seconds or more
            self.jump_height = self.jump_max_height

        # Jump logic
        if key[pygame.K_SPACE] and self.landed:
            if not self.is_jumping:
                self.landed = False
                self.is_jumping = True
                

        if self.is_jumping and not self.bumped:
            self.is_jumping = False
            self.set_player_gravity(0.8)
            self.vel_y = -self.jump_height  
            
        if self.is_jumping and self.bumped and self.wall_bumped == "bottom":
            self.is_jumping = False
            self.set_player_gravity(3)
            self.vel_y = -self.jump_height 
        
        self.rect.x += dx 
        self.rect.y += dy  


    def draw(self, window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)