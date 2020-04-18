import json
import os
from configuration import DATA_PATH


def create_data_file():
    """create an empty data file if there isn't one already"""
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'w'): pass


class GamesDataHandler(object):
    """ handles saving & reading game's data """
    @staticmethod
    def add(data: dict):
        """ add current game's information to the data file """
        create_data_file()
        with open(DATA_PATH, "a") as file:
            to_write = json.dumps(data) + '\n'
            file.write(to_write)

    @staticmethod
    def get(path=None):
        """ get all data from previous games"""
        create_data_file()
        with open(path if path else DATA_PATH, 'r') as f:
            data = f.readlines()
            return [json.loads(line) for line in data]
