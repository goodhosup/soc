# 레퍼런스

본문을 읽다가 "그 칩은 몇 nm였더라", "그 규격은 어느 단체 문서였지", "이 대역폭이면 LLM이 몇 tok/s 나오지"를 빠르게 찾기 위한 섹션입니다. 개념 설명보다 표와 링크 중심으로 구성했고, 각 항목은 자세히 다루는 본문 페이지로 연결됩니다. 본문이 일부러 쓰지 않은 세대별 사양도 여기 모았습니다.

| 페이지 | 핵심 질문 |
|---|---|
| [칩셋 세대 인덱스](chipset-index.md) | Snapdragon·Exynos·Dimensity·Apple A·Tensor 각 세대의 공정, CPU 구성, GPU, LPDDR, 모뎀은? |
| [제조사별 비교](vendor-compare.md) | 다섯 회사는 사업 모델, CPU·GPU·NPU·모뎀 전략, 파운드리, 업데이트 정책이 어떻게 다른가? |
| [표준 인덱스](standards.md) | Arm·AMBA·JEDEC·MIPI·PCIe·USB·코덱 표준은 어느 버전이고, 이 책 어디에 나오나? |
| [약어 사전](glossary.md) | SLC, DVFS, EAS, SMMU, CSI… 약어의 풀네임과 뜻은? |
| [계산기](calculators.md) | LPDDR 대역폭, LLM 토큰 속도, DVFS 전력, 다이 수·수율, TOPS, 화소 데이터 속도, 배터리 시간을 직접 계산하려면? |
| [참고 자료](resources.md) | 표준 원문, 제조사 자료, 커널·Android 문서, 학회와 참고서는 어디서 구하나? |

!!! basic "세대별 숫자는 한곳에"
    코어 구성·공정·메모리 속도처럼 매년 바뀌는 숫자는 본문에 흩어 쓰지 않고 [칩셋 세대 인덱스](chipset-index.md)에 **기준 시점과 출처**를 붙여 모았습니다. 회사가 공식으로 밝히지 않은 값은 "추정", 확인하지 못한 값은 "—"로 적습니다. 본문 페이지의 "세대별 …는 칩셋 세대 인덱스에 모읍니다" 문장이 이 페이지로 연결됩니다.

!!! tip "수치 검산"
    이 책의 대역폭·전력·수율·토큰 속도 수치는 모두 저장소의 `tools/soc_numbers.py` 한 곳에서 계산합니다. [계산기](calculators.md)도 같은 공식을 씁니다. 원고를 고친 뒤에는 다음 명령으로 본문에 적힌 대표 값이 계산 결과와 일치하는지 확인할 수 있습니다.

    ```bash
    python3 tools/soc_numbers.py          # LPDDR 대역폭, UFS 속도, DVFS, 다이 수·수율, LLM 속도 표 출력
    python3 tools/soc_numbers.py --check  # 본문 대표 값 검산 (불일치 시 종료 코드 1)
    ```

    예: LPDDR5X-8533 64비트 = 68.3 GB/s, 7B INT4 생성 상한 = 19.5 tok/s, 3.0 GHz·1.0 V → 1.5 GHz·0.7 V 전력 비 0.245·에너지 비 0.49, 120 mm² 다이 = 웨이퍼당 528개·수율 88.7%·양품 468개.
