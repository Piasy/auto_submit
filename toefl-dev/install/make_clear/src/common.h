// @file: src/common.h
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#ifndef SRC_COMMON_H_094DB5C2F9DC11E3AE8884383555E6CC
#define SRC_COMMON_H_094DB5C2F9DC11E3AE8884383555E6CC

#include "config.h"

#define NOCOPY(CLASS)                                                     \
  private:                                                                \
    CLASS(CLASS const&);                                                  \
    CLASS& operator=(CLASS const&);

#define arraysize(ARR)                                                    \
  (sizeof((ARR)) / sizeof((ARR)[0]))

template <typename T>
static inline T const& Min(T const& a, T const& b) {
  return a < b ? a : b;
}

template <typename T>
static inline T const& Max(T const& a, T const& b) {
  return a > b ? a : b;
}

#endif // SRC_COMMON_H_094DB5C2F9DC11E3AE8884383555E6CC
