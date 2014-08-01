// @file: src/linalg.h
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#ifndef SRC_LINALG_H_283E718FF9D311E3AB3284383555E6CC
#define SRC_LINALG_H_283E718FF9D311E3AB3284383555E6CC

#include <iosfwd>
#include <type_traits>
#include "config.h"
#include "realtype.h"

// Generic Vector type for ray tracing
template <typename Float, int N>
class Vector
{
public:
  static const int Dim = N;
  typedef Float value_type;
  typedef RealArith<Float> arith_type;
  typedef Vector<Float, N> vector_type;
  
  // -------- Basic constructors for the vector --------
  
  // Construct a new Vector whose items are initialized with Float().
  Vector() {
    for (int i=0; i<N; ++i) {
      d_[i] = Float();
    }
  }
  
  // Construct a new Vector whose items are all filled with |v|.
  explicit Vector(Float const& v) {
    for (int i=0; i<N; ++i) {
      d_[i] = v;
    }
  }
  
  // Construct a new Vector whose first 2 items are filled with [a1, a2].
  explicit Vector(Float const& a1, Float const& a2) {
    d_[0] = a1;
    d_[1] = a2;
  }
  
  // Construct a new Vector whose first 3 items are filled with [a1, a2, a3].
  explicit Vector(Float const& a1, Float const& a2, Float const& a3) {
    d_[0] = a1;
    d_[1] = a2;
    d_[2] = a3;
  }
  
  // Construct a new Vector whose first 4 items are filled with [a1, a2, a3, a4]
  explicit Vector(Float const& a1, Float const& a2, Float const& a3,
                  Float const& a4) {
    d_[0] = a1;
    d_[1] = a2;
    d_[2] = a3;
    d_[3] = a4;
  }
  
  // Construct a new Vector that is copied from |other|.
  Vector(vector_type const& other) {
    for (int i=0; i<N; ++i) {
      d_[i] = other[i];
    }
  }
  
  // Construct a new Vector whose first |size| items are copied from |d_|.
  explicit Vector(Float const* d, int size=N) {
    int minsize = (size < N) ? size : N;
    for (int i=0; i<minsize; ++i) {
      d_[i] = d[i];
    }
  }
  
  // Construct a new Vector whose items remains uninitialized.
  struct NoInit {};
  explicit Vector(NoInit const&) {
  }
  
  // -------- Basic subscript interface --------
  Float get(int idx) const { return d_[idx]; }
  void set(int idx, Float const& v) { d_[idx] = v; }
  
  Float& operator[](int idx) { return d_[idx]; }
  Float const& operator[](int idx) const { return d_[idx]; }
  
  Float* data() { return d_; }
  Float const* data() const { return d_; }
  
  // -------- Unary operators that produce a new vector --------
  vector_type operator-() const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = -d_[i];
    }
    return ret;
  }

  // -------- Arithmetics between two vectors --------
  vector_type operator+(vector_type const& other) const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] + other[i];
    }
    return ret;
  }
  
  vector_type& operator+=(vector_type const& other) {
    for (int i=0; i<N; ++i) {
      d_[i] += other[i];
    }
    return *this;
  }
  
  vector_type operator-(vector_type const& other) const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] - other[i];
    }
    return ret;
  }
  
  vector_type& operator-=(vector_type const& other) {
    for (int i=0; i<N; ++i) {
      d_[i] -= other[i];
    }
    return *this;
  }
  
  vector_type operator*(vector_type const& other) const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] * other[i];
    }
    return ret;
  }

  vector_type& operator*=(vector_type const& other) {
    for (int i=0; i<N; ++i) {
      d_[i] *= other[i];
    }
    return *this;
  }
  
  vector_type operator/(vector_type const& other) const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] / other[i];
    }
    return ret;
  }
  
  vector_type& operator/=(vector_type const& other) {
    for (int i=0; i<N; ++i) {
      d_[i] /= other[i];
    }
    return *this;
  }
  
  // -------- Arithmetics between a vector and a scalar --------
  vector_type operator*(Float const& s) const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] * s;
    }
    return ret;
  }
  
  vector_type& operator*=(Float const& s) {
    for (int i=0; i<N; ++i) {
      d_[i] *= s;
    }
    return *this;
  }
  
  vector_type operator/(Float const& s) const {
    vector_type ret((NoInit()));
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] / s;
    }
    return ret;
  }
  
  vector_type& operator/=(Float const& s) {
    for (int i=0; i<N; ++i) {
      d_[i] /= s;
    }
    return *this;
  }
  
  // -------- Comparisons between two vectors --------
  bool allZero() const {
    for (int i=0; i<N; ++i) {
      if (!IsZero(d_[i]))
        return false;
    }
    return true;
  }
  
  bool allClose(vector_type const& other) const {
    for (int i=0; i<N; ++i) {
      if (!IsClose(d_[i], other[i]))
        return false;
    }
    return true;
  }
  
  // -------- Special arithmetic operations between vectors --------
  Float dot(vector_type const& other) const
  {
    Float ret = Float();
    for (int i=0; i<N; ++i) {
      ret += d_[i] * other[i];
    }
    return ret;
  }
  
  Float normPow2() const
  {
    return dot(*this);
  }
  
  Float norm() const
  {
    return arith_type::sqrt(normPow2());
  }
  
  vector_type normalize() const
  {
    Float nv = norm();
    if (nv == 0)
      return vector_type();
    
    vector_type ret((NoInit()));
    nv = 1. / nv;
    for (int i=0; i<N; ++i) {
      ret[i] = d_[i] * nv;
    }
    return ret;
  }
  
  void toNormalized()
  {
    Float nv = norm();
    if (nv != 0) {
      nv = 1. / nv;
      for (int i=0; i<N; ++i) {
        d_[i] *= nv;
      }
    }
  }
  
protected:
  Float d_[N];
};

// -------- More operators for Float & Vector(Float, N) --------
template <typename Float, int N, typename F=Float>
static inline Vector<Float, N> operator*(
    typename std::enable_if<std::is_convertible<F, Float>::value, F>::type a,
    Vector<Float, N> const& v)
{
  Vector<Float, N> ret((typename Vector<Float, N>::NoInit()));
  for (int i=0; i<N; ++i) {
    ret[i] = a * v[i];
  }
  return ret;
}

template <typename Float, int N, typename F=Float>
static inline Vector<Float, N> operator/(
    typename std::enable_if<std::is_convertible<F, Float>::value, F>::type a,
    Vector<Float, N> const& v)
{
  Vector<Float, N> ret((typename Vector<Float, N>::NoInit()));
  for (int i=0; i<N; ++i) {
    ret[i] = a / v[i];
  }
  return ret;
}

// -------- Commonly used vector types --------
typedef Vector<Real, 2> Point2D, Vector2D;
typedef Vector<Real, 3> Point3D, Vector3D;

// -------- Arithmetic operations for special type vectors --------
template <typename Float>
Vector<Float, 3> VectorCross(Vector<Float, 3> const& lhs,
                             Vector<Float, 3> const& rhs)
{
  Vector<Float, 3> ret((typename Vector<Float, 3>::NoInit()));
  ret[0] = lhs[1] * rhs[2] - lhs[2] * rhs[1];
  ret[1] = lhs[2] * rhs[0] - lhs[0] * rhs[2];
  ret[2] = lhs[0] * rhs[1] - lhs[1] * rhs[0];
  return ret;
}

// -------- IO utilities for Vector<Float, N> --------
std::ostream& operator<<(std::ostream& os, Vector<float, 2> const& v);
std::ostream& operator<<(std::ostream& os, Vector<float, 3> const& v);
std::ostream& operator<<(std::ostream& os, Vector<double, 2> const& v);
std::ostream& operator<<(std::ostream& os, Vector<double, 3> const& v);

#endif // SRC_LINALG_H_283E718FF9D311E3AB3284383555E6CC
