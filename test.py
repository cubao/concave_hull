import time

import numpy as np
from pybind11_rdp import LineSegment
from pybind11_rdp import rdp as rdp_pybind
from pybind11_rdp import rdp_mask as rdp_mask
from rdp import rdp as rdp_python

seg = LineSegment([0, 0, 0], [10, 0, 0])
assert 4.0 == seg.distance([5.0, 4.0, 0.0])
assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
assert 5.0 == seg.distance([14.0, 3.0, 0.0])
seg = LineSegment([0, 0, 0], [0, 0, 0])
assert 5.0 == seg.distance([3.0, 4.0, 0.0])
assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
assert 13.0 == seg.distance([5.0, 12.0, 0.0])

for fn in [rdp_python, rdp_pybind]:
    print("#" * 80)
    print(fn)

    print()
    coords = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], dtype=np.float64)
    print(coords)
    print(fn(coords))

    print()
    coords = np.array([[1, 1], [1, 1.1], [2, 2]], dtype=np.float64)
    print(coords)
    print(fn(coords, epsilon=0.5))

enus = np.load("data/enus.npy")
assert enus.shape == (2000, 3)
print("enus")
print(enus)

durations = []


def my_timer(func):
    def wrapper(*arg, **kw):
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        delta = max(t2 - t1, 1e-18)
        print(f"{delta} seconds")
        durations.append(delta)
        return res

    return wrapper


@my_timer
def python_rdp(xyzs: np.ndarray, *, epsilon: float = 0.0, return_mask: bool = False):
    return rdp_python(xyzs, epsilon=epsilon, return_mask=return_mask)


@my_timer
def cpp_rdp(
    xyzs: np.ndarray, *, epsilon: float = 0.0, return_mask: bool = False
) -> np.ndarray:
    return (
        rdp_pybind(xyzs, epsilon=epsilon)
        if not return_mask
        else rdp_mask(xyzs, epsilon=epsilon)
    )


print("benchmarking... python/c++ version")
for return_mask in (True, False):
    for eps in (10.0, 5.0, 2.0, 1.0, 0.5, 0.1, 0.0):
        for dim in (3, 2):
            print("\n" * 4)
            ret1 = python_rdp(enus[:, :dim], epsilon=eps, return_mask=return_mask)
            ret2 = cpp_rdp(enus[:, :dim], epsilon=eps, return_mask=return_mask)
            print(f"mask?: {return_mask}, epsilon: {eps}, dim: {dim}")
            print(ret1.shape, ret2.shape)
            print(f"speed up: {durations[-2] / durations[-1]:.2f}")
            if return_mask:
                if len(ret1) != len(ret2):
                    raise Exception(f"mismatch! {len(ret1)} != {len(ret2)}")
                else:
                    ret1 = ret1.astype(np.int32)
                    ret2 = ret2.astype(np.int32)
                    delta = np.abs(ret1 - ret2).sum()
                    if delta != 0:
                        raise Exception(f"mismatch! {ret1 - ret2}")
            delta = np.abs(np.array(ret1) - np.array(ret2)).sum()
            assert delta == 0
