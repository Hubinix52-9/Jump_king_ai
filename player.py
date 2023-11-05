import pygame
import keyboard
import time


class Player():
    def __init__(self, x, y, image, scr_width, scr_height):
        self.image = pygame.transform.scale(image, (45, 45))
        self.width = 45
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.flip = False
        self.jumping = False
        self.is_jumping = False
        self.jump_height = 20
        self.jump_max_height = 20
        self.jump_min_height = 10
        self.gravity = 1
        self.lockkey = False
        self.duration = 0

    def make_move(self):
        key = pygame.key.get_pressed()
        space_pressed_time = None
        space_released_time = None 

        def on_key_event(e):
            nonlocal space_pressed_time, space_released_time
            if e.name == "space" and space_pressed_time is None and space_released_time is None and e.event_type == "down" and not self.lockkey: 
                space_pressed_time = time.time()
            elif e.name == "space" and space_released_time is None and space_pressed_time is not None and e.event_type == "up" and not self.lockkey:
                space_released_time = time.time()
                if space_pressed_time is not None:
                    if space_released_time - space_pressed_time > 0:
                        self.duration = int((space_released_time - space_pressed_time)*1000)
                        self.lockkey = True
                        space_pressed_time = None
                        space_released_time = None
                        print(self.duration)

        keyboard.hook(on_key_event)
        self.move(key)

    def move(self, key):
        # reset variables
        dx = 0
        dy = 0
        # process keypress
        
        if key[pygame.K_a] and not key[pygame.K_SPACE] and not self.jumping:
            dx = -5
            self.flip = True
        if key[pygame.K_d] and not key[pygame.K_SPACE] and not self.jumping:
            dx = 5
            self.flip = False

        # gravity
        self.vel_y += self.gravity
        dy += self.vel_y

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > self.scr_width:
            dx = self.scr_width - self.rect.right

        # check collision with ground
        if self.rect.bottom + dy > self.scr_height:
            dy = 0
            self.jumping = False
            self.lockkey = False

        # Jump logic
        if key[pygame.K_SPACE] and not self.jumping:
            if not self.is_jumping:
                self.jumping = True
                self.is_jumping = True
                self.jump_height = 0

            if self.duration < 1000:  # Less than 1 second          
                self.jump_height = self.jump_min_height
            elif self.duration > 1000 and self.duration < 1500:  # 1 to 1.5 seconds
                self.jump_height = self.jump_min_height + (self.duration / 1500) * (self.jump_max_height - self.jump_min_height)
            else:  # 1.5 seconds or more
                self.jump_height = self.jump_max_height

        elif self.is_jumping:
            self.is_jumping = False
            self.vel_y = -self.jump_height  # Set the vertical velocity to the calculated jump height

        self.rect.x += dx  # Położenie w poziomie jest aktualizowane, niezależnie od skoku
        self.rect.y += dy

    def draw(self, window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)