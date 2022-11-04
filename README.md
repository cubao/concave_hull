# Ramer-Douglas-Peucker Algorithm (c++ binding for python via pybind11)

>   A speed up (~8000x) version of [python version of rdp](https://github.com/fhirschmann/rdp).

C++/pybind11/NumPy implementation of the Ramer-Douglas-Peucker algorithm (Ramer 1972; Douglas and Peucker 1973) for 2D and 3D data.

The Ramer-Douglas-Peucker algorithm is an algorithm for reducing the number of points in a curve that is approximated by a series of points.


## Installation

### via pip

```
pip install pybind11-rdp
```

### from source

```bash
git clone --recursive https://github.com/cubao/pybind11-rdp
pip install ./pybind11-rdp
```

Or

```
pip install git+https://github.com/cubao/pybind11-rdp.git
```

(you can build wheels for later reuse by ` pip wheel git+https://github.com/cubao/pybind11-rdp.git`)

## Usage

Test installation: `python -c 'from pybind11_rdp import rdp; print(rdp([[1, 1], [2, 2], [3, 3], [4, 4]]))'`

Simple pythonic interface:

```python
from pybind11_rdp import rdp

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
from pybind11_rdp import rdp

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
