import pygame
import time as timeee
import copy

class Player():
    def __init__(self, current_map, current_map_id, wages, id):
        # character parameters
        self.width = 44
        self.height = 44
        self.id = id
        self.hero_image = pygame.image.load("assets/standing2.png").convert_alpha()
        self.image = pygame.transform.scale(self.hero_image, (self.width, self.height))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (630, 550)
        self.starting_x = self.rect.x
        self.starting_y = self.rect.y
        self.ending_x = 0
        self.ending_y = 0
        self.current_map = current_map
        self.starting_map = 0
        self.current_map_id = current_map_id
        self.starting_map_id = 0
        # screen parameters
        self.scr_width = 680
        self.scr_height = 680
        # moving parameters
        self.vel_y = 0
        self.vel_x = 0
        self.flip = False
        self.is_jumping = False
        self.landed = False
        # alghoritm parameters
        self.moves_list = []
        self.parent_moves = []
        self.wages = wages
        self.moves_did = -1
        self.go_next_gen = False
        # jump parameters
        self.jump_height = 10
        self.jump_max_height = 12
        self.jump_min_height = 6
        self.jump_distance = 0
        self.jump_max_distance = 11
        self.jump_min_distance = 7
        self.gravity = 4
        self.direction = ''
        # ai controlling movements
        self.steping = False
        self.step = 0
        self.released_time = None
        self.space_pressed_time = None
        self.charging_jump = False
        self.duration = 0
    # character parameters functions
    def get_player_xy(self):
        return self.rect.x, self.rect.y
    def get_player_rect(self):
        return self.rect
    def update_rect(self, war):
        xx,yy = war
        self.rect.x = xx
        self.rect.y = yy 
    def update_rect_x(self, x):
        self.rect.x = x 
    def update_rect_y(self, y):
        self.rect.y = y     
    def get_player_current_map(self):
        return self.current_map
    def set_player_current_map(self, map):
        self.current_map = map
    def get_player_current_map_id(self):
        return self.current_map_id
    def set_player_current_map_id(self, id):
    
        self.current_map_id = id
    # screen parameters functions
    def get_player_width(self):
        return self.height
    def get_player_height(self):
        return self.height
    # moving parameters functions
    def get_player_velocity_y(self):
        return self.vel_y
    def set_player_velocity_y(self, vel_y):
        self.vel_y = vel_y
    def get_player_velocity_x(self):
        return self.vel_x
    def set_player_velocity_x(self, vel_x):
        self.vel_x = vel_x
        return self.flip
    def get_player_jumping(self):
        return self.is_jumping
    def set_player_jumping(self, flag):
        self.is_jumping = flag
    def get_player_landed(self):
        return self.landed
    def set_player_landed(self, flag):
        self.landed = flag
    # alghoritm parameters functions
    def get_player_moves(self):
        return self.moves_list
    def set_player_moves(self, moves):
        moves_to_add = copy.deepcopy(moves)
        self.moves_list = moves_to_add
    def player_add_new_move(self, move):
        move_to_add = copy.deepcopy(move)
        self.moves_list.append(move_to_add)
    def get_parent_moves(self):
        return self.parent_moves
    def set_parent_moves(self, moves):
        moves_to_add = copy.deepcopy(moves)
        self.parent_moves = moves_to_add
    def add_parent_moves(self, moves):
        moves_to_add = copy.deepcopy(moves)
        for x in moves_to_add:
            self.parent_moves.append(x)
    def rem_last_parent_move(self):
        self.parent_moves = self.parent_moves[:-1]
    def get_player_wages(self):
        return self.wages
    def set_player_wages(self, wages):
        self.wages = wages
    def get_player_did_moves(self):
        return self.moves_did
    def set_player_did_moves(self, number):
        self.moves_did = number
    def get_go_next(self):
        return self.go_next_gen
    def set_go_next(self):
        self.go_next_gen = self.moves_did == len(self.moves_list)-1 and self.landed
    # ai controlling parameters functions
    def get_player_steping(self):
        return self.steping
    def get_player_charging(self):
        return self.charging_jump
    def get_value(self):
        return 680-self.rect.bottom + (self.current_map_id*680)
    # moving functions
    def make_move(self, keys, jump_time):
        character_image_jumping = None
        space, right, left = keys
        if self.landed:
            if space and self.space_pressed_time is None and not self.charging_jump: 
                self.space_pressed_time = timeee.perf_counter()
                self.charging_jump = True
                character_image_jumping = pygame.image.load('assets/jumping2.png').convert_alpha()
                self.image = pygame.transform.scale(character_image_jumping, (self.width, self.height))
            elif space and self.space_pressed_time is not None and self.charging_jump:
                self.released_time = timeee.perf_counter()
                duration = (self.released_time - self.space_pressed_time) *1000
                if duration >= jump_time:
                    self.charging_jump = False
                    self.space_pressed_time = None
                    self.released_time = None
                    character_image_jumping = pygame.image.load('assets/standing2.png').convert_alpha()
        if not self.charging_jump or not space:
            character_image_jumping = pygame.image.load('assets/standing2.png').convert_alpha()
            self.image = pygame.transform.scale(character_image_jumping, (self.width, self.height))
            self.move(keys, jump_time)
    def move(self, key, time):
        dx = 0
        dy = 0

        space, right, left = key

        if self.landed:
            self.vel_x = 0
            self.vel_y = 0
            self.direction = None  

        # walking left
        if left and not space and self.landed and not self.steping:
            self.step = -2*time//100
            self.steping = True
            self.flip = False
        if left and not space and self.landed and self.steping:
            dx = -2
            self.step += 2
            if self.step > 0:
                self.steping = False

        # walking right
        if right and not space and self.landed and not self.steping:
            self.step = 2*time//100
            self.steping = True
            self.flip = True
        if right and not space and self.landed and self.steping:
            dx = 2
            self.step -= 2
            if self.step < 0:
                self.steping = False

        

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
        if space and not left and not right and self.landed:
            if not self.is_jumping:
                self.direction = "UP"
                self.landed = False
                self.is_jumping = True

        # left jump
        if space and left and not right and self.landed:
            if not self.is_jumping:
                self.direction = 'LEFT'
                self.landed = False
                self.is_jumping = True

        # Right jump
        if space and right and not left and self.landed:
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