

class AutomatonFrame(object):
    """
    iterable that contains the cell-automation frame (& more info) at every iteration.
    """
    def __init__(self, game):
        """
        game - type CellAutomatonGameBase.
        """
        self.game = game

    def get_board(self):
        return self.game.get_board()

    def __iter__(self):
        return self

    def __next__(self):
        self.game.update_board()
        return self
