from utils import Utils
from typing import List


class Cell:
    EMPTY = 0

    def __init__(self, pos: tuple, blocked: bool, size: int, value: int):
        self.pos = pos
        self.is_blocked = blocked
        self.value = value
        self.guesses = [i for i in range(1, size + 1)]

    def remove_guess(self, value: int) -> bool:
        """Tries removing value from the `self.guesses`. Returns `True` if successful."""
        if value in self.guesses:
            self.guesses.remove(value)
            return True
        return False

    def remove_guess_set(self, value_set: set) -> bool:
        """Tries removing all values in `value_set` from self.guesses. Returns `True` if any were removed."""
        result = False
        for value in value_set:
            success = self.remove_guess(value)
            result = result or success
        return result

    def unique_guess_left(self) -> bool:
        """Returns whether there is only one possible guess left."""
        return len(self.guesses) == 1

    def try_filling_unique_guess(self) -> bool:
        """Fills the cell if only one possible value is left. Returns `True` if successful."""
        if self.is_blocked:
            raise Exception(f'Trying to write to blocked cell at position {self.pos}".')
        if self.unique_guess_left():
            self.value = self.guesses[0]
            return True
        return False

    def __repr__(self):
        return repr(self.pos)

    @property
    def is_empty(self) -> bool:
        return self.value == Cell.EMPTY


class Board:
    def __init__(self, size: int):
        self.size = size
        self.all_pos = [(x, y) for x in range(size) for y in range(size)]
        self.grid = {pos: Cell(pos, blocked=False, size=size, value=Cell.EMPTY) for pos in self.all_pos}

    def load(self, filename: str):
        """Loads a game state from file."""
        number_board = {}
        blocked_board = {}
        with open(filename) as f:
            for decoder_function, board in zip([Utils.decode_blocked_board_line, Utils.decode_number_board_line],
                                               [blocked_board, number_board]):
                for y in range(self.size):
                    line = next(f).strip()
                    row = decoder_function(line)
                    if len(line) != self.size:
                        raise Exception(
                            f"Corrupted text file. Length of line is {len(line)} and should be {self.size}.")
                    row = {(x, y): row[x] for x in range(self.size)}
                    board.update(row)
                try: # The empty line is only after the first block
                    empty_line = next(f).strip()
                    if empty_line != "":
                        raise Exception(f'Corrupted text file. Expected empty line, but got "{empty_line}".')
                except StopIteration:
                    pass

            for pos in self.all_pos:
                self.grid[pos].is_blocked = blocked_board[pos]
                self.grid[pos].value = number_board[pos]

    def get_cell(self, pos: tuple) -> Cell:
        """Returns the cell at position `pos`."""
        x, y = pos
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise IndexError
        return self.grid[pos]

    def get_guesses(self, pos: tuple) -> list:
        """
        Returns the guesses of a cell.
        :param pos: tuple
        :return: list
        """
        return self.get_cell(pos).guesses

    def is_blocked(self, pos: tuple) -> bool:
        """
        Returns whether the cell is blocked.
        :type pos: tuple
        """
        return self.get_cell(pos).is_blocked

    def is_empty(self, pos: tuple) -> bool:
        """
        Checks if cell is empty.
        :param pos: tuple
        :return: bool
        """
        return self.get_cell(pos).is_empty

    def set_cell_value(self, pos: tuple, value: int):
        """
        Sets cell to number.
        :param pos:
        :param value:
        """
        self.get_cell(pos).value = value

    def remove_guess(self, pos: tuple, value: int):
        """
        Remove `value` from the list of guesses in `cell`.
        :param pos:
        :param value:
        """
        self.get_cell(pos).remove_guess(value)

    def unique_guess_left(self, pos):
        return self.get_cell(pos).unique_guess_left()

    @property
    def all_cells(self) -> List[Cell]:
        return list(self.grid.values())

    def save(self, filename: str):
        pass
