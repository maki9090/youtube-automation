# quick_test.py
from pytrends.request import TrendReq

# 1) pytrends 세팅 (글로벌, 영어, UTC)
pytrends = TrendReq(hl='en-US', tz=0)

# 2) daily trends(전 세계 급상승 검색어) 가져오기
df = pytrends.trending_searches()
print(df.head())
