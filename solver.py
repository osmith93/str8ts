from segment import Segment
from utils import Utils


class Solver:
    def __init__(self, board):
        self.board = board
        self.new_cell_positions = set()
        for cell in board.all_pos:
            if not board.is_empty(cell):
                self.new_cell_positions.add(cell)
        self.segments, self.list_of_segments_in_rows, self.list_of_segments_in_columns = self.generate_segments()

    def next_step(self):
        self.check_solvability()
        self.find_solo_guesses()
        self.delete_rook_moves()
        self.maintain_segment_bounds_and_essential_guesses()
        self.decrease_ranges_of_segments_by_values()
        self.decrease_ranges_of_segments_by_guesses()
        self.dead_ends()
        self.enforce_bounds_on_segments()
        self.delete_pigeonhole_guesses()
        self.find_solo_essential_guesses()
        self.delete_essential_guesses_from_other_segments()
        self.delete_lonely_guesses()
        self.delete_guesses_from_essential_guess_cells()
        self.setti()

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
                if i != y and not self.board.is_blocked((x, i)):
                    self.board.remove_guess((x, i), value)
                if i != x and not self.board.is_blocked((i, y)):
                    self.board.remove_guess((i, y), value)
        self.new_cell_positions = set()

    def decrease_ranges_of_segments_by_values(self):
        for segment in self.segments:
            if segment.max_value is not None:
                length = len(segment)
                segment.lower_bound = max(segment.lower_bound, segment.max_value - length + 1)
                segment.upper_bound = min(segment.upper_bound, segment.min_value + length - 1)

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
                if len(guesses) == 0:
                    raise ValueError(f"Cell {cell} has an empty guesses list.")
                segment.lower_bound = max(segment.lower_bound, min(guesses) - len(segment) + 1)
                segment.upper_bound = min(segment.upper_bound, max(guesses) + len(segment) - 1)

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

    def delete_pigeonhole_guesses(self):
        for length in range(2, self.board.size):
            for index in range(self.board.size):
                column = [self.board.get_cell((index, y)) for y in range(self.board.size) if
                          self.board.is_empty((index, y)) and not self.board.is_blocked((index, y))]
                row = [self.board.get_cell((x, index)) for x in range(self.board.size) if
                       self.board.is_empty((x, index)) and not self.board.is_blocked((x, index))]
                for cells in [column, row]:
                    for tuple_of_cells in Utils.find_subsets(set(cells), length):
                        union_of_guesses = [cell.guesses for cell in tuple_of_cells]
                        union_of_guesses = Utils.union_of_lists(union_of_guesses)
                        if len(union_of_guesses) == length:
                            for cell in set(cells) - set(tuple_of_cells):
                                cell.remove_guess_set(union_of_guesses)

    @staticmethod
    def get_essential_guesses(segment):
        lower = segment.upper_bound - len(segment) + 1
        upper = segment.lower_bound + len(segment)
        return [i for i in range(lower, upper)]

    def find_solo_essential_guesses(self):
        for segment in self.segments:
            for guess in segment.essential:
                counter = 0
                relevant_cell = None
                for cell in segment:
                    if guess in cell.guesses:
                        counter += 1
                        relevant_cell = cell
                if counter == 1:
                    relevant_cell.guesses = [guess]

    def delete_essential_guesses_from_other_segments(self):
        for line in self.list_of_segments_in_rows + self.list_of_segments_in_columns:
            for i, segment in enumerate(line):
                for j, other_segment in enumerate(line):
                    if i != j:
                        for cell in other_segment:
                            cell.remove_guess_set(segment.essential)

    def delete_lonely_guesses(self):
        for segment in self.segments:
            if len(segment) > 1:
                for i, cell in enumerate(segment):
                    union_of_guesses = set()
                    for j, other_cell in enumerate(segment):
                        if i != j:
                            union_of_guesses = union_of_guesses.union(set(other_cell.guesses))
                    for guess in cell.guesses:
                        if guess + 1 not in union_of_guesses and guess - 1 not in union_of_guesses:
                            cell.remove_guess(guess)

    def generate_segments(self):
        segments = []
        list_of_segments_in_rows = []
        list_of_segments_in_columns = []
        size = self.board.size

        for line_type, segment_direction, list_of_segments_in_line in [
            (Utils.ROW, Segment.horizontal, list_of_segments_in_rows),
            (Utils.COLUMN, Segment.vertical, list_of_segments_in_columns)]:
            for index in range(size):
                cells_in_current_segment = set()
                segments_in_line = []
                for pos in Utils.get_positions_in_line(index, self.board.size, line_type):
                    cell = self.board.get_cell(pos)
                    if cell.is_blocked:
                        if len(cells_in_current_segment) > 0:
                            new_segment = Segment(cells_in_current_segment, segment_direction, size)
                            segments.append(new_segment)
                            segments_in_line.append(new_segment)
                            cells_in_current_segment = set()
                    else:
                        cells_in_current_segment.add(cell)
                if len(cells_in_current_segment) > 0:
                    new_segment = Segment(cells_in_current_segment, segment_direction, size)
                    segments.append(new_segment)
                    segments_in_line.append(new_segment)
                list_of_segments_in_line.append(segments_in_line)
        return segments, list_of_segments_in_rows, list_of_segments_in_columns

    def maintain_segment_bounds_and_essential_guesses(self):
        for segment in self.segments:
            segment.lower_bound = max(segment.lower_bound, segment.min_guess)
            segment.upper_bound = min(segment.upper_bound, segment.max_guess)
            lower = segment.upper_bound - len(segment) + 1
            upper = segment.lower_bound + len(segment)
            segment.essential = segment.essential | {i for i in range(lower, upper)}

    def delete_guesses_from_essential_guess_cells(self):
        for segment in self.segments:
            cells_with_essential_guesses = []
            for cell in segment:
                if set(cell.guesses) & segment.essential:
                    cells_with_essential_guesses.append(cell)
            if len(cells_with_essential_guesses) == len(segment.essential):
                for cell in cells_with_essential_guesses:
                    cell.guesses = [guess for guess in cell.guesses if guess in segment.essential]

    def setti(self):
        essential_in_rows = []
        impossible_in_rows = []
        essential_in_columns = []
        impossible_in_columns = []
        for essential_in_lines, impossible_in_lines, line_type, list_of_segments_in_line in [
            (essential_in_rows, impossible_in_rows, Utils.ROW, self.list_of_segments_in_rows),
            (essential_in_columns, impossible_in_columns, Utils.COLUMN, self.list_of_segments_in_columns)]:
            for i, segments in enumerate(list_of_segments_in_line):
                essential_in_line = set()
                for pos in Utils.get_positions_in_line(i, self.board.size, line_type):
                    cell = self.board.get_cell(pos)
                    if not cell.is_empty:
                        essential_in_line.add(cell.value)
                for segment in segments:
                    essential_in_line = essential_in_line | segment.essential
                essential_in_lines.append(essential_in_line)
                impossible_in_line = set(range(1, self.board.size + 1))
                for segment in segments:
                    for cell in segment:
                        impossible_in_line = impossible_in_line - set(cell.guesses)
                impossible_in_line = impossible_in_line - essential_in_line
                impossible_in_lines.append(impossible_in_line)

        for value in range(1, self.board.size + 1):
            rows_containing_value = [i for i in range(self.board.size) if value in essential_in_rows[i]]
            columns_containing_value = [i for i in range(self.board.size) if value in essential_in_columns[i]]
            rows_without_value = [i for i in range(self.board.size) if value in impossible_in_rows[i]]
            columns_without_value = [i for i in range(self.board.size) if value in impossible_in_columns[i]]
            ess_row_count = len(rows_containing_value)
            imp_row_count = len(rows_without_value)
            row_count = ess_row_count + imp_row_count
            ess_col_count = len(columns_containing_value)
            imp_col_count = len(columns_without_value)
            column_count = ess_col_count + imp_col_count
            if row_count == self.board.size and column_count != self.board.size:
                if ess_col_count == ess_row_count:
                    new_impossible_columns = set(range(self.board.size)) - set(
                        columns_without_value + columns_containing_value)
                    for index in new_impossible_columns:
                        for pos in Utils.get_positions_in_line(index, self.board.size, Utils.COLUMN):
                            if not self.board.is_blocked(pos):
                                self.board.remove_guess(pos, value)

            if row_count != self.board.size and column_count == self.board.size:
                if ess_col_count == ess_row_count:
                    new_impossible_rows = set(range(self.board.size)) - set(
                        rows_without_value + rows_containing_value)
                    for index in new_impossible_rows:
                        for pos in Utils.get_positions_in_line(index, self.board.size, Utils.ROW):
                            if not self.board.is_blocked(pos):
                                self.board.remove_guess(pos, value)
