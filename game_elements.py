from segment import Segment
from utils import Utils


class Box:
    EMPTY = 0
    def __init__(self, pos: tuple, blocked: bool, size: int, value: int):
        self.pos = pos
        self.is_blocked = blocked
        self.value = value
        self.guesses = [i for i in range(1, size + 1)]

    def remove_guess(self, value: int):
        """Tries removing value from the `self.guesses`. Returns `True` if successful."""
        if value in self.guesses:
            self.guesses.remove(value)
            return True
        return False

    def remove_guess_set(self, value_set: set):
        """Tries removing all values in `value_set` from self.guesses. Returns `True` if any were removed."""
        result = False
        for value in value_set:
            success = self.remove_guess(value)
            result = result or success
        return result

    def unique_guess_left(self):
        """Returns whether there is only one possible guess left."""
        return len(self.guesses) == 1

    def try_filling_unique_guess(self):
        """Fills the cell if only one possible value is left. Returns `True` if successful."""
        if self.unique_guess_left():
            self.value = self.guesses[0]
            return True
        return False


class Line:
    def __init__(self, list_of_boxes):
        self.line = list_of_boxes
        pass

    def __len__(self):
        return len(self.line)

    def get_segments(self) -> list:
        pass


class Board:
    def __init__(self, size: int):
        self.size = size
        self.all_cells = [(x, y) for x in range(size) for y in range(size)]
        self.grid = {cell: Box(cell, False, size, Box.EMPTY) for cell in self.all_cells}

    def get_box(self, cell: tuple) -> Box:
        """Returns the box at position `cell`."""
        x, y = cell
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise IndexError
        return self.grid[cell]

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

            for cell in self.all_cells:
                self.grid[cell].is_blocked = blocked_board[cell]
                self.grid[cell].value = number_board[cell]

    def save(self, filename: str):
        pass

    def get_row(self, row_id: int) -> Line:
        pass
