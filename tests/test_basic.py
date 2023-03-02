import numpy as np

from concave_hull import concave_hull, concave_hull_indexes


# see ../test.py for testing data
def __all_points():
    points = []
    c = np.array([250, 250])
    for x in np.arange(100, 400, 5 * np.pi):
        for y in np.arange(100, 400, 5 * np.pi):
            if x > c[0] and y > c[1]:
                continue
            r = np.linalg.norm(c - [x, y])
            if r > 150:
                continue
            points.append([x, y])
    return np.array(points)


def __convex_hull_indexes():
    return [208, 138, 83, 49, 19, 7, 0, 8, 34, 66, 166, 183, 198, 204]


def __concave_hull_indexes():
    return [
        205,
        206,
        208,
        207,
        203,
        197,
        190,
        182,
        174,
        165,
        156,
        147,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        138,
        119,
        101,
        83,
        65,
        49,
        33,
        19,
        18,
        7,
        6,
        5,
        4,
        3,
        2,
        1,
        0,
        9,
        8,
        20,
        34,
        50,
        66,
        84,
        102,
        120,
        139,
        148,
        157,
        166,
        175,
        183,
        191,
        198,
        199,
        204,
    ]  # noqa


def __concave_hull_indexes_thresh50():
    return [
        208,
        207,
        203,
        197,
        190,
        182,
        174,
        165,
        156,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        138,
        83,
        49,
        19,
        7,
        5,
        2,
        1,
        0,
        8,
        34,
        66,
        120,
        139,
        166,
        183,
        198,
        204,
    ]


def __test_concave_hull(points):
    convex_hull = __convex_hull_indexes()
    idxes = concave_hull_indexes(
        points,
        convex_hull_indexes=convex_hull,
    )
    assert np.all(idxes == __concave_hull_indexes())

    idxes = concave_hull_indexes(points)  # integrated convex hull
    assert np.all(idxes == __concave_hull_indexes())

    idxes = concave_hull_indexes(
        points,
        convex_hull_indexes=convex_hull,
        length_threshold=50,
    )
    assert np.all(idxes == __concave_hull_indexes_thresh50())
    idxes = concave_hull_indexes(points, length_threshold=50)
    assert np.all(idxes == __concave_hull_indexes_thresh50())


def test_concave_hull_np_array():
    points = __all_points()
    __test_concave_hull(points)
    # Nx3
    points = np.c_[points, np.zeros(len(points))]
    __test_concave_hull(points)


def test_concave_hull_list_tuple():
    points = __all_points()
    __test_concave_hull(points.tolist())
    __test_concave_hull(tuple(points.tolist()))
    # Nx3
    points = np.c_[points, np.zeros(len(points))]
    __test_concave_hull(points.tolist())
    __test_concave_hull(tuple(points.tolist()))


def test_concave_hull_api():
    all_points = __all_points()
    all_points = np.c_[all_points, np.random.random(len(all_points))]
    assert all_points.shape == (209, 3)

    hull_points = concave_hull(all_points)
    assert isinstance(hull_points, np.ndarray)
    assert hull_points.shape == (57, 3)

    indexes = concave_hull_indexes(all_points)
    assert np.all(all_points[indexes] == hull_points)

    hull_points = concave_hull(all_points.tolist())
    assert isinstance(hull_points, list)
    assert len(hull_points) == 57

    hull_points = concave_hull(tuple(all_points.tolist()))
    assert isinstance(hull_points, list)
    assert len(hull_points) == 57
