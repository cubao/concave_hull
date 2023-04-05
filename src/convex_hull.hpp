// https://github.com/cubao/concave_hull/discussions/20
// based on
// https://cp-algorithms.com/geometry/convex-hull.html#grahams-scan-algorithm

#ifndef CUBAO_CONVEX_HULL_HPP
#define CUBAO_CONVEX_HULL_HPP

#include <Eigen/Core>
#include <vector>
#include <algorithm>

namespace cubao
{
namespace convex_hull
{

inline int orientation(const Eigen::Vector2d &a, //
                       const Eigen::Vector2d &b, //
                       const Eigen::Vector2d &c)
{
    // np.sign(np.cross(a->b, a->c)[2])
    double v =
        a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]);
    if (v < 0)
        return -1; // clockwise
    if (v > 0)
        return +1; // counter-clockwise
    return 0;
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
    const int N = points.rows();
    Eigen::Vector2d p0(points(0, 0), points(0, 1));
    for (int i = 1; i < N; ++i) {
        if (points(i, 1) < p0[1] ||
            (points(i, 1) == p0[1] && points(i, 0) < p0[0])) {
            p0[0] = points(i, 0);
            p0[1] = points(i, 1);
        }
    }
    std::vector<int> index(N);
    std::iota(index.begin(), index.end(), 0);
    std::sort(index.begin(), index.end(), [&](int i, int j) {
        int o = orientation(p0, points.row(i), points.row(j));
        if (o == 0) {
            return squaredNorm(points.row(i), p0) <
                   squaredNorm(points.row(j), p0);
        }
        return o < 0;
    });
    if (include_colinear) {
        int i = N - 1;
        while (i >= 0 &&
               colinear(p0, points.row(index[i]), points.row(index.back()))) {
            i--;
        }
        std::reverse(index.begin() + i + 1, index.end());
    }
    if (order_only) {
        return Eigen::VectorXi::Map(&index[0], index.size());
    }
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
    std::reverse(st.begin(), st.end());
    return Eigen::VectorXi::Map(&st[0], st.size());
}

} // namespace convex_hull
} // namespace cubao

#endif
