# test_gemini_adapter.py
from ai_adapter import AdapterFactory
import os, json

# (기존과 동일하게 config 불러오는 부분은 생략)

# Gemini 환경변수 이름
cfg_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "ai_providers.json")
)
cfg = json.load(open(cfg_path, encoding="utf-8"))
gem_env = cfg["providers"]["gemini"]["api_key_env"]
print("Gemini api_key_env:", gem_env, "→", os.getenv(gem_env))

# 어댑터 생성
gem_adapter = AdapterFactory.get_adapter("gemini")
print("Gemini Adapter instance:", gem_adapter)
