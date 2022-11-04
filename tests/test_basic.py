import numpy as np

from concave_hull import concave_hull_indexes


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


def test_concave_hull():
    points = __all_points()
    convex_hull = __convex_hull_indexes()

    expected = [
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
    ]
    idxes = concave_hull_indexes(
        points,
        convex_hull_indexes=convex_hull,
    )
    assert np.all(idxes == expected)

    expected = [
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
        4,
        1,
        0,
        8,
        34,
        66,
        84,
        102,
        139,
        166,
        183,
        198,
        204,
    ]
    idxes = concave_hull_indexes(
        points,
        convex_hull_indexes=convex_hull,
        length_threshold=50,
    )
    assert np.all(idxes == expected)
