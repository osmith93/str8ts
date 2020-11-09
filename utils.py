import random
vertical = "vertical"
horizontal = "horizontal"


class Game:
    EMPTY = 0
    BLOCKED = -1
    def __init__(self):
        self.size = 9
        self.board = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
#                row.append(Game.EMPTY)
                row.append(random.randint(-1,9))
            self.board.append(row)
        self.segments = []

    def load(self, filename):
        """Loads a game state from file."""
        pass

    def check(self):
        pass

    def cell(self,x,y):
        """Returns the contents of a cell."""
        return self.board[y][x]

    def is_cell_empty(self,x,y):
        """Checks if cell is empty."""
        return self.cell(x,y) == Game.EMPTY

    def is_cell_blocked(self,x,y):
        """Checks if cell is blocked."""
        return self.cell(x,y) == Game.BLOCKED

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
                cells.add((self.x+i, self.y))
        return cells

    def intersection(self, segment):
        return self.cells.intersection(segment.cells)

    def __len__(self):
        return self.length

