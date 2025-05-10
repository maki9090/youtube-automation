# ai_adapter.py
import os, json
from abc import ABC, abstractmethod

class AIAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

class OpenAIAdapter(AIAdapter):
    def __init__(self, model, api_key):
        import openai
        openai.api_key = api_key
        self.model = model

    def generate(self, prompt, **kwargs):
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"user","content":prompt}],
            **kwargs
        )
        return resp.choices[0].message.content

class GoogleGeminiAdapter(AIAdapter):
    def __init__(self, model, api_key):
        from google.generativeai import client
        client.configure(api_key=api_key)
        self.model = model

    def generate(self, prompt, **kwargs):
        resp = client.generate(model=self.model, prompt=prompt, **kwargs)
        return resp.text

class AdapterFactory:
    @staticmethod
    def get_adapter(name: str) -> AIAdapter:
        # config 위치를 프로젝트 루트의 config 폴더로 가리킵니다.
        cfg_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "config", "ai_providers.json")
        )
        cfg = json.load(open(cfg_path, encoding="utf-8"))
        p = cfg["providers"][name]
        key = os.getenv(p["api_key_env"])
        if p["type"] == "openai":
            return OpenAIAdapter(p["model"], key)
        if p["type"] == "google":
            return GoogleGeminiAdapter(p["model"], key)
        raise ValueError(f"Unknown provider: {name}")
