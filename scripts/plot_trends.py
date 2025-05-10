# plot_trends.py
import os
import pandas as pd
import matplotlib.pyplot as plt

# trends.csv 파일 경로
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRENDS_CSV = os.path.join(BASE_DIR, "data", "trends.csv")

# CSV 불러오기
df = pd.read_csv(TRENDS_CSV, names=["Region","Timestamp","Keyword","Traffic"], skiprows=1)

# 예시: 시간별 전체 검색량(대략) 합계 시각화
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
summary = df.groupby(pd.Grouper(key="Timestamp", freq="H"))["Keyword"].count()

plt.figure()
plt.plot(summary.index, summary.values)
plt.title("Hourly Trend Count")
plt.xlabel("Time")
plt.ylabel("Number of Keywords")
plt.tight_layout()
plt.show()
