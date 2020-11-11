class Segment:
    horizontal = "horizontal"
    vertical = "vertical"

    def __init__(self, cells, direction, maximum=9):
        self.min = 1
        self.max = maximum
        self.cells = cells
        self.direction = direction

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"Segment({self.cells},{self.direction},{self.max})"
