from pybind11_rdp import LineSegment, rdp


def test_segment():
    seg = LineSegment([0, 0, 0], [10, 0, 0])
    assert 4.0 == seg.distance([5.0, 4.0, 0.0])
    assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
    assert 5.0 == seg.distance([14.0, 3.0, 0.0])
    seg = LineSegment([0, 0, 0], [0, 0, 0])
    assert 5.0 == seg.distance([3.0, 4.0, 0.0])
    assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
    assert 13.0 == seg.distance([5.0, 12.0, 0.0])


def test_rdp():
    assert rdp([[1, 1], [2, 2], [3, 3], [4, 4]], epsilon=1e-9).shape == (2, 2)
    assert rdp([[0, 0], [5, 1 + 1e-3], [10, 0]], epsilon=1).shape == (3, 2)
    assert rdp([[0, 0], [5, 1 - 1e-3], [10, 0]], epsilon=1).shape == (2, 2)
