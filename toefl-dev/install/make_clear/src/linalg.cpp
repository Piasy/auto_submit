// @file: src/linalg.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#include "linalg.h"
#include <iostream>

namespace {
  template <typename F, int N>
  void printVector(std::ostream& os, Vector<F, N> const& v)
  {
    os << "[" << v[0];
    for (int i=1; i<N; ++i) {
      os << ", " << v[i];
    }
    os << "]";
  }
}

std::ostream& operator<<(std::ostream& os, Vector<float, 2> const& v)
{
  printVector(os, v);
  return os;
}

std::ostream& operator<<(std::ostream& os, Vector<float, 3> const& v)
{
  printVector(os, v);
  return os;
}

std::ostream& operator<<(std::ostream& os, Vector<double, 2> const& v)
{
  printVector(os, v);
  return os;
}

std::ostream& operator<<(std::ostream& os, Vector<double, 3> const& v)
{
  printVector(os, v);
  return os;
}
