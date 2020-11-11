from segment import Segment
class Utils:
    @staticmethod
    def get_numbers_in_small_blocks(blocks, max_size):
        """Get a set of all numbers contained in blocks smaller than max_size."""
        small_blocks = [block for block in blocks if len(block) < max_size]
        return Utils.union_of_lists(small_blocks)

    @staticmethod
    def get_blocks(integer_set):
        """Splits set of integers into consecutive blocks."""
        all_blocks = []
        block = []
        for number in range(1, max(integer_set) + 1):
            if number in integer_set:
                block.append(number)
            else:
                all_blocks.append(block)
                block = []
        if block:
            all_blocks.append(block)
        return all_blocks

    @staticmethod
    def union_of_lists(lists):
        """Returns a union of lists."""
        result = set()
        for list in lists:
            result = result | set(list)
        return result

    @staticmethod
    def generate_segments(game):
        segments = []
        size = game.size

        for x in range(size):
            cells_in_current_segment = set()
            for y in range(size):
                if game.is_blocked((x, y)):
                    if len(cells_in_current_segment) > 0:
                        segments.append(Segment(cells_in_current_segment, Segment.vertical, size))
                        cells_in_current_segment = set()
                else:
                    cells_in_current_segment.add((x, y))
            if len(cells_in_current_segment) > 0:
                segments.append(Segment(cells_in_current_segment, Segment.vertical, size))

        for y in range(size):
            cells_in_current_segment = set()
            for x in range(size):
                if game.is_blocked((x, y)):
                    if len(cells_in_current_segment) > 0:
                        segments.append(Segment(cells_in_current_segment, Segment.horizontal, size))
                        cells_in_current_segment = set()
                else:
                    cells_in_current_segment.add((x, y))
                if len(cells_in_current_segment) > 0:
                    segments.append(Segment(cells_in_current_segment, Segment.horizontal, size))
        return segments
