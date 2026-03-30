//gpt-oss:20b

/*********************************************************************
 *  Canny Edge Detection – lenna.png → lenna_canny.png
 *  - Works with both color and grayscale input images.
 *  - Uses OpenCV 4.11.0 (any 4.x version is fine).
 *
 *  Build command (Linux/macOS):
 *      g++ -std=c++17 -O2 -Wall -I/usr/include/opencv4 \
 *          -L/usr/lib -lopencv_core -lopencv_imgproc \
 *          -lopencv_highgui -lopencv_imgcodecs \
 *          canny_lenna.cpp -o canny_lenna
 *
 *  Build command (Windows, Visual Studio):
 *      Add OpenCV include and lib paths in project settings.
 *
 *********************************************************************/

#include <opencv2/opencv.hpp>
#include <iostream>

int main()
{
    const std::string inputFile  = "lenna.png";
    const std::string outputFile = "lenna_canny.png";

    // 1. 画像を読み込む
    cv::Mat img = cv::imread(inputFile, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "Error: Cannot load image '" << inputFile << "'.\n";
        return EXIT_FAILURE;
    }

    // 2. カラー画像ならグレースケールへ変換
    cv::Mat gray;
    if (img.channels() == 3 || img.channels() == 4) {   // RGB or RGBA
        cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
    } else if (img.channels() == 1) {                  // already grayscale
        gray = img.clone();
    } else {
        std::cerr << "Error: Unsupported number of channels (" << img.channels() << ").\n";
        return EXIT_FAILURE;
    }

    // 3. Canny エッジ検出
    cv::Mat edges;
    double lowThreshold  = 100.0;   // 例: 低い閾値
    double highThreshold = 200.0;   // 例: 高い閾値
    int    apertureSize = 3;       // 例: 3x3 Sobel フィルタ

    cv::Canny(gray, edges, lowThreshold, highThreshold, apertureSize);

    // 4. 画像を保存
    if (!cv::imwrite(outputFile, edges)) {
        std::cerr << "Error: Could not write image to '" << outputFile << "'.\n";
        return EXIT_FAILURE;
    }

    std::cout << "Canny edge image saved to '" << outputFile << "'.\n";
    return EXIT_SUCCESS;
}
