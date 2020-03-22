import pygame as pg

from Game import *
from Gameplay import *
from MainMenu import *

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((0, 0))

    icon = pg.image.load("icon.png").convert_alpha()
    pg.display.set_icon(icon)
    pg.display.set_caption("Minesweeper")

    states = {"MAINMENU": MainMenu(),
              "GAMEPLAY": Gameplay()}
    game = Game(screen, states, "MAINMENU")
    game.run()
    pg.quit()
