import pygame
import os
import random
import sqlite3


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, health, speed):
        super().__init__()
        self.image, _ = load_image(image_path, -1)
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.move_speed = speed / 10
        self.gravity = 2
        self.jump_speed = -35
        self.on_ground = True
        self.start_y = y
        self.health = health

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


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image, _ = load_image(image_path, -1)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image, _ = load_image(image_path, -1)
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed = 3  # Скорость движения врага

    def update(self):
        self.rect.x -= self.move_speed

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

coin_image_path = '../data/coin.png'
all_coins = pygame.sprite.Group()
coin_sound = pygame.mixer.Sound(os.path.join('..', 'data', 'coin_sound.mp3'))
camera_x = 0
scroll_speed = 5
coin_spawn_timer = 0
coin_spawn_interval = 150
coins_collected = 0  # Счетчик собранных монет
font = pygame.font.Font(None, 36)  # Шрифт для текста

conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()
try:
    cursor.execute("SELECT setting_value FROM game_settings WHERE setting_name = 'selected_character'")
    result = cursor.fetchone()
    selected_character = result[0] if result else "character1.png"  # Ставим character1.png по умолчанию если не найдено

    player_stats = {
        "character1.png": {"health": 150, "speed": 100},
        "character2.png": {"health": 100, "speed": 150}
    }
    player_image_path = f'../data/{selected_character}'
    player_health = player_stats[selected_character]['health']
    player_speed = player_stats[selected_character]['speed']
    player = Player(50, 860 - 70, player_image_path, player_health, player_speed)
except sqlite3.Error as e:
    print(f"Ошибка при загрузке данных персонажа: {e}")
    selected_character = "character1.png"
    player_stats = {
        "character1.png": {"health": 150, "speed": 100},
        "character2.png": {"health": 100, "speed": 150}
    }
    player_image_path = f'../data/{selected_character}'
    player_health = player_stats[selected_character]['health']
    player_speed = player_stats[selected_character]['speed']
    player = Player(50, 860 - 70, player_image_path, player_health, player_speed)
finally:
    conn.close()

enemy_image_path = '../data/character3.png'
all_enemies = pygame.sprite.Group()
enemy_spawn_timer = 0
enemy_spawn_interval = 200
enemy_damage = 10
health_text_surface = None
health_text_rect = None
game_over = False
game_won = False
game_over_font = pygame.font.Font(None, 72)
damage_sound = pygame.mixer.Sound(os.path.join('..', 'data', 'damage.mp3'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    if not game_over and not game_won:
        player.update()
        camera_x += player.move_speed

        for i in range(-1, 2):
            bg_x = (i * background_width) - (camera_x % background_width)
            screen.blit(scaled_background, (bg_x, 0))

        coin_spawn_timer += 1
        if coin_spawn_timer > coin_spawn_interval:
            coin_spawn_timer = 0
            coin_x = camera_x + width + 100
            coin_y = random.randint(500, 700)
            new_coin = Coin(coin_x, coin_y, coin_image_path)
            all_coins.add(new_coin)

        for coin in all_coins.copy():
            if player.rect.colliderect(coin.rect):
                all_coins.remove(coin)
                coins_collected += 1
                coin_sound.play()
                if coins_collected >= 10:
                     game_won = True

            else:
                coin.draw(screen, camera_x)

        enemy_spawn_timer += 1
        if enemy_spawn_timer > enemy_spawn_interval:
            enemy_spawn_timer = 0
            enemy_x = camera_x + width + 100
            enemy_y = random.randint(500, 800)
            new_enemy = Enemy(enemy_x, enemy_y, enemy_image_path)
            all_enemies.add(new_enemy)

        for enemy in all_enemies.copy():
            enemy.update()
            if enemy.rect.right < camera_x:
                all_enemies.remove(enemy)
            else:
                enemy.draw(screen, camera_x)

        for enemy in all_enemies:
            if player.rect.colliderect(enemy.rect):
                all_enemies.remove(enemy)
                player.health -= enemy_damage
                damage_sound.play()
                if player.health <= 0:
                   game_over = True

        player.draw(screen, camera_x)
        coin_text = font.render(f"Количество монет: {coins_collected}", True, (255, 255, 0))
        text_rect = coin_text.get_rect()
        text_rect.topright = (width - 10, 10)
        screen.blit(coin_text, text_rect)

        health_text_surface = font.render(f"Здоровье: {player.health}", True, (255, 0, 0))
        if health_text_rect is None:
            health_text_rect = health_text_surface.get_rect()
            health_text_rect.topleft = (10, 10)
        screen.blit(health_text_surface, health_text_rect)
    if game_over:
          screen.fill((0, 0, 0))
          game_over_text = game_over_font.render("Ты проиграл", True, (255, 0, 0))
          text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
          screen.blit(game_over_text, text_rect)
    elif game_won:
        screen.fill((0, 0, 0))
        game_win_text = game_over_font.render("Ты выиграл", True, (0, 255, 0))
        text_rect = game_win_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_win_text, text_rect)
    pygame.display.flip()
    clock.tick(60)

    if game_over or game_won:
        pygame.time.delay(2000)
        running = False
pygame.quit()