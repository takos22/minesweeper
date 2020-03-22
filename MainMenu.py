import os

import pygame as pg
from pygame.locals import *

from GameState import *
from MenuElements import *

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (224, 224, 224)
DARK_GRAY = (32, 32, 32)
BLACK = (0, 0, 0)


class MainMenu(GameState):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.next_state = "GAMEPLAY"

    def startup(self, persistent: dict):
        self.persist = {}

        self.persist["difficulty"] = 0
        self.persist["dark_theme"] = False

        self.persist["rows"] = 5
        self.persist["cols"] = 5
        self.persist["mines"] = 5

        self.persist.update(persistent)

        self.width = 512
        self.height = 512
        self.size = (self.width, self.height)

        self.screen = pg.display.set_mode(self.size)

        self.menu = "MAIN"

        self.mouse_click = False
        self.mouse_released = True
        self.return_click = False
        self.return_released = True
        self.mouse_pos = (0, 0)

        self.selected_button = 0

        self.font_name = "minesweeper.ttf"
        self.font_size_title = 34
        self.fontSizeButtonLarge = 32
        self.fontSizeButtonSmall = 22

        if self.persist["dark_theme"]:
            theme = "dark"
            self.text_color = WHITE
            self.background_color = DARK_GRAY
        else:
            theme = "basic"
            self.text_color = BLACK
            self.background_color = LIGHT_GRAY

        self.tile_cell = pg.image.load(
            os.path.join("tiles", theme, "game", "cell.png"))

        self.menu_title = pg.image.load(
            os.path.join("tiles", theme, "menu", "title.png"))

        self.menu_button = pg.image.load(
            os.path.join("tiles", theme, "menu", "button.png"))
        self.menu_button_hovered = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_hovered.png"))
        self.menu_button_clicked = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_clicked.png"))

        self.menu_button_small = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_small.png"))
        self.menuButtonSmallHovered = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_small_hovered.png"))
        self.menuButtonSmallClicked = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_small_clicked.png"))

        self.menu_button_large = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_large.png"))
        self.menuButtonLargeHovered = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_large_hovered.png"))
        self.menuButtonLargeClicked = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_large_clicked.png"))

        # main menu elements
        self.title_pos = (self.width/2, self.height/4-16)
        self.mainPlayButtonPos = (self.width/2, self.height/2-32)
        self.options_button_pos = (self.width/2, self.mainPlayButtonPos[1]+96)
        self.exit_button_pos = (self.width/2, self.options_button_pos[1]+96)

        self.title = Text(self.screen, self.title_pos, "MINESWEEPER", self.text_color,
                          self.font_name, self.font_size_title, self.menu_title)
        self.main_play_button = Button(self.screen, self.mainPlayButtonPos, "PLAY", self.text_color, self.font_name, self.fontSizeButtonLarge, 0,
                                       self.menu_button, self.menu_button_hovered, self.menu_button_clicked, self.play_game)
        self.options_button = Button(self.screen, self.options_button_pos, "OPTIONS", self.text_color, self.font_name, self.fontSizeButtonSmall, 1,
                                     self.menu_button, self.menu_button_hovered, self.menu_button_clicked, self.options_menu)
        self.exit_button = Button(self.screen, self.exit_button_pos, "EXIT", self.text_color, self.font_name, self.fontSizeButtonLarge, 2,
                                  self.menu_button, self.menu_button_hovered, self.menu_button_clicked, self.quit_game)
        self.main_elements = [self.title,
                              self.main_play_button,
                              self.options_button,
                              self.exit_button]

        # options menu elements
        self.optionsPlayButtonPos = (self.width/2, self.height/4-64)
        self.difficulty_text_pos = (
            self.width/2, self.optionsPlayButtonPos[1]+96)
        self.difficulty_selector_pos = (
            self.width/2, self.difficulty_text_pos[1]+64)
        self.darkModeButtonPos = (
            self.width/2, self.difficulty_selector_pos[1]+96)
        self.back_button_pos = (self.width/2, self.darkModeButtonPos[1]+96)

        self.difficulty_selector_labels = ["EASY", "MEDIUM", "HARD", "CUSTOM"]
        self.difficulty_selector_state = 0

        self.options_play_button = Button(self.screen, self.optionsPlayButtonPos, "PLAY", self.text_color, self.font_name, self.fontSizeButtonLarge, 0,
                                          self.menu_button, self.menu_button_hovered, self.menu_button_clicked, self.play_game)
        self.difficulty_text = Text(self.screen, self.difficulty_text_pos, "DIFFICULTY", self.text_color,
                                    self.font_name, self.fontSizeButtonSmall, self.menu_button_large)
        self.difficulty_selector = Selector(self.screen, self.difficulty_selector_pos, self.difficulty_selector_labels, self.text_color,
                                            self.font_name, self.fontSizeButtonSmall, 1, self.menu_button, self.menu_button_small, self.menuButtonSmallHovered,
                                            self.menuButtonSmallClicked, self.change_difficulty_down, self.change_difficulty_up)
        self.custom_button = Button(self.screen, self.difficulty_selector_pos, "CUSTOM", self.text_color, self.font_name, self.fontSizeButtonSmall,
                                    1, self.menu_button, self.menu_button_hovered, self.menu_button_clicked, self.custom_size_menu)
        self.dark_mode_button = Button(self.screen, self.darkModeButtonPos, "DARK MODE", self.text_color, self.font_name, self.fontSizeButtonSmall,
                                       2, self.menu_button_large, self.menuButtonLargeHovered, self.menuButtonLargeClicked, self.change_theme)
        self.back_button = Button(self.screen, self.back_button_pos, "BACK", self.text_color, self.font_name, self.fontSizeButtonLarge,
                                  3, self.menu_button, self.menu_button_hovered, self.menu_button_clicked, self.main_menu)
        self.options_elements = [self.options_play_button,
                                 self.difficulty_text,
                                 self.difficulty_selector,
                                 self.custom_button,
                                 self.dark_mode_button,
                                 self.back_button]

        self.menu_elements = self.main_elements + self.options_elements

    def get_event(self, event):
        self.mouse_click = False
        self.mouse_released = True
        self.return_click = False
        self.return_released = True

        self.mouse_pos = pg.mouse.get_pos()

        if event.type == QUIT:
            self.quit = True

        elif event.type == KEYDOWN:
            if event.key == K_1:
                self.persist["difficulty"] = 0
            elif event.key == K_2:
                self.persist["difficulty"] = 1
            elif event.key == K_3:
                self.persist["difficulty"] = 2
            elif event.key == K_4:
                self.persist["difficulty"] = 3

            elif event.key == K_RETURN:
                self.return_click = True
                self.return_released = False

            elif event.key == K_DOWN:
                self.selected_button += 1
            elif event.key == K_UP:
                self.selected_button -= 1

        elif event.type == KEYUP:
            if event.key == K_RETURN:
                self.return_released = True

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                self.mouse_click = True
                self.mouse_released = False

        elif event.type == MOUSEBUTTONUP:
            if event.button == BUTTON_LEFT:
                self.mouse_released = True

    def draw(self, surface):
        for i in range(self.height//32):
           for j in range(self.width//32):
               self.screen.blit(self.tile_cell, (j*32, i*32))
        # self.screen.fill(self.background_color)

        if self.menu == "MAIN":
            self.selected_button = self.selected_button % 3

            self.title.draw()
            self.selected_button = self.main_play_button.draw(
                self.selected_button, self.return_click)
            self.selected_button = self.options_button.draw(
                self.selected_button, self.return_click)
            self.selected_button = self.exit_button.draw(
                self.selected_button, self.return_click)

        elif self.menu == "OPTIONS":
            self.selected_button = self.selected_button % 3

            self.selected_button = self.options_play_button.draw(
                self.selected_button, self.return_click)
            self.difficulty_text.draw()
            self.selected_button, self.difficulty_selector_state = self.difficulty_selector.draw(
                self.selected_button, self.return_click)
            if self.difficulty_selector_state == 3:
                self.selected_button = self.custom_button.draw(
                    self.selected_button, self.return_click)
            self.selected_button = self.dark_mode_button.draw(
                self.selected_button, self.return_click)
            self.selected_button = self.back_button.draw(
                self.selected_button, self.return_click)

            self.persist["difficulty"] = self.difficulty_selector_state

        elif self.menu == "CUSTOM":
            self.selected_button = self.options_play_button.draw(
                self.selected_button, self.return_click)
            self.selected_button = self.back_button.draw(
                self.selected_button, self.return_click)
        else:
            self.menu = "MAIN"

    def play_game(self):
        self.done = True

    def main_menu(self):
        self.menu = "MAIN"
        self.selected_button = 0

    def options_menu(self):
        self.menu = "OPTIONS"
        self.selected_button = 0

    def custom_size_menu(self):
        self.menu = "CUSTOM"
        self.selected_button = 0

    def quit_game(self):
        self.quit = True

    def change_difficulty_down(self):
        self.persist["difficulty"] -= 1
        self.persist["difficulty"] = self.persist["difficulty"] % 4

    def change_difficulty_up(self):
        self.persist["difficulty"] += 1
        self.persist["difficulty"] = self.persist["difficulty"] % 4

    def change_theme(self):
        self.persist["dark_theme"] = not self.persist["dark_theme"]

        if self.persist["dark_theme"]:
            theme = "dark"
            self.text_color = WHITE
            self.background_color = DARK_GRAY
        else:
            theme = "basic"
            self.text_color = BLACK
            self.background_color = LIGHT_GRAY

        self.tile_cell = pg.image.load(
            os.path.join("tiles", theme, "game", "cell.png"))

        self.menu_title = pg.image.load(
            os.path.join("tiles", theme, "menu", "title.png"))

        self.menu_button = pg.image.load(
            os.path.join("tiles", theme, "menu", "button.png"))
        self.menu_button_hovered = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_hovered.png"))
        self.menu_button_clicked = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_clicked.png"))

        self.menu_button_small = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_small.png"))
        self.menuButtonSmallHovered = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_small_hovered.png"))
        self.menuButtonSmallClicked = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_small_clicked.png"))

        self.menu_button_large = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_large.png"))
        self.menuButtonLargeHovered = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_large_hovered.png"))
        self.menuButtonLargeClicked = pg.image.load(
            os.path.join("tiles", theme, "menu", "button_large_clicked.png"))
