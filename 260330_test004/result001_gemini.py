#gemini

import random
import time
import sys

def main():
    # 起動時のメッセージ
    print("こんにちは。なんでもお申し付けください。")
    
    # 返答のリスト
    responses = ["はい", "イエス！", "喜んで！！"]
    
    try:
        while True:
            # ユーザーからの入力を取得
            user_input = input("> ")
            
            # 終了判定
            if user_input == "もういいですよ。":
                break
            
            # ランダムに返答を選択して表示
            print(random.choice(responses))
            
    except KeyboardInterrupt:
        # Ctrl+Cなどで強制終了された場合のハンドリング
        pass

    # ループ終了後の処理
    print("ご指導、ありがとうございました！")
    
    # 3秒待機
    time.sleep(3)
    
    # プログラムを終了
    sys.exit()

if __name__ == "__main__":
    main()