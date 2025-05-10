# scripts/visualize_trends.py

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 1) 한글 폰트 설정 (Windows)
font_path = r"C:\Windows\Fonts\malgun.ttf"
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    rc('font', family='Malgun Gothic')

# ────────────────────────────────────────────────────────────
# 2) 데이터 불러오기
BASE_DIR   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH   = os.path.join(BASE_DIR, "data", "trends.csv")

df = pd.read_csv(
    CSV_PATH,
    names=["Region","Timestamp","Keyword","Traffic"],
    skiprows=1,
    dtype={"Traffic": str}
)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 3) Traffic 숫자만 추출하여 int 변환
df["Traffic"] = df["Traffic"].fillna("").apply(lambda x: int(re.sub(r"\D", "", x) or 0))

# 4) 시간별·키워드별 피벗 테이블 생성
pivot = df.pivot_table(
    index=pd.Grouper(key="Timestamp", freq="h"),
    columns="Keyword",
    values="Traffic",
    aggfunc="sum",
    fill_value=0,
)

# 5) 상위 N개 키워드만 선택
top_n = 5
total = pivot.sum().sort_values(ascending=False)
top_kws = total.head(top_n).index.tolist()
sub = pivot[top_kws]

# 6) 스택플롯 그리기
plt.figure(figsize=(12, 7))
plt.stackplot(
    sub.index,
    [sub[k] for k in top_kws],
    labels=top_kws,
    alpha=0.8
)

# 7) 레이블, 범례, 눈금, 타이틀 설정
plt.title("시간대별 상위 5개 키워드 트래픽 변화", fontsize=16)
plt.xlabel("시간", fontsize=12)
plt.ylabel("검색량 합계", fontsize=12)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.4)

# 범례를 그래프 밖에 배치
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), title="키워드")

plt.tight_layout()

# 8) 이미지 저장 및 표시
OUT_FILE = os.path.join(BASE_DIR, "trend_stackplot.png")
plt.savefig(OUT_FILE, dpi=150)
print(f"✅ Saved plot to {OUT_FILE}")
plt.show()
