import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

from concave_hull import concave_hull_indexes

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
    plt.plot(points[simplex, 0], points[simplex, 1], "g-", alpha=0.5)

idxes = concave_hull_indexes(
    points[:, :2],
    convex_hull_indexes=convex_hull.vertices.astype(np.int32),
    length_threshold=50,
)

for f, t in zip(idxes[:-1], idxes[1:]):
    seg = points[[f, t]]
    plt.plot(seg[:, 0], seg[:, 1], "r-", alpha=0.5)
plt.show()
