// https://github.com/microsoft/vscode-cpptools/issues/9692
#if __INTELLISENSE__
#undef __ARM_NEON
#undef __ARM_NEON__
#endif

#include <Eigen/Core>

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#include "convex_hull.hpp"
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

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// based on
// https://github.com/cubao/headers/blob/main/include/cubao/crs_transform.hpp
inline Eigen::Vector3d cheap_ruler_k(double latitude)
{
    // based on https://github.com/mapbox/cheap-ruler-cpp
    static constexpr double RE = 6378.137;
    static constexpr double FE = 1.0 / 298.257223563;
    static constexpr double E2 = FE * (2 - FE);
    static constexpr double RAD = M_PI / 180.0;
    static constexpr double MUL = RAD * RE * 1000.;
    double coslat = std::cos(latitude * RAD);
    double w2 = 1 / (1 - E2 * (1 - coslat * coslat));
    double w = std::sqrt(w2);
    return Eigen::Vector3d(MUL * w * coslat, MUL * w * w2 * (1 - E2), 1.0);
}
// use first wgs84 as anchor point to scale all lon/lat coords to east/north,
// results in meters
inline RowVectorsNx2
WGS84_to_EAST_NORTH(const Eigen::Ref<const RowVectorsNx2> &llas)
{
    Eigen::Vector2d anchor = llas.row(0);
    auto k = cheap_ruler_k(anchor[1]);
    RowVectorsNx2 enus = llas;
    for (int i = 0; i < 2; ++i) {
        enus.col(i).array() -= anchor[i];
        enus.col(i).array() *= k[i];
    }
    return enus;
}

PYBIND11_MODULE(_core, m)
{
    m.doc() = R"pbdoc(
        A very fast 2D concave hull algorithm
        -------------------------------------

        credits:
            -   https://github.com/mapbox/concaveman
            -   https://github.com/sadaszewski/concaveman-cpp
            -   https://cp-algorithms.com/geometry/convex-hull.html#implementation
    )pbdoc";

    m.def("concave_hull_indexes", &concave_hull_indexes, "points"_a,
          py::kw_only(),           //
          "convex_hull_indexes"_a, //
          "concavity"_a = 2.0,
          "length_threshold"_a = 0.0, //
          "documents here: https://github.com/mapbox/concaveman");

    m.def("wgs84_to_east_north", &WGS84_to_EAST_NORTH, "wgs84"_a,
          "documents here: https://github.com/mapbox/cheap-ruler");

    m.def("convex_hull_indexes", &cubao::convex_hull::convex_hull_indexes,
          "points"_a,                   //
          py::kw_only(),                //
          "include_colinear"_a = false, //
          "order_only"_a = false)
        .def("orientation", &cubao::convex_hull::orientation, //
             "prev"_a, "curr"_a, "next"_a)
        .def("clockwise", &cubao::convex_hull::cw, //
             "prev"_a, "curr"_a, "next"_a,         //
             py::kw_only(),                        //
             "include_colinear"_a = false)
        .def("colinear", &cubao::convex_hull::colinear, //
             "prev"_a, "curr"_a, "next"_a)
        //
        ;

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
