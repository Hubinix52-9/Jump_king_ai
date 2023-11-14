import pygame


class Platforma:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y-height, width, height)

    def get_x(self):
        return self.x
        
    def get_y(self):
        return self.y
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_rect(self):
        return self.rect
    
    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)