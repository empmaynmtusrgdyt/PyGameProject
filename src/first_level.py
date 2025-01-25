import pygame
import os


pygame.init()
size = width, height = 1500, 900
PURPLE = (139, 0, 255)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Jumper Game')
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('..', 'data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f"Cannot load image: {fullname}")
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        image = image.convert_alpha()
    else:
        image = image.convert()
    image_rect = image.get_rect()
    return image, image_rect


background_image, background_rect = load_image("first_level_fone.png")
scaled_background = pygame.transform.scale(background_image, (1500, 900))
background_rect.topleft = (0, 0)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(scaled_background, background_rect)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()