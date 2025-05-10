# scripts/test_embed.py

import os
import openai

# 1) 환경변수에서 키 로드
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되어 있지 않습니다.")

# 2) 단일 문장으로 임베딩 요청
resp = openai.Embedding.create(
    input="한국어 테스트",
    model="text-embedding-ada-002"
)

# 3) 결과 출력 (벡터 앞 부분만)
print("✅ 임베딩 성공:", resp["data"][0]["embedding"][:5], "…")
