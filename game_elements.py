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
        self.grid = {pos: Cell(pos, False, size, Cell.EMPTY) for pos in self.all_pos}

    def get_cell(self, pos: tuple) -> Cell:
        """Returns the cell at position `pos`."""
        x, y = pos
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise IndexError
        return self.grid[pos]

    def load(self, filename: str):
        """Loads a game state from file."""
        number_board = {}
        blocked_board = {}
        with open(filename) as f:
            for y in range(self.size):
                line = next(f).strip()
                row = Utils.decode_blocked_board_line(line)
                if len(line) != self.size:
                    raise Exception(f"Corrupted text file. Length of line is {len(line)} and should be {self.size}.")
                row = {(x, y): row[x] for x in range(self.size)}
                blocked_board.update(row)
            empty_line = next(f).strip()
            if empty_line != "":
                raise Exception(f'Corrupted text file. Expected empty line, but got "{empty_line}".')
            for y in range(self.size):
                line = next(f).strip()
                row = Utils.decode_number_board_line(line)
                if len(row) != self.size:
                    raise Exception(f"Corrupted text file. Length of line is {len(row)} and should be {self.size}.")
                row = {(x, y): row[x] for x in range(self.size)}
                number_board.update(row)

            for pos in self.all_pos:
                self.grid[pos].is_blocked = blocked_board[pos]
                self.grid[pos].value = number_board[pos]
    @property
    def all_cells(self) -> List[Cell]:
        return list(self.grid.values())

    def save(self, filename: str):
        pass

