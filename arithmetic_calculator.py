def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("数値を入力してください。")

def main():
    print("=== 四則演算プログラム ===")
    a = get_number("1つ目の数を入力してください: ")
    b = get_number("2つ目の数を入力してください: ")

    print(f"\n--- 計算結果 ---")
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} × {b} = {a * b}")

    if b != 0:
        print(f"{a} ÷ {b} = {a / b}")
    else:
        print(f"{a} ÷ {b} = 0では割り算できません")

if __name__ == "__main__":
    main()
