from utils import Game


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


class Solver:
    def __init__(self, game):
        self.game = game
        self.new_cells = set()
        for x in range(game.size):
            for y in range(game.size):
                if not game.is_cell_empty(x, y):
                    self.new_cells.add((x, y))
        self.segments = self.get_segments(game)

    def get_horizontal_segments_containing(self, cell):
        pass

    def get_vertical_segments_containing(self, cell):
        pass

    def next_step(self):
        self.check_solvability()
        self.find_solo_guesses()
        self.delete_rook_moves()
        self.decrease_ranges_of_segments_by_values()
        self.decrease_ranges_of_segments_by_guesses()
        self.enforce_bounds_on_segments()

    @staticmethod
    def get_segments(game):
        segments = []
        for x in range(game.size):
            cells = set()
            for y in range(game.size):
                if game.is_cell_blocked(x, y):
                    if len(cells) > 0:
                        segments.append(Segment(cells, Segment.vertical, game.size))
                        cells = set()
                else:
                    cells.add((x, y))
            if len(cells) > 0:
                segments.append(Segment(cells, Segment.vertical, game.size))

        for y in range(game.size):
            cells = set()
            for x in range(game.size):
                if game.is_cell_blocked(x, y):
                    if len(cells) > 0:
                        segments.append(Segment(cells, Segment.horizontal, game.size))
                        cells = set()
                else:
                    cells.add((x, y))
                if len(cells) > 0:
                    segments.append(Segment(cells, Segment.horizontal, game.size))
        return segments

    def find_solo_guesses(self):
        for x in range(self.game.size):
            for y in range(self.game.size):
                if self.game.is_cell_blocked(x, y) or not self.game.is_cell_empty(x, y):
                    continue
                numbers = self.game.guesses_in_cell(x, y)
                if len(numbers) == 1:
                    self.game.set_cell_to_number(x, y, numbers[0])
                    self.new_cells.add((x, y))
        pass

    def delete_rook_moves(self):
        for cell in self.new_cells:
            x, y = cell
            number = self.game.cell(x, y)
            for i in range(self.game.size):
                self.remove_guess_from_cell(number, (x, i))
                self.remove_guess_from_cell(number, (i, y))

        self.new_cells = set()

    def decrease_ranges_of_segments_by_values(self):
        for segment in self.segments:
            min_entry = self.game.size + 1
            max_entry = 0
            for cell in segment.cells:
                x, y = cell
                if not self.game.is_cell_empty(x, y):
                    if self.game.cell(x, y) > max_entry:
                        max_entry = self.game.cell(x, y)
                    if self.game.cell(x, y) < min_entry:
                        min_entry = self.game.cell(x, y)
            if max_entry != 0:
                length = len(segment)
                min_possible = max(0, max_entry - length + 1)
                max_possible = min(self.game.size, min_entry + length - 1)
                segment.min = min_possible
                segment.max = max_possible
        # Need to do the same for guesses

    def enforce_bounds_on_segments(self):
        for segment in self.segments:
            for cell in segment.cells:
                for number in range(segment.min):
                    self.remove_guess_from_cell(number, cell)
                for number in range(segment.max + 1, self.game.size + 1):
                    self.remove_guess_from_cell(number, cell)

    def check_solvability(self):
        pass

    def remove_guess_from_cell(self, number, cell):
        x, y = cell
        if number in self.game.guesses[y][x]:
            self.game.guesses[y][x].remove(number)

    def decrease_ranges_of_segments_by_guesses(self):
        for segment in self.segments:
            for cell in segment.cells:
                x, y = cell
                guesses = self.game.guesses_in_cell(x, y)
                if not self.game.is_cell_empty(x,y):
                    guesses = [self.game.cell(x,y)]
                segment.min = max(min(guesses) - len(segment) + 1, segment.min)
                segment.max = min(max(guesses) + len(segment) - 1, segment.max)
