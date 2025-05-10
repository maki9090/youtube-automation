# test_ai_adapter.py
import os, json
from ai_adapter import AdapterFactory

# 1) 설정 파일 경로
cfg_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 "..", "config", "ai_providers.json")
)
cfg = json.load(open(cfg_path, encoding="utf-8"))

# 2) 환경변수 이름 꺼내보기
name = cfg["providers"]["gpt"]["api_key_env"]
print("GPT api_key_env:", name, "→", os.getenv(name))

# 3) 어댑터 생성해보기
adapter = AdapterFactory.get_adapter("gpt")
print("Adapter instance:", adapter)
