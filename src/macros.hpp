#pragma once

#include <cmath>

namespace cubao
{
namespace robust_predicates
{
// https://github.com/mourner/robust-predicates/blob/312178014c173cfa5ed0a8cb5496baaf82a63663/compile.js#L6
#define Fast_Two_Sum(a, b, x, y) \
    do { \
        x = a + b; \
        y = b - (x - a); \
    } while (0)

#define Two_Sum(a, b, x, y) \
    do { \
        double bvirt; \
        x = a + b; \
        bvirt = x - a; \
        y = a - (x - bvirt) + (b - bvirt); \
    } while (0)


#define Two_Diff_Tail(a, b, x, y) \
    do { \
        double bvirt = a - x; \
        y = a - (x + bvirt) + (bvirt - b); \
    } while (0)

#define Two_Diff(a, b, x, y) \
    do { \
        x = a - b; \
        Two_Diff_Tail(a, b, x, y); \
    } while (0)

#define Split(a, ahi, alo) \
    do { \
        double c = splitter * a; \
        ahi = c - (c - a); \
        alo = a - ahi; \
    } while (0)

#define Two_Product(a, b, x, y) \
    do { \
        double ahi, alo, bhi, blo; \
        x = a * b; \
        Split(a, ahi, alo); \
        Split(b, bhi, blo); \
        y = alo * blo - (x - ahi * bhi - alo * bhi - ahi * blo); \
    } while (0)

#define Two_Product_Presplit(a, b, bhi, blo, x, y) \
    do { \
        double ahi, alo; \
        x = a * b; \
        Split(a, ahi, alo); \
        y = alo * blo - (x - ahi * bhi - alo * bhi - ahi * blo); \
    } while (0)

#define Square(a, x, y) \
    do { \
        double ahi, alo; \
        x = a * a; \
        Split(a, ahi, alo); \
        y = alo * alo - (x - ahi * ahi - (ahi + ahi) * alo); \
    } while (0)

#define Two_One_Sum(a1, a0, b, x2, x1, x0) \
    do { \
        double _i; \
        Two_Sum(a0, b, _i, x0); \
        Two_Sum(a1, _i, x2, x1); \
    } while (0)

#define Two_One_Diff(a1, a0, b, x2, x1, x0) \
    do { \
        double _i; \
        Two_Diff(a0, b, _i, x0); \
        Two_Sum(a1, _i, x2, x1); \
    } while (0)

#define Two_Two_Sum(a1, a0, b1, b0, x3, x2, x1, x0) \
    do { \
        double _j, _0; \
        Two_One_Sum(a1, a0, b0, _j, _0, x0); \
        Two_One_Sum(_j, _0, b1, x3, x2, x1); \
    } while (0)

#define Two_Two_Diff(a1, a0, b1, b0, x3, x2, x1, x0) \
    do { \
        double _j, _0; \
        Two_One_Diff(a1, a0, b0, _j, _0, x0); \
        Two_One_Diff(_j, _0, b1, x3, x2, x1); \
    } while (0)

#define Two_One_Product(a1, a0, b, D) \
    do { \
        double bhi, blo, _i, _j, _0, _k, u3; \
        Split(b, bhi, blo); \
        Two_Product_Presplit(a0, b, bhi, blo, _i, D[0]); \
        Two_Product_Presplit(a1, b, bhi, blo, _j, _0); \
        Two_Sum(_i, _0, _k, D[1]); \
        Fast_Two_Sum(_j, _k, u3, D[2]); \
        D[3] = u3; \
    } while (0)

#define Cross_Product(a, b, c, d, D) \
    do { \
        double s1, s0, t1, t0, u3; \
        Two_Product(a, d, s1, s0); \
        Two_Product(c, b, t1, t0); \
        Two_Two_Diff(s1, s0, t1, t0, u3, D[2], D[1], D[0]); \
        D[3] = u3; \
    } while (0)

#define Two_Product_Sum(a, b, c, d, D) \
    do { \
        double s1, s0, t1, t0, u3; \
        Two_Product(a, b, s1, s0); \
        Two_Product(c, d, t1, t0); \
        Two_Two_Sum(s1, s0, t1, t0, u3, D[2], D[1], D[0]); \
        D[3] = u3; \
    } while (0)

#define Square_Sum(a, b, D) \
    do { \
        double s1, s0, t1, t0, u3; \
        Square(a, s1, s0); \
        Square(b, t1, t0); \
        Two_Two_Sum(s1, s0, t1, t0, u3, D[2], D[1], D[0]); \
        D[3] = u3; \
    } while (0)

}
}