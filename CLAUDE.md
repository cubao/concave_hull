# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

concave_hull is a fast 2D concave hull algorithm implemented as a Python package with C++ backend. It provides both concave and convex hull computation capabilities, based on algorithms from Mapbox's concaveman and C++ adaptation by sadaszewski.

## Build System

This project uses scikit-build-core with CMake as the build backend. Key build commands:

- **Install in development mode**: `make build` or `make python_install`
- **Build wheel**: `make python_wheel`
- **Run tests**: `make python_test` or `make pytest`
- **Clean build artifacts**: `make clean`

The build system compiles a C++ extension module (`_core`) using pybind11, which is then wrapped by Python code in `src/concave_hull/`.

## Code Architecture

### Core Components

1. **C++ Implementation** (`src/`):
   - `main.cpp`: pybind11 bindings exposing C++ functions to Python
   - `concaveman.h`: Core concave hull algorithm implementation
   - `convex_hull.hpp`, `convex_hull2.hpp`: Convex hull implementations (Graham scan)
   - `orient2d.hpp`, `macros.hpp`: Geometry utilities

2. **Python Interface** (`src/concave_hull/__init__.py`):
   - High-level API that wraps the C++ `_core` module
   - Provides `concave_hull()`, `concave_hull_indexes()`, `convex_hull()`, `convex_hull_indexes()`
   - Handles input validation, coordinate transformations (WGS84 support), and type conversions

3. **Key Design Pattern**:
   - C++ functions handle heavy computation using Eigen for linear algebra
   - Python wrapper provides convenient API and handles edge cases
   - All array operations use NumPy-compatible interfaces

### Testing Strategy

- Tests are in `tests/test_basic.py` using pytest
- Tests compare results against pre-computed expected values
- Many tests are currently disabled (marked with `return` at the beginning)
- Test data includes both synthetic points and real geographic data (WGS84 coordinates)

## Development Workflow

### Code Quality Tools

- **Linting**: `make lint` (runs pre-commit hooks)
- **Code formatting**: Uses black, isort, clang-format via pre-commit
- **Type stubs**: `make restub` generates Python type stubs from C++ bindings using pybind11-stubgen

### Common Development Tasks

1. **After modifying C++ code**: Rebuild with `make build`
2. **After modifying Python code**: Re-run tests with `make pytest`
3. **Before committing**: Run `make lint` to ensure code quality
4. **Updating type signatures**: Run `make restub` if C++ function signatures changed

### Geographic Data Support

The package includes special support for WGS84 coordinates through:
- `wgs84_to_east_north()` function in the C++ bindings
- `is_wgs84` parameter in hull functions that triggers coordinate transformation
- Example data in `docs/data/songjiang.json`

## Important Considerations

- The C++ code uses Eigen matrices with row-major storage for NumPy compatibility
- Convex hull implementation uses a modified Graham scan algorithm
- Concave hull implementation uses the concaveman algorithm with tunable concavity parameter
- Input points are always projected to 2D (only x,y coordinates used)
