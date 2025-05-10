# scripts/cluster_keywords.py

import os
import time
import pandas as pd
import openai
from sklearn.cluster import DBSCAN

# ──────────────────────────────────────────────────────────────────────────
# 프로젝트 루트 경로 계산
BASE_DIR   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR   = os.path.join(BASE_DIR, "data")

# 0) OpenAI API 키 설정 (환경변수에서 가져오기)
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다.")
# ──────────────────────────────────────────────────────────────────────────

# 1) 키워드 로드 & 상위 N개 추출
KEYWORDS_CSV = os.path.join(DATA_DIR, "keywords.csv")
df = pd.read_csv(KEYWORDS_CSV, header=None, names=["Keyword"])
top_n = 200
top_keywords = (
    df["Keyword"]
      .value_counts()
      .head(top_n)
      .index
      .tolist()
)
print(f"🔍 총 {len(df)}개 키워드 중 상위 {len(top_keywords)}개만 클러스터링합니다.")

# 2) 배치별로 임베딩 생성
batch_size = 20    # ← 20개씩 한 번에 요청
embeddings = []

for i in range(0, len(top_keywords), batch_size):
    batch = top_keywords[i : i + batch_size]
    print(f"⚙️ 배치 {i//batch_size + 1}: {len(batch)}개 키워드 임베딩 요청...")
    resp = openai.Embedding.create(
        input=batch,
        model="text-embedding-ada-002"
    )
    embeddings.extend(d["embedding"] for d in resp["data"])
    time.sleep(0.5)   # ← 0.5초만 대기

# 3) DBSCAN 군집화
db = DBSCAN(eps=0.6, min_samples=2, metric="cosine")
labels = db.fit_predict(embeddings)

# 4) 결과 저장
LABELS_CSV = os.path.join(DATA_DIR, "labels.csv")
out = pd.DataFrame({
    "Keyword": top_keywords,
    "Cluster": labels
})
out.to_csv(LABELS_CSV, index=False, encoding="utf-8-sig")
print(f"✅ Saved labels for {len(top_keywords)} keywords to {LABELS_CSV}")
