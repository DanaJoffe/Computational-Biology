from statistics.GamesDataHandler import GamesDataHandler

"""
todo: calc % of infected creatures for timestep t
todo: calc infection rate = disease spreading rate
todo: look for K that enables linear growth and not exponential growth.
"""

if __name__ == '__main__':
    # get all data from all saved games in json format
    all_data = GamesDataHandler.get()
