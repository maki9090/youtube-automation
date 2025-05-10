# scripts/label_clusters.py

import os
import pandas as pd
import openai

# ────────────────────────────────────────────────────────────
# 프로젝트 루트 경로 계산
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
# ────────────────────────────────────────────────────────────

# 1) 환경변수에서 API 키 로드
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되어 있지 않습니다.")

# 2) 클러스터링 결과 불러오기
LABELS_CSV = os.path.join(DATA_DIR, "labels.csv")
df = pd.read_csv(LABELS_CSV)  # columns: Keyword,Cluster

# 3) 클러스터별 대표 키워드(상위 5개) 추출
top_kw = (
    df.groupby("Cluster")["Keyword"]
      .apply(lambda kws: kws.value_counts().head(5).index.tolist())
      .to_dict()
)

# 4) GPT에게 레이블 요청
labels = {}
for cluster_id, kws in top_kw.items():
    prompt = (
        f"다음 키워드들을 보고 이 군집이 어떤 주제를 다루고 있는지, "
        f"짧고 분명한 레이블 하나만 답해주세요.\n\n"
        f"키워드: {', '.join(kws)}"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    labels[cluster_id] = resp.choices[0].message.content.strip()

# 5) 결과 DataFrame으로 변환 및 저장
CLUSTER_LABELS_CSV = os.path.join(DATA_DIR, "cluster_labels.csv")
out = pd.DataFrame([
    {"Cluster": cid, "Top Keywords": "; ".join(top_kw[cid]), "Label": labels[cid]}
    for cid in top_kw
])
out.to_csv(CLUSTER_LABELS_CSV, index=False, encoding="utf-8-sig")
print(f"✅ Saved cluster labels → {CLUSTER_LABELS_CSV}")
