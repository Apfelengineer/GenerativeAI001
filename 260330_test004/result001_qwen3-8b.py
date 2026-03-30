#qwen3:8b

import random
import time

print("こんにちは。なんでもお申し付けください。")

while True:
    user_input = input()
    if user_input == "もういいですよ。":
        break
    response = random.choice(["はい", "イエス！", "喜んで！！"])
    print(response)

print("ご指導、ありがとうございました！")
time.sleep(3)
