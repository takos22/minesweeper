import pygame as pg
from pygame.locals import *


class Menu(object):
    def __init__(self, screen, size, text_color: tuple, font_name: str):
        self.screen = screen
        self.size = size
        self.text_color = text_color
        self.font_name = font_name

        self.button_index = 0

        self.elements = {}
        self.texts = {}
        self.buttons = {}
        self.selectors = {}

    def get_event(self, event):
        if self.texts:
            for text in self.texts.values:
                text.get_event(event)

        if self.buttons:
            for button in self.buttons.values:
                button.get_event(event)

        if self.selectors:
            for selector in self.selectors.values:
                selector.get_event(event)

    def draw(self):
        if self.texts:
            for text in self.texts.values:
                text.draw()

        if self.buttons:
            for button in self.buttons.values:
                button.draw()

        if self.selectors:
            for selector in self.selectors.values:
                selector.draw()

    def add_text(self, name: str, pos_center: tuple, label: str, font_size: int, sprite=None):
        new_text = Text(self.screen, pos_center, label, self.text_color,
                        self.font_name, font_size, sprite)
        self.elements[name] = new_text
        self.texts[name] = new_text

    def add_button(self, name: str, pos_center: tuple, label: str, font_size: int,
                   sprite_inactive, sprite_hovered, sprite_clicked, on_click):
        new_button = Button(self.screen, pos_center, label, self.text_color, self.font_name,
                            font_size, self.button_index, sprite_inactive, sprite_hovered,
                            sprite_clicked, on_click)
        self.button_index += 1
        self.elements[name] = new_button
        self.buttons[name] = new_button

    def add_selector(self, name: str, pos_center: tuple, labels: list, font_size: int,
                     sprite_text, sprite_inactive, sprite_hovered, sprite_clicked,
                     on_left_click, on_right_click):
        new_selector = Selector(self.screen, pos_center, labels, self.text_color, self.font_name,
                                font_size, self.button_index, sprite_text, sprite_inactive,
                                sprite_hovered, sprite_clicked, on_left_click, on_right_click)
        self.button_index += 1
        self.elements[name] = new_selector
        self.selectors[name] = new_selector


class Element(object):
    def __init__(self, screen, pos_center: tuple, label: str, text_color: tuple, font_name: str, font_size: int):
        self.screen = screen
        self.pos_center = pos_center
        self.label = label
        self.text_color = text_color
        self.font_name = font_name
        self.font_size = font_size
        self.font = pg.font.Font(self.font_name, self.font_size)

        self.mouse_click = False
        self.mouse_released = True
        self.return_click = False
        self.return_released = True

    def get_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
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

    def draw(self):
        pass

    def set_label(self, new_label):
        self.label = new_label

    def set_text_color(self, new_text_color):
        self.text_color = new_text_color


class Text(Element):
    def __init__(self, screen, pos_center: tuple, label: str, text_color: tuple, font_name: str, font_size: int, sprite=None):
        super(Text, self).__init__(screen, pos_center, label, text_color,
                                   font_name, font_size)

        self.text = self.font.render(self.label, False, self.text_color)
        self.text_pos = self.text.get_rect()
        self.text_pos.center = self.pos_center

        if sprite:
            self.is_sprite_set = True
            self.sprite = sprite
            self.sprite_pos = self.sprite.get_rect()
            self.sprite_pos.center = self.pos_center
        else:
            self.is_sprite_set = False

    def draw(self, *args):
        if self.is_sprite_set:
            self.screen.blit(self.sprite, self.sprite_pos)
        self.screen.blit(self.text, self.text_pos)

    def set_label(self, new_label):
        super(Text, self).set_label(new_label)

        self.text = self.font.render(self.label, False, self.text_color)
        self.text_pos = self.text.get_rect()
        self.text_pos.center = self.pos_center

    def set_text_color(self, new_text_color):
        super(Text, self).set_text_color(new_text_color)

        self.text = self.font.render(self.label, False, self.text_color)

    def set_text_sprite(self, new_sprite):
        self.is_sprite_set = True
        self.sprite = new_sprite
        self.sprite_pos = self.sprite.get_rect()
        self.sprite_pos.center = self.pos_center


class Button(Element):
    def __init__(self, screen, pos_center: tuple, label: str, text_color: tuple,
                 font_name: str, font_size: int, button_index: int, sprite_inactive,
                 sprite_hovered, sprite_clicked, on_click):
        super(Button, self).__init__(screen, pos_center, label, text_color,
                                     font_name, font_size)

        self.button_index = button_index
        self.sprite_inactive = sprite_inactive
        self.sprite_hovered = sprite_hovered
        self.sprite_clicked = sprite_clicked
        self.on_click = on_click

        self.text = Text(self.screen, self.pos_center, self.label, self.text_color,
                         self.font_name, self.font_size, self.sprite_inactive)

    def draw(self, selected_button_index, is_return_clicked):
        mouse_pos = pg.mouse.get_pos()
        clicked = pg.mouse.get_pressed()
        if self.text.sprite_pos.collidepoint(mouse_pos) or selected_button_index == self.button_index:
            hovered = True
        else:
            hovered = False

        if hovered:
            if (clicked[0] and self.text.sprite_pos.collidepoint(mouse_pos)) or is_return_clicked:
                self.screen.blit(self.sprite_clicked, self.text.sprite_pos)
                self.on_click()
            else:
                self.screen.blit(self.sprite_hovered, self.text.sprite_pos)
        else:
            self.screen.blit(self.sprite_inactive, self.text.sprite_pos)

        self.screen.blit(self.text.text, self.text.text_pos)

        if hovered:
            return self.button_index
        else:
            return selected_button_index


class Selector(Element):
    def __init__(self, screen, pos_center: tuple, labels: list, text_color: tuple,
                 font_name: str, font_size: int, button_index: int, sprite_text, sprite_inactive,
                 sprite_hovered, sprite_clicked, on_left_click, on_right_click):
        super(Selector, self).__init__(screen, pos_center, labels[0], text_color,
                                       font_name, font_size)

        self.labels = labels
        self.states = len(self.labels)
        self.state = 0
        self.label = self.labels[self.state]
        self.button_index = button_index

        self.sprite_text = sprite_text
        self.sprite_inactive = sprite_inactive
        self.sprite_hovered = sprite_hovered
        self.sprite_clicked = sprite_clicked

        self.on_left_click = on_left_click
        self.on_right_click = on_right_click

        self.text = Text(self.screen, self.pos_center, self.label, self.text_color,
                         self.font_name, self.font_size, self.sprite_text)

        self.left_button_pos = (self.text.sprite_pos.left-32,
                                self.text.sprite_pos.centery)
        self.left_button = Button(self.screen, self.left_button_pos, "<", self.text_color, self.font_name, self.font_size,
                                  self.button_index, self.sprite_inactive, self.sprite_hovered, self.sprite_clicked, self.left_click)

        self.right_button_pos = (self.text.sprite_pos.right+32,
                                 self.text.sprite_pos.centery)
        self.right_button = Button(self.screen, self.right_button_pos, ">", self.text_color, self.font_name, self.font_size,
                                   self.button_index, self.sprite_inactive, self.sprite_hovered, self.sprite_clicked, self.right_click)

    def draw(self, selected_button_index, is_return_clicked):
        self.text.draw()
        selected_button = self.left_button.draw(
            selected_button_index, is_return_clicked)
        selected_button = self.right_button.draw(
            selected_button_index, is_return_clicked)
        return selected_button, self.state

    def left_click(self):
        self.state = (self.state-1) % self.states
        self.text.set_label(self.labels[self.state])
        self.on_left_click

    def right_click(self):
        self.state = (self.state+1) % self.states
        self.text.set_label(self.labels[self.state])
        self.on_right_click
