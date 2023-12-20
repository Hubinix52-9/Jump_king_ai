import pygame
import keyboard
import time


class Player():
    def __init__(self, x, y, image, scr_width, scr_height, current_map, current_map_id):
        self.width = 44
        self.height = 44
        self.hero_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.hero_image, (self.width, self.height))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.flip = False
        self.is_jumping = False
        self.landed = True
        self.jump_height = 10
        self.jump_max_height = 11
        self.jump_min_height = 6
        self.gravity = 4
        self.charging_jump = False
        self.duration = 0
        self.jump_distance = 0
        self.jump_max_distance = 11
        self.jump_min_distance = 7
        self.direction = ''
        #self.list_of_moves = 
        self.current_map = current_map
        self.current_map_id = current_map_id

    def set_player_current_map_id(self, id):
        self.current_map_id = id
    
    def get_player_current_map_id(self):
        return self.current_map_id

    def get_player_current_map(self):
        return self.current_map

    def set_player_current_map(self, map):
        self.current_map = map

    def get_player_jumping(self):
        return self.is_jumping

    def get_player_flip(self):
        return self.flip

    def get_player_direction(self):
        return self.direction

    def set_player_velocity_x(self, wart):
        self.vel_x = wart

    def get_player_velocity_x(self):
        return self.vel_x

    def set_player_velocity_y(self, wart):
        self.vel_y = wart

    def get_player_velocity_y(self):
        return self.vel_y

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

    def get_player_height(self):
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
            if self.landed:
                if e.name == "space" and space_pressed_time is None and space_released_time is None and e.event_type == "down" and not self.charging_jump: 
                    space_pressed_time = time.time()
                    self.charging_jump = True
                    character_image_jumping = pygame.image.load('assets/jumping2.png').convert_alpha()
                    self.image = pygame.transform.scale(character_image_jumping, (self.width, self.height))
                elif e.name == "space" and space_released_time is None and space_pressed_time is not None and e.event_type == "up" and self.charging_jump:
                    space_released_time = time.time()
                    if space_pressed_time is not None:
                        self.duration = int((space_released_time - space_pressed_time)*1000)
                        self.charging_jump = False
                        space_pressed_time = None
                        space_released_time = None
        keyboard.hook(on_key_event)
        if not self.charging_jump:
            character_image_jumping = pygame.image.load('assets/standing2.png').convert_alpha()
            self.image = pygame.transform.scale(character_image_jumping, (self.width, self.height))
            self.move(key, self.duration)

    def move(self, key, time):
        dx = 0
        dy = 0
        if self.landed:
            self.vel_x = 0
            self.vel_y = 0
            self.direction = None
        
        

        # walking left
        if key[pygame.K_a] and not key[pygame.K_SPACE] and self.landed:
            dx = -4
            self.flip = False
        # walking right
        if key[pygame.K_d] and not key[pygame.K_SPACE] and self.landed:
            dx = 4
            self.flip = True

        if not self.landed:
            self.vel_y += self.gravity/self.jump_height
            dy += self.vel_y
            if self.direction == 'LEFT':
                self.vel_x += self.gravity/self.jump_distance
                dx += self.vel_x
                if self.vel_x >=-self.jump_distance/2.8:
                    self.vel_x -= self.gravity/self.jump_distance
                    dx += self.vel_x
            if self.direction == 'RIGHT':
                self.vel_x -= self.gravity/self.jump_distance
                dx += self.vel_x
                if self.vel_x <= self.jump_distance/2.8:
                    self.vel_x += self.gravity/self.jump_distance
                    dx += self.vel_x

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > self.scr_width:
            dx = self.scr_width - self.rect.right

        if not self.landed:
            if self.rect.left + self.vel_x < 0:
                self.vel_x = -self.vel_x/8
            if self.rect.right + self.vel_x > self.scr_width:
                self.vel_x = -self.vel_x/8

        # math how long/high player will jump
        if time < 200:          
            self.jump_height = self.jump_min_height
            self.jump_distance = self.jump_min_distance
        elif time > 200 and time < 1800:
            self.jump_height = self.jump_min_height + (time / 1800) * (self.jump_max_height - self.jump_min_height)
            self.jump_distance = self.jump_min_distance + (time / 1800) * (self.jump_max_distance - self.jump_min_distance)
        else: 
            self.jump_height = self.jump_max_height
            self.jump_distance = self.jump_max_distance

        # Jump logic
        # up jump
        if key[pygame.K_SPACE] and not key[pygame.K_a] and not key[pygame.K_d] and self.landed:
            if not self.is_jumping:
                self.direction = "UP"
                self.landed = False
                self.is_jumping = True

        # left jump
        if key[pygame.K_SPACE] and key[pygame.K_a] and not key[pygame.K_d] and self.landed:
            if not self.is_jumping:
                self.direction = 'LEFT'
                self.landed = False
                self.is_jumping = True

        # Right jump
        if key[pygame.K_SPACE] and key[pygame.K_d] and not key[pygame.K_a] and self.landed:
            if not self.is_jumping:
                self.direction = 'RIGHT'
                self.landed = False
                self.is_jumping = True

        if self.is_jumping:
            self.is_jumping = False
            self.vel_y = -self.jump_height 
            if self.direction == "LEFT":
                self.vel_x = -self.jump_distance
            elif self.direction == "RIGHT":
                self.vel_x = self.jump_distance

        # update coordinates
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))