from typing import List, Tuple, Union

import numpy as np
from pybind11_concave_hull import __version__  # noqa
from pybind11_concave_hull import (  # noqa
    concave_hull_indexes as concave_hull_indexes_impl,
)
from scipy.spatial import ConvexHull


def concave_hull_indexes(
    points: Union[np.ndarray, List, Tuple],
    *,
    concavity: float = 2.0,
    length_threshold: float = 0.0,
    convex_hull_indexes: np.ndarray = None,
):
    """
    Get concave hull indexes of points.

    -   `points` is an array of [x, y, [z]] points (can be numpy.ndarray, list, or tuple).
    -   `concavity` is a relative measure of concavity. 1 results in a relatively
        detailed shape, Infinity results in a convex hull. You can use values lower
        than 1, but they can produce pretty crazy shapes.
    -   `length_threshold`: when a segment length is under this threshold, it stops
        being considered for further detalization. Higher values result in simpler
        shapes.

    See original document here: https://github.com/mapbox/concaveman
    """
    points = np.asarray(points, dtype=np.float64)
    points = points[:, :2]
    if convex_hull_indexes is None:
        convex_hull = ConvexHull(points)
        convex_hull_indexes = convex_hull.vertices.astype(np.int32)
    return concave_hull_indexes_impl(
        points,
        convex_hull_indexes=convex_hull_indexes,
        concavity=concavity,
        length_threshold=length_threshold,
    )


def concave_hull(points: Union[np.ndarray, List, Tuple], *args, **kwargs):
    indexes = concave_hull_indexes(points, *args, **kwargs)
    return (
        points[indexes]
        if isinstance(points, np.ndarray)
        else [points[i] for i in indexes]
    )
