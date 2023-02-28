// https://github.com/microsoft/vscode-cpptools/issues/9692
#if __INTELLISENSE__
#undef __ARM_NEON
#undef __ARM_NEON__
#endif

#include <Eigen/Core>

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#include "concaveman.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

using RowVectors = Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>;
using RowVectorsNx3 = RowVectors;
using RowVectorsNx2 = Eigen::Matrix<double, Eigen::Dynamic, 2, Eigen::RowMajor>;

Eigen::VectorXi concave_hull_indexes(
    const RowVectorsNx2 &points2d,
    const Eigen::Ref<const Eigen::VectorXi> &convex_hull_indexes,
    double concavity, double lengthThreshould)
{
    std::vector<int> hull;
    hull.resize(convex_hull_indexes.size());
    Eigen::VectorXi::Map(&hull[0], hull.size()) = convex_hull_indexes;

    std::vector<std::array<double, 2>> points;
    points.resize(points2d.rows());
    RowVectorsNx2::Map(&points[0][0], points.size(), 2) = points2d;
    auto indexes = concaveman_indexes<double, 16>(points, hull, concavity,
                                                  lengthThreshould);
    return Eigen::VectorXi::Map(&indexes[0], indexes.size());
}

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(pybind11_concave_hull, m)
{
    m.doc() = R"pbdoc(
        A very fast 2D concave hull algorithm
        -------------------------------------

        credits:
            -   https://github.com/mapbox/concaveman
            -   https://github.com/sadaszewski/concaveman-cpp

        .. currentmodule:: concave_hull

        .. autosummary::
           :toctree: _generate

           rdp
           rdp_mask
    )pbdoc";

    m.def("concave_hull_indexes", &concave_hull_indexes, "points"_a,
          py::kw_only(),           //
          "convex_hull_indexes"_a, //
          "concavity"_a = 2.0,
          "length_threshold"_a = 0.0, //
          "documents here: https://github.com/mapbox/concaveman");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
