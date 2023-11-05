import pygame


class Platforma:
    def __init__(self, x, y, width, height) -> None:
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)