# ---------------------------------------------------------------- #

import random

from constants import *

# ---------------------------------------------------------------- #

class Snake:

    def __init__(self):

        self.direction = random.choice(directions)

        self.fields = [random.choice(grid)]
        self.fields.insert(0, self.new_tile(self.direction_opposite))

    @property
    def direction_opposite(self):
        return direction_opposite_dict[self.direction]

    @property
    def body(self):
        return self.fields[:-1]

    @property
    def head(self):
        return self.fields[-1]

    def new_tile(self, direction=None):

        if direction is None: direction = self.direction

        x, y = self.head

        if direction == "up":    y = (y - 1) % HEIGHT
        if direction == "down":  y = (y + 1) % HEIGHT
        if direction == "left":  x = (x - 1) % WIDTH
        if direction == "right": x = (x + 1) % WIDTH

        return x, y

    def move(self, eat):

        new_tile = self.new_tile()

        if new_tile in self.fields:
            return False
        else:
            self.fields.append(new_tile)
            if not eat: self.fields.pop(0)
            return True

class Board:

    def __init__(self):

        self.snake = Snake()

        self.spawn_food()

    def spawn_food(self):
        self.food = random.choice([field for field in grid if field not in self.snake.body])

class Game:

    def __init__(self, screen, images, sounds):

        self.screen = screen
        self.images = images
        self.sounds = sounds

        self.board = Board()
        self.run = True
        self.arrows_statuses = {direction: "unclicked" for direction in directions}

        self.pause = False
        self.mute = False

    def get_arrow_status(self, direction):
        return self.arrows_statuses[direction]

    def set_arrow_status(self, direction, status):
        if self.board.snake.direction != direction_opposite_dict[direction]:
            self.arrows_statuses[direction] = status

    def coordinates_pixels(self, coordinates):
        x, y = coordinates
        return 180 + x * 30, 80 + y * 30

    @property
    def head(self):
        return self.coordinates_pixels(self.board.snake.head)

    def move(self):
        if not self.pause:

            new_tile = self.board.snake.new_tile()
            eat = new_tile == self.board.food
            self.run = self.board.snake.move(eat)

            if eat:
                if not self.mute: self.sounds["eat"].play()
                self.board.spawn_food()

    @property
    def score(self):
        return len(self.board.snake.fields) - 2

    def draw(self):

        if self.board.snake.direction in ["up", "down"]:
            self.screen.blit(self.images["arrows"][self.get_arrow_status("left")] ["left"],  (0, 0))
            self.screen.blit(self.images["arrows"][self.get_arrow_status("right")]["right"], (0, 0))
        if self.board.snake.direction in ["left", "right"]:
            self.screen.blit(self.images["arrows"][self.get_arrow_status("up")]   ["up"],    (0, 0))
            self.screen.blit(self.images["arrows"][self.get_arrow_status("down")] ["down"],  (0, 0))

        self.screen.blit(self.images["elements"]["head"], self.coordinates_pixels(self.board.snake.head))
        for body_element in self.board.snake.body:
            self.screen.blit(self.images["elements"]["body"], self.coordinates_pixels(body_element))

        self.screen.blit(self.images["food"], self.coordinates_pixels(self.board.food))

        self.screen.blit(pg.font.SysFont("comic sans bold", 64).render(str(self.score), True, pg.Color("black")), (1010, 80))

        if self.pause: self.screen.blit(self.images["pause"], (0, 0))
        if not self.mute: self.screen.blit(self.images["speaker"], (0, 0))

    def update(self, event):
        if not self.pause:

            for direction, status in self.arrows_statuses.items():
                if status == "clicked":
                    self.board.snake.direction = direction
                    if not self.mute: self.sounds["change direction"][random.choice([12, 15, 16, 18, 19, 20])].play()

            x, y = pg.mouse.get_pos()

            if 940 <= x <= 1260 and 255 <= y <= 395:
                if event.type == pg.MOUSEBUTTONDOWN: self.set_arrow_status("up", "clicked")
                if event.type == pg.MOUSEBUTTONUP:   self.set_arrow_status("up", "unclicked")
            if 940 <= x <= 1260 and 440 <= y <= 580:
                if event.type == pg.MOUSEBUTTONDOWN: self.set_arrow_status("down", "clicked")
                if event.type == pg.MOUSEBUTTONUP:   self.set_arrow_status("down", "unclicked")
            if 950 <= x <= 1090 and 270 <= y <= 590:
                if event.type == pg.MOUSEBUTTONDOWN: self.set_arrow_status("left", "clicked")
                if event.type == pg.MOUSEBUTTONUP:   self.set_arrow_status("left", "unclicked")
            if 1130 <= x <= 1280 and 270 <= y <= 590:
                if event.type == pg.MOUSEBUTTONDOWN: self.set_arrow_status("right", "clicked")
                if event.type == pg.MOUSEBUTTONUP:   self.set_arrow_status("right", "unclicked")

            if event.type == pg.KEYDOWN:
                for key, direction in zip([pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT] + [pg.K_w, pg.K_s, pg.K_a, pg.K_d], directions*2):
                    if event.key == key: self.set_arrow_status(direction, "clicked")
            elif event.type == pg.KEYUP:
                for key, direction in zip([pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT] + [pg.K_w, pg.K_s, pg.K_a, pg.K_d], directions*2):
                    if event.key == key: self.set_arrow_status(direction, "unclicked")

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: self.pause = not self.pause
            if event.key == pg.K_m: self.mute = not self.mute

# ---------------------------------------------------------------- #
