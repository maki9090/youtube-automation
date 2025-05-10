# scripts/classify_keywords.py

import os, json, csv, time
import pandas as pd
from openai import OpenAI  # ← 최신 SDK 사용
     
# ── 설정 ──
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE, "data")
KEYWORD_CSV = os.path.join(DATA_DIR, "keywords.csv")
OUT_CSV = os.path.join(DATA_DIR, "keyword_themes.csv")
THEMES_JSON = os.path.join(BASE, "config", "themes.json")

# 1) OpenAI 클라이언트 초기화
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되어 있지 않습니다.")
client = OpenAI(api_key=api_key)

# 2) 테마 사전 불러오기
with open(THEMES_JSON, encoding="utf-8") as f:
    themes = json.load(f)
theme_names = list(themes.keys())

# 3) 키워드 로드 & 중복 제거
df = pd.read_csv(KEYWORD_CSV, header=None, names=["Keyword"])
keywords = df["Keyword"].drop_duplicates().tolist()

# 4) GPT 분류 함수 (batch 단위)
def classify_batch(batch):
    prompt = f"""
아래 키워드를, 사전({theme_names}) 중 하나 또는 최대 두 개 테마로 분류해 주세요.
출력은 CSV 형식(키워드,테마1,테마2)로만 해 주십시오.

키워드:
{chr(10).join(batch)}
"""
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    text = resp.choices[0].message.content.strip()
    reader = csv.reader(text.splitlines())
    return list(reader)

# 5) 배치 처리 & 결과 수집
results = []
batch_size = 20
for i in range(0, len(keywords), batch_size):
    batch = keywords[i : i+batch_size]
    print(f"⚙️ 분류 중: 배치 {i//batch_size+1} / {((len(keywords)-1)//batch_size)+1}")
    try:
        classified = classify_batch(batch)
        results.extend(classified)
    except Exception as e:
        print("❌ 분류 실패:", e)
    time.sleep(1)

# 6) 결과 저장
out_df = pd.DataFrame(results, columns=["Keyword", "Theme1", "Theme2"])
out_df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ 키워드 테마 분류 완료 → {OUT_CSV}")
