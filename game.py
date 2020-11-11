from game_elements import Cell, Board

vertical = "vertical"
horizontal = "horizontal"


class Game:
    EMPTY = 0
    BLOCKED = True

    def __init__(self, size=9):
        self.size = size
        self.board = Board(size)

    def load(self, filename):
        """
        Load game state from `filename'.
        :param filename:  str
        """
        self.board.load(filename)

    def save(self, filename):
        """Save a game state to file."""
        pass

    def check(self):
        pass

    def get_cell(self, pos: tuple) -> Cell:
        """
        Returns the contents of a cell.
        :param pos: tuple
        :return: Box
        """
        return self.board.get_cell(pos)

    def get_guesses(self, pos: tuple) -> list:
        """
        Returns the guesses of a cell.
        :param pos: tuple
        :return: list
        """
        return self.board.get_cell(pos).guesses

    def is_blocked(self, pos: tuple) -> bool:
        """
        Returns whether the cell is blocked.
        :type pos: tuple
        """
        return self.board.get_cell(pos).is_blocked

    def is_empty(self, pos: tuple) -> bool:
        """
        Checks if cell is empty.
        :param pos: tuple
        :return: bool
        """
        return self.get_cell(pos).is_empty

    def set_to_number(self, pos: tuple, value: int):
        """
        Sets cell to number.
        :param pos: 
        :param value: 
        """
        self.board.get_cell(pos).value = value

    def remove_guess(self, pos: tuple, value: int):
        """
        Remove `value` from the list of guesses in `cell`.
        :param pos:
        :param value:
        """
        self.board.get_cell(pos).remove_guess(value)

    def unique_guess_left(self, pos):
        return self.board.get_cell(pos).unique_guess_left()
