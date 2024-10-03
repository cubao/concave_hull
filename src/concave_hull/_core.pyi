"""

        A very fast 2D concave hull algorithm
        -------------------------------------

        credits:
            -   https://github.com/mapbox/concaveman
            -   https://github.com/sadaszewski/concaveman-cpp
            -   https://cp-algorithms.com/geometry/convex-hull.html#implementation

"""
from __future__ import annotations

import numpy

__all__ = [
    "clockwise",
    "colinear",
    "concave_hull_indexes",
    "convex_hull_indexes",
    "orientation",
    "wgs84_to_east_north",
]

def clockwise(
    prev: numpy.ndarray[numpy.float64[2, 1]],
    curr: numpy.ndarray[numpy.float64[2, 1]],
    next: numpy.ndarray[numpy.float64[2, 1]],
    *,
    include_colinear: bool = False,
) -> bool: ...
def colinear(
    prev: numpy.ndarray[numpy.float64[2, 1]],
    curr: numpy.ndarray[numpy.float64[2, 1]],
    next: numpy.ndarray[numpy.float64[2, 1]],
) -> bool: ...
def concave_hull_indexes(
    points: numpy.ndarray[numpy.float64[m, 2]],
    *,
    convex_hull_indexes: numpy.ndarray[numpy.int32[m, 1]],
    concavity: float = 2.0,
    length_threshold: float = 0.0,
) -> numpy.ndarray[numpy.int32[m, 1]]:
    """
    documents here: https://github.com/mapbox/concaveman
    """

def convex_hull_indexes(
    points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    *,
    include_colinear: bool = False,
    order_only: bool = False,
) -> numpy.ndarray[numpy.int32[m, 1]]: ...
def orientation(
    prev: numpy.ndarray[numpy.float64[2, 1]],
    curr: numpy.ndarray[numpy.float64[2, 1]],
    next: numpy.ndarray[numpy.float64[2, 1]],
) -> int: ...
def wgs84_to_east_north(
    wgs84: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous]
) -> numpy.ndarray[numpy.float64[m, 2]]:
    """
    documents here: https://github.com/mapbox/cheap-ruler
    """

__version__: str = "0.0.8"
