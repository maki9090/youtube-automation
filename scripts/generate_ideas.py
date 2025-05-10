# scripts/generate_ideas.py

import os
import pandas as pd
from openai import OpenAI
import csv, time

# ── 설정 ──
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY 환경변수가 필요합니다.")
client = OpenAI(api_key=api_key)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEYWORD_THEMES_CSV = os.path.join(BASE_DIR, "data", "keyword_themes.csv")
IDEAS_CSV          = os.path.join(BASE_DIR, "data", "ideas.csv")

# 1) 키워드·테마 로드
df = pd.read_csv(KEYWORD_THEMES_CSV)  # 컬럼: Keyword, Theme1, Theme2
keywords = df["Keyword"].tolist()
themes1  = df["Theme1"].tolist()
themes2  = df["Theme2"].fillna("").tolist()

results = []
batch_size = 10

# 2) 배치 단위 요청
for i in range(0, len(keywords), batch_size):
    batch_keys   = keywords[i : i + batch_size]
    batch_th1    = themes1 [i : i + batch_size]
    batch_th2    = themes2 [i : i + batch_size]
    print(f"▶ 배치 {i//batch_size+1} 시작: 키워드 {i+1}~{min(i+batch_size, len(keywords))}")
    
    prompt = "다음 키워드와 테마에 맞게, 각 키워드별로\n" \
             "1) 숏폼 영상용 제목 1개\n" \
             "2) 1줄 스크립트 아이디어 1개\n" \
             "CSV 형식(키워드,제목,스크립트)으로 출력해 주세요.\n\n"
    for k, t1, t2 in zip(batch_keys, batch_th1, batch_th2):
        prompt += f"{k} / 테마1: {t1}" + (f", 테마2: {t2}" if t2 else "") + "\n"
    
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content":prompt}],
        temperature=0.7,
        max_tokens=300 * batch_size // 3
    )
    text = resp.choices[0].message.content.strip()
    
    # CSV 파싱
    reader = csv.reader(text.splitlines())
    for row in reader:
        if len(row) >= 3:
            results.append({
                "Keyword":   row[0],
                "Title":     row[1],
                "Script":    row[2]
            })
    print(f"✔ 배치 {i//batch_size+1} 완료")
    time.sleep(1)

# 3) 결과 저장
out = pd.DataFrame(results)
os.makedirs(os.path.dirname(IDEAS_CSV), exist_ok=True)
out.to_csv(IDEAS_CSV, index=False, encoding="utf-8-sig")
print(f"✅ 전체 아이디어 생성 완료 → {IDEAS_CSV}")
