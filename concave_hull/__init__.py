from pybind11_concave_hull import concave_hull_indexes as concave_hull_indexes_impl  # noqa
from pybind11_concave_hull import __version__  # noqa

import numpy as np
from scipy.spatial import ConvexHull

def concave_hull_indexes(
    points: np.ndarray,
    *,
    convex_hull_indexes: np.ndarray = None,
    concavity: float = 2.0,
    length_threshold: float = 0.0,
):
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
