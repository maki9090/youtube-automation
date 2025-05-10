# scripts/trends.py

import os
import csv
import feedparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone

# ────────────────────────────────────────────────────────────
# 설정 파트: 환경마다 바꿀 것은 여기에만!
from os.path import abspath, join, dirname

# 프로젝트 루트 경로 계산 (scripts/ 아래에서 한 단계 위)
BASE_DIR = abspath(join(dirname(__file__), ".."))

# credentials 폴더 안의 서비스 계정 JSON
SERVICE_ACCOUNT_FILE = join(BASE_DIR, "credentials", "service_account.json")

SPREADSHEET_NAME     = "YouTube auto"
WORKSHEET_NAME       = "Trends"

# 지원하는 지역별 RSS URL
FEEDS = {
    "US": "https://trends.google.com/trending/rss?geo=US&hl=en",
    "KR": "https://trends.google.com/trending/rss?geo=KR&hl=ko",
}

# 로컬에 저장할 경로
DATA_DIR      = join(BASE_DIR, "data")
TRENDS_CSV    = join(DATA_DIR, "trends.csv")
KEYWORDS_CSV  = join(DATA_DIR, "keywords.csv")
# ────────────────────────────────────────────────────────────

def init_sheets():
    """구글 시트 인증 후 워크시트 객체 반환"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE,
        scope
    )
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

def append_rss_to_sheet(sheet):
    """FEEDS 딕셔너리의 RSS 데이터를 읽어 시트에 append"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    for region, url in FEEDS.items():
        data = feedparser.parse(url)
        for entry in data.entries:
            keyword = entry.title
            traffic = entry.get("ht_approx_traffic", "")
            sheet.append_row([region, now, keyword, traffic])
    print("✅ RSS 트렌드를 Google Sheets에 기록 완료")

def export_csv_from_sheet(sheet):
    """시트 전체를 trends.csv로 덮어쓰고, keywords.csv를 생성"""
    os.makedirs(DATA_DIR, exist_ok=True)

    # 1) 전체 덮어쓰기
    rows = sheet.get_all_values()
    with open(TRENDS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ trends.csv 생성: {TRENDS_CSV}")

    # 2) 키워드 열만 추출
    with open(TRENDS_CSV, "r", encoding="utf-8") as f_in, \
         open(KEYWORDS_CSV, "w", encoding="utf-8", newline="") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        next(reader, None)  # 헤더 건너뛰기
        for row in reader:
            writer.writerow([row[2]])
    print(f"✅ keywords.csv 생성: {KEYWORDS_CSV}")

def main():
    sheet = init_sheets()
    append_rss_to_sheet(sheet)
    export_csv_from_sheet(sheet)

if __name__ == "__main__":
    main()
