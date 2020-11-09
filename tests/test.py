import pytest
import main
from utils import Game, Segment, vertical, horizontal


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
    for seg_v in [Segment(x,y,l,vertical) for x in range(4) for y in range(4) for l in range(3)]:
        for seg_h in [Segment(x, y, l, horizontal) for x in range(4) for y in range(4) for l in range(3)]:
            assert seg_v.intersection(seg_h) == seg_h.intersection(seg_v)

