# ---------------------------------------------------------------- #

import itertools
import pygame as pg

# ---------------------------------------------------------------- #

DELAY_GAME = 10
DELAY_SNAKE = 0.25

WIDTH  = 21
HEIGHT = 19

grid = list(itertools.product(range(WIDTH), range(HEIGHT)))

statuses = ["clicked", "unclicked"]
directions = ["up", "down", "left", "right"]
direction_opposite_dict = {
    "up":   "down",  "down":  "up",
    "left": "right", "right": "left",
}

background = pg.image.load("images//background.png")
arrows = {status: {direction: pg.image.load(f"images//arrow_{status}_{direction}.png") for direction in directions} for status in statuses}
elements = {
    "body": pg.image.load("images//element_body.png"),
    "head": pg.image.load("images//element_head.png"),
}
food = pg.image.load("images//food.png")
pause = pg.image.load("images//pause.png")
speaker = pg.image.load("images//speaker.png")
images = {
    "background": background,
    "arrows": arrows,
    "elements": elements,
    "food": food,
    "pause": pause,
    "speaker": speaker,
}

pg.mixer.init()

sounds = {
    "eat": pg.mixer.Sound("sounds//eat.mp3"),
    "change direction": {i: pg.mixer.Sound(f"sounds//page-flip-{i}.mp3") for i in [12, 15, 16, 18, 19, 20]},
}

# ---------------------------------------------------------------- #
