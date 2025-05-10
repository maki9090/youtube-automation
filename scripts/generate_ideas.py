# scripts/generate_ideas.py

import os
import pandas as pd
import openai

# 0) API 키
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY가 없습니다.")

# 0-1) 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLUSTER_LABELS_CSV = os.path.join(BASE_DIR, "data", "cluster_labels.csv")
IDEAS_CSV = os.path.join(BASE_DIR, "data", "ideas.csv")

# 1) 클러스터 레이블 로드
df = pd.read_csv(CLUSTER_LABELS_CSV)  
# 예상 컬럼: Cluster, Top Keywords, Label

results = []

for _, row in df.iterrows():
    label       = row["Label"]
    keywords    = row["Top Keywords"]
    prompt = f"""
You are a YouTube content strategist.
Cluster name: "{label}"
Top keywords: {keywords}

1) 이 클러스터에 맞는 숏폼 영상용 제목 3개를 한국어로 제안해 주세요.
2) 각 제목별로 1~2줄 분량의 스크립트 개요를 한국어로 써 주세요.
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are a helpful assistant."},
                  {"role":"user",  "content":prompt}],
        temperature=0.8,
        max_tokens=500
    )
    text = resp.choices[0].message.content.strip()
    results.append({
        "Cluster":        row["Cluster"],
        "Label":          label,
        "Top Keywords":   keywords,
        "Generated Idea": text
    })

# 2) 결과 저장
out = pd.DataFrame(results)
out.to_csv(IDEAS_CSV, index=False, encoding="utf-8-sig")
print(f"✅ Saved ideas for {len(results)} clusters to {IDEAS_CSV}")
