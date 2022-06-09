#ifndef SPLINE_SMATH_H
#define SPLINE_SMATH_H

#include "spline.h"

typedef long double real;
const real nothingRoots = -243674.24736887;

real takeDistance(real x0, real mu, FUNCTION* func1, FUNCTION* func2);
real derivativeDistance(real x0, real mu, FUNCTION* func1, FUNCTION* func2);
real R_x(real x, FUNCTION* func1, FUNCTION* func2);
real checkRoots(real a, real b, FUNCTION* func1, FUNCTION* func2);
real calcMinDistance(real a, real b, FUNCTION* func1, FUNCTION* func2);

#endif  // SPLINE_SMATH_H
