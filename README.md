# concave_hull

A very fast 2D concave hull algorithm.

Source from:

-   https://github.com/mapbox/concaveman
-   https://github.com/sadaszewski/concaveman-cpp

TODO: integrate concaveman.

https://stackoverflow.com/questions/18169587/get-the-index-of-point-which-create-convexhull

### via pip

```
pip install concave_hull
```

### from source

```bash
git clone --recursive https://github.com/cubao/concave_hull
pip install ./concave_hull
```

Or

```
pip install git+https://github.com/cubao/concave_hull.git
```

(you can build wheels for later reuse by ` pip wheel git+https://github.com/cubao/concave_hull.git`)

## Usage

Test installation: `python -c 'from concave_hull import rdp; print(rdp([[1, 1], [2, 2], [3, 3], [4, 4]]))'`

Simple pythonic interface:

```python
from concave_hull import rdp

rdp([[1, 1], [2, 2], [3, 3], [4, 4]])
[[1, 1], [4, 4]]
```

With epsilon=0.5:

```python
rdp([[1, 1], [1, 1.1], [2, 2]], epsilon=0.5)
[[1.0, 1.0], [2.0, 2.0]]
```

Numpy interface:

```python
import numpy as np
from concave_hull import rdp

rdp(np.array([1, 1, 2, 2, 3, 3, 4, 4]).reshape(4, 2))
array([[1, 1],
       [4, 4]])
```

## Tests

```
python3 test.py
```

## Links

-   https://github.com/fhirschmann/rdp

## References

Douglas, David H, and Thomas K Peucker. 1973. “Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or Its Caricature.” Cartographica: The International Journal for Geographic Information and Geovisualization 10 (2): 112–122.

Ramer, Urs. 1972. “An Iterative Procedure for the Polygonal Approximation of Plane Curves.” Computer Graphics and Image Processing 1 (3): 244–256.
