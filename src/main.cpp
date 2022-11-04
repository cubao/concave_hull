// https://github.com/microsoft/vscode-cpptools/issues/9692
#if __INTELLISENSE__
#undef __ARM_NEON
#undef __ARM_NEON__
#endif

#include <Eigen/Core>

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

struct LineSegment
{
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    const Eigen::Vector3d A, B, AB;
    const double len2, inv_len2;
    LineSegment(const Eigen::Vector3d &a, const Eigen::Vector3d &b)
        : A(a), B(b), AB(b - a), //
          len2((b - a).squaredNorm()), inv_len2(1.0 / len2)
    {
    }
    double distance2(const Eigen::Vector3d &P) const
    {
        double dot = (P - A).dot(AB);
        if (dot <= 0) {
            return (P - A).squaredNorm();
        } else if (dot >= len2) {
            return (P - B).squaredNorm();
        }
        // P' = A + dot/length * normed(AB)
        //    = A + dot * AB / (length^2)
        return (A + (dot * inv_len2 * AB) - P).squaredNorm();
    }
    double distance(const Eigen::Vector3d &P) const
    {
        return std::sqrt(distance2(P));
    }
};

using RowVectors = Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>;
using RowVectorsNx3 = RowVectors;
using RowVectorsNx2 = Eigen::Matrix<double, Eigen::Dynamic, 2, Eigen::RowMajor>;

void douglas_simplify(const Eigen::Ref<const RowVectors> &coords,
                      Eigen::VectorXi &to_keep, const int i, const int j,
                      const double epsilon)
{
    to_keep[i] = to_keep[j] = 1;
    if (j - i <= 1) {
        return;
    }
    LineSegment line(coords.row(i), coords.row(j));
    double max_dist2 = 0.0;
    int max_index = i;
    for (int k = i + 1; k < j; ++k) {
        double dist2 = line.distance2(coords.row(k));
        if (dist2 > max_dist2) {
            max_dist2 = dist2;
            max_index = k;
        }
    }
    if (max_dist2 <= epsilon * epsilon) {
        return;
    }
    douglas_simplify(coords, to_keep, i, max_index, epsilon);
    douglas_simplify(coords, to_keep, max_index, j, epsilon);
}

Eigen::VectorXi
douglas_simplify_mask(const Eigen::Ref<const RowVectors> &coords,
                      double epsilon)
{
    Eigen::VectorXi mask(coords.rows());
    mask.setZero();
    douglas_simplify(coords, mask, 0, mask.size() - 1, epsilon);
    return mask;
}

Eigen::VectorXi mask2indexes(const Eigen::Ref<const Eigen::VectorXi> &mask)
{
    Eigen::VectorXi indexes(mask.sum());
    for (int i = 0, j = 0, N = mask.size(); i < N; ++i) {
        if (mask[i]) {
            indexes[j++] = i;
        }
    }
    return indexes;
}

Eigen::VectorXi
douglas_simplify_indexes(const Eigen::Ref<const RowVectors> &coords,
                         double epsilon)
{
    return mask2indexes(douglas_simplify_mask(coords, epsilon));
}

RowVectors select_by_mask(const Eigen::Ref<const RowVectors> &coords,
                          const Eigen::Ref<const Eigen::VectorXi> &mask)
{
    RowVectors ret(mask.sum(), coords.cols());
    int N = mask.size();
    for (int i = 0, k = 0; i < N; ++i) {
        if (mask[i]) {
            ret.row(k++) = coords.row(i);
        }
    }
    return ret;
}

inline RowVectors douglas_simplify(const Eigen::Ref<const RowVectors> &coords,
                                   double epsilon)
{
    return select_by_mask(coords, douglas_simplify_mask(coords, epsilon));
}

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(pybind11_rdp, m)
{
    m.doc() = R"pbdoc(
        c++/pybind11 version of Ramer-Douglas-Peucker (rdp) algorithm
        -------------------------------------------------------------

        .. currentmodule:: pybind11_rdp

        .. autosummary::
           :toctree: _generate

           rdp
           rdp_mask
    )pbdoc";

    py::class_<LineSegment>(m, "LineSegment") //
        .def(py::init<const Eigen::Vector3d, const Eigen::Vector3d>(), "A"_a,
             "B"_a)
        .def("distance", &LineSegment::distance, "P"_a)
        .def("distance2", &LineSegment::distance2, "P"_a)
        //
        ;

    auto rdp_doc = R"pbdoc(
        Simplifies a given array of points using the Ramer-Douglas-Peucker algorithm.

        Example:
        >>> from pybind11_rdp import rdp
        >>> rdp([[1, 1], [2, 2], [3, 3], [4, 4]])
        [[1, 1], [4, 4]]
    )pbdoc";

    m.def(
        "rdp",
        [](const Eigen::Ref<const RowVectors> &coords, double epsilon)
            -> RowVectors { return douglas_simplify(coords, epsilon); },
        rdp_doc, "coords"_a, py::kw_only(), "epsilon"_a = 0.0);
    m.def(
        "rdp",
        [](const Eigen::Ref<const RowVectorsNx2> &coords,
           double epsilon) -> RowVectorsNx2 {
            RowVectors xyzs(coords.rows(), 3);
            xyzs.setZero();
            xyzs.leftCols(2) = coords;
            return douglas_simplify(xyzs, epsilon).leftCols(2);
        },
        rdp_doc, "coords"_a, py::kw_only(), "epsilon"_a = 0.0);

    auto rdp_mask_doc = R"pbdoc(
        Simplifies a given array of points using the Ramer-Douglas-Peucker algorithm.
        return a mask.
    )pbdoc";
    m.def(
        "rdp_mask",
        [](const Eigen::Ref<const RowVectors> &coords,
           double epsilon) -> Eigen::VectorXi {
            return douglas_simplify_mask(coords, epsilon);
        },
        rdp_mask_doc, "coords"_a, py::kw_only(), "epsilon"_a = 0.0);
    m.def(
        "rdp_mask",
        [](const Eigen::Ref<const RowVectorsNx2> &coords,
           double epsilon) -> Eigen::VectorXi {
            RowVectors xyzs(coords.rows(), 3);
            xyzs.setZero();
            xyzs.leftCols(2) = coords;
            return douglas_simplify_mask(xyzs, epsilon);
        },
        rdp_mask_doc, "coords"_a, py::kw_only(), "epsilon"_a = 0.0);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
