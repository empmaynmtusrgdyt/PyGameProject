import pygame
import menu

LIGHT_BLUE = (66, 170, 255)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Jumper Game')
    clock = pygame.time.Clock()
    menu_instance = menu.Menu(screen)
    running = True
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(LIGHT_BLUE)
        menu_instance.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()