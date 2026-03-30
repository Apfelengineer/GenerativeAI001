#gemma3:4b

import random
import time

# プログラムのメッセージ
print("こんにちは。なんでもお申し付けください。")

# 永続ループ
while True:
    user_input = input(">> ")

    # 終了条件のチェック
    if user_input == "もういいですよ。":
        break

    # 応答の生成
    responses = ["はい", "イエス！", "喜んで！！"]
    response = random.choice(responses)

    # 応答の表示
    print(response)

# ループ終了後のメッセージと終了処理
print("ご指導、ありがとうございました！")
time.sleep(3)
