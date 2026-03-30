//qwen3:8b

#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // 画像の読み込み
    cv::Mat src = cv::imread("lenna.png");
    if (src.empty()) {
        std::cerr << "エラー: 画像ファイルが見つからないか読み込めません。" << std::endl;
        return -1;
    }

    // グレースケール変換（カラー画像の場合のみ）
    cv::Mat gray;
    if (src.channels() == 3) {
        cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);
    } else {
        gray = src.clone();
    }

    // Cannyエッジ検出の実行
    cv::Mat edges;
    cv::Canny(gray, edges, 100, 200, 3);

    // 結果の保存
    if (!cv::imwrite("lenna_canny.png", edges)) {
        std::cerr << "エラー: 結果画像の保存に失敗しました。" << std::endl;
        return -1;
    }

    std::cout << "Cannyエッジ検出が完了し、lenna_canny.pngに保存されました。" << std::endl;
    return 0;
}
