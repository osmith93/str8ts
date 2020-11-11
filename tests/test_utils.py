from utils import Utils
import pytest

class TestUtils:
    @staticmethod
    def test_get_numbers_in_small_blocks():
        guess_union = {1, 3, 4, 5, 6, 7, 8, 9}
        guess_union2 = {1, 3, 4, 7, 8, 9}
        guess_union3 = {1, 3, 5, 7, 9}
        assert Utils.get_numbers_in_small_blocks(Utils.get_blocks(guess_union), 3) == {1}
        assert Utils.get_numbers_in_small_blocks(Utils.get_blocks(guess_union2), 3) == {1, 3, 4}
        assert Utils.get_numbers_in_small_blocks(Utils.get_blocks(guess_union3), 3) == {1, 3, 5, 7, 9}

    @staticmethod
    def test_get_blocks():
        guess_union = {1, 3, 4, 5, 6, 7, 8, 9}
        guess_union2 = {1, 3, 4, 5, 7, 8, 9}
        guess_union3 = {1, 3, 5, 7, 9}
        assert Utils.get_blocks(guess_union) == [[1], [3, 4, 5, 6, 7, 8, 9]]
        assert Utils.get_blocks(guess_union2) == [[1], [3, 4, 5], [7, 8, 9]]
        assert Utils.get_blocks(guess_union3) == [[1], [3], [5], [7], [9]]

    @staticmethod
    def test_union_of_lists():
        lists1 = [[1, 2, 3], [2, 3, 4], [10]]
        assert Utils.union_of_lists(lists1) == {1, 2, 3, 4, 10}
