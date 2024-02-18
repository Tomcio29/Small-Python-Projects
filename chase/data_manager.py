import csv
import json
import logging


class DataManager:
    def __init__(self):
        self.pos_file_path = "./pos.json"
        self.alive_file_path = "./alive.csv"

    def to_json(self, sheep_array, wolf, round_no):
        logging.debug("saved round" + str(round_no) + " data to json")
        round_data = {
            "round_no": round_no,
            "wolf_pos": (wolf.x, wolf.y),
            "sheep_pos": [(sheep.x, sheep.y) if sheep.status == "alive" else None for sheep in sheep_array]
        }
        if round_no == 1:
            existing_data = [round_data]
        else:
            with open(self.pos_file_path, "r") as f:
                existing_data = json.load(f)
                existing_data.append(round_data)
        with open(self.pos_file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

    def to_csv(self, round_no, sheep_no):
        logging.debug("saved round" + str(round_no) + " data to csv")
        if round_no == 1:
            with open(self.alive_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['round', 'alive']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerow({'round': round_no, 'alive': sheep_no})
        else:
            with open(self.alive_file_path, mode='a', newline='') as csv_file:
                fieldnames = ['round', 'alive']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
                writer.writerow({'round': round_no, 'alive': sheep_no})
