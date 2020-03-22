import os
from random import choice

import pygame as pg
from pygame.locals import *

from GameState import *
from Cell import *


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.next_state = "MAINMENU"

    def startup(self, persistent: dict):
        self.persist = persistent

        difficulty = self.persist["difficulty"]
        dark_theme = self.persist["dark_theme"]

        self.cell_size = 32

        easy = (9, 9, 10)
        medium = (16, 16, 40)
        hard = (30, 16, 99)
        custom = (self.persist["cols"],
                  self.persist["rows"],
                  self.persist["mines"])
        difficulty_levels = [easy, medium, hard, custom]
        self.cols, self.rows, self.mines = difficulty_levels[difficulty]

        self.size = (self.cols*self.cell_size, self.rows*self.cell_size)
        self.screen = pg.display.set_mode(self.size)

        self.pos_click = (0, 0)
        self.new_click = False
        self.first_click = True
        self.reveal_cell = False
        self.flag_cell = False

        self.board = []
        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                line.append(Cell(i, j, self.cell_size))
            self.board.append(line)
        self.cells_with_mines = []

        if dark_theme:
            theme = "dark"
        else:
            theme = "basic"

        self.tile1 = pg.image.load(
            os.path.join("tiles", theme, "game", '1.png'))
        self.tile2 = pg.image.load(
            os.path.join("tiles", theme, "game", '2.png'))
        self.tile3 = pg.image.load(
            os.path.join("tiles", theme, "game", '3.png'))
        self.tile4 = pg.image.load(
            os.path.join("tiles", theme, "game", '4.png'))
        self.tile5 = pg.image.load(
            os.path.join("tiles", theme, "game", '5.png'))
        self.tile6 = pg.image.load(
            os.path.join("tiles", theme, "game", '6.png'))
        self.tile7 = pg.image.load(
            os.path.join("tiles", theme, "game", '7.png'))
        self.tile8 = pg.image.load(
            os.path.join("tiles", theme, "game", '8.png'))

        self.tile_cell = pg.image.load(
            os.path.join("tiles", theme, "game", 'cell.png'))
        self.tile_empty = pg.image.load(
            os.path.join("tiles", theme, "game", 'empty.png'))
        self.tile_flag = pg.image.load(
            os.path.join("tiles", theme, "game", 'flag.png'))
        self.tile_mine = pg.image.load(
            os.path.join("tiles", theme, "game", 'mine.png'))
        self.tile_mine_click = pg.image.load(
            os.path.join("tiles", theme, "game", 'mine_click.png'))

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                self.pos_click = event.pos
                self.reveal_cell = True
                self.new_click = True
            elif event.button == BUTTON_RIGHT:
                self.pos_click = event.pos
                self.flag_cell = True
                self.new_click = True

    def update(self, dt: int):
        if self.new_click:
            self.new_click = False
            i = self.pos_click[1]//self.cell_size
            j = self.pos_click[0]//self.cell_size
            clicked_cell = self.board[i][j]

            if self.first_click and self.reveal_cell:
                self.first_click = False

                # Set mines
                self.cells_with_mines.append(clicked_cell)
                for i in range(-1, 2):
                    i = clicked_cell.i+i
                    for j in range(-1, 2):
                        j = clicked_cell.j+j
                        if not (i < 0 or i > self.rows-1 or j < 0 or j > self.cols-1):
                            cell = self.board[i][j]
                            self.cells_with_mines.append(cell)

                for i in range(self.mines):
                    while True:
                        cell = choice(choice(self.board))
                        if not cell in self.cells_with_mines:
                            cell.mine = True
                            self.cells_with_mines.append(cell)
                            break
                        else:
                            continue

                # Set the number of mines around each cell
                for i in range(self.rows):
                    for j in range(self.cols):
                        cell = self.board[i][j]
                        cell.mines_around_count(self.board)

            # Reveal the cell
            if self.reveal_cell:
                self.reveal_cell = False
                clicked_cell.reveal(self.board)

            # Flag the cell
            if self.flag_cell:
                self.flag_cell = False
                clicked_cell.flag()

        if self.game_ended():
            self.done = True

    def draw(self, surface):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.board[i][j]
                square = pg.Surface((self.cell_size, self.cell_size))

                if cell.flaged:
                    square.blit(self.tile_flag, (0, 0))
                elif not cell.revealed:
                    square.blit(self.tile_cell, (0, 0))
                elif cell.mine_clicked:
                    square.blit(self.tile_mine_click, (0, 0))
                elif cell.mine:
                    square.blit(self.tile_mine, (0, 0))
                else:
                    if cell.mines_around == 0:
                        square.blit(self.tile_empty, (0, 0))
                    elif cell.mines_around == 1:
                        square.blit(self.tile1, (0, 0))
                    elif cell.mines_around == 2:
                        square.blit(self.tile2, (0, 0))
                    elif cell.mines_around == 3:
                        square.blit(self.tile3, (0, 0))
                    elif cell.mines_around == 4:
                        square.blit(self.tile4, (0, 0))
                    elif cell.mines_around == 5:
                        square.blit(self.tile5, (0, 0))
                    elif cell.mines_around == 6:
                        square.blit(self.tile6, (0, 0))
                    elif cell.mines_around == 7:
                        square.blit(self.tile7, (0, 0))
                    elif cell.mines_around == 8:
                        square.blit(self.tile8, (0, 0))

                pos_square = cell.coord()
                self.screen.blit(square, pos_square)
        pg.display.flip()

    def game_ended(self) -> bool:
        not_revealed_cells = 0

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.board[i][j]
                if not cell.revealed:
                    not_revealed_cells += 1

        return True if not_revealed_cells <= self.mines else False
