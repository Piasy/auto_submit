// @file: src/image.h
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#ifndef SRC_IMAGE_H_BA152A3DF9DB11E3918884383555E6CC
#define SRC_IMAGE_H_BA152A3DF9DB11E3918884383555E6CC

#include <string>
#include "common.h"
#include "linalg.h"

// Type to represent a float-pointing Rgb color value.
typedef Vector<float, 3> Rgb;

// A basic class for manipulating Rgba images.
class RgbImage
{
public:
  RgbImage();
  RgbImage(int width, int height);
  ~RgbImage();
  
  // Copy construct from an existing image, or assign from another image.
  RgbImage(RgbImage const& other);
  RgbImage& operator=(RgbImage const& other);
  
  // Get width & height of this image.
  int width() const { return w_; }
  int height() const { return h_; }
  
  // Resize the image to fit given size.
  void resize(int width, int height);
  
  // Pixel get/set interface
  Rgb const& get(int row, int col) const {
    return data_[row * w_ + col];
  }
  
  void set(int row, int col, Rgb const& v) {
    data_[row * w_ + col] = v;
  }

  // Pixel subscript interface
  Rgb const* operator[](int row) const {
    return data_ + row * w_;
  }
  Rgb* operator[](int row) {
    return data_ + row * w_;
  }
  
  // Fill the whole image with given color.
  void fill(Rgb const& c);
  
  // Load image from external BMP file.
  void loadBmp(std::string const& path);
  
  // Save this image as BMP format to an external file.
  void saveBmp(std::string const& path);

  // Convert from RGB 24bpp raw data.
  void fromRgbBytes(std::string const& s, int w, int h);
  
  // Convert to RGB 24bpp raw data.
  std::string toRgbBytes() const;
  
  // Get access to the raw data of this image
  Rgb* data() { return data_; }
  Rgb const* data() const { return data_; }
  Rgb* lineData(int row) { return data_ + w_ * row; }
  Rgb const* lineData(int row) const { return data_ + w_ * row; }
  
  // Swap internal data between two images.
  void swap(RgbImage& other);
  
protected:
  int w_, h_;
  Rgb *data_;

  // Construct a new data chunk sized (w, h).
  void init_data(int w, int h, Rgb const* src);
};

// Shortcut |Image| to |RgbImage|.
typedef RgbImage Image;

#endif // SRC_IMAGE_H_BA152A3DF9DB11E3918884383555E6CC
