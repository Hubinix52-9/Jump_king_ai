import pygame


class Player():
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (45, 45))
        self.width = 45
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        self.jumping = False
        self.jump_charge = 0
        self.is_jumping = False
        self.jump_start_time = 0
        self.jump_height = 0
        self.jump_max_height = 20
        self.jump_min_height = 5
        self.gravity

    def move(self):
        # reset variables
        dx = 0
        dy = 0

        # process keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -5
            self.flip = True
        if key[pygame.K_d]:
            dx = 5
            self.flip = False

        # gravity
        self.vel_y += self.gravity
        dy += self.vel_y

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # check collision with ground
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            # self.vel_y = -20

        # Jump logic
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            if not self.is_jumping:
                self.is_jumping = True
                self.jump_start_time = pygame.time.get_ticks()
                self.jump_height = 0

            jump_duration = pygame.time.get_ticks() - self.jump_start_time

            if jump_duration < 1000:  # Less than 1 second
                self.jump_height = self.jump_min_height
            elif jump_duration < 1500:  # 1 to 1.5 seconds
                self.jump_height = self.jump_min_height + ((jump_duration - 1000) / 500) * (self.jump_max_height - self.jump_min_height)
            else:  # 1.5 seconds or more
                self.jump_height = self.jump_max_height

        elif self.is_jumping:
            self.is_jumping = False
            self.vel_y = -self.jump_height  # Set the vertical velocity to the calculated jump height
            self.jump_start_time = 0  # Reset jump start time

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)