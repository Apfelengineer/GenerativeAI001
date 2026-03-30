#gemini

#include <iostream>
#include <opencv2/opencv.hpp>

int main() {
    // 1. 画像の読み込み (lenna.png)
    // cv::IMREAD_UNCHANGED を指定し、元の形式を保持して読み込みます
    cv::Mat src = cv::imread("lenna.png", cv::IMREAD_UNCHANGED);

    // 画像が正しく読み込めたか確認
    if (src.empty()) {
        std::cerr << "エラー: 画像ファイル 'lenna.png' が見つかりません。" << std::endl;
        return -1;
    }

    cv::Mat gray;

    // 2. カラー画像（チャンネル数が3以上）の場合はグレースケールに変換
    if (src.channels() >= 3) {
        cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);
    } else {
        // すでにグレースケールの場合はそのままコピー
        gray = src.clone();
    }

    // 3. エッジ処理 (Canny法)
    // 閾値1: 50, 閾値2: 150 (一般的な値) で処理
    cv::Mat edges;
    cv::Canny(gray, edges, 50, 150);

    // 4. 画像の保存 (lenna_canny.png)
    bool isSaved = cv::imwrite("lenna_canny.png", edges);

    if (isSaved) {
        std::cout << "エッジ処理が完了し、'lenna_canny.png' として保存されました。" << std::endl;
    } else {
        std::cerr << "エラー: 画像の保存に失敗しました。" << std::endl;
        return -1;
    }

    return 0;
}