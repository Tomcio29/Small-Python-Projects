import argparse
import logging
import os
from configparser import ConfigParser
from wolf import Wolf
from sheep_manager import SheepManager
from data_manager import DataManager


def check_positive(value):
    amount = int(value)
    if amount <= 0:
        raise argparse.ArgumentTypeError("%s value must be positive" % value)
    return amount


def check_file_existence(file):
    if not os.path.exists(file):
        raise argparse.ArgumentTypeError("The config file %s not found!" % file)
    return file


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="set config file", action='store',
                        type=check_file_existence, dest='conf_file', metavar='FILE')
    parser.add_argument('-l', '--log', action='store', help="create log file with log LEVEL", dest='log_lvl',
                        metavar='LEVEL')
    parser.add_argument('-r', '--rounds', action='store',
                        help="choose amount of rounds", dest='amount_of_rounds',
                        type=check_positive, metavar='NUM')
    parser.add_argument('-s', '--sheep', action='store',
                        help="choose amount of sheep", dest='amount_of_sheep', type=check_positive,
                        metavar='NUM')
    parser.add_argument('-w', '--wait', action='store_true', help="wait for input after each round")
    args = parser.parse_args()
    return args


def parse_config(file):
    config = ConfigParser()
    config.read(file)
    init = float(config.get('Sheep', 'InitPosLimit'))
    sheep = float(config.get('Sheep', 'MoveDist'))
    wolf = float(config.get('Wolf', 'MoveDist'))
    if init < 0 or sheep < 0 or wolf < 0:
        raise ValueError("Arguments are not positive numbers")
    return init, sheep, wolf


def run_simulation(amount_of_sheep, amount_of_rounds, init_pos_limit, sheep_move_dist, wolf_move_dist, wait):
    sheep_manager = SheepManager(amount_of_sheep, init_pos_limit)
    wolf = Wolf(wolf_move_dist)
    data_exporter = DataManager()

    for i in range(amount_of_rounds):
        print("")
        logging.info("Round: " + str(i + 1))
        print("Round: ", i + 1)
        if not sheep_manager.check_alive():
            alive = sheep_manager.count_alive()
            data_exporter.to_csv(i + 1, alive)
            data_exporter.to_json(sheep_manager.sheep_array, wolf, i)
            print("No sheep alive")
            break
        sheep_manager.make_turn(sheep_move_dist)
        wolf.make_turn(sheep_manager.sheep_array)
        alive = sheep_manager.count_alive()
        data_exporter.to_json(sheep_manager.sheep_array, wolf, i+1)
        data_exporter.to_csv(i + 1, alive)
        print("")
        print("Alive Sheep: ", alive)
        print("-------------------------------")
        if wait:
            logging.debug("Waiting for user")
            input("Press a key to continue...")
    if not sheep_manager.check_alive():
        logging.info("Simulation ended, all Sheep eaten.")
    else:
        logging.info("Simulation ended, maximum number of rounds has been reached")


def main():
    amount_of_sheep = 15
    amount_of_rounds = 50
    init_pos_limit = 10
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    wait = False
    args = parse_arguments()
    if args.log_lvl:
        log_levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        try:
            lvl = log_levels[args.log_lvl.lower()]
        except KeyError:
            raise ValueError("Invalid log level!")
        logging.basicConfig(level=lvl, filename="./chase.log", filemode='w', force=True)
    if args.conf_file:
        init_pos_limit, sheep_move_dist, wolf_move_dist = parse_config(args.conf_file)
        logging.debug("Values from configuration file loaded: init_pos_limit "+str(init_pos_limit)
                      + ", sheep_move_dist: " + str(sheep_move_dist) + " , wolf_move_dist "
                      + str(wolf_move_dist))
    if args.amount_of_rounds:
        amount_of_rounds = args.amount_of_rounds
    if args.amount_of_sheep:
        amount_of_sheep = args.amount_of_sheep
    if args.wait:
        wait = args.wait
    run_simulation(amount_of_sheep, amount_of_rounds, init_pos_limit, sheep_move_dist, wolf_move_dist, wait)


main()
