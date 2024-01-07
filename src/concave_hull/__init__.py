from typing import List, Tuple, Union

import numpy as np

from ._core import __version__  # noqa
from ._core import clockwise, colinear  # noqa
from ._core import concave_hull_indexes as concave_hull_indexes_impl  # noqa
from ._core import convex_hull_indexes as convex_hull_indexes_impl
from ._core import orientation, wgs84_to_east_north  # noqa


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


def concave_hull(
    points: Union[np.ndarray, List, Tuple],
    *,
    concavity: float = 2.0,
    length_threshold: float = 0.0,
    convex_hull_indexes: np.ndarray = None,  # noqa
    is_wgs84: bool = False,
):
    indexes = concave_hull_indexes(
        points,
        concavity=concavity,
        length_threshold=length_threshold,
        convex_hull_indexes=convex_hull_indexes,
        is_wgs84=is_wgs84,
    )
    return (
        points[indexes]
        if isinstance(points, np.ndarray)
        else [points[i] for i in indexes]
    )


def convex_hull_indexes(
    points: Union[np.ndarray, List, Tuple],
    *,
    include_colinear: bool = False,
    order_only: bool = False,
):
    points = np.asarray(points, dtype=np.float64)
    return convex_hull_indexes_impl(
        points[:, :2],
        include_colinear=include_colinear,
        order_only=order_only,
    )


def convex_hull(
    points: Union[np.ndarray, List, Tuple],
    *,
    include_colinear: bool = False,
    order_only: bool = False,
):
    indexes = convex_hull_indexes(
        points,
        include_colinear=include_colinear,
        order_only=order_only,
    )
    return (
        points[indexes]
        if isinstance(points, np.ndarray)
        else [points[i] for i in indexes]
    )
