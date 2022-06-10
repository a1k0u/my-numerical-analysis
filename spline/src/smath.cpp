#include <cmath>
#include <vector>
#include "smath.h"
#include "spline.h"

#define INT_MAX 2147483647

using namespace std;

real takeDistance(real x0, real mu, FUNCTION* func1, FUNCTION* func2) {
    return sqrt((x0 - mu) * (x0 - mu) +
                (func1->getY(x0) - func2->getY(mu)) *
                (func1->getY(x0) - func2->getY(mu)));
}

real derivativeDistance(real x0, real mu, FUNCTION* func1, FUNCTION* func2) {
    return (takeDistance(x0, mu + 1e-9, func1, func2) - takeDistance(x0, mu, func1, func2)) /
           1e-9;
}

real R_x(real x, FUNCTION* func1, FUNCTION* func2) {
    return func1->getY(x) - func2->getY(x);
}

real diff_R_x(real x, FUNCTION* func1, FUNCTION* func2) {
    return (R_x(x + 1e-9, func1, func2) - R_x(x, func1, func2)) / 1e-9;
}

real checkRoots(real a, real b, FUNCTION* func1, FUNCTION* func2) {
    real step = (b - a) / 1000;
    real _a, _b;
    bool exist = false;
    for (_a = a; _a < b; _a += step) {
        _b = _a + step;
        if (R_x(_a, func1, func2) * R_x(_b, func1, func2) <= 0) {
            exist = true;
            break;
        }
    }

    if (!exist) return nothingRoots;
    real x0;
    if (R_x(_a, func1, func2) * diff_R_x(_a, func1, func2) > 0)
        x0 = _a;
    else
        x0 = _b;
    real x1 = x0 - R_x(x0, func1, func2) / diff_R_x(x0, func1, func2);
    while (abs(x0 - x1) >= 1e-9) {
        x0 = x1;
        if (diff_R_x(x0, func1, func2) == 0) x0 += step;
        x1 = x0 - R_x(x0, func1, func2) / diff_R_x(x0, func1, func2);
    }

    return x1;
}

real calcMinDistance(real a, real b, FUNCTION* func1, FUNCTION* func2) {
    real step = (b - a) / 1000;
    real minDist = INT_MAX;
    for (real x0 = a; x0 <= b; x0 += step) {
        real r1 = a;
        for (real r2 = a + step; r2 < b; r2 += step) {
            if (derivativeDistance(x0, r1, func1, func2) < 0 &&
                    derivativeDistance(x0, r2, func1, func2) > 0) {
                real left = r1, right = r2;
                while (abs(left - right) > 1e-9) {
                    real middle = (left + right) / 2;
                    if (derivativeDistance(x0, middle, func1, func2) < 0)
                        left = middle;
                    else if (derivativeDistance(x0, middle, func1, func2) > 0)
                        right = middle;
                    else
                        break;
                }
                real u = (left + right) / 2;
                minDist = min(minDist, takeDistance(x0, u, func1, func2));
            }
            r1 = r2;
        }
    }
    return minDist;
}
