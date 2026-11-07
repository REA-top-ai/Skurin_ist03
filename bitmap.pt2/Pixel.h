#pragma once

struct Pixel {
    unsigned char R;
    unsigned char G;
    unsigned char B;
    double Y;

    Pixel() {
        R = 0;
        G = 0;
        B = 0;
        Y = 0;
    }

    Pixel(unsigned char r, unsigned char g, unsigned char b) {
        R = r;
        G = g;
        B = b;
        Y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
};
