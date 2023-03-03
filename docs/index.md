# cmake_example

Example pybind11 module built with a CMake-based build system.

It's a [fork](https://github.com/cubao/cmake_example) of [pybind/cmake_example](https://github.com/pybind/cmake_example)
with some modifications:

-   integrate python code along side c++ pybind code
-   release to pypi
-   use markdown document

## Usage

Install:

```bash
python3 -m pip install cubao_cmake_example # install from pypi
python3 -c 'import cubao_cmake_example; print(cubao_cmake_example.add(1, 2))'
```

CLI interface:

```bash
python3 -m cubao_cmake_example add 1 2
python3 -m cubao_cmake_example subtract 9 4
```

Help:

```bash
$ python3 -m cubao_cmake_example pure_python_func --help
INFO: Showing help with the command '__main__.py pure_python_func -- --help'.

NAME
    __main__.py pure_python_func

SYNOPSIS
    __main__.py pure_python_func <flags>

FLAGS
    --arg1=ARG1
        Type: int
        Default: 42
    --arg2=ARG2
        Type: float
        Default: 3.14
    --arg3=ARG3
        Type: str
        Default: 'you shall not pass'

$ python3 -m cubao_cmake_example pure_python_func --arg1=43234
int: 43234, float: 3.14, str: you shall not pass
```

<div class="text-center">
<a href="https://github.com/cubao/cmake_example" class="btn btn-primary" role="button">Code on GitHub</a>
<a href="https://pypi.org/project/cubao-cmake-example" class="btn btn-primary" role="button">Package on Pypi</a>
</div>

## Related

More examples at [cubao](https://github.com/cubao), e.g.:

-   [pybind11-rdp](https://github.com/cubao/pybind11-rdp): C++ implementation
    of the Ramer-Douglas-Peucker algorithm (binding to python via pybind11)
-   [concave_hull](https://github.com/cubao/concave_hull):  A very fast 2D concave hull algorithm, for python
