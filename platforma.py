import pygame


class Platforma:
    def __init__(self, x, y, width, height, window_height) -> None:
        self.rect = pygame.Rect(x, window_height-y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)