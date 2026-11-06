#include <iostream>
#include <fstream>
#include <vector>

int read2(const unsigned char* p) {
    return p[0] + p[1] * 256;
}

int read4(const unsigned char* p) {
    return p[0] + p[1] * 256 + p[2] * 256 * 256 + p[3] * 256 * 256 * 256;
}

void printPixel(const char* name, const unsigned char* data, int dataOffset, int rowSize, int height, int x, int y) {
    int pos = dataOffset + (height - 1 - y) * rowSize + x * 3;
    int b = data[pos];
    int g = data[pos + 1];
    int r = data[pos + 2];
    std::cout << name << " R: " << r << " G: " << g << " B: " << b << std::endl;
}

int main(const int argc, char** argv) {

    const char* path = argc > 1 ? argv[1] : "image.bmp";

    std::ifstream file(path, std::ios::binary);
    if (!file) {
        std::cerr << "Не удалось открыть файл: " << path << std::endl;
        return 1;
    }

    unsigned char header[54];
    file.read(reinterpret_cast<char*>(header), 54);
    if (!file){
        std::cout << "Фаил короче 54 байт" << std::endl;
        return 1;
    }

    for (int i = 0 ; i < 54; i++){
        std::cout << int(header[i]) << " ";
    }
    std::cout << std::endl;

    std::cout << "" << std::endl;

    int width = read4(header + 18);
    std::cout << "Ширина изображения: " << width << std::endl;

    int height = read4(header + 22);
    std::cout << "Высота изображения: " << height << std::endl;

    int fileSize = read4(header + 2);
    std::cout << "Размер файла: " << fileSize << std::endl;

    int bitsPerPixel = read2(header + 28);
    std::cout << "Количество бит на пиксель: " << bitsPerPixel << std::endl;

    std::cout << "" << std::endl;

    std::cout << "Сигнатура: " << header[0] << header[1] << std::endl;

    int dataOffset = read4(header + 10);
    std::cout << "Смещение пикселей: " << dataOffset << std::endl;

    int infoHeaderSize = read4(header + 14);
    std::cout << "Размер информационного заголовка: " << infoHeaderSize << std::endl;

    int planes = read2(header + 26);
    std::cout << "Плоскости: " << planes << std::endl;

    int compression = read4(header + 30);
    std::cout << "Сжатие: " << compression << std::endl;

    int imageSize = read4(header + 34);
    std::cout << "Размер данных картинки: " << imageSize << std::endl;

    int xPixelsPerMeter = read4(header + 38);
    std::cout << "Пикселей на метр по X: " << xPixelsPerMeter << std::endl;

    int yPixelsPerMeter = read4(header + 42);
    std::cout << "Пикселей на метр по Y: " << yPixelsPerMeter << std::endl;

    int colorsUsed = read4(header + 46);
    std::cout << "Используется цветов: " << colorsUsed << std::endl;

    int colorsImportant = read4(header + 50);
    std::cout << "Важных цветов: " << colorsImportant << std::endl;

        if (bitsPerPixel != 24) {
        std::cout << "Пока поддерживается только 24 бита на пиксель" << std::endl;
        return 1;
    }

    int rowSize = ((bitsPerPixel * width + 31) / 32) * 4;

    std::vector<unsigned char> data(fileSize);
    file.clear();
    file.seekg(0);
    file.read(reinterpret_cast<char*>(data.data()), fileSize);
    if (!file) {
        std::cout << "Не удалось прочитать весь файл" << std::endl;
        return 1;
    }
    std::cout << "" << std::endl;
    printPixel("Левый верхний:  ", data.data(), dataOffset, rowSize, height, 0, 0);
    printPixel("Правый верхний: ", data.data(), dataOffset, rowSize, height, width - 1, 0);
    printPixel("Левый нижний:   ", data.data(), dataOffset, rowSize, height, 0, height - 1);
    printPixel("Правый нижний:  ", data.data(), dataOffset, rowSize, height, width - 1, height - 1);

    return 0;
}
