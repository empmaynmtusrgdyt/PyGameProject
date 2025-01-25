import pygame
import menu
import pygame_widgets

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
                
        if menu_instance.showing_skin_selector:
            menu_instance.draw_skin_selector()
        elif menu_instance.showing_settings:
            menu_instance.open_settings()
        else:
            menu_instance.draw()

        pygame_widgets.update(events)  # Обновляем виджеты
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()