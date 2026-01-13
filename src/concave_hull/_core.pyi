"""

        A very fast 2D concave hull algorithm
        -------------------------------------

        credits:
            -   https://github.com/mapbox/concaveman
            -   https://github.com/sadaszewski/concaveman-cpp
            -   https://cp-algorithms.com/geometry/convex-hull.html#implementation

"""
from __future__ import annotations

import typing

import numpy
import numpy.typing

__all__: list[str] = [
    "clockwise",
    "colinear",
    "concave_hull_indexes",
    "convex_hull_indexes",
    "orientation",
    "wgs84_to_east_north",
]

def clockwise(
    prev: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    curr: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    next: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    *,
    include_colinear: bool = False,
) -> bool: ...
def colinear(
    prev: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    curr: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    next: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
) -> bool: ...
def concave_hull_indexes(
    points: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 2]"],
    *,
    convex_hull_indexes: typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"],
    concavity: typing.SupportsFloat = 2.0,
    length_threshold: typing.SupportsFloat = 0.0,
) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
    """
    documents here: https://github.com/mapbox/concaveman
    """

def convex_hull_indexes(
    points: typing.Annotated[
        numpy.typing.NDArray[numpy.float64], "[m, 2]", "flags.c_contiguous"
    ],
    *,
    include_colinear: bool = False,
    order_only: bool = False,
) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]: ...
def orientation(
    prev: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    curr: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
    next: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[2, 1]"],
) -> int: ...
def wgs84_to_east_north(
    wgs84: typing.Annotated[
        numpy.typing.NDArray[numpy.float64], "[m, 2]", "flags.c_contiguous"
    ]
) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 2]"]:
    """
    documents here: https://github.com/mapbox/cheap-ruler
    """

__version__: str = "0.1.0"
