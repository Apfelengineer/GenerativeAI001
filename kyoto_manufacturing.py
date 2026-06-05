#!/usr/bin/env python3
"""
京都府の製造業割合 全国ランキング & 業種別割合表示
データソース: 令和3年経済センサス‐活動調査（総務省・経済産業省）
         政府統計の総合窓口(e-Stat) API
統計表ID: 0003449701

使用方法:
  python kyoto_manufacturing.py <e-Stat_APP_ID>
  または: ESTAT_APP_ID=<APP_ID> python kyoto_manufacturing.py

APIキー無料登録: https://www.e-stat.go.jp/api/
"""

import requests
import sys
import os
from collections import defaultdict

STATS_DATA_ID = "0003449701"
API_BASE = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
KYOTO_CODE = "26000"

# 都道府県コード → 名称（e-Statの5桁コード形式）
PREF_NAMES = {
    "01000": "北海道", "02000": "青森県", "03000": "岩手県",
    "04000": "宮城県", "05000": "秋田県", "06000": "山形県",
    "07000": "福島県", "08000": "茨城県", "09000": "栃木県",
    "10000": "群馬県", "11000": "埼玉県", "12000": "千葉県",
    "13000": "東京都", "14000": "神奈川県", "15000": "新潟県",
    "16000": "富山県", "17000": "石川県", "18000": "福井県",
    "19000": "山梨県", "20000": "長野県", "21000": "岐阜県",
    "22000": "静岡県", "23000": "愛知県", "24000": "三重県",
    "25000": "滋賀県", "26000": "京都府", "27000": "大阪府",
    "28000": "兵庫県", "29000": "奈良県", "30000": "和歌山県",
    "31000": "鳥取県", "32000": "島根県", "33000": "岡山県",
    "34000": "広島県", "35000": "山口県", "36000": "徳島県",
    "37000": "香川県", "38000": "愛媛県", "39000": "高知県",
    "40000": "福岡県", "41000": "佐賀県", "42000": "長崎県",
    "43000": "熊本県", "44000": "大分県", "45000": "宮崎県",
    "46000": "鹿児島県", "47000": "沖縄県",
}


def fetch_data(app_id):
    params = {
        "appId": app_id,
        "statsDataId": STATS_DATA_ID,
        "metaGetFlg": "Y",
        "cntGetFlg": "N",
        "explanationGetFlg": "N",
        "annotationGetFlg": "N",
        "sectionHeaderFlg": "1",
        "limit": 100000,
    }
    resp = requests.get(API_BASE, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def ensure_list(obj):
    if obj is None:
        return []
    return obj if isinstance(obj, list) else [obj]


def parse_dims(class_obj_raw):
    """Return {dim_id: {code: name}} from CLASS_OBJ"""
    dims = {}
    for obj in ensure_list(class_obj_raw):
        dim_id = obj["@id"]
        classes = ensure_list(obj.get("CLASS", []))
        dims[dim_id] = {c["@code"]: c.get("@name", c["@code"]) for c in classes}
    return dims


def find_code(code_map, keywords):
    """Return first code whose name contains any keyword, else None."""
    for code, name in code_map.items():
        if any(kw in name for kw in keywords):
            return code
    return None


def is_pref_code(code):
    """True if area code represents one of 47 prefectures (e.g. '26000')."""
    try:
        n = int(code)
        return 1000 <= n <= 47999
    except ValueError:
        return False


def normalize_area_code(code):
    """Normalize area codes: '26' or '260' -> '26000', '26000' stays."""
    code = code.strip()
    try:
        n = int(code)
        if 1 <= n <= 47:
            return f"{n:02d}000"
        if 1000 <= n <= 47999:
            return f"{n:05d}"
    except ValueError:
        pass
    return code


def get_value(v):
    """Parse numeric value from a data entry, return None if missing."""
    raw = str(v.get("$", "")).replace(",", "").strip()
    if raw in ("", "-", "…", "x", "X"):
        return None
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return None


def aggregate(values, dims, tab_dim, est_code, filter_codes):
    """
    Sum establishment counts by (area, cat01).
    - tab_dim / est_code : dimension id and code for 事業所数 (may be None)
    - filter_codes       : {dim_id: code} — only keep rows matching these
    """
    area_industry = defaultdict(lambda: defaultdict(float))

    for v in values:
        # Filter by tab (measure) if applicable
        if tab_dim and v.get(f"@{tab_dim}") != est_code:
            continue

        # Filter by other required codes (e.g. 経営組織=合計)
        skip = any(v.get(f"@{dim}") != code for dim, code in filter_codes.items())
        if skip:
            continue

        raw_area = v.get("@area", "")
        industry = v.get("@cat01", "")
        count = get_value(v)
        if count is None:
            continue

        area = normalize_area_code(raw_area)
        area_industry[area][industry] += count

    return area_industry


def print_ranking(ranked, area_industry, total_ind_code, mfg_code, area_code_map):
    width = 62
    print("\n" + "=" * width)
    print("  全国都道府県別 製造業事業所割合ランキング")
    print("  データ: 令和3年経済センサス‐活動調査（速報集計）")
    print("=" * width)
    print(f"  {'順位':>4}  {'都道府県':<12}  {'製造業割合':>10}  "
          f"{'製造業':>8}  {'全産業':>9}")
    print("-" * width)

    kyoto_rank = None
    kyoto_ratio = None
    for rank, (code, ratio, mfg, total) in enumerate(ranked, 1):
        name = PREF_NAMES.get(code) or area_code_map.get(code, code)
        marker = " ◀ 京都府" if code == KYOTO_CODE else ""
        print(f"  {rank:>4}  {name:<12}  {ratio:>9.2f}%  "
              f"{int(mfg):>8,}  {int(total):>9,}{marker}")
        if code == KYOTO_CODE:
            kyoto_rank, kyoto_ratio = rank, ratio

    print("=" * width)
    if kyoto_rank:
        kyoto_mfg  = next(m for c, _, m, _ in ranked if c == KYOTO_CODE)
        kyoto_total = next(t for c, _, _, t in ranked if c == KYOTO_CODE)
        print(f"\n  ★ 京都府の製造業事業所割合は全国 第{kyoto_rank}位")
        print(f"     製造業事業所数 {int(kyoto_mfg):,} / 全産業 {int(kyoto_total):,}"
              f"（{kyoto_ratio:.2f}%）")


def print_kyoto_breakdown(area_industry, industry_codes, total_ind_code):
    kyoto = area_industry.get(KYOTO_CODE, {})
    total = kyoto.get(total_ind_code, 0)
    if total == 0:
        total = sum(v for k, v in kyoto.items() if k != total_ind_code)

    rows = []
    for code, name in industry_codes.items():
        if code == total_ind_code:
            continue
        count = kyoto.get(code, 0)
        ratio = count / total * 100 if total > 0 else 0.0
        rows.append((name, int(count), ratio))

    rows.sort(key=lambda x: x[2], reverse=True)

    width = 66
    print("\n" + "=" * width)
    print("  京都府内 業種別事業所数・割合（全産業比）")
    print("  データ: 令和3年経済センサス‐活動調査（速報集計）")
    print("=" * width)
    print(f"  {'業種':<34}  {'事業所数':>9}  {'割合':>7}")
    print("-" * width)
    for name, count, ratio in rows:
        bar = "▊" * max(1, round(ratio / 2))
        print(f"  {name:<34}  {count:>9,}  {ratio:>6.2f}%  {bar}")
    print("-" * width)
    print(f"  {'合計':<34}  {int(total):>9,}  {'100.00%':>7}")


def main():
    app_id = os.environ.get("ESTAT_APP_ID") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not app_id:
        print("=" * 60)
        print("  エラー: e-Stat APIキーが指定されていません。")
        print("=" * 60)
        print("\n  APIキーの取得方法（無料）:")
        print("    1. https://www.e-stat.go.jp/api/ にアクセス")
        print("    2. ユーザ登録・ログイン後「アプリケーション追加」")
        print("    3. 発行されたアプリケーションIDを使用")
        print("\n  使用方法:")
        print("    python kyoto_manufacturing.py <APP_ID>")
        print("    または: ESTAT_APP_ID=<APP_ID> python kyoto_manufacturing.py")
        sys.exit(1)

    print("政府統計(e-Stat) 令和3年経済センサス‐活動調査 データ取得中...")

    try:
        raw = fetch_data(app_id)
    except requests.exceptions.RequestException as e:
        print(f"通信エラー: {e}")
        sys.exit(1)

    result = raw.get("GET_STATS_DATA", {}).get("RESULT", {})
    if result.get("STATUS", -1) != 0:
        print(f"APIエラー: {result.get('ERROR_MSG', '不明なエラー')}")
        sys.exit(1)

    stat = raw["GET_STATS_DATA"]["STATISTICAL_DATA"]
    dims = parse_dims(stat["CLASS_INF"]["CLASS_OBJ"])
    values = ensure_list(stat["DATA_INF"]["VALUE"])

    # ---- Identify key dimension codes ----
    industry_codes = dims.get("cat01", {})
    total_ind_code = find_code(industry_codes, ["合計", "総数", "全産業"])
    mfg_code = find_code(industry_codes, ["製造業"])
    if mfg_code is None:
        mfg_code = "E"  # 日本標準産業分類の大分類コード

    if not industry_codes:
        print("エラー: 産業分類データが見つかりません。")
        sys.exit(1)

    # Find 事業所数 in the tab (measure) dimension
    tab_codes = dims.get("tab", {})
    est_code = find_code(tab_codes, ["事業所数"])
    tab_dim = "tab" if tab_codes else None

    # For other category dims (経営組織, 単一・複数 etc.) filter on 合計 if present
    filter_codes = {}
    for dim_id, code_map in dims.items():
        if dim_id in ("cat01", "area", "time", "tab"):
            continue
        total_code = find_code(code_map, ["合計", "総数", "計"])
        if total_code:
            filter_codes[dim_id] = total_code

    # Use latest time period
    time_codes = dims.get("time", {})
    if time_codes:
        latest_time = sorted(time_codes.keys())[-1]
        filter_codes["time"] = latest_time

    # ---- Aggregate ----
    area_industry = aggregate(values, dims, tab_dim, est_code, filter_codes)

    # ---- Build national ranking ----
    area_code_map = dims.get("area", {})
    pref_stats = []
    for pref_code in PREF_NAMES:
        data = area_industry.get(pref_code, {})
        total = data.get(total_ind_code, 0)
        mfg = data.get(mfg_code, 0)
        if total > 0:
            pref_stats.append((pref_code, mfg / total * 100, mfg, total))

    if not pref_stats:
        print("\n注意: 都道府県別データが集計できませんでした。")
        print("      APIキーが正しいか、または統計表の構造が変わった可能性があります。")
        print(f"      取得データ件数: {len(values)}")
        print(f"      利用可能な次元: {list(dims.keys())}")
        sys.exit(1)

    ranked = sorted(pref_stats, key=lambda x: x[1], reverse=True)

    # ---- Display ----
    print_ranking(ranked, area_industry, total_ind_code, mfg_code, area_code_map)
    print_kyoto_breakdown(area_industry, industry_codes, total_ind_code)

    print("\n  データ出典: 令和3年経済センサス‐活動調査（総務省・経済産業省）")
    print("  政府統計の総合窓口(e-Stat): https://www.e-stat.go.jp/")
    print(f"  統計表ID: {STATS_DATA_ID}")


if __name__ == "__main__":
    main()
