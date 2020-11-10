import pytest
import main
from utils import Game, Segment, vertical, horizontal
from solver import Solver


def test_cells():
    segment_vert = Segment(0, 0, 4, vertical)
    assert segment_vert.cells == {(0, 0), (0, 1), (0, 2), (0, 3)}
    segment_hor = Segment(0, 0, 4, horizontal)
    assert segment_hor.cells == {(0, 0), (1, 0), (2, 0), (3, 0)}


def test_intersect():
    empty_set = set()
    segment_vert_0 = Segment(0, 0, 4, vertical)
    segment_vert_1 = Segment(1, 0, 4, vertical)
    segment_hor_0 = Segment(0, 0, 4, horizontal)
    segment_hor_1 = Segment(1, 0, 4, horizontal)
    assert segment_vert_0.intersection(segment_hor_0) == {(0, 0)}
    assert segment_vert_0.intersection(segment_vert_1) == empty_set
    assert segment_hor_0.intersection(segment_vert_1) == {(1, 0)}
    for seg_v in [Segment(x, y, l, vertical) for x in range(4) for y in range(4) for l in range(3)]:
        for seg_h in [Segment(x, y, l, horizontal) for x in range(4) for y in range(4) for l in range(3)]:
            assert seg_v.intersection(seg_h) == seg_h.intersection(seg_v)


def test_get_blocks():
    guess_union = set([1, 3, 4, 5, 6, 7, 8, 9])
    guess_union2 = set([1, 3, 4, 5, 7, 8, 9])
    guess_union3 = set([1, 3, 5, 7, 9])
    assert Solver.get_blocks(guess_union, size=9) == [[1], [3, 4, 5, 6, 7, 8, 9]]
    assert Solver.get_blocks(guess_union2, size=9) == [[1], [3, 4, 5], [7, 8, 9]]
    assert Solver.get_blocks(guess_union3, size=9) == [[1], [3], [5], [7], [9]]


def test_get_segments_smaller_than():
    guess_union = set([1, 3, 4, 5, 6, 7, 8, 9])
    guess_union2 = set([1, 3, 4, 7, 8, 9])
    assert Solver.get_blocks_smaller_than(Solver.get_blocks(guess_union, 9), 3) == set([1])
    # assert Solver.get_blocks_smaller_than(Solver.get_blocks(guess_union2, 9), 3) == set([1, 3, 4])
    guess_union3 = set([1, 3, 5, 7, 9])
    assert Solver.get_blocks_smaller_than(Solver.get_blocks(guess_union3, 9), 3) == set([1, 3, 5, 7, 9])
