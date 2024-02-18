import logging
from sheep import Sheep


class SheepManager:
    def __init__(self, amount_of_sheep, init_pos_limit):
        self.sheep_array = []
        for i in range(amount_of_sheep):
            sheep = Sheep(i, init_pos_limit)
            self.sheep_array.append(sheep)
            logging.debug("Initial position sheep: " + str(self.sheep_array[i].sheep_nr) + " X " +
                          str(round(self.sheep_array[i].x, 3)) + " Y " + str(round(self.sheep_array[i].y, 3)))
        logging.info("Sheep positions determined")

    def check_alive(self):
        alive = False
        for sheep in self.sheep_array:
            if sheep.status == "alive":
                alive = True
                break
        if not alive:
            logging.warning("There is no sheep alive")
        else:
            logging.debug("There are sheep alive")
        return alive

    def count_alive(self):
        alive = 0
        for sheep in self.sheep_array:
            if sheep.status == "alive":
                alive = alive + 1
        logging.info("Alive sheep : " + str(alive))
        return alive

    def make_turn(self, sheep_move_dist):
        for sheep in self.sheep_array:
            sheep.move(sheep_move_dist)
            if sheep.status == "alive":
                print("Sheep", sheep.sheep_nr, " X ", round(sheep.x, 3), " Y ", round(sheep.y, 3))
                logging.debug(
                    "Sheep " + str(sheep.sheep_nr) + " X " + str(round(sheep.x, 3)) + " Y " + str(round(sheep.y, 3)))
            else:
                print("Sheep", sheep.sheep_nr, "EATEN")
                logging.info("Sheep: " + str(sheep.sheep_nr) + " EATEN")
        logging.info("All Sheep moved")
