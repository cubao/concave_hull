#pragma once

#include <cmath>
#include "macros.hpp"

namespace cubao
{
namespace robust_predicates
{
// fast_expansion_sum_zeroelim routine from original code
inline int sum(int elen, const double *e, int flen, const double *f, double *h)
{
    double Q, Qnew, hh, bvirt;
    double enow = e[0];
    double fnow = f[0];
    int eindex = 0;
    int findex = 0;
    if ((fnow > enow) == (fnow > -enow)) {
        Q = enow;
        enow = e[++eindex];
    } else {
        Q = fnow;
        fnow = f[++findex];
    }
    int hindex = 0;
    if (eindex < elen && findex < flen) {
        if ((fnow > enow) == (fnow > -enow)) {
            Fast_Two_Sum(enow, Q, Qnew, hh);
            enow = e[++eindex];
        } else {
            Fast_Two_Sum(fnow, Q, Qnew, hh);
            fnow = f[++findex];
        }
        Q = Qnew;
        if (hh != 0) {
            h[hindex++] = hh;
        }
        while (eindex < elen && findex < flen) {
            if ((fnow > enow) == (fnow > -enow)) {
                Two_Sum(Q, enow, Qnew, hh);
                enow = e[++eindex];
            } else {
                Two_Sum(Q, fnow, Qnew, hh);
                fnow = f[++findex];
            }
            Q = Qnew;
            if (hh != 0) {
                h[hindex++] = hh;
            }
        }
    }
    while (eindex < elen) {
        Two_Sum(Q, enow, Qnew, hh);
        enow = e[++eindex];
        Q = Qnew;
        if (hh != 0) {
            h[hindex++] = hh;
        }
    }
    while (findex < flen) {
        Two_Sum(Q, fnow, Qnew, hh);
        fnow = f[++findex];
        Q = Qnew;
        if (hh != 0) {
            h[hindex++] = hh;
        }
    }
    if (Q != 0 || hindex == 0) {
        h[hindex++] = Q;
    }
    return hindex;
}

template <typename T> T estimate(int elen, const T *e)
{
    T Q = e[0];
    for (int i = 1; i < elen; i++) {
        Q += e[i];
    }
    return Q;
}

// https://github.com/mourner/robust-predicates/blob/main/src/util.js
static constexpr double epsilon = 1.1102230246251565e-16;
static constexpr double splitter = 134217729;
static constexpr double resulterrbound = (3 + 8 * epsilon) * epsilon;

static constexpr double ccwerrboundA = (3 + 16 * epsilon) * epsilon;
static constexpr double ccwerrboundB = (2 + 12 * epsilon) * epsilon;
static constexpr double ccwerrboundC = (9 + 64 * epsilon) * epsilon * epsilon;

inline double orient2dadapt( //
    double ax, double ay,    //
    double bx, double by,    //
    double cx, double cy,    //
    double detsum)
{
    double B[4];
    double C1[8];
    double C2[12];
    double D[16];
    double u[4];

    double acxtail = 0, acytail = 0, bcxtail = 0, bcytail = 0;
    double bvirt, c, ahi, alo, bhi, blo, _i, _j, _0, s1, s0, t1, t0, u3;

    double acx = ax - cx;
    double bcx = bx - cx;
    double acy = ay - cy;
    double bcy = by - cy;

    Cross_Product(acx, bcx, acy, bcy, B);

    double det = estimate(4, B);
    double errbound = ccwerrboundB * detsum;
    if (det >= errbound || -det >= errbound) {
        return det;
    }

    Two_Diff_Tail(ax, cx, acx, acxtail);
    Two_Diff_Tail(bx, cx, bcx, bcxtail);
    Two_Diff_Tail(ay, cy, acy, acytail);
    Two_Diff_Tail(by, cy, bcy, bcytail);

    if (acxtail == 0 && acytail == 0 && bcxtail == 0 && bcytail == 0) {
        return det;
    }

    errbound = ccwerrboundC * detsum + resulterrbound * std::abs(det);
    det += (acx * bcytail + bcy * acxtail) - (acy * bcxtail + bcx * acytail);
    if (det >= errbound || -det >= errbound)
        return det;

    Cross_Product(acxtail, bcx, acytail, bcy, u);
    int C1len = sum(4, B, 4, u, C1);

    Cross_Product(acx, bcxtail, acy, bcytail, u);
    int C2len = sum(C1len, C1, 4, u, C2);

    Cross_Product(acxtail, bcxtail, acytail, bcytail, u);
    int Dlen = sum(C2len, C2, 4, u, D);

    return D[Dlen - 1];
}

inline double orient2d(double ax, double ay, //
                       double bx, double by, //
                       double cx, double cy)
{
    double detleft = (ay - cy) * (bx - cx);
    double detright = (ax - cx) * (by - cy);
    double det = detleft - detright;

    double detsum = std::fabs(detleft + detright);
    if (std::fabs(det) >= ccwerrboundA * detsum)
        return det;

    return -orient2dadapt(ax, ay, bx, by, cx, cy, detsum);
}

inline double orient2dfast(double ax, double ay, //
                           double bx, double by, //
                           double cx, double cy)
{
    return (ay - cy) * (bx - cx) - (ax - cx) * (by - cy);
}

} // namespace robust_predicates
} // namespace cubao
