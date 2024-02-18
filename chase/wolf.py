import logging
import math


class Wolf:
    def __init__(self, wolf_move_distance):
        self.x = 0
        self.y = 0
        self.wolf_move_distance = wolf_move_distance

    def make_turn(self, sheep_array):
        nearest_num, distance = self.count_euclidean_distance(sheep_array)
        nearest_sheep = sheep_array[nearest_num-1]
        self.move(nearest_sheep, distance)
        logging.info("WOLF moved")
        if nearest_sheep.status == "eaten":
            logging.info("WOLF : EATEN SHEEP " + str(nearest_sheep.sheep_nr))
        else:
            logging.info("WOLF : Chasing Sheep " + str(nearest_sheep.sheep_nr))
            logging.debug("WOLF new position " + str(round(self.x, 3)) + " , " + str(round(self.y, 3)))

    def count_euclidean_distance(self, sheep_array):
        # Ensure that minimal_distance is out of wolf's range at beginning of simulation
        minimal_distance = 100
        sheep_no = 0
        for sheep in sheep_array:
            if sheep.status == "alive":
                distance = math.sqrt((sheep.x - self.x) ** 2 + (sheep.y - self.y) ** 2)
                if distance < minimal_distance:
                    minimal_distance = distance
                    sheep_no = sheep.sheep_nr
        logging.debug("Minimal distance from the wolf " + str(minimal_distance) + " Sheep " + str(sheep_no))
        return [sheep_no, minimal_distance]

    def move(self, sheep, distance):
        print("")
        if distance < 1.0:
            self.x = sheep.x
            self.y = sheep.y
            sheep.status = "eaten"
            sheep.x = None
            sheep.y = None
            print("WOLF : EATEN SHEEP", sheep.sheep_nr)
        else:
            new_x = (sheep.x - self.x) * self.wolf_move_distance / distance
            new_y = (sheep.y - self.y) * self.wolf_move_distance / distance
            self.x += new_x
            self.y += new_y
            print("WOLF : Chasing Sheep ", sheep.sheep_nr)
        print("WOLF", round(self.x, 3), round(self.y, 3))
