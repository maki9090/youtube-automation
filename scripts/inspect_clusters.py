# scripts/inspect_clusters.py

import pandas as pd

# 1) labels.csv 불러오기
df = pd.read_csv("../data/labels.csv")

# 2) 클러스터별 사이즈 집계
count_by_cluster = (
    df.groupby("Cluster")
      .size()
      .sort_values(ascending=False)
      .rename("Count")
)

# 3) 각 클러스터 상위 3개 키워드 뽑기
top_keywords = (
    df.groupby("Cluster")["Keyword"]
      .apply(lambda kws: kws.value_counts().head(3).index.tolist())
      .rename("Top Keywords")
)

# 4) 결과 합치기
summary = pd.concat([count_by_cluster, top_keywords], axis=1).reset_index()
print(summary.to_string(index=False))
