# concave_hull

A very fast 2D concave hull algorithm.

![](docs/hull.png)

Credits goes to:

-   <https://github.com/mapbox/concaveman>
-   <https://github.com/sadaszewski/concaveman-cpp>

Online document: <https://concave-hull.readthedocs.io/en/latest/>

<!--intro-start-->

## Install

### via pip

```bash
pip install -U concave_hull
```

### from source

```bash
git clone --recursive https://github.com/cubao/concave_hull
pip install ./concave_hull
```

Or

```bash
pip install git+https://github.com/cubao/concave_hull.git
```

(you can build wheels for later reuse by ` pip wheel git+https://github.com/cubao/concave_hull.git`)

### in the browser (pyodide / wasm)

A pyodide wheel is built by the `Wheel on pyodide` job in
[`.github/workflows/wheels.yml`](.github/workflows/wheels.yml) and published to
PyPI together with the other wheels. Inside pyodide:

```js
const pyodide = await loadPyodide();
await pyodide.loadPackage(["numpy", "micropip"]);
const micropip = pyodide.pyimport("micropip");
await micropip.install("concave-hull"); // or a local wheel: "./concave_hull-...wasm32.whl"
const { concave_hull } = pyodide.pyimport("concave_hull");
```

To build and test locally:

```bash
make pyodide_install   # pip install pyodide-build
make pyodide_wheel     # -> dist/*wasm32.whl
make pyodide_web       # builds, writes tests/pyodide/wheels.json, serves :8123
# open http://localhost:8123/tests/pyodide/index.html
```

Each wheel is ABI-tagged for one pyodide runtime (`pyemscripten_2024_0_wasm32` …)
and the page's pyodide version has to match that tag. CI builds one wheel per
supported pyodide version; locally `pyodide build` picks the xbuildenv whose
CPython matches your host interpreter, so a Python 3.12 host gets pyodide 0.27.x
(ABI 2024_0). Use `pyodide xbuildenv install <version> --force` to target
another version — `gen_wheels_json.py` then writes it into `wheels.json`, and
`?pyodide_version=` overrides it in the browser.

[`tests/pyodide/index.html`](tests/pyodide/index.html) loads pyodide (by default
from the jsdelivr CDN), installs the wheel from `dist/` and runs `tests/` in the
browser. If the CDN is slow, mirror the runtime once and the page picks it up
automatically:

```bash
python tests/pyodide/fetch_pyodide_dist.py --version 0.27.8
```

## Usage

Signature:

```python
# import
from concave_hull import concave_hull, concave_hull_indexes

# get concave hull indexes
concave_hull_indexes(
       points: Union[numpy.ndarray, List, Tuple],
       *,
       concavity: float = 2.0,
       length_threshold: float = 0.0,
       # you can just ignore "convex_hull_indexes"
       convex_hull_indexes: numpy.ndarray[numpy.int32[m, 1]] = None,
) -> numpy.ndarray[numpy.int32[m, 1]]

# get concave hull points
concave_hull(
       points: Union[numpy.ndarray, List, Tuple],
       ... # same as
) -> Union[numpy.ndarray, List, Tuple]

# P.S., we provide convex_hull (Graham scan)
from concave_hull import convex_hull, convex_hull_indexes
```

-   `concavity` is a relative measure of concavity. 1 results in a relatively
    detailed shape, Infinity results in a convex hull. You can use values lower
    than 1, but they can produce pretty crazy shapes.
-   `length_threshold`: when a segment length is under this threshold, it stops
    being considered for further detalization. Higher values result in simpler
    shapes.

(document from <https://github.com/mapbox/concaveman>)

Example (see full code in [`test.py`](test.py)):

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

from concave_hull import concave_hull, concave_hull_indexes

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
convex_hull = ConvexHull(points[:, :2])  # it's already N-by-2, I'm just emphasizing

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html

plt.plot(points[:, 0], points[:, 1], "o")
for simplex in convex_hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], "g-", alpha=0.5)

idxes = concave_hull_indexes(
    points[:, :2],
    length_threshold=50,
)
# you can get coordinates by `points[idxes]`
assert np.all(points[idxes] == concave_hull(points, length_threshold=50))

for f, t in zip(idxes[:-1], idxes[1:]):  # noqa
    seg = points[[f, t]]
    plt.plot(seg[:, 0], seg[:, 1], "r-", alpha=0.5)
# plt.savefig('hull.png')
plt.show()
```

<!--intro-end-->

## Tests

```
make python_install
make python_test
```
