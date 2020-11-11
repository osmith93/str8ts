from game_elements import Cell
from typing import Set


class Segment:
    horizontal = "horizontal"
    vertical = "vertical"

    def __init__(self, cells: Set[Cell], direction: str, maximum=9):
        self.min = 1
        self.max = maximum
        self.cells = cells
        self.direction = direction

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"Segment({self.cells},{self.direction},{self.max})"

    @property
    def max_entry(self) -> int or None:
        """
        Maximum entry in segment. Returns `None` if no cells are filled.
        :return: int
        """
        maximum = 0
        for cell in self.cells:
            if cell.value != Cell.EMPTY:
                maximum = max(maximum, cell.value)
        if maximum == 0:
            return None
        return maximum

    @property
    def min_entry(self) -> int or None:
        """
        Maximum entry in segment. Returns `None` if no cells are filled.
        :return: int
        """
        minimum = 10
        for cell in self.cells:
            if cell.value != Cell.EMPTY:
                minimum = min(minimum, cell.value)
        if minimum == 10:
            return None
        return minimum

    def __iter__(self):
        return iter(self.cells)