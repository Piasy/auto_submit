// @file: src/realtype.h
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#ifndef SRC_REALTYPE_H_C3330742F9D611E3853384383555E6CC
#define SRC_REALTYPE_H_C3330742F9D611E3853384383555E6CC

#include <stdint.h>
#include <stddef.h>
#include <math.h>
#include <stdlib.h>
#include "config.h"
#include "common.h"

// **** Floating-number bootstrap ****

#if !defined(HIGH_PRECISION)
  typedef float Real;
  static const Real Epsilon = 1e-5;
#else
  typedef double Real;
  static const Real Epsilon = 1e-7;
#endif
static const Real PI = 3.14159265358979323846264338;

// Some pre-defined realtype constants used in raytracer
static const Real Infinity = 1e10;
static const Real InfinityObjectSize = 1e5;
static const Real LightTravelSmallStep = 0.001;

// The arithmetic operations for Real type.
template <typename T> struct RealArith {};

template <>
struct RealArith<float>
{
  static inline float abs(float v) {
    return ::fabsf(v);
  }
  
  static inline float sqrt(float v) {
    return ::sqrtf(v);
  }
  
  static inline float tan(float v) {
    return ::tanf(v);
  }
  
  static inline float sin(float v) {
    return ::sinf(v);
  }
  
  static inline float asin(float v) {
    return ::asinf(v);
  }
  
  static inline float cos(float v) {
    return ::cosf(v);
  }
  
  static inline float acos(float v) {
    return ::acosf(v);
  }
  
  static inline float pow(float v, double n) {
    return ::powf(v, n);
  }
  
  static inline float exp(float v) {
    return ::expf(v);
  }
  
  static inline float log(float v) {
    return ::logf(v);
  }
  
  static inline float floor(float v) {
    return ::floorf(v);
  }
  
  static inline float ceil(float v) {
    return ::ceilf(v);
  }
};

template <>
struct RealArith<double>
{
  static inline double abs(double v) {
    return ::fabs(v);
  }
  
  static inline double sqrt(double v) {
    return ::sqrt(v);
  }
  
  static inline double tan(double v) {
    return ::tan(v);
  }
  
  static inline double sin(double v) {
    return ::sin(v);
  }
  
  static inline double asin(double v) {
    return ::asin(v);
  }
  
  static inline double cos(double v) {
    return ::cos(v);
  }
  
  static inline double acos(double v) {
    return ::acos(v);
  }
  
  static inline double pow(double v, double n) {
    return ::pow(v, n);
  }
  
  static inline double exp(double v) {
    return ::exp(v);
  }
  
  static inline double log(double v) {
    return ::log(v);
  }
  
  static inline double floor(double v) {
    return ::floor(v);
  }
  
  static inline double ceil(double v) {
    return ::ceil(v);
  }
};

typedef RealArith<Real> Arith;

// A readom generator to serve real type.
//
// This random generator is drafted according to "MT19937-64" by Takuji
// Nishimura and Makoto Matsumoto.  The original version is not thread-safe,
// thus I altered the global status vector to per-instance manner.
class RandomGenerator
{
  NOCOPY(RandomGenerator);
  
public:
  RandomGenerator();
  explicit RandomGenerator(unsigned long long seed);
  ~RandomGenerator();
  
  // Get a randomized floating-point number range in [0, 1).
  Real operator()();
  
protected:
  struct Private;
  Private *d_;
};


#endif // SRC_REALTYPE_H_C3330742F9D611E3853384383555E6CC
