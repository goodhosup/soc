# SoC Handbook — Snapdragon · Exynos · Dimensity · Apple Silicon

스마트폰 SoC(System on Chip)의 CPU·GPU·NPU·ISP부터 메모리·전력·보안·공정까지 다루는 한글 모바일 칩셋 핸드북입니다.
각 페이지는 **기초 → 중급 → 전문가** 순서로 깊어집니다.

- 웹 사이트: https://goodhosup.github.io/soc/
- 자매 핸드북: [Bluetooth Handbook](https://goodhosup.github.io/bluetooth/) · [Cellular Handbook](https://goodhosup.github.io/cellular/) (LTE · 5G NR · 6G) · [Wi-Fi Handbook](https://goodhosup.github.io/wifi/) (IEEE 802.11)

## 로컬 실행

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/build_figures.py   # 그림 생성
.venv/bin/mkdocs serve                    # http://127.0.0.1:8000
```

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `mkdocs.yml` | 사이트 설정과 **전체 목차(nav)** — 페이지 추가는 여기서 시작 |
| `docs/` | 본문 마크다운 |
| `docs/assets/figures/` | 스크립트로 생성한 SVG 그림 (직접 수정하지 않음) |
| `diagrams/scripts/` | 그림 생성 스크립트 (matplotlib). 공통 색·스타일은 `style.py` |
| `includes/abbreviations.md` | 사이트 전체 약어 툴팁 (`tools/gen_abbreviations.py`가 약어 사전에서 생성) |
| `tools/soc_numbers.py` | **수치의 단일 출처** — LPDDR 대역폭, UFS 링크 속도, 동적 전력, 다이 수·수율, LLM 토큰 속도 상한 계산과 본문 검산(`--check`) |
| `tools/scaffold.py` | nav에 있는데 파일이 없는 페이지를 스텁으로 생성 |
| `tools/build_figures.py` | 모든 그림 스크립트 실행 |
| `tools/gen_abbreviations.py` | `docs/reference/glossary.md` 표 → 약어 툴팁 파일 생성 |
| `tools/make_cover.py` | 위키독스 표지 이미지 생성 |
| `tools/export_wikidocs.py` | 위키독스 책 형식으로 내보내기 (`--render`로 Mermaid PNG) |
| `tools/publish_wikidocs.py` | 위키독스 API로 업로드 (`WIKIDOCS_TOKEN` 환경 변수) |
| `docs/javascripts/diagrams.mjs` | Mermaid 렌더러 (큰 다이어그램 가독성, 다크 모드, 전체 화면) |

## 페이지 작성 규칙

1. 맨 위에 `!!! spec "규격 · 세대"` 박스로 관련 표준(Arm 아키텍처 버전, JEDEC LPDDR·UFS, MIPI, AMBA 등)과 기능이 처음 들어간 칩셋 세대를 적습니다. 확실하지 않은 세대 정보는 쓰지 않습니다.
2. 본문은 세 단계로 씁니다.
    - `!!! basic "한눈에 보기"` — 블록의 역할과 비유 (수식·코어 이름 없이)
    - 본문 `## 제목 { .l2 }` (헤딩 옆에 중급 배지) — 구조, 파라미터 표, 블록 그림, 칩셋 비교
    - `??? expert "전문가 노트 — …"` — 접히는 전문가 노트 (마이크로아키텍처, 수식, 트레이드오프, 커널 코드 위치, 실무 팁)
3. 끝에는 해당하면 **칩셋 비교** 표(Snapdragon ↔ Exynos ↔ Dimensity ↔ Apple)와 **관련 페이지** 링크를 붙입니다.
4. 절차는 Mermaid로(라벨에 괄호가 있으면 따옴표로 감쌈), 블록 다이어그램·곡선·계층 그림은 `diagrams/scripts/`의 스크립트로 그립니다.
5. 대역폭·전력·수율 같은 수치는 `tools/soc_numbers.py`로 계산해 넣고 `--check`로 검산합니다.
6. 세대별 사양(코어 구성·클럭·공정·캐시 용량)은 본문에 흩어 쓰지 않고 `reference/chipset-index.md`에 기준 시점과 출처(공식 발표·추정)를 붙여 모읍니다.
7. 발표되지 않은 칩셋·공정은 "논의 중"·"보도 기준"으로 쓰고 단정하지 않습니다. 공개 분석에서 나온 값은 "추정"으로 표시합니다.
8. 제조사 다이 사진·블록도·발표 슬라이드를 복사하지 않습니다. 그림은 직접 그리고, 문서·발표 이름만 출처로 인용합니다.
9. 벤치마크 점수는 측정 조건과 함께 적거나 쓰지 않습니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/deploy.yml`)가 그림을 생성하고 사이트를 빌드해 GitHub Pages에 올립니다.
저장소의 **Settings → Pages → Source**를 `GitHub Actions`로 설정하세요.

## 진행 상황

- 1차 완료: 시작하기, 공통 기초, CPU, 메모리와 저장장치 (+ 전력과 열 › DVFS 샘플, 약어 사전 초안)
- 2차 완료: GPU, NPU와 AI, 멀티미디어, 연결, 전력과 열 (01–09장 전체 집필, 약어 216개, 수치 검산 84건)
- 나머지 페이지는 `scaffold.py`가 만든 "작성 예정" 스텁 상태
