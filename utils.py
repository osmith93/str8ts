import random

vertical = "vertical"
horizontal = "horizontal"


class Game:
    EMPTY = 0
    BLOCKED = True

    def __init__(self, size=9):
        self.size = size
        self.number_board = size * [size * [Game.EMPTY]]
        self.blocked_board = size * [size * [False]]
        self.segments = []
        possible_numbers = [i for i in range(1,size+1)]
        self.guesses = [[possible_numbers.copy() for _ in range(size)] for _ in range(size)]
        print(self.guesses)

    def load(self, filename):
        """Loads a game state from file."""
        self.number_board = []
        self.blocked_board = []
        with open(filename) as f:
            for _ in range(self.size):
                line = next(f).strip()
                row = self.decode_blocked_board_line(line)
                self.blocked_board.append(row)
            empty_line = next(f).strip()
            if empty_line != "":
                raise Exception(f'Corrupted text file. Expected empty line, but got "{empty_line}".')
            for _ in range(self.size):
                line = next(f).strip()
                row = self.decode_number_board_line(line)
                self.number_board.append(row)

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

    def cell(self, x, y):
        """Returns the contents of a cell."""
        return self.number_board[y][x]

    def guesses_in_cell(self, x,y):
        """Returns the guesses of a cell."""
        return self.guesses[y][x]

    def is_cell_blocked(self, x, y):
        """Returns whether the cell is blocked."""
        return self.blocked_board[y][x]

    def is_cell_empty(self, x, y):
        """Checks if cell is empty."""
        return self.cell(x, y) == Game.EMPTY

    def set_cell_to_number(self,x,y,number):
        """Sets cell to number."""
        self.number_board[y][x] = number




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
        return self.cells.intersection(segment.cells)

    def __len__(self):
        return self.length
