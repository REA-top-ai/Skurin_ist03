#pragma once

#include <vector>
#include "Pixel.h"

class Bitmap {
public:
    Bitmap(int w, int h);

    int GetWidth() const;
    int GetHeight() const;

    void SetPixel(int x, int y, Pixel p);
    Pixel GetPixel(int x, int y) const;

    std::vector<int> GetHistogram(char channel) const;
    double GetMean(char channel) const;
    int GetMedian(char channel) const;

    void WhiteBalance();
    void PrintStats() const;

private:
    int width;
    int height;
    std::vector<Pixel> pixels;
};
