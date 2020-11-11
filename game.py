import random

vertical = "vertical"
horizontal = "horizontal"





class Game:
    EMPTY = 0
    BLOCKED = True

    def __init__(self, size=9):
        self.size = size
        cells = [(x, y) for x in range(size) for y in range(size)]
        self.number_board = {cell: Game.EMPTY for cell in cells}
        self.blocked_board = {cell: False for cell in cells}
        self.segments = []
        possible_numbers = [i for i in range(1, size + 1)]
        self.guesses = {cell: possible_numbers.copy() for cell in cells}

    def load(self, filename):
        """Loads a game state from file."""
        self.number_board = {}
        self.blocked_board = {}
        with open(filename) as f:
            for y in range(self.size):
                line = next(f).strip()
                row = self.decode_blocked_board_line(line)
                row = {(x, y): row[x] for x in range(self.size)}
                self.blocked_board.update(row)
            empty_line = next(f).strip()
            if empty_line != "":
                raise Exception(f'Corrupted text file. Expected empty line, but got "{empty_line}".')
            for y in range(self.size):
                line = next(f).strip()
                row = self.decode_number_board_line(line)
                row = {(x, y): row[x] for x in range(self.size)}
                self.number_board.update(row)

    def decode_number_board_line(self, line):
        row = []
        if len(line) != self.size:
            raise Exception(f"Corrupted text file. Length of line is {len(line)} and should be {self.size}.")
        for c in line:
            if c == ".":
                row.append(Game.EMPTY)
            elif c.isnumeric() and 0 < int(c) <= self.size:
                row.append(int(c))
            else:
                raise Exception(f'Corrupted text file. Illegal character "{c}"')
        return row

    def decode_blocked_board_line(self, line):
        row = []
        if len(line) != self.size:
            raise Exception(f"Corrupted text file. Length of line is {len(line)} and should be {self.size}.")
        for c in line:
            if c == "x":
                row.append(Game.BLOCKED)
            elif c == ".":
                row.append(not Game.BLOCKED)
            else:
                raise Exception(f'Corrupted text file. Illegal character "{c}"')
        return row

    def save(self, filename):
        """Save a game state to file."""
        pass

    def check(self):
        pass

    def get_cell(self, cell):
        """Returns the contents of a cell."""
        return self.number_board[cell]

    def get_guesses(self, cell):
        """Returns the guesses of a cell."""
        return self.guesses[cell]

    def is_blocked(self, cell):
        """Returns whether the cell is blocked."""
        return self.blocked_board[cell]

    def is_empty(self, cell):
        """Checks if cell is empty."""
        return self.get_cell(cell) == Game.EMPTY

    def set_to_number(self, cell, number):
        """Sets cell to number."""
        self.number_board[cell] = number

    def remove_guess(self, number, cell):
        if number in self.guesses[cell]:
            self.guesses[cell].remove(number)

    def single_possibility(self, cell):
        return len(self.guesses[cell]) == 1


class Segment:
    def __init__(self, x=0, y=0, length=1, dir=vertical):
        self.x = x
        self.y = y
        self.length = length
        self.direction = dir

    @property
    def cells(self):
        cells = set()
        if self.direction == vertical:
            for i in range(self.length):
                cells.add((self.x, self.y + i))
        else:
            for i in range(self.length):
                cells.add((self.x + i, self.y))
        return cells

    def intersection(self, segment):
        return self.cells.intersection(segment.all_cells)

    def __len__(self):
        return self.length
