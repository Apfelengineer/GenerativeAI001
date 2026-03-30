#gpt-oss:20b

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import sys

def main():
    # 初期メッセージ
    print("こんにちは。なんでもお申し付けください。")

    # 返答候補
    responses = ["はい", "イエス！", "喜んで！！"]

    while True:
        # ユーザーからの入力を取得
        user_input = input()

        # 「もういいですよ。」だったらループを抜ける
        if user_input == "もういいですよ。":
            break

        # ランダムに返答を選択して表示
        reply = random.choice(responses)
        print(reply)

    # ループを抜けた後のメッセージ
    print("ご指導、ありがとうございました！")
    # 3 秒待機
    time.sleep(3)
    # プログラム終了
    sys.exit(0)

if __name__ == "__main__":
    main()
