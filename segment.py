from board import Cell
from typing import Set


class Segment:
    horizontal = "horizontal"
    vertical = "vertical"

    def __init__(self, cells: Set[Cell], direction: str, maximum=9):
        self.lower_bound = 1
        self.upper_bound = maximum
        self.cells = cells
        self.direction = direction

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"Segment({self.cells},{self.direction},{self.upper_bound})"

    @property
    def all_values(self):
        return [cell.value for cell in self if not cell.is_empty]

    @property
    def max_value(self) -> int or None:
        """
        Maximum value in segment. Returns `None` if all cells are empty.
        :return: int
        """
        try:
            return max(self.all_values)
        except ValueError:  # this happens when no self.all_values is empty
            return None

    @property
    def min_value(self) -> int or None:
        """
        Minimum entry in segment. Returns `None` if no cells are filled.
        :return: int
        """
        try:
            return min(self.all_values)
        except ValueError:  # this happens when no self.all_values is empty
            return None

    @property
    def min_guess(self):
        return min([min(cell.guesses) for cell in self])

    @property
    def max_guess(self):
        return max([max(cell.guesses) for cell in self])

    def __iter__(self):
        return iter(self.cells)
