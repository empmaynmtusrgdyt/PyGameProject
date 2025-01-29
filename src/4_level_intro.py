import pygame
import os
import signal
import time

WIDTH = 1500
HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumper Game")

font_path = os.path.join("..", "data", "first_level_intro_font.ttf")
try:
    font = pygame.font.Font(font_path, 74)
except pygame.error as e:
    print(f"Ошибка загрузки шрифта: {e}")
    pygame.quit()
    exit()

text = font.render("Четвертый уровень: Затерянный корабль", True, WHITE)
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

text_2 = font.render("Цель - собрать 55 монет", True, WHITE)
text_2_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
running = True
clock = pygame.time.Clock()
start_time = time.time()
shutdown = False


def handle_sigterm(signum, frame):
    global shutdown
    shutdown = True
    pygame.quit()


if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, handle_sigterm)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or shutdown:
            running = False
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    screen.blit(text_2, text_2_rect)
    pygame.display.flip()
    clock.tick(60)
    if time.time() - start_time >= 3 or shutdown:
        running = False
pygame.quit()
