import pygame


class Platforma:
    def __init__(self, x, y, width, height) -> None:
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect, 2)