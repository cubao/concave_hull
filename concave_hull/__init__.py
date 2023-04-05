from typing import List, Tuple, Union

import numpy as np
import pybind11_concave_hull  # noqa
from pybind11_concave_hull import __version__  # noqa
from pybind11_concave_hull import clockwise, colinear  # noqa
from pybind11_concave_hull import (  # noqa
    concave_hull_indexes as concave_hull_indexes_impl,
)
from pybind11_concave_hull import convex_hull_indexes as convex_hull_indexes_impl
from pybind11_concave_hull import orientation, wgs84_to_east_north  # noqa


def concave_hull_indexes(
    points: Union[np.ndarray, List, Tuple],
    *,
    concavity: float = 2.0,
    length_threshold: float = 0.0,
    convex_hull_indexes: np.ndarray = None,  # noqa
    is_wgs84: bool = False,
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
    if is_wgs84:
        points = wgs84_to_east_north(points)
    if convex_hull_indexes is None:
        convex_hull_indexes = convex_hull_indexes_impl(points)
    return concave_hull_indexes_impl(
        points,
        concavity=concavity,
        length_threshold=length_threshold,
        convex_hull_indexes=convex_hull_indexes,
    )


def concave_hull(points: Union[np.ndarray, List, Tuple], *args, **kwargs):
    indexes = concave_hull_indexes(points, *args, **kwargs)
    return (
        points[indexes]
        if isinstance(points, np.ndarray)
        else [points[i] for i in indexes]
    )


def convex_hull_indexes(points: Union[np.ndarray, List, Tuple], *args, **kwargs):
    points = np.asarray(points, dtype=np.float64)
    return convex_hull_indexes_impl(points[:, :2], *args, **kwargs)


def convex_hull(points: Union[np.ndarray, List, Tuple], *args, **kwargs):
    indexes = convex_hull_indexes(points, *args, **kwargs)
    return (
        points[indexes]
        if isinstance(points, np.ndarray)
        else [points[i] for i in indexes]
    )
