import pygame
import os
import time
from pygame_widgets.button import Button as PygameWidgetsButton
from pygame_widgets.textbox import TextBox
import sqlite3
import subprocess

pygame.init()


class Button():
    def __init__(self, screen, x, y, radius, color, pressed_color, hover_color, text, font, icon_path, action,
                 text_offset_y=40):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.font = font
        self.icon_path = icon_path
        self.action = action
        self.text_offset_y = text_offset_y
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        self.button, self.button_text_surface, self.button_text_rect = self._create_button()

    def _create_button(self):
        button_image = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(button_image, self.color,
                           (self.radius, self.radius), self.radius)

        try:
            icon_image = pygame.transform.scale(
                pygame.image.load(os.path.join(
                    '..', 'data', self.icon_path)).convert_alpha(),
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
            text_rect = text_surface.get_rect(
                center=(self.screen.get_width() / 2, 50))
        return text_surface, text_rect

    def draw(self):
        self.screen.blit(self.button_text_surface, self.button_text_rect)
        self.button.draw()


class Menu():
    def __init__(self, screen):
        try:
            self.db_connection = sqlite3.connect('game_data.db')
            self.db_cursor = self.db_connection.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            self.db_connection = None
            self.db_cursor = None
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.button_radius = 50
        self.button_spacing = 300
        self.font = self.load_font('cartton_font.ttf', 60)
        self.small_font = self.load_font('cartton_font.ttf', 30)
        self.centre_button = Button(screen, self.screen_width // 2, self.screen_height // 2, self.button_radius,
                                    (0, 255, 0), (80, 200, 120), (0, 165, 80),
                                    "Начать игру",
                                    self.font, "icon-play.png", self.start_game)
        self.right_button = Button(screen, self.screen_width // 2 + self.button_spacing, self.screen_height // 2,
                                   self.button_radius,
                                   (0, 0, 255), (102, 0, 255), (0, 0, 139),
                                   "Персонажи", self.font, "icon-smile.png", self.select_skin)
        self.left_button = Button(screen, self.screen_width // 2 - self.button_spacing, self.screen_height // 2,
                                  self.button_radius,
                                  (255, 0, 0), (255, 73, 108), (171, 52, 58),
                                  "Настройки", self.font, "icon-settings.png", self.open_settings)
        self.screen = screen
        self.cloud_image, self.cloud_image_rect = self.load_image('cloud.png',
                                                                  colorkey=-1, scale=(200, 150), pos=(30, 10))
        self.title_surface, self.title_rect = self.render_text("Jump: Приключение прыгуна", self.font,
                                                               (0, 0, 0))
        self.menu_music_is_playing = [item for item in self.db_cursor.execute(
            'SELECT music_is_playing FROM game_settings')][-1][-1]
        self.showing_settings = False
        self.showing_account_management = False
        self.settings_screen = None
        self.showing_skin_selector = False
        self.skin_selector_screen = None
        self.skin_selector_buttons = None
        self.click_sound = pygame.mixer.Sound('../data/click.mp3')
        self.click_sound.set_volume(35)
        self.menu_music = pygame.mixer.Sound('../data/menu.wav')
        self.character_names = ["character1.png", "character2.png"]
        self.showing_skin_selector = False
        self.skin_selector_screen = None
        self.skin_selector_buttons = None
        self.character_names = ["character1.png", "character2.png"]
        self.character_stats = {
            "character1.png": {"health": 150, "speed": 100, "name": "Red-BSD"},
            "character2.png": {"health": 100, "speed": 150, "name": "Blue-BSD"}
        }
        self.selected_character = self.load_selected_character()

        if self.menu_music_is_playing:
            self.menu_music.play()
        else:
            self.menu_music.stop()

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
        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() / 2, 50))
        return text_surface, text_rect

    def draw(self):
        self.screen.fill((66, 170, 255))  # Используем цвет LIGHT_BLUE
        self.screen.blit(self.cloud_image, self.cloud_image_rect)
        self.screen.blit(self.title_surface, self.title_rect)
        self.centre_button.draw()
        self.right_button.draw()
        self.left_button.draw()

    def start_game(self):
        subprocess.Popen(['python', 'first_level_intro.py'])
        time.sleep(3)
        subprocess.Popen(['python', 'first_level_intro.py']).kill()
        subprocess.Popen(['python', 'first_level.py'])

    def select_skin(self):
        if not self.showing_skin_selector:  # Проверяем, отображается ли уже окно выбора скина
            self.showing_skin_selector = True
            self.skin_selector_screen = pygame.display.set_mode((1000, 600))
            self.create_skin_selector_buttons()
            self.right_button = None
            self.centre_button = None
            self.left_button = None
            self.click_sound.play()

    def create_skin_selector_buttons(self):
        button_width = 150
        button_height = 50
        # если не удалось загрузить шрифт то будет использоваться Arial
        font = self.font if self.font else pygame.font.SysFont("Arial", 30)
        self.current_character_index = self.character_names.index(
            self.selected_character) if self.selected_character in self.character_names else 0

        self.skin_selector_buttons = [
            PygameWidgetsButton(self.skin_selector_screen, 50, 100, button_width,
                                button_height, text="Следующий", font=font, onClick=self.next_skin),
            PygameWidgetsButton(self.skin_selector_screen, 50, 170, button_width,
                                button_height, text="Сохранить", font=font, onClick=self.save_skin),
            PygameWidgetsButton(self.skin_selector_screen, 50, 240, button_width,
                                button_height, text="Меню", font=font, onClick=self.hide_skin_selector)
        ]

    def draw_skin_selector(self):
        if self.skin_selector_buttons and self.showing_skin_selector:
            self.skin_selector_screen.fill((66, 170, 255))  # LIGHT_BLUE
            try:
                character_image = pygame.transform.scale(
                    pygame.image.load(os.path.join(
                        '..', 'data', self.character_names[self.current_character_index])).convert_alpha(),
                    (400, 400))
                self.skin_selector_screen.blit(character_image, (400, 30))
            except pygame.error as e:
                print(f"Ошибка загрузки картинки персонажа: {
                self.character_names[self.current_character_index]}. {e}")

            stats = self.character_stats[self.character_names[self.current_character_index]]
            name_text = self.render_text(stats['name'], self.small_font, (0, 0, 0))
            health_text = self.render_text(f"Здоровье: {stats['health']}", self.font, (0, 0, 0))
            speed_text = self.render_text(f"Скорость: {stats['speed']}", self.font, (0, 0, 0))
            self.skin_selector_screen.blit(name_text[0], (515, 0))
            self.skin_selector_screen.blit(health_text[0], (425, 420))
            self.skin_selector_screen.blit(speed_text[0], (425, 470))

            for button in self.skin_selector_buttons:
                button.draw()

            pygame.display.update()

    def hide_skin_selector(self):
        self.showing_skin_selector = False
        if self.skin_selector_screen:
            self.skin_selector_screen.fill((66, 170, 255))  # LIGHT_BLUE
            pygame.display.flip()
            self.skin_selector_screen = None
            self.skin_selector_buttons = None
            self.screen = pygame.display.set_mode((1000, 600))

            self.centre_button = Button(self.screen, self.screen_width // 2, self.screen_height // 2,
                                        self.button_radius,
                                        (0, 255, 0), (80, 200, 120), (0, 165, 80),
                                        "Начать игру",
                                        self.font, "icon-play.png", self.start_game)
            self.right_button = Button(self.screen, self.screen_width // 2 + self.button_spacing,
                                       self.screen_height // 2,
                                       self.button_radius,
                                       (0, 0, 255), (102, 0, 255), (0, 0, 139),
                                       "Персонажи", self.font, "icon-smile.png", self.select_skin)
            self.left_button = Button(self.screen, self.screen_width // 2 - self.button_spacing,
                                      self.screen_height // 2,
                                      self.button_radius,
                                      (255, 0, 0), (255, 73, 108), (171, 52, 58),
                                      "Настройки", self.font, "icon-settings.png", self.open_settings)
        self.click_sound.play()

    def next_skin(self):
        self.current_character_index = (
                                               self.current_character_index + 1) % len(self.character_names)
        self.draw_skin_selector()
        self.click_sound.play()

    def save_skin(self):
        self.selected_character = self.character_names[self.current_character_index]
        self.save_selected_character(self.selected_character)
        self.hide_skin_selector()
        self.click_sound.play()

    def create_table(self):
        if self.db_cursor:
            try:
                self.db_cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_settings (
                        setting_name TEXT PRIMARY KEY,
                        setting_value TEXT
                    )
                ''')
                self.db_connection.commit()
            except sqlite3.Error as e:
                print(f"Ошибка создания таблицы: {e}")

    def load_selected_character(self):
        if self.db_cursor:
            try:
                self.db_cursor.execute(
                    "SELECT setting_value FROM game_settings WHERE setting_name = 'selected_character'")
                result = self.db_cursor.fetchone()
                return result[0] if result else self.character_names[0]
            except sqlite3.Error as e:
                print(f"Ошибка при загрузке данных персонажа: {e}")
                return self.character_names[0]
        else:
            return self.character_names[0]

    def save_selected_character(self, character_name):
        if self.db_cursor:
            try:
                self.db_cursor.execute("UPDATE game_settings SET setting_value = ? WHERE setting_name = ?",
                                       (character_name, 'selected_character'))
                if self.db_cursor.rowcount == 0:
                    self.db_cursor.execute("INSERT INTO game_settings (setting_name, setting_value) VALUES (?, ?)",
                                           ('selected_character', character_name))
                self.db_connection.commit()
            except sqlite3.Error as e:
                print(f"Ошибка сохранения данных персонажа: {e}")

    def open_settings(self):
        if not self.showing_settings:
            self.showing_settings = True
            self.settings_screen = pygame.display.set_mode((1000, 600))
            self.settings_screen.fill((66, 170, 255))
            self.def_buttons()
            self.right_button.button.hide()
            self.left_button.button.hide()
            self.centre_button.button.hide()
            self.click_sound.play()

    def def_buttons(self):
        if self.menu_music_is_playing:
            self.music_button = Button(self.settings_screen, 300, 300, 100, 'GREEN', (0, 200, 0),
                                       (0, 150, 0), 'Музыка', self.font, 'music.png', self.play_music_menu)
        else:
            self.music_button = Button(self.settings_screen, 300, 300, 100, 'RED', (200, 0, 0),
                                       (150, 0, 0), 'Музыка', self.font, 'music.png', self.play_music_menu)
        self.music_button.draw()
        self.quit = PygameWidgetsButton(self.settings_screen, 0, 0, 200, 50)
        self.quit.font = self.font
        self.quit.setText('МЕНЮ')
        self.quit.setOnClick(self.leave_settings)
        self.account_button = Button(self.settings_screen, 700, 300, 100, (235, 128, 52),
                                     (255, 155, 52), (125, 125, 52), 'Аккаунт', self.font, 'account.png',
                                     self.account_manage)
        self.account_button.draw()

    def account_manage(self):
        if not self.showing_account_management:
            self.showing_account_management = True
            self.account_button.button.hide()
            self.music_button.button.hide()
            self.quit.hide()
            self.account_screen = pygame.display.set_mode((1000, 600))
            self.account_screen.fill((66, 170, 255))
            self.quit_from_account_management = PygameWidgetsButton(self.account_screen, 350, 490, 300, 100)
            self.quit_from_account_management.font = self.font
            self.quit_from_account_management.setOnClick(self.leave_account_manage)
            self.quit_from_account_management.setText('Назад')
            self.text = f'За всё время Вы наиграли {round(float([item for item in self.db_cursor.execute('SELECT time_played FROM game_settings')][-1][-1]), 1)}'
            self.info_about_account = TextBox(self.account_screen, 100, 100, 800, 100)
            self.info_about_account.disable()
            self.info_about_account.font = self.font
            self.info_about_account.setText(self.text + ' ч.')
        self.click_sound.play()

    def leave_account_manage(self):
        self.quit_from_account_management.hide()
        self.info_about_account.hide()
        self.settings_screen.fill((66, 170, 255))
        self.def_buttons()
        self.showing_account_management = False
        self.click_sound.play()

    def leave_settings(self):
        self.showing_settings = False
        self.centre_button.button.show()
        self.right_button.button.show()
        self.left_button.button.show()
        self.account_button.button.hide()
        self.music_button.button.hide()
        self.quit.hide()
        self.click_sound.play()

    def play_music_menu(self):
        self.menu_music_is_playing = 1 if not self.menu_music_is_playing else 0
        if self.menu_music_is_playing:
            self.menu_music.play()
            self.music_button = Button(self.settings_screen, 300, 300, 100, 'GREEN', (0, 200, 0),
                                       (0, 150, 0), 'Музыка', self.font, 'music.png', self.play_music_menu)
        elif not self.menu_music_is_playing:
            self.music_button = Button(self.settings_screen, 300, 300, 100, 'RED', (200, 0, 0),
                                       (150, 0, 0), 'Музыка', self.font, 'music.png', self.play_music_menu)
            self.menu_music.stop()
        self.music_button.draw()
        self.click_sound.play()

        self.db_cursor.execute(f'UPDATE game_settings SET music_is_playing={
        self.menu_music_is_playing}')
        self.db_connection.commit()