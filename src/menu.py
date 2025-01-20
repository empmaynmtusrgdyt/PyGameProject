import pygame
from pygame_widgets.button import Button as PygameWidgetsButton
import os


class Button():
    def __init__(self, screen, x, y, radius, color, pressed_color, hover_color, text, font, icon_path,
                 action, text_offset_y=40):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.font = font
        self.font = font
        self.icon_path = icon_path
        self.action = action
        self.text_offset_y = text_offset_y
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        self.button, self.button_text_surface, self.button_text_rect = self._create_button()

    def _create_button(self):
        button_image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(button_image, self.color, (self.radius, self.radius), self.radius)

        try:
            icon_image = pygame.transform.scale(
                pygame.image.load(os.path.join('..', 'data', self.icon_path)).convert_alpha(),
                (int(self.radius * 1.2), int(self.radius * 1.2)))
            icon_rect = icon_image.get_rect(center=(self.radius, self.radius))
            button_image.blit(icon_image, icon_rect)
        except pygame.error as e:
            print(f"Ошибка загрузки иконки: {self.icon_path}. {e}")

        button = PygameWidgetsButton(
            self.screen, self.x - self.radius, self.y - self.radius,
                         self.radius * 2, self.radius * 2,
            inactiveColour=self.color,
            hoverColour=self.hover_color,
            pressedColour=self.pressed_color,
            onClick=self.action,
            image=button_image,
            text=""
        )
        button.mask = pygame.mask.from_surface(button_image)

        button_text_surface, button_text_rect = self._render_text(self.text, self.font, (0, 0, 0), pos=(
            self.x, self.y + self.radius + self.text_offset_y))

        return button, button_text_surface, button_text_rect

    def _render_text(self, text, font, color, pos=None):
        text_surface = font.render(text, True, color)
        if pos:
            text_rect = text_surface.get_rect(center=(pos[0], pos[1]))
        else:
            text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 50))
        return text_surface, text_rect

    def draw(self):
        self.screen.blit(self.button_text_surface, self.button_text_rect)
        self.button.draw()


class Menu():
    def __init__(self, screen):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        button_radius = 50
        button_spacing = 300
        self.font = self.load_font('cartton_font.ttf', 60)
        self.centre_button = Button(screen, screen_width // 2, screen_height // 2, button_radius,
                                    (0, 255, 0), (80, 200, 120), (0, 165, 80),
                                    "Начать игру",
                                    self.font, "icon-play.png", self.start_game)
        self.right_button = Button(screen, screen_width // 2 + button_spacing, screen_height // 2, button_radius,
                                   (0, 0, 255), (102, 0, 255), (0, 0, 139),
                                   "Персонажи", self.font, "icon-smile.png", self.select_skin)
        self.left_button = Button(screen, screen_width // 2 - button_spacing, screen_height // 2, button_radius,
                                  (255, 0, 0), (255, 73, 108), (171, 52, 58),
                                  "Настройки", self.font, "icon-settings.png", self.open_settings)
        self.screen = screen
        self.cloud_image, self.cloud_image_rect = self.load_image('cloud.png',
                                                                  colorkey=-1, scale=(200, 150), pos=(30, 10))
        self.title_surface, self.title_rect = self.render_text("Jump: Приключение прыгуна", self.font,
                                                               (0, 0, 0))

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

    def load_font(self, name, size):
        fullname = os.path.join('..', 'data', name)
        try:
            font = pygame.font.Font(fullname, size)
        except pygame.error as message:
            print('Cannot load font:', name)
            raise SystemExit(message)
        return font

    def render_text(self, text, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 50))
        return text_surface, text_rect

    def draw(self):
        self.screen.blit(self.cloud_image, self.cloud_image_rect)
        self.screen.blit(self.title_surface, self.title_rect)
        self.centre_button.draw()
        self.right_button.draw()
        self.left_button.draw()

    def start_game(self):
        pass

    def select_skin(self):
        pass

    def open_settings(self):
        pass
