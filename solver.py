from segment import Segment
from utils import Utils


class Solver:
    def __init__(self, board):
        self.board = board
        self.new_cell_positions = set()
        for cell in board.all_pos:
            if not board.is_empty(cell):
                self.new_cell_positions.add(cell)
        self.segments = self.generate_segments()

    def next_step(self):
        self.check_solvability()
        self.find_solo_guesses()
        self.delete_rook_moves()
        self.decrease_ranges_of_segments_by_values()
        self.decrease_ranges_of_segments_by_guesses()
        self.dead_ends()
        self.enforce_bounds_on_segments()
        self.delete_duplicates()

    def find_solo_guesses(self):
        for cell in self.board.all_cells:
            if cell.is_blocked or not cell.is_empty:
                continue
            if cell.try_filling_unique_guess():
                self.new_cell_positions.add(cell.pos)

    def delete_rook_moves(self):
        for pos in self.new_cell_positions:
            x, y = pos
            value = self.board.get_cell(pos).value
            for i in range(self.board.size):
                if i != y:
                    self.board.remove_guess((x, i), value)
                if i != x:
                    self.board.remove_guess((i, y), value)
        self.new_cell_positions = set()

    def decrease_ranges_of_segments_by_values(self):
        for segment in self.segments:
            if segment.max_value is not None:
                length = len(segment)
                segment.lower_bound = max(0, segment.max_value - length + 1)
                segment.upper_bound = min(self.board.size, segment.min_entry + length - 1)

    def enforce_bounds_on_segments(self):
        for segment in self.segments:
            for cell in segment:
                cell.remove_guess_set(set(range(segment.lower_bound)))
                cell.remove_guess_set(set(range(segment.upper_bound + 1, self.board.size + 1)))

    def check_solvability(self):
        pass

    def decrease_ranges_of_segments_by_guesses(self):
        for segment in self.segments:
            for cell in segment:
                guesses = cell.guesses
                if not cell.is_empty:
                    guesses = [cell.value]
                segment.lower_bound = max(min(guesses) - len(segment) + 1, segment.lower_bound)
                segment.upper_bound = min(max(guesses) + len(segment) - 1, segment.upper_bound)

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

            for block in blocks:
                remove_block = False
                for cell in segment:
                    guesses = set(cell.guesses)
                    if len(guesses.intersection(set(block))) == 0:
                        remove_block = True
                        break
                if remove_block:
                    for cell in segment:
                        cell.remove_guess_set(set(block))
            # maybe do something like decrease_range_by_guesses on separate blocks

    def delete_duplicates(self):
        length = 2
        for index in range(self.board.size):
            row = [self.board.get_cell((index, y)) for y in range(self.board.size) if
                   self.board.is_empty((index, y)) and not self.board.is_blocked((index, y))]
            for cell1 in row:
                for cell2 in row:
                    if cell1 == cell2:
                        continue
                    union_of_guesses = set(cell1.guesses).union(set(cell2.guesses))
                    if len(union_of_guesses) == 2:
                        for cell in row:
                            if cell == cell1 or cell == cell2:
                                continue
                            cell.remove_guess_set(union_of_guesses)


    def generate_segments(self):
        segments = []
        size = self.board.size

        for x in range(size):
            cells_in_current_segment = set()
            for y in range(size):
                cell = self.board.get_cell((x, y))
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
                cell = self.board.get_cell((x, y))
                if cell.is_blocked:
                    if len(cells_in_current_segment) > 0:
                        segments.append(Segment(cells_in_current_segment, Segment.horizontal, size))
                        cells_in_current_segment = set()
                else:
                    cells_in_current_segment.add(cell)
                if len(cells_in_current_segment) > 0:
                    segments.append(Segment(cells_in_current_segment, Segment.horizontal, size))
        return segments
