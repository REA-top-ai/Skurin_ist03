#include "Bitmap.h"

#include <iostream>

Bitmap::Bitmap(int w, int h) {
    width = w;
    height = h;
    pixels.resize(w * h);
}

int Bitmap::GetWidth() const {
    return width;
}

int Bitmap::GetHeight() const {
    return height;
}

void Bitmap::SetPixel(int x, int y, Pixel p) {
    pixels[y * width + x] = p;
}

Pixel Bitmap::GetPixel(int x, int y) const {
    return pixels[y * width + x];
}

std::vector<int> Bitmap::GetHistogram(char channel) const {
    std::vector<int> hist(256, 0);
    for (int i = 0; i < width * height; i++) {
        int value = 0;
        if (channel == 'R') {
            value = pixels[i].R;
        } else if (channel == 'G') {
            value = pixels[i].G;
        } else if (channel == 'B') {
            value = pixels[i].B;
        } else if (channel == 'Y') {
            value = int(pixels[i].Y + 0.5);
        }
        hist[value]++;
    }
    return hist;
}

double Bitmap::GetMean(char channel) const {
    std::vector<int> hist = GetHistogram(channel);
    double sum = 0;
    for (int v = 0; v < 256; v++) {
        sum += double(v) * hist[v];
    }
    return sum / (width * height);
}

int Bitmap::GetMedian(char channel) const {
    std::vector<int> hist = GetHistogram(channel);
    int half = (width * height + 1) / 2;
    int cumulative = 0;
    for (int v = 0; v < 256; v++) {
        cumulative += hist[v];
        if (cumulative >= half) {
            return v;
        }
    }
    return 255;
}

void Bitmap::WhiteBalance() {
    double meanR = GetMean('R');
    double meanG = GetMean('G');
    double meanB = GetMean('B');

    double target = meanR;
    if (meanG > target) {
        target = meanG;
    }
    if (meanB > target) {
        target = meanB;
    }

    double gainR = meanR > 0 ? target / meanR : 1.0;
    double gainG = meanG > 0 ? target / meanG : 1.0;
    double gainB = meanB > 0 ? target / meanB : 1.0;

    for (int i = 0; i < width * height; i++) {
        double r = pixels[i].R * gainR;
        double g = pixels[i].G * gainG;
        double b = pixels[i].B * gainB;
        if (r > 255) {
            r = 255;
        }
        if (g > 255) {
            g = 255;
        }
        if (b > 255) {
            b = 255;
        }
        pixels[i] = Pixel((unsigned char)(r + 0.5), (unsigned char)(g + 0.5), (unsigned char)(b + 0.5));
    }
}

void Bitmap::PrintStats() const {
    const char names[3] = {'R', 'G', 'B'};
    for (int c = 0; c < 3; c++) {
        std::cout << names[c] << ": среднее " << GetMean(names[c]) << ", медиана " << GetMedian(names[c]) << std::endl;
    }
}
