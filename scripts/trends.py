# scripts/trends.py

import os
import csv
from datetime import datetime
from serpapi import GoogleSearch

# ── 설정 ──
BASE_DIR     = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR     = os.path.join(BASE_DIR, "data")
TRENDS_CSV   = os.path.join(DATA_DIR, "trends.csv")
KEYWORDS_CSV = os.path.join(DATA_DIR, "keywords.csv")

# 지역 설정: "KR" 또는 "US"
GEO     = "KR"
HL      = "ko"  # 언어 코드: 한국어
API_KEY = os.getenv("SERPAPI_KEY")
if not API_KEY:
    raise RuntimeError("환경변수 SERPAPI_KEY가 설정되어 있지 않습니다.")

def fetch_trends():
    params = {
        "engine": "google_trends",
        "type": "daily",   # 일간 트렌드
        "hl": HL,
        "geo": GEO,
        "api_key": API_KEY
    }
    client = GoogleSearch(params)
    data = client.get_dict()
    # SerpApi 결과 구조에서 일일 트렌드 리스트 추출
    items = data.get("daily_trends", {}).get("trendingSearches", [])
    # 각 아이템의 title.query 값(없으면 title)
    return [
        item["title"].get("query", item["title"])
        for item in items
    ]

def save_csv(keywords):
    os.makedirs(DATA_DIR, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # trends.csv: [timestamp, rank, keyword]
    with open(TRENDS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","rank","keyword"])
        for idx, kw in enumerate(keywords, start=1):
            writer.writerow([now, idx, kw])

    # keywords.csv: 키워드 열만
    with open(KEYWORDS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for kw in keywords:
            writer.writerow([kw])

    print("✅ SerpApi로 트렌드 수집 및 CSV 생성 완료")

def main():
    kws = fetch_trends()
    if not kws:
        print("⚠️ 오늘의 트렌드를 불러오지 못했습니다.")
    else:
        save_csv(kws)

if __name__ == "__main__":
    main()
