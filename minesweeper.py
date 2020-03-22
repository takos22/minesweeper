import os
from random import choice

import pygame as pg
from pygame.locals import *

from Cell import *


def minesweeper(difficulty: int, dark_theme: bool = False):
    """Minesweeper game

    difficulty:
    - 0: easy
    - 1: medium
    - 2: hard

    *dark_theme:
    - True: activate dark theme
    - False: don't activate dark theme
    """

    # Variables
    pos_click = (0, 0)
    new_click = False
    first_click = True
    reveal_cell = False
    flag_cell = False

    easy = (9, 9, 10)
    medium = (16, 16, 40)
    hard = (30, 16, 99)
    difficulty_levels = [easy, medium, hard]
    cols, rows, mines = difficulty_levels[difficulty]

    cell_size = 32
    board = []
    cells_with_mines = []

    size = (cols*cell_size, rows*cell_size)

    # Tiles
    if dark_theme:
        theme = "dark"
    else:
        theme = "basic"

    tile1 = pg.image.load(os.path.join("tiles", theme, '1.png'))
    tile2 = pg.image.load(os.path.join("tiles", theme, '2.png'))
    tile3 = pg.image.load(os.path.join("tiles", theme, '3.png'))
    tile4 = pg.image.load(os.path.join("tiles", theme, '4.png'))
    tile5 = pg.image.load(os.path.join("tiles", theme, '5.png'))
    tile6 = pg.image.load(os.path.join("tiles", theme, '6.png'))
    tile7 = pg.image.load(os.path.join("tiles", theme, '7.png'))
    tile8 = pg.image.load(os.path.join("tiles", theme, '8.png'))

    tile_cell = pg.image.load(os.path.join("tiles", theme, 'cell.png'))
    tile_empty = pg.image.load(os.path.join("tiles", theme, 'empty.png'))
    tile_flag = pg.image.load(os.path.join("tiles", theme, 'flag.png'))
    tile_mine = pg.image.load(os.path.join("tiles", theme, 'mine.png'))
    tile_mine_click = pg.image.load(
        os.path.join("tiles", theme, 'mine_click.png'))

    # Board
    for i in range(rows):
        line = []
        for j in range(cols):
            line.append(Cell(i, j, cell_size))
        board.append(line)

    # -------------------------------------------------------------------------
    # Pygame window init

    pg.init()

    window = pg.display.set_mode(size)

    icon = pg.image.load("icon.png").convert_alpha()
    pg.display.set_icon(icon)
    pg.display.set_caption("Minesweeper")

    # ---------------------------------
    # Game display

    # Draw each cell
    for i in range(rows):
        for j in range(cols):
            cell = board[i][j]
            pos_square = cell.coord()

            square = pg.Surface((cell_size, cell_size))
            square.blit(tile_cell, (0, 0))

            window.blit(square, pos_square)
    pg.display.flip()

    while not game_ended(board, mines):
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    pos_click = event.pos
                    reveal_cell = True
                    new_click = True
                elif event.button == BUTTON_RIGHT:
                    pos_click = event.pos
                    flag_cell = True
                    new_click = True

            if new_click:
                new_click = False
                i = pos_click[1]//cell_size
                j = pos_click[0]//cell_size
                clicked_cell = board[i][j]

                if first_click and reveal_cell:
                    first_click = False

                    # Set mines
                    cells_with_mines.append(clicked_cell)
                    for i in range(-1, 2):
                        i = clicked_cell.i+i
                        for j in range(-1, 2):
                            j = clicked_cell.j+j
                            if not (i < 0 or i > rows-1 or j < 0 or j > cols-1):
                                cell = board[i][j]
                                cells_with_mines.append(cell)

                    for i in range(mines):
                        while True:
                            cell = choice(choice(board))
                            if not cell in cells_with_mines:
                                cell.mine = True
                                cells_with_mines.append(cell)
                                break
                            else:
                                continue

                    # Set the number of mines around each cell
                    for i in range(rows):
                        for j in range(cols):
                            cell = board[i][j]
                            cell.mines_around_count(board)

                # Reveal the cell
                if reveal_cell:
                    reveal_cell = False
                    clicked_cell.reveal(board)

                # Flag the cell
                if flag_cell:
                    flag_cell = False
                    clicked_cell.flag()

                # Draw each cell
                for i in range(rows):
                    for j in range(cols):
                        cell = board[i][j]
                        square = pg.Surface((cell_size, cell_size))

                        if cell.flaged:
                            square.blit(tile_flag, (0, 0))
                        elif not cell.revealed:
                            square.blit(tile_cell, (0, 0))
                        elif cell.mine_clicked:
                            square.blit(tile_mine_click, (0, 0))
                        elif cell.mine:
                            square.blit(tile_mine, (0, 0))
                        else:
                            if cell.mines_around == 0:
                                square.blit(tile_empty, (0, 0))
                            elif cell.mines_around == 1:
                                square.blit(tile1, (0, 0))
                            elif cell.mines_around == 2:
                                square.blit(tile2, (0, 0))
                            elif cell.mines_around == 3:
                                square.blit(tile3, (0, 0))
                            elif cell.mines_around == 4:
                                square.blit(tile4, (0, 0))
                            elif cell.mines_around == 5:
                                square.blit(tile5, (0, 0))
                            elif cell.mines_around == 6:
                                square.blit(tile6, (0, 0))
                            elif cell.mines_around == 7:
                                square.blit(tile7, (0, 0))
                            elif cell.mines_around == 8:
                                square.blit(tile8, (0, 0))

                        pos_square = cell.coord()
                        window.blit(square, pos_square)
                pg.display.flip()


def game_ended(board,mines) -> bool:
        rows = len(board)
        cols = len(board[0])
        not_revealed_cells = 0

        for i in range(rows):
            for j in range(cols):
                cell = board[i][j]
                if not cell.revealed:
                    not_revealed_cells += 1

        return True if not_revealed_cells <= mines else False

if __name__ == "__main__":
    difficulty = 0
    dark_theme = False
    minesweeper(difficulty, dark_theme)
