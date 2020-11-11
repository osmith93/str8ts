class Utils:
    EMPTY = 0
    BLOCKED = True
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
        for lst in lists:
            result = result | set(lst)
        return result

    @staticmethod
    def decode_number_board_line(line):
        row = []
        for c in line:
            if c == ".":
                row.append(Utils.EMPTY)
            elif c.isnumeric() and 0 < int(c):
                row.append(int(c))
            else:
                raise Exception(f'Corrupted text file. Illegal character "{c}"')
        return row

    @staticmethod
    def decode_blocked_board_line(line):
        row = []
        for c in line:
            if c == "x":
                row.append(Utils.BLOCKED)
            elif c == ".":
                row.append(not Utils.BLOCKED)
            else:
                raise Exception(f'Corrupted text file. Illegal character "{c}"')
        return row
