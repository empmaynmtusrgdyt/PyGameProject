import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image, _ = load_image(image_path, -1)
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.move_speed = 5
        self.gravity = 2
        self.jump_speed = -35
        self.on_ground = True
        self.start_y = y

    def update(self):
        self.rect.x += self.move_speed

        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= self.start_y:
                self.rect.y = self.start_y
                self.velocity_y = 0
                self.is_jumping = False
                self.on_ground = True
        if not self.is_jumping and self.rect.y < self.start_y:
            self.rect.y += self.gravity

    def jump(self):
        if not self.is_jumping and self.on_ground:
            self.is_jumping = True
            self.velocity_y = self.jump_speed
            self.on_ground = False

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))


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
background_width = scaled_background.get_width()

player_image_path = '../data/character1.png'
player = Player(50, 860 - 70, player_image_path)

camera_x = 0
scroll_speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    player.update()
    camera_x += scroll_speed
    for i in range(-1, 2):
        bg_x = (i * background_width) - (camera_x % background_width)
        screen.blit(scaled_background, (bg_x, 0))
    player.draw(screen, camera_x)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
