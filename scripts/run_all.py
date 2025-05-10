# scripts/run_all.py

import subprocess
import sys
import os
import json

# ────────────────────────────────────────────────────────────
# 1) 경로 준비
#    이 파일이 있는 scripts/ 디렉터리
BASE = os.path.dirname(__file__)
#    그 위가 프로젝트 루트(=YoutubeTemplate)
ROOT = os.path.abspath(os.path.join(BASE, ".."))
#    현재 사용하는 Python 실행 경로
PY = sys.executable
# ────────────────────────────────────────────────────────────

# 2) 설정(config.json) 읽기
with open(os.path.join(ROOT, "config", "config.json"), encoding="utf-8") as f:
    cfg = json.load(f)

DATA_DIR = os.path.join(ROOT, cfg["data_dir"])
files    = cfg["files"]

# 3) 단계별 실행 목록
#    (단계 이름, 스크립트 파일명, 그 단계가 필요로 하는 입력 파일 경로 목록)
steps = [
    ("1단계: 트렌드 수집",       "trends.py",           []),
    ("2단계: 키워드 클러스터링", "cluster_keywords.py", [os.path.join(DATA_DIR, files["trends"])]),
    ("3단계: 클러스터 라벨",     "label_clusters.py",   [os.path.join(DATA_DIR, files["keywords"])]),
    ("4단계: 아이디어 생성",     "generate_ideas.py",   [os.path.join(DATA_DIR, files["cluster_labels"])]),
    # 이후 단계가 추가되면 여기에 (이름, 스크립트, [inputs]) 형식으로 넣으시면 됩니다.
]

# 4) 각 단계 순서대로 실행
for title, script, inputs in steps:
    print(f"▶️ {title} 실행 중…")
    cmd = [PY, os.path.join(BASE, script)] + inputs
    # 예: ['C:\\Python\\python.exe', '...\\scripts\\trends.py']
    subprocess.run(cmd, check=True)

print("✅ 모든 단계가 완료되었습니다.")
