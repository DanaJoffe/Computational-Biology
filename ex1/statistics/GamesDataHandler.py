import json
import os
from configuration import DATA_PATH


def create_data_file():
    """create an empty data file if there isn't one already"""
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'w'): pass


class GamesDataHandler(object):
    @staticmethod
    def add(data: dict):
        create_data_file()
        with open(DATA_PATH, "a") as file:
            to_write = json.dumps(data) + '\n'
            file.write(to_write)

    @staticmethod
    def get(path=None):
        create_data_file()
        with open(path if path else DATA_PATH, 'r') as f:
            data = f.readlines()
            return [json.loads(line) for line in data]
