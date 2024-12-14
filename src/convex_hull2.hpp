// https://github.com/mapbox/concaveman/pull/17/files

// https://github.com/mourner/robust-predicates/blob/main/src/orient2d.js
#pragma once

#include "orient2d.hpp"
#include <vector>
#include <array>

namespace cubao
{
namespace convex_hull2
{
// https://github.com/mourner/robust-predicates/blob/main/src/orient2d.js

inline double cross(const double *p1, const double *p2, const double *p3)
{
    return robust_predicates::orient2d(p1[0], p1[1], //
                                       p2[0], p2[1], //
                                       p3[0], p3[1]);
}

// https://github.com/mapbox/concaveman/blob/master/index.js
// check if the edges (p1,q1) and (p2,q2) intersect
inline bool intersects(const double *p1, const double *q1, //
                       const double *p2, const double *q2)
{
    return !(p1[0] == q2[0] && p1[1] == q2[1]) &&
           !(q1[0] == p2[0] && q1[1] == p2[1]) &&
           (cross(p1, q1, p2) > 0) != (cross(p1, q1, q2) > 0) &&
           (cross(p2, q2, p1) > 0) != (cross(p2, q2, q1) > 0);
}

inline std::vector<std::array<double, 3>>
convexHull(std::vector<std::array<double, 3>> points)
{
    std::sort(points.begin(), points.end(), [](const auto &a, const auto &b) {
        return a[0] == b[0] ? a[1] - b[1] : a[0] - b[0];
    });

    std::vector<std::array<double, 3>> lower;
    for (size_t i = 0; i < points.size(); i++) {
        while (lower.size() >= 2 &&
               cross(lower[lower.size() - 2].data(),
                     lower[lower.size() - 1].data(), points[i].data()) <= 0) {
            lower.pop_back();
        }
        lower.push_back(points[i]);
    }

    std::vector<std::array<double, 3>> upper;
    for (int i = points.size() - 1; i >= 0; i--) {
        while (upper.size() >= 2 &&
               cross(upper[upper.size() - 2].data(),
                     upper[upper.size() - 1].data(), points[i].data()) <= 0) {
            upper.pop_back();
        }
        upper.push_back(points[i]);
    }

    upper.pop_back();
    lower.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());
    return lower;
}

// https://www.npmjs.com/package/point-in-polygon?activeTab=code
inline bool pointInPolygon(const double *point,                  //
                           const double *polygon, size_t length, //
                           int start = -1, int end = -1)
{
    double x = point[0], y = point[1];
    bool inside = false;
    if (start < 0)
        start = 0;
    if (end < 0)
        end = length;
    int len = end - start;
    for (int i = 0, j = len - 1; i < len; j = i++) {
        double xi = polygon[(i + start) * 2], yi = polygon[(i + start) * 2 + 1];
        double xj = polygon[(j + start) * 2], yj = polygon[(j + start) * 2 + 1];
        bool intersect = ((yi > y) != (yj > y)) &&
                         (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect)
            inside = !inside;
    }
    return inside;
}

// speed up convex hull by filtering out points inside quadrilateral formed by 4
// extreme points
inline std::vector<std::array<double, 3>>
fastConvexHull(const std::vector<std::array<double, 3>> &points)
{
    if (points.empty()) {
        return {};
    }

    auto left = points[0];
    auto top = points[0];
    auto right = points[0];
    auto bottom = points[0];

    // find the leftmost, rightmost, topmost and bottommost points
    for (const auto &p : points) {
        if (p[0] < left[0])
            left = p;
        if (p[0] > right[0])
            right = p;
        if (p[1] < top[1])
            top = p;
        if (p[1] > bottom[1])
            bottom = p;
    }

    // filter out points that are inside the resulting quadrilateral
    std::vector<std::array<double, 2>> cull = {{left[0], left[1]},
                                               {top[0], top[1]},
                                               {right[0], right[1]},
                                               {bottom[0], bottom[1]}};
    std::vector<std::array<double, 3>> filtered = {left, top, right, bottom};
    for (const auto &p : points) {
        if (!pointInPolygon(&p[0], &cull[0][0], cull.size())) {
            filtered.push_back(p);
        }
    }
    // get convex hull around the filtered points
    return convexHull(filtered);
}

} // namespace convex_hull2
} // namespace cubao
