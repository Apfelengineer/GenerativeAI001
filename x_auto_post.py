#!/usr/bin/env python3
"""
X (Twitter) 自動投稿プログラム

機能:
  - x_test フォルダ内のテキストファイルを投稿文として読み込む
  - x_test フォルダ内の画像ファイル（JPG/PNG/GIF/WEBP）を添付
  - 当日9:00に投稿（9:00を過ぎている場合は翌日9:00）

必要ライブラリ:
  pip install tweepy

X Developer Portal での事前設定:
  https://developer.x.com/en/portal/projects-and-apps
  - App の「User authentication settings」で Read and Write を有効化
  - 以下の認証情報を取得して環境変数に設定する

環境変数（必須）:
  X_API_KEY              : API Key (Consumer Key)
  X_API_SECRET           : API Key Secret (Consumer Secret)
  X_ACCESS_TOKEN         : Access Token
  X_ACCESS_TOKEN_SECRET  : Access Token Secret

使用方法:
  python x_auto_post.py
"""

import os
import sys
import glob
import time
import tweepy
from datetime import datetime, timedelta

# --- 設定 ---
POST_FOLDER = "x_test"
POST_HOUR = 9        # 投稿時刻（時）
POST_MINUTE = 0      # 投稿時刻（分）
IMAGE_EXTENSIONS = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp"]


def load_credentials():
    """環境変数から認証情報を取得し、未設定の場合はエラー終了。"""
    keys = {
        "X_API_KEY": os.environ.get("X_API_KEY", ""),
        "X_API_SECRET": os.environ.get("X_API_SECRET", ""),
        "X_ACCESS_TOKEN": os.environ.get("X_ACCESS_TOKEN", ""),
        "X_ACCESS_TOKEN_SECRET": os.environ.get("X_ACCESS_TOKEN_SECRET", ""),
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        print("=" * 55)
        print("  エラー: 以下の環境変数が設定されていません")
        print("=" * 55)
        for k in missing:
            print(f"  {k}")
        print("\n  設定方法（例）:")
        print("    export X_API_KEY=xxxxxxxxxxxxxxxxxxxx")
        print("    export X_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx")
        print("    export X_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("    export X_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxxxx")
        sys.exit(1)
    return keys


def find_text_file():
    """x_test フォルダ内の .txt ファイルを探す（複数ある場合は最初のもの）。"""
    files = sorted(glob.glob(os.path.join(POST_FOLDER, "*.txt")))
    if not files:
        raise FileNotFoundError(
            f"'{POST_FOLDER}' フォルダに .txt ファイルが見つかりません。"
        )
    if len(files) > 1:
        print(f"  ※ テキストファイルが複数あります。最初のファイルを使用: {files[0]}")
    return files[0]


def find_image_file():
    """x_test フォルダ内の画像ファイルを探す（複数ある場合は最初のもの）。"""
    for ext in IMAGE_EXTENSIONS:
        files = sorted(glob.glob(os.path.join(POST_FOLDER, ext)))
        if files:
            if len(files) > 1:
                print(f"  ※ 画像ファイルが複数あります。最初のファイルを使用: {files[0]}")
            return files[0]
    return None


def read_text(filepath):
    """テキストファイルを UTF-8 で読み込む。"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def calc_post_time():
    """次の投稿時刻（当日または翌日9:00）と待機秒数を返す。"""
    now = datetime.now()
    target = now.replace(hour=POST_HOUR, minute=POST_MINUTE, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    wait_sec = (target - now).total_seconds()
    return target, wait_sec


def format_wait(seconds):
    """秒数を「X時間Y分Z秒」形式に変換。"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    parts = []
    if h:
        parts.append(f"{h}時間")
    if m:
        parts.append(f"{m}分")
    parts.append(f"{s}秒")
    return "".join(parts)


def wait_until(target_time, wait_sec):
    """投稿時刻まで待機。1分ごとに残り時間を表示。"""
    print(f"  投稿予定: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  待機時間: {format_wait(wait_sec)}")
    print("  待機中... (Ctrl+C で中断)\n")

    interval = 60  # 表示更新間隔（秒）
    while True:
        remaining = (target_time - datetime.now()).total_seconds()
        if remaining <= 0:
            break
        if remaining <= interval:
            time.sleep(remaining)
            break
        print(f"  残り {format_wait(remaining)}", end="\r", flush=True)
        time.sleep(interval)

    print()


def upload_media(api_v1, image_path):
    """画像をアップロードし media_id を返す。"""
    print(f"  画像アップロード中: {image_path}")
    media = api_v1.media_upload(filename=image_path)
    print(f"  アップロード完了 (media_id: {media.media_id})")
    return media.media_id


def post_tweet(creds, text, image_path=None):
    """X に投稿する（画像あり / なし両対応）。"""
    # v1.1 API（メディアアップロード用）
    auth = tweepy.OAuth1UserHandler(
        creds["X_API_KEY"], creds["X_API_SECRET"],
        creds["X_ACCESS_TOKEN"], creds["X_ACCESS_TOKEN_SECRET"],
    )
    api_v1 = tweepy.API(auth)

    # v2 Client（ツイート投稿用）
    client = tweepy.Client(
        consumer_key=creds["X_API_KEY"],
        consumer_secret=creds["X_API_SECRET"],
        access_token=creds["X_ACCESS_TOKEN"],
        access_token_secret=creds["X_ACCESS_TOKEN_SECRET"],
    )

    media_ids = None
    if image_path:
        media_id = upload_media(api_v1, image_path)
        media_ids = [media_id]

    response = client.create_tweet(text=text, media_ids=media_ids)
    return response.data["id"]


def main():
    print("=" * 55)
    print("  X (Twitter) 自動投稿プログラム")
    print("=" * 55)

    # 認証情報の読み込み
    creds = load_credentials()

    # フォルダ確認
    if not os.path.isdir(POST_FOLDER):
        print(f"エラー: '{POST_FOLDER}' フォルダが見つかりません。")
        print(f"       スクリプトと同じ場所に '{POST_FOLDER}' フォルダを作成し、")
        print("       テキストファイルと画像ファイルを配置してください。")
        sys.exit(1)

    # ファイル読み込み
    try:
        txt_path = find_text_file()
        post_text = read_text(txt_path)
    except FileNotFoundError as e:
        print(f"エラー: {e}")
        sys.exit(1)

    img_path = find_image_file()

    # 投稿内容の確認
    print(f"\n  [投稿内容]")
    print(f"  テキストファイル : {txt_path}")
    print(f"  画像ファイル     : {img_path if img_path else 'なし'}")
    print(f"  文字数           : {len(post_text)} 文字")
    print(f"\n  --- 投稿文 ---")
    preview = post_text if len(post_text) <= 100 else post_text[:100] + "..."
    for line in preview.splitlines():
        print(f"  {line}")
    print(f"  ---------------")

    # 文字数チェック（X は140文字制限）
    if len(post_text) > 140:
        print(f"\n  警告: 投稿文が140文字を超えています（{len(post_text)}文字）。")
        print("  X の文字数制限により投稿が失敗する可能性があります。")

    # 投稿時刻の計算と待機
    target_time, wait_sec = calc_post_time()
    print(f"\n  [投稿スケジュール]")

    if wait_sec < 5:
        print("  投稿時刻になりました。直ちに投稿します。")
    else:
        wait_until(target_time, wait_sec)

    # 投稿実行
    print("  投稿中...")
    try:
        tweet_id = post_tweet(creds, post_text, img_path)
        print(f"\n  投稿成功!")
        print(f"  Tweet ID : {tweet_id}")
        print(f"  URL      : https://x.com/i/web/status/{tweet_id}")
    except tweepy.TweepyException as e:
        print(f"\n  投稿エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
