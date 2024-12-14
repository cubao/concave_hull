// https://github.com/mapbox/concaveman/pull/17/files

// https://github.com/mourner/robust-predicates/blob/main/src/orient2d.js
#pragma once

#include "orient2d.hpp"

namespace cubao
{
namespace convex_hull2
{
// https://github.com/mourner/robust-predicates/blob/main/src/orient2d.js

double cross(const double *p1, const double *p2, const double *p3)
{
    return robust_predicates::orient2d(p1[0], p1[1], p2[0], p2[1], p3[0],
                                       p3[1]);
}

// https://github.com/mapbox/concaveman/blob/master/index.js
// check if the edges (p1,q1) and (p2,q2) intersect
bool intersects(const double *p1, const double *q1, const double *p2,
                const double *q2)
{
    return !(p1[0] == q2[0] && p1[1] == q2[1]) &&
           !(q1[0] == p2[0] && q1[1] == p2[1]) &&
           (cross(p1, q1, p2) > 0) != (cross(p1, q1, q2) > 0) &&
           (cross(p2, q2, p1) > 0) != (cross(p2, q2, q1) > 0);
}

} // namespace convex_hull2
} // namespace cubao
