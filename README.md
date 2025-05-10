# YouTube 자동화 파이프라인

## 🚀 프로젝트 개요
- **목적**: 구글 트렌드에서 키워드 수집 → 클러스터링 → 레이블 생성 → 숏폼 아이디어 자동 생성  
- **언어/툴**: Python, gspread, pandas, scikit-learn(DBSCAN), OpenAI API, Google Sheets API

## 📁 디렉토리 구조
YoutubeTemplate/
├── config/                   # 환경 설정 (config.json, ai_providers.json)
├── credentials/              # 서비스 계정 키 JSON
├── data/                     # 수집·산출물 저장 폴더
├── scripts/                  # 실행 스크립트
│   ├── trends.py
│   ├── cluster_keywords.py
│   ├── label_clusters.py
│   ├── generate_ideas.py
│   └── run_all.py
├── requirements.txt          # 의존 패키지 목록
└── README.md                 # 이 파일
## ⚙️ 설치 및 실행
1. 리포지토리 복제  
   `git clone https://github.com/maki9090/youtube-automation.git`  
2. 프로젝트 폴더 이동  
   `cd youtube-automation`  
3. 가상환경 생성 & 활성화  
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
의존성 설치
pip install -r requirements.txt

전체 파이프라인 실행
python -m scripts.run_all

---

## 3. 다른 이름으로 저장  
- 메모장에서 **파일 → 다른 이름으로 저장**  
  - **파일 이름**: `README.md`  
  - **저장 위치**: `C:\Users\youmi\Desktop\YoutubeTemplate\README.md`  
  - **인코딩**: UTF-8  
- **저장** 버튼 클릭

이제 `C:\Users\youmi\Desktop\YoutubeTemplate` 폴더에 `README.md`가 생성됩니다.  
파일 탐색기에서 확인해 보세요!

