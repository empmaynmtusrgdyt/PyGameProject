import pygame
import os


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.cloud_image, self.cloud_image_rect = self.load_image('cloud.png', colorkey=-1, scale=(200, 150), pos=(30, 10))

    def load_image(self, name, colorkey=None, scale=None, pos=None):
        fullname = os.path.join('..', 'data', name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)
        if colorkey is not None:
            if colorkey == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        if scale:
            scaled_image = pygame.transform.scale(image, scale)
        else:
            scaled_image = image
        image_rect = scaled_image.get_rect()
        if pos:
            image_rect.x = pos[0]
            image_rect.y = pos[1]
        return scaled_image, image_rect

    def draw(self):
        self.screen.blit(self.cloud_image, self.cloud_image_rect)