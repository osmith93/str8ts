from board import Cell, Board

vertical = "vertical"
horizontal = "horizontal"


class Game:
    EMPTY = 0
    BLOCKED = True

    def __init__(self, size=9):
        self.size = size
        self.board = Board(size)
        self.selected_cell = None

    def load(self, filename):
        """
        Load game state from `filename'.
        :param filename:  str
        """
        self.board.load(filename)

    def save(self, filename):
        """Save a game state to file."""
        pass
