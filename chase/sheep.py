import logging
import random


class Sheep:
    def __init__(self, sheep_nr, init_pos_limit):
        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.status = "alive"
        self.sheep_nr = sheep_nr + 1

    def move(self, sheep_move_dist):
        if self.status == "alive":
            direction = random.choice(['north', 'south', 'east', 'west'])

            if direction == 'north':
                self.y += sheep_move_dist
            if direction == 'south':
                self.y -= sheep_move_dist
            if direction == 'east':
                self.x += sheep_move_dist
            if direction == 'west':
                self.x -= sheep_move_dist
            logging.debug("Sheep" + str(self.sheep_nr) + " chosen to move " + str(direction))
