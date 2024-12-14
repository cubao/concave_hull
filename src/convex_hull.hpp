// https://github.com/cubao/concave_hull/discussions/20
// based on
// https://cp-algorithms.com/geometry/convex-hull.html#grahams-scan-algorithm

#ifndef CUBAO_CONVEX_HULL_HPP
#define CUBAO_CONVEX_HULL_HPP

#include <Eigen/Core>
#include <vector>
#include <algorithm>
#include "dbg.h"

namespace cubao
{
namespace convex_hull
{

inline int orientation(const Eigen::Vector2d &a, //
                       const Eigen::Vector2d &b, //
                       const Eigen::Vector2d &c)
{
    const double EPSILON = 1e-12;
    double v = a[0] * (b[1] - c[1]) + 
               b[0] * (c[1] - a[1]) + 
               c[0] * (a[1] - b[1]);
    if (std::abs(v) < EPSILON) return 0;
    return (v < 0) ? -1 : +1;
}
inline bool cw(const Eigen::Vector2d &a, //
               const Eigen::Vector2d &b, //
               const Eigen::Vector2d &c, //
               bool include_colinear)
{
    int o = orientation(a, b, c);
    return o < 0 || (include_colinear && o == 0);
}
inline bool colinear(const Eigen::Vector2d &a, //
                     const Eigen::Vector2d &b, //
                     const Eigen::Vector2d &c)
{
    return orientation(a, b, c) == 0;
}

using RowVectorsNx2 = Eigen::Matrix<double, Eigen::Dynamic, 2, Eigen::RowMajor>;

inline double squaredNorm(const Eigen::Vector2d &a, const Eigen::Vector2d &b)
{
    return (a - b).squaredNorm();
}

inline Eigen::VectorXi
convex_hull_indexes(const Eigen::Ref<const RowVectorsNx2> &points,
                    bool include_colinear = false, //
                    bool order_only = false)
{
    std::cout << "shit me points" << points << std::endl;
    const int N = points.rows();
    if (N == 0) {
        return Eigen::VectorXi(0);
    }
    dbg(N);
    dbg(include_colinear);
    dbg(order_only);
    dbg("hello");
    Eigen::Vector2d p0(points(0, 0), points(0, 1));
    for (int i = 1; i < N; ++i) {
        if (points(i, 1) < p0[1] ||
            (points(i, 1) == p0[1] && points(i, 0) < p0[0])) {
            p0[0] = points(i, 0);
            p0[1] = points(i, 1);
        }
    }
    dbg("yes");
    std::vector<int> index(N);
    std::iota(index.begin(), index.end(), 0);
    std::cout << "index" << Eigen::VectorXi::Map(&index[0], index.size()).transpose() << std::endl;
    dbg(index);
    dbg("yes2");
    std::sort(index.begin(), index.end(), [&](int i, int j) {
        dbg(i, j);
        int o = orientation(p0, points.row(i), points.row(j));
        dbg(o);
        if (o == 0) {
            return squaredNorm(points.row(i), p0) <
                   squaredNorm(points.row(j), p0);
        }
        return o < 0;
    });
    dbg("yes3");
    if (include_colinear) {
        int i = N - 1;
        while (i >= 0 &&
               colinear(p0, points.row(index[i]), points.row(index.back()))) {
            i--;
        }
        std::reverse(index.begin() + i + 1, index.end());
    }
    dbg("yes4");
    if (order_only) {
        return Eigen::VectorXi::Map(&index[0], index.size());
    }
    dbg("yes5");
    std::vector<int> st;
    for (int i = 0; i < N; i++) {
        while (st.size() > 1 && !cw(points.row(st[st.size() - 2]), //
                                    points.row(st.back()),         //
                                    points.row(index[i]),          //
                                    include_colinear)) {
            st.pop_back();
        }
        st.push_back(index[i]);
    }
    // in ccw orientation
    dbg(st.size());
    std::reverse(st.begin(), st.end());
    dbg(st);
    return Eigen::VectorXi::Map(&st[0], st.size());
}

} // namespace convex_hull
} // namespace cubao

#endif
