import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

from concave_hull import LineSegment, concave_hull_indexes

seg = LineSegment([0, 0, 0], [10, 0, 0])
assert 4.0 == seg.distance([5.0, 4.0, 0.0])
assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
assert 5.0 == seg.distance([14.0, 3.0, 0.0])
seg = LineSegment([0, 0, 0], [0, 0, 0])
assert 5.0 == seg.distance([3.0, 4.0, 0.0])
assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
assert 13.0 == seg.distance([5.0, 12.0, 0.0])

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
points = np.array(points)
convex_hull = ConvexHull(points)

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html

plt.plot(points[:, 0], points[:, 1], "o")
for simplex in convex_hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], "k-")

idxes = concave_hull_indexes(
    points[:, :2],
    convex_hull_indexes=convex_hull.vertices.astype(np.int32),
)

for f, t in zip(idxes[:-1], idxes[1:]):
    seg = points[[f, t]]
    plt.plot(seg[:, 0], seg[:, 1], "k-")
plt.show()
