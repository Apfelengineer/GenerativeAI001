#ChatGPT

import random
import time

responses = ["はい", "イエス！", "喜んで！！"]

print("こんにちは。なんでもお申し付けください。")

while True:
    user_input = input(">> ")

    if user_input == "もういいですよ。":
        break

    print(random.choice(responses))

print("ご指導、ありがとうございました！")
time.sleep(3)