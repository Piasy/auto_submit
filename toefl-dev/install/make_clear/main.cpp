// @file: main.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#include <time.h>
#include <iostream>
#include <time.h>
#include <string.h>
#include "src/linalg.h"
#include "src/image.h"

// Convolution kernel for NxN filter.
template <typename Float, int N>
struct ConvKernel
{
  static const int halfN = N / 2;
  Float kernel[N][N];
  Float factor;
  
  ConvKernel(Float d[N][N], Float factor=1.0) {
  memcpy(kernel, d, sizeof(kernel));
  for (int i=0; i<N; ++i) {
    for (int j=0; j<N; ++j) {
    kernel[i][j] *= factor;
    }
  }
  }
  
  Rgb operator()(Image const* im, int row, int col, bool detail=false) const {
  int start_row = -halfN, end_row = halfN;
  int start_col = -halfN, end_col = halfN;
  
  if (start_row + row < 0) {
    start_row = -row;
  }
  if (end_row + row >= im->height()) {
    end_row = im->height() - row - 1;
  }
  if (start_col + col < 0) {
    start_col = -col;
  }
  if (end_col + col >= im->width()) {
    end_col = im->width() - col - 1;
  }
  
  Rgb ret;
  for (int i=start_row; i<=end_row; ++i) {
    for (int j=start_col; j<=end_col; ++j) {
    ret += im->get(row+i, col+j) * kernel[i+halfN][j+halfN];
    }
  }
  
  return ret;
  }
};

float rgb2grey(Rgb const& c)
{
  return c[0]*0.299 + c[1]*0.587 + c[2]*0.114;  
}

int main(int argc, char** argv)
{
  // Read a.bmp
  Image im, im2;
  im2.loadBmp("1.bmp");
  
  // Gaussian filter on (row, col) to denoise the image.
  im.resize(im2.width(), im2.height());
  float gaussian_filter[5][5] = {
    {2, 4, 5, 4, 2},
    {4, 9, 12, 9, 4},
    {5, 12, 15, 12, 5},
    {4, 9, 12, 9, 4},
    {2, 4, 5, 4, 2}
  };
  ConvKernel<float, 5> gaussian(gaussian_filter, 1.0/159);
  
  for (int i=0; i<im.height(); ++i) {
    for (int j=0; j<im.width(); ++j) {
      im[i][j] = gaussian(&im2, i, j);
    }
  }
 
  // Valv
  im.loadBmp("1.bmp");
  
  // settings
  float B = -0.3, C = 0.5;
  float K = tan((45 + 44 * C) / 180 * PI);

  
  // contrast tweak
  for (int i=0; i<im.height(); ++i) {
    for (int j=0; j<im.width(); ++j) {
      for (int k=0; k<3; ++k) {
        float c;
        c = (im[i][j][k] - 0.5 * (1 - B)) * K + 0.5 * (1 + B);
        if (c >= 1.0) c = 1.0;
        if (c <= 0.0) c = 0.0;
        im[i][j][k] = c;
      }
    }
  }
  im.saveBmp("2.bmp");
  
  return 0;
}
