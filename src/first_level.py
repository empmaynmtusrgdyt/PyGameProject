import pygame
import os


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, player):
        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top + 5 and player.velocity.y >= 0:
                player.rect.bottom = self.rect.top
                player.velocity.y = 0


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

platform1 = Platform(290, 710, 100, 70, '../data/first_level_platform.png')
platform2 = Platform(150, 770, 100, 70, '../data/first_level_platform.png')
platform3 = Platform(10, 830, 100, 70, '../data/first_level_platform.png')

all_sprites = pygame.sprite.Group()
all_sprites.add(platform1, platform2, platform3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(scaled_background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
