import menu
import datetime
import pygame
import pygame_widgets
import sys
import os


start_time = datetime.datetime.now()
LIGHT_BLUE = (66, 170, 255)


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


def show_splash_screen(screen, splash_image, font):
    running_splash = True
    text = font.render("Нажмите любую кнопку для продолжения", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
    text_2 = font.render("Jump: Приключение Прыгуна", True, (255, 255, 255))
    text_2_rect = text_2.get_rect(center=(screen.get_width() // 2, 50))
    while running_splash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running_splash = False
        screen.blit(splash_image, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(text_2, text_2_rect)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Jumper Game')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    splash_image, _ = load_image("splash.jpeg", colorkey=-1)
    splash_image = pygame.transform.scale(splash_image, (width, height))
    show_splash_screen(screen, splash_image, font)
    menu_instance = menu.Menu(screen)
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                end_time = datetime.datetime.now() - start_time
                end_time = str(end_time).split(':')
                end_time = int(end_time[0]) + int(end_time[1]) / \
                           60 + round(float(end_time[2]) / 3600, 4)
                all_time = float([item for item in menu_instance.db_cursor.execute(
                    "SELECT time_played FROM game_settings")][-1][-1])
                menu_instance.db_cursor.execute(
                    f'UPDATE game_settings SET time_played = {all_time + end_time}')
                menu_instance.db_connection.commit()
                menu_instance.db_connection.close()

        if menu_instance.showing_skin_selector:
            menu_instance.draw_skin_selector()
        elif menu_instance.showing_level_list:
            menu_instance.open_level_list()
        elif menu_instance.showing_settings:
            menu_instance.open_settings()
        else:
            menu_instance.draw()

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
