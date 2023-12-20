import pygame


class Map:
    def __init__(self, src_img, scr_width, scr_height):
        self.list = []
        self.image = pygame.image.load(src_img).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image,
                                                   (scr_width, scr_height))

    def add(self, object):
        self.list.append(object)

    def getObject(self, id):
        return self.list[id]

    def get_bg(self):
        return self.scaled_image

