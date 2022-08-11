# ---------------------------------------------------------------- #

import time
import pygame as pg

from constants import *
from classes import *

# ---------------------------------------------------------------- #

pg.init()

pg.display.set_caption("Doodle-Snake")

screen = pg.display.set_mode((1280, 720))

icon = pg.image.load("icon.png")
pg.display.set_icon(icon)

# ---------------------------------------------------------------- #

game = Game(screen, images, sounds)

run = True
while run:

    pg.display.update()
    pg.time.delay(DELAY_GAME)

    screen.blit(background, (0, 0))
    game.draw()

    for event in pg.event.get():

        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): run = False

        game.update(event)

    if not game.run:
        time.sleep(1)
        run = False

    game.move()

pg.quit()

# ---------------------------------------------------------------- #
