# generate_topic_scripts.py
import os, json, csv
import openai
from ai_adapter import AdapterFactory

def safe_generate(name: str, prompt: str, **kwargs) -> str:
    try:
        adapter = AdapterFactory.get_adapter(name)
        return adapter.generate(prompt, **kwargs)
    except openai.error.RateLimitError:
        # gpt → gpt35 로 대체
        alt = "gpt35" if name == "gpt" else "gpt"
        adapter = AdapterFactory.get_adapter(alt)
        return adapter.generate(prompt, **kwargs)

# 1) 설정 & 어댑터 준비
cfg_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "ai_providers.json")
)
cfg = json.load(open(cfg_path, encoding="utf-8"))
default_provider = cfg["default"]

# 2) 키워드 불러오기 (시트에 기록된 시트 이름은 "Trend" 입니다)
#    트렌드 스크립트가 구글 시트에 기록된 다음, trends.py 로 받은 CSV 파일을
#    scripts/data/keywords.csv 로 저장했다고 가정합니다.
keywords_csv = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "keywords.csv")
)
with open(keywords_csv, encoding="utf-8") as f:
    keywords = [row[0] for row in csv.reader(f) if row]

# 3) 스크립트 생성 & 저장
output_csv = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "scripts.csv")
)
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, "w", encoding="utf-8", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["keyword", "script"])
    for kw in keywords:
        prompt = f"‘{kw}’ 관련 숏폼 영상 스크립트를 3문장으로 요약해줘."
        script = safe_generate(default_provider, prompt, temperature=0.7, max_tokens=200)
        writer.writerow([kw, script])
        print(f"✅ Generated for {kw}")
