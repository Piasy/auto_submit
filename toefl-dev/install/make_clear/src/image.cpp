// @file: src/image.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#include "image.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <iostream>
#include <stdexcept>

RgbImage::RgbImage()
: w_(0), h_(0), data_(NULL)
{
}

RgbImage::RgbImage(int width, int height)
: w_(0), h_(0), data_(NULL)
{
  init_data(width, height, NULL);
}

RgbImage::~RgbImage()
{
  delete [] data_;
}

RgbImage::RgbImage(RgbImage const& other)
{
  init_data(other.width(), other.height(), other.data());
}

RgbImage& RgbImage::operator=(const RgbImage &other)
{
  init_data(other.width(), other.height(), other.data());
  return *this;
}

void RgbImage::init_data(int w, int h, Rgb const* src)
{
  // Delete the old data.
  if (data_)
    delete [] data_;
  data_ = NULL;

  // Set to new size, and construct data buffer if (w * h) > 0.
  w_ = w;
  h_ = h;
  if (w * h > 0) {
    data_ = new Rgb[w * h];
    
    // Now fill the image with (0, 0, 0), or copy from |src|.
    if (src) {
      memcpy(data_, src, sizeof(Rgb) * w * h);
    } else {
      fill(Rgb(0, 0, 0));
    }
  }
}

void RgbImage::resize(int width, int height)
{
  init_data(width, height, NULL);
}

void RgbImage::fill(const Rgb &c)
{
  for (int i=0; i<w_*h_; ++i) {
    data_[i] = c;
  }
}

void RgbImage::swap(RgbImage &other)
{
  std::swap(data_, other.data_);
  std::swap(w_, other.w_);
  std::swap(h_, other.h_);
}

void RgbImage::fromRgbBytes(std::string const& s, int w, int h)
{
  RgbImage tmp(w, h);
  const char* d = s.data();
  if (w * h * 3 > s.size()) {
    char buf[64];
    snprintf(buf, sizeof(buf), "Size of raw data is %d, which does "
             "not contain enough RGB data to construct a %dx%d picture.",
             int(s.size()), w, h);
    throw std::runtime_error(buf);
  }

#define F(c) (int(uint8_t((c))) / 255.0)
  for (int i=0; i<h; ++i) {
    for (int j=0; j<w; ++j) {
      tmp[i][j] = Rgb(F(d[0]), F(d[1]), F(d[2]));
    }
  }
#undef F

  swap(tmp);
}

std::string RgbImage::toRgbBytes() const
{
  std::string ret;
  ret.reserve(w_ * h_ * 3);
  for (int i=0; i<h_; ++i) {
    for (int j=0; j<w_; ++j) {
      Rgb const& rgb = data_[i * w_ + j];
      for (int z=0; z<3; ++z) {
        ret.push_back(uint8_t(rgb[z] * 255));
      }
    }
  }
  return ret;
}

// -------- save image data into bmp file --------
struct BmpHeader
{
  uint64_t file_size;
  uint32_t data_offset;
  
  uint32_t header_size; // 40
  int32_t  width;
  int32_t  height;
  uint16_t planes;      // 1
  uint16_t bpp;         // 24
  uint32_t compression; // BI_RGB = 0
  uint32_t data_size;   // including pad
  int32_t  horizon_res; // horizon resolution, pixel per meter.
  int32_t  vertical_res;// vertical resolution.
  uint32_t palette;     // 0
  uint32_t ignored;     // 0
  
  BmpHeader() {}
  
  BmpHeader(int width, int height)
  : width(width), height(height)
  {
    int scanline = (width * 3 + 3) / 4 * 4;
    data_offset = 52 + 2 /* BM signature */;
    file_size = data_offset + scanline * height;
    header_size = data_offset - 14;
    planes = 1;
    bpp = 24;
    compression = 0;
    data_size = scanline * height;
    horizon_res = 2835;
    vertical_res = 2835;
    palette = 0;
    ignored = 0;
  }
};

void RgbImage::loadBmp(const std::string &path)
{
#define READ_FILE(FD, DATA, SIZE)                                     \
  if (fread((DATA), 1, (SIZE), (FD)) != (SIZE)) {                     \
    goto exit_point;                                                  \
  }
  
  FILE *fd = NULL;
  int scanline;
  char sig[2];
  BmpHeader hdr0, *hdr;
  RgbImage im_data;
  bool ret = false;
  int dynhdr_offset, skip_offset;
  uint8_t *hdrdata = NULL;
  uint8_t *linedata = NULL;

  fd = fopen(path.c_str(), "rb");
  if (!fd)
    goto exit_point;

  // "BM" signature.
  READ_FILE(fd, sig, 2);
  if (sig[0] != 'B' || sig[1] != 'M') {
    goto exit_point;
  }

  // Read in the whole header.
  dynhdr_offset = (sizeof(hdr0.file_size) + sizeof(hdr0.data_offset) +
                   sizeof(hdr0.header_size));
  READ_FILE(fd, &hdr0, dynhdr_offset);
  hdrdata = new uint8_t[hdr0.header_size + dynhdr_offset -
                        sizeof(hdr0.header_size)];
  memcpy(hdrdata, &hdr0, dynhdr_offset);
  READ_FILE(fd, hdrdata + dynhdr_offset, (hdr0.header_size -
                                          sizeof(hdr0.header_size)));
  hdr = (BmpHeader*)hdrdata;

  // Whether it looks like a valid header?
  scanline = (hdr->width * 3 + 3) / 4 * 4;
  if (scanline * hdr->height != hdr->data_size || hdr->bpp != 24) {
    goto exit_point;
  }
  linedata = new uint8_t[scanline];
  
  // Skip invalid data.
  skip_offset = (hdr->data_offset - hdr->header_size - sizeof(hdr->file_size) -
                 sizeof(hdr->data_offset) - 2);
  for (int count=0; count<skip_offset; count+=scanline) {
    READ_FILE(fd, linedata, std::min(scanline, skip_offset-count));
  }
  
  // Read in each line.
  im_data.resize(hdr->width, hdr->height);
  for (int i=0; i<hdr->height; ++i) {
    READ_FILE(fd, linedata, scanline);
    int j, k;
    for (j=0, k=0; j<hdr->width; ++j, k+=3) {
      Rgb c(float(linedata[k+2]) / 255.0f, float(linedata[k+1]) / 255.0f,
            float(linedata[k]) / 255.0f);
      im_data.set(hdr->height-i-1, j, c);
    }
  }
  
  // Successfully read the whole image, set the data to current image instance.
  ret = true;
  swap(im_data);

exit_point:
  fclose(fd);
  if (linedata)
    delete [] linedata;
  if (hdrdata)
    delete [] hdrdata;
  
  if (!ret)
    throw std::runtime_error("Cannot load image '" + path + "'.");
  
#undef READ_FILE
}

void RgbImage::saveBmp(const std::string &path)
{
#define WRITE_FILE(FD, DATA, SIZE)                                    \
  if (fwrite((DATA), 1, (SIZE), (FD)) != (SIZE)) {                    \
    goto exit_point;                                                  \
  }
  
  bool ret = false;
  FILE *fd = NULL;
  BmpHeader hdr(w_, h_);
  std::vector<uint8_t> scanline;

  fd = fopen(path.c_str(), "wb");
  if (!fd)
    goto exit_point;
  
  WRITE_FILE(fd, "BM", 2);
  WRITE_FILE(fd, &hdr, hdr.data_offset - 2);

  scanline.resize((w_ * 3 + 3) / 4 * 4);
  memset(scanline.data(), 0, scanline.size());

  for (int i=h_-1; i>=0; --i) {
    int j, k;
    for (j=0, k=0; j<w_; ++j) {
      Rgb const& rgb = data_[i*w_+j];
      for (int z=0; z<3; ++z)
        scanline[k++] = uint8_t(rgb[2-z] * 255);
    }
    WRITE_FILE(fd, scanline.data(), scanline.size());
  }
  ret = true;
  
exit_point:
  if (!ret)
    throw std::runtime_error("Cannot save image '" + path + "'.");
  fclose(fd);
  
#undef WRITE_FILE
}
