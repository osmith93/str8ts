from game import Game
from utils import Utils


class Solver:
    def __init__(self, game):
        self.game = game
        self.new_cells = set()
        cells = [(x, y) for x in range(game.size) for y in range(game.size)]
        for cell in cells:
            if not game.is_empty(cell):
                self.new_cells.add(cell)
        self.segments = Utils.generate_segments(game)

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
        self.dead_ends()
        self.enforce_bounds_on_segments()



    def find_solo_guesses(self):
        cells = [(x, y) for x in range(self.game.size) for y in range(self.game.size)]
        for cell in cells:
            if self.game.is_blocked(cell) or not self.game.is_empty(cell):
                continue
            if self.game.single_possibility(cell):
                self.game.set_to_number(cell, self.game.get_guesses(cell)[0])
                self.new_cells.add(cell)

    def delete_rook_moves(self):
        for cell in self.new_cells:
            x, y = cell
            number = self.game.get_cell(cell)
            for i in range(self.game.size):
                if i != y:
                    self.game.remove_guess(number, (x, i))
                if i != x:
                    self.game.remove_guess(number, (i, y))
        self.new_cells = set()

    def decrease_ranges_of_segments_by_values(self):
        for segment in self.segments:
            min_entry = self.game.size + 1
            max_entry = 0
            for cell in segment.cells:
                if not self.game.is_empty(cell):
                    if self.game.get_cell(cell) > max_entry:
                        max_entry = self.game.get_cell(cell)
                    if self.game.get_cell(cell) < min_entry:
                        min_entry = self.game.get_cell(cell)
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
                    self.game.remove_guess(number, cell)
                for number in range(segment.max + 1, self.game.size + 1):
                    self.game.remove_guess(number, cell)

    def check_solvability(self):
        pass

    def decrease_ranges_of_segments_by_guesses(self):
        for segment in self.segments:
            for cell in segment.cells:
                x, y = cell
                guesses = self.game.get_guesses(cell)
                if not self.game.is_empty(cell):
                    guesses = [self.game.get_cell(cell)]
                segment.min = max(min(guesses) - len(segment) + 1, segment.min)
                segment.max = min(max(guesses) + len(segment) - 1, segment.max)

    def dead_ends(self):
        """Parse guesses of segments into blocks and make sure that consecutive runs which are too short are excluded"""
        for segment in self.segments:

            guess_union = [self.game.get_guesses(cell) for cell in segment.cells]
            guess_union = Utils.union_of_lists(guess_union)
            blocks = Utils.get_blocks(guess_union)
            removable_guesses = Utils.get_numbers_in_small_blocks(blocks, max_size=len(segment))

            for cell in segment.cells:
                for number in removable_guesses:
                    self.game.remove_guess(number, cell)




