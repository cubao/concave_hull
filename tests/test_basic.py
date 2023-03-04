import json
import os

import numpy as np

from concave_hull import concave_hull, concave_hull_indexes, wgs84_to_east_north


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


def test_concave_for_wgs84():
    # https://geojson.io/#data=data:text/x-url,https%3A%2F%2Fgithub.com%2Fcubao%2Fconcave_hull%2Fraw%2Fmaster%2Fdata%2Fsongjiang.json
    pass


def write_json(path: str, data):
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"wrote to {path}")


def handle_wgs84():
    PWD = os.path.abspath(os.path.dirname(__file__))
    with open(f"{PWD}/../data/songjiang.json") as f:
        data = json.load(f)
        wgs84 = np.array(data["geometry"]["coordinates"][0])
    east_north = wgs84_to_east_north(wgs84)  # to meters
    assert (
        np.linalg.norm(east_north.max(axis=0) - [32706.73422749, 24204.0419051]) < 1e-3
    )

    export_dir = None  # f'{PWD}/../docs/data'
    features = []
    for is_wgs84 in [False, True]:
        for thresh in [10.0, 100.0, 1000.0, 5000.0, 10000.0]:
            wgs84_hull = concave_hull(wgs84, length_threshold=thresh, is_wgs84=is_wgs84)
            wgs84_hull = wgs84_hull.tolist()
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[*wgs84_hull, wgs84_hull[0]]],  # as polygon
                    },
                    "properties": {
                        "is_wgs84": is_wgs84,
                        "length_threshold": thresh,
                        "#origin_points": len(wgs84),
                        "#concave_bounds": len(wgs84_hull),
                    },
                }
            )
            if export_dir:
                path = f'{export_dir}/concave_hull_thresh_{thresh}_{"wgs84" if is_wgs84 else "xy"}.json'
                write_json(path, features[-1])

    if export_dir:
        write_json(
            f"{export_dir}/concave_hull.json",
            {
                "type": "FeatureCollection",
                "features": features,
            },
        )

    ret0 = concave_hull(wgs84, length_threshold=50.0)
    ret1 = concave_hull(wgs84, length_threshold=50.0, is_wgs84=False)
    ret2 = concave_hull(wgs84, length_threshold=50.0, is_wgs84=True)
    assert len(ret0) == len(ret1)
    assert len(ret0) < len(ret2)
