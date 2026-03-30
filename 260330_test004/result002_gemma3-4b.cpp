//gemma3:4b

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main() {
  // 読み込み画像
  Mat image = imread("lenna.png", IMREAD_COLOR); // カラー画像を読み込み

  // 画像が読み込めたか確認
  if (!image.load("lenna.png")) {
    cout << "画像ファイルの読み込みに失敗しました。" << endl;
    return -1;
  }

  // グレースケールに変換
  Mat grayImage;
  cvtColor(image, grayImage, COLOR_BGR2GRAY);

  // Cannyエッジ検出
  Mat edges;
  // Cannyエッジ検出のパラメータ:
  // threshold1: 閾値1 (下限)
  // threshold2: 閾値2 (上限)
  // apertureSize: カーネルサイズ (通常は3)
  // L2gradient: L2距離を使用するか (true/false)
  Canny(grayImage, edges, 30, 100, 3);

  // 結果の保存
  if (!edges.empty()) {
    imwrite("lenna_canny.png", edges);
    cout << "画像を lenna_canny.png に保存しました。" << endl;
  } else {
    cout << "エッジ検出に失敗しました。" << endl;
  }

  return 0;
}
