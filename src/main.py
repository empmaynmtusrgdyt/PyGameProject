import menu
import datetime
import pygame
import pygame_widgets

start_time = datetime.datetime.now()
LIGHT_BLUE = (66, 170, 255)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Jumper Game')
    clock = pygame.time.Clock()
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
        elif menu_instance.showing_settings:
            menu_instance.open_settings()
        else:
            menu_instance.draw()

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
