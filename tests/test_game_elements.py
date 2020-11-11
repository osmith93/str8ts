import pytest
from game_elements import Cell, Board


@pytest.fixture
def box():
    new_box = Cell((5, 5), False, 9, Cell.EMPTY)
    return new_box


class TestBox:
    @staticmethod
    def test_init():
        box = Cell((5, 5), False, 9, Cell.EMPTY)
        assert box.guesses == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert box.is_blocked == False
        assert box.pos == (5, 5)
        assert box.value == Cell.EMPTY

    @staticmethod
    def test_remove_guess(box):
        for i in range(4):
            box.remove_guess(i)
        assert box.guesses == [4, 5, 6, 7, 8, 9]

    @staticmethod
    def test_remove_guess_set(box):
        removal_set = {2, 5, 7, 9}
        box.remove_guess_set(removal_set)
        assert box.guesses == [1, 3, 4, 6, 8]

    @staticmethod
    def test_unique_guess_left(box):
        assert box.unique_guess_left() == False
        for i in range(9):
            box.remove_guess(i)
        return box.unique_guess_left() == True

    @staticmethod
    def test_try_filling_unique_guess(box):
        assert box.try_filling_unique_guess() == False
        assert box.value == Cell.EMPTY
        assert box.remove_guess_set({2, 3, 4, 5, 6, 7, 8, 9}) == True
        assert box.try_filling_unique_guess() == True
        assert box.value == 1


@pytest.fixture()
def empty_board():
    new_board = Board(size=9)
    return empty_board


class TestBoard:
    @staticmethod
    def test_init():
        board = Board(9)
        assert board.size == 9
        assert len(board.all_pos) == 9 * 9
        assert len(board.grid) == 9 * 9

    @staticmethod
    def test_load(empty_board):
        board = Board(9)
        with pytest.raises(FileNotFoundError):
            board.load("/THIS/FILE/DOES/NOT/EXIST")
        board.load("../data/board01.txt")
        assert board.get_cell((0, 0)).is_blocked == True
