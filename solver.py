from game_elements import Cell
from segment import Segment
from utils import Utils


class Solver:
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.new_cell_positions = set()
        for cell in game.board.all_pos:
            if not game.is_empty(cell):
                self.new_cell_positions.add(cell)
        self.segments = self.generate_segments()

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
        for cell in self.board.all_cells:
            if cell.is_blocked or not cell.is_empty:
                continue
            if cell.try_filling_unique_guess():
                self.new_cell_positions.add(cell.pos)

    def delete_rook_moves(self):
        for pos in self.new_cell_positions:
            x, y = pos
            value = self.game.get_cell(pos).value
            for i in range(self.game.size):
                if i != y:
                    self.game.remove_guess((x, i), value)
                if i != x:
                    self.game.remove_guess((i, y), value)
        self.new_cell_positions = set()

    def decrease_ranges_of_segments_by_values(self):
        for segment in self.segments:
            if segment.max_entry is not None:
                length = len(segment)
                segment.min = max(0, segment.max_entry - length + 1)
                segment.max = min(self.game.size, segment.min_entry + length - 1)
        # Need to do the same for guesses

    def enforce_bounds_on_segments(self):
        for segment in self.segments:
            for cell in segment:
                cell.remove_guess_set(set(range(segment.min)))
                cell.remove_guess_set(set(range(segment.max + 1, self.game.size + 1)))

    def check_solvability(self):
        pass

    def decrease_ranges_of_segments_by_guesses(self):
        for segment in self.segments:
            for cell in segment:
                guesses = cell.guesses
                if not cell.is_empty:
                    guesses = [cell.value]
                segment.min = max(min(guesses) - len(segment) + 1, segment.min)
                segment.max = min(max(guesses) + len(segment) - 1, segment.max)

    def dead_ends(self):
        """
        Parse guesses of segments into blocks and make sure that consecutive runs which are too short are excluded
        """
        for segment in self.segments:
            guess_union = [cell.guesses for cell in segment]
            guess_union = Utils.union_of_lists(guess_union)
            blocks = Utils.get_blocks(guess_union)
            removable_guesses = Utils.get_numbers_in_small_blocks(blocks, max_size=len(segment))
            for cell in segment:
                cell.remove_guess_set(removable_guesses)

    def generate_segments(self):
        segments = []
        size = self.game.size

        for x in range(size):
            cells_in_current_segment = set()
            for y in range(size):
                cell = self.game.get_cell((x,y))
                if cell.is_blocked:
                    if len(cells_in_current_segment) > 0:
                        segments.append(Segment(cells_in_current_segment, Segment.vertical, size))
                        cells_in_current_segment = set()
                else:
                    cells_in_current_segment.add(cell)
            if len(cells_in_current_segment) > 0:
                segments.append(Segment(cells_in_current_segment, Segment.vertical, size))

        for y in range(size):
            cells_in_current_segment = set()
            for x in range(size):
                cell = self.game.get_cell((x,y))
                if cell.is_blocked:
                    if len(cells_in_current_segment) > 0:
                        segments.append(Segment(cells_in_current_segment, Segment.horizontal, size))
                        cells_in_current_segment = set()
                else:
                    cells_in_current_segment.add(cell)
                if len(cells_in_current_segment) > 0:
                    segments.append(Segment(cells_in_current_segment, Segment.horizontal, size))
        return segments
