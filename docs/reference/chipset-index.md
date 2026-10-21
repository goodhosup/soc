# 칩셋 세대 인덱스

!!! spec "기준 시점 · 출처"
    **기준 시점: 2026년 10월 20일.** 2026년 10월까지 공식 발표된 세대(Snapdragon 8 Elite Gen 6, Dimensity 9600 Pro, A20 Pro, Tensor G6 등)까지 넣었습니다. 막 발표된 세대는 세부 사양이 아직 다 공개되지 않아 "—"나 "추정"이 많습니다. 최신 값은 각 회사의 제품 소개 자료(product brief)로 확인하십시오.
    값은 **회사 공식 발표** 기준입니다. 회사가 공개하지 않아 분해 분석·보도에서 나온 값은 "추정", 확인하지 못한 값은 "—"로 적었습니다. 확신이 없는 세대는 행을 넣지 않았습니다.

!!! basic "한눈에 보기"
    본문 페이지는 특정 칩의 숫자를 거의 쓰지 않고 이 페이지로 연결합니다. 숫자는 매년 바뀌지만 원리는 오래가기 때문입니다.

    1. **세대 이름**은 마케팅 이름입니다. 부품 번호(예: SM8550)와의 관계는 [칩셋 이름 읽는 법](../getting-started/naming.md)을 참고하십시오.
    2. **공정**은 생산 파운드리와 회사가 부르는 노드 이름입니다. 같은 "4nm"라도 회사마다 실제 치수와 성능이 다릅니다([공정 노드와 미세화](../basics/process-node.md)).
    3. **CPU 구성**은 "코어 종류 × 개수"입니다. 코어 이름은 Arm 코어(Cortex·C1 계열) 또는 회사 자체 코어입니다([이기종 클러스터](../cpu/clusters.md)).
    4. **LPDDR**는 지원하는 최고 세대와, 공개된 경우 최대 데이터 레이트입니다. 대역폭은 [계산기](calculators.md)로 바로 환산할 수 있습니다.

표 읽는 법: 연도는 **발표 연도**이며, 탑재 기기는 대개 발표 직후부터 다음 해 초 사이에 나옵니다. 클럭은 같은 칩도 기기에 따라 다르게 쓰여 이 표에서 뺐습니다. Qualcomm은 LPDDR5X까지의 메모리 속도를 MHz로 발표하므로 MT/s는 그 2배로 환산했습니다. LPDDR6는 환산 방식이 달라 발표 표기를 그대로 적었습니다.

## Qualcomm Snapdragon 8 계열 { .l2 }

| 칩셋 | 발표 | 공정 | CPU 구성 | GPU | LPDDR | 모뎀 |
|---|---|---|---|---|---|---|
| Snapdragon 865 | 2019 | TSMC 7nm (N7P) | Cortex-A77 기반 Kryo 585: 1 + 3 (A77) + 4 (A55) | Adreno 650 | LPDDR5 5500 MT/s, LPDDR4X | 외장 (Snapdragon X55) |
| Snapdragon 888 | 2020 | 삼성 5nm (5LPE) | 1 × Cortex-X1 + 3 × A78 + 4 × A55 | Adreno 660 | LPDDR5 6400 MT/s | 통합 (X60) |
| Snapdragon 8 Gen 1 | 2021 | 삼성 4nm | 1 × Cortex-X2 + 3 × A710 + 4 × A510 | Adreno 730 | LPDDR5 6400 MT/s | 통합 (X65) |
| Snapdragon 8+ Gen 1 | 2022 | TSMC 4nm (N4) | 8 Gen 1과 같은 구성 | Adreno 730 | LPDDR5 6400 MT/s | 통합 (X65) |
| Snapdragon 8 Gen 2 | 2022 | TSMC 4nm (N4) | 1 × Cortex-X3 + 2 × A715 + 2 × A710 + 3 × A510 | Adreno 740 | LPDDR5X 8400 MT/s | 통합 (X70) |
| Snapdragon 8 Gen 3 | 2023 | TSMC 4nm (N4P) | 1 × Cortex-X4 + 5 × A720 + 2 × A520 | Adreno 750 | LPDDR5X 9600 MT/s | 통합 (X75) |
| Snapdragon 8 Elite | 2024 | TSMC 3nm (N3E, 추정) | 자체 Oryon 2세대: 2 (Prime) + 6 (Performance) | Adreno 830 | LPDDR5X 10600 MT/s | 통합 (X80) |
| Snapdragon 8 Elite Gen 5 | 2025 | TSMC 3nm (N3P, 추정) | 자체 Oryon 3세대: 2 (Prime) + 6 (Performance) | Adreno 840 | LPDDR5X 10600 MT/s | 통합 (X85) |
| Snapdragon 8 Elite Gen 6 | 2026 | 2nm (TSMC N2P, 추정) | 자체 Oryon: 2 (Prime) + 6 (Performance) | Adreno (번호 비공개) | LPDDR6 / LPDDR5X (최대 5300 MHz 표기) | 통합 (X105) |
| Snapdragon 8 Elite Extreme Gen 6 | 2026 | 2nm (TSMC N2P, 추정) | 자체 Oryon: 2 (Prime) + 6 (Performance) | Adreno (행렬 코어 추가, 번호 비공개) | LPDDR6 / LPDDR5X (최대 5300 MHz 표기) | 통합 (X105) |

Snapdragon 8 Elite부터 CPU가 Arm 코어 기반 Kryo에서 자체 설계 Oryon으로 바뀌었고, 효율 코어 클러스터가 사라졌습니다([자체 설계 코어](../cpu/custom-cores.md)). Qualcomm은 공정을 "3nm"·"2nm"처럼 숫자로만 밝히는 경우가 많아, 괄호 안 TSMC 세부 노드 이름(N3E·N3P·N2P)은 보도 기준입니다. 8 Elite Gen 5·Gen 6 제품 소개 자료는 GPU를 "Adreno GPU"로만 적으며, 표의 840 같은 번호는 기기 정보·보도에서 쓰는 이름입니다. 2026년 세대는 일반형(8 Elite Gen 6)과 최상위형(8 Elite Extreme Gen 6) 두 가지로 나뉘었고, CPU 구성은 같으며 GPU·NPU 쪽이 다릅니다. 865는 5G 모뎀이 외장인 마지막 Snapdragon 8 계열 플래그십입니다([모뎀의 통합](../connectivity/modem.md)).

## Samsung Exynos 플래그십 { .l2 }

| 칩셋 | 발표 | 공정 | CPU 구성 | GPU | LPDDR | 모뎀 |
|---|---|---|---|---|---|---|
| Exynos 990 | 2019 | 삼성 7nm EUV (7LPP) | 2 × 자체 Mongoose M5 + 2 × Cortex-A76 + 4 × A55 | Mali-G77 MP11 | LPDDR5 | 외장 (Exynos Modem 5123) |
| Exynos 2100 | 2021 | 삼성 5nm (5LPE) | 1 × Cortex-X1 + 3 × A78 + 4 × A55 | Mali-G78 MP14 | LPDDR5 | 통합 |
| Exynos 2200 | 2022 | 삼성 4nm | 1 × Cortex-X2 + 3 × A710 + 4 × A510 | Xclipse 920 (AMD RDNA 2 기반) | LPDDR5 | 통합 |
| Exynos 2400 | 2023 | 삼성 4nm | 1 × Cortex-X4 + 5 × A720 + 4 × A520 (10코어) | Xclipse 940 (AMD RDNA 3 기반) | LPDDR5X | 통합 |
| Exynos 2500 | 2025 | 삼성 3nm GAA | 1 × Cortex-X925 + 7 × A725 + 2 × A520 (10코어) | Xclipse 950 (AMD RDNA 기반) | LPDDR5X | 통합 |
| Exynos 2600 | 2025 | 삼성 2nm GAA | 1 × C1-Ultra + 3 × C1-Pro + 6 × C1-Pro (10코어) | Xclipse 960 (AMD RDNA 기반) | LPDDR5X | 외장 (Exynos Modem 5410) |

Exynos 990은 자체 CPU 코어(Mongoose)를 쓴 마지막 세대이고, 2200부터 GPU가 Mali에서 AMD RDNA 기반 Xclipse로 바뀌었습니다. 2023년 초 출시된 Galaxy S23 시리즈는 전 지역에 Snapdragon을 탑재해, 2200(2022년 1월 발표)과 2400(2023년 10월 발표) 사이에는 Galaxy S용 Exynos 플래그십이 없었습니다. Exynos 2600은 2nm GAA 공정의 첫 Exynos이며, 패키지 안에 구리 방열 블록(HPB)을 넣었고, 2100 이후 처음으로 5G 모뎀을 SoC에 넣지 않고 별도 칩(Exynos Modem 5410)으로 분리했습니다([모뎀의 통합](../connectivity/modem.md)).

## MediaTek Dimensity 플래그십 { .l2 }

| 칩셋 | 발표 | 공정 | CPU 구성 | GPU | LPDDR | 모뎀 |
|---|---|---|---|---|---|---|
| Dimensity 1000 | 2019 | TSMC 7nm | 4 × Cortex-A77 + 4 × A55 | Mali-G77 MC9 | LPDDR4X 4266 MT/s | 통합 |
| Dimensity 9000 | 2021 | TSMC 4nm (N4) | 1 × Cortex-X2 + 3 × A710 + 4 × A510 | Mali-G710 MC10 | LPDDR5X 7500 MT/s | 통합 |
| Dimensity 9200 | 2022 | TSMC 4nm (N4P) | 1 × Cortex-X3 + 3 × A715 + 4 × A510 | Immortalis-G715 MC11 | LPDDR5X 8533 MT/s | 통합 |
| Dimensity 9300 | 2023 | TSMC 4nm (N4P) | 4 × Cortex-X4 + 4 × A720 (효율 코어 없음) | Immortalis-G720 MC12 | LPDDR5T 9600 MT/s | 통합 |
| Dimensity 9400 | 2024 | TSMC 3nm (N3E) | 1 × Cortex-X925 + 3 × X4 + 4 × A720 | Immortalis-G925 MC12 | LPDDR5X 10667 MT/s | 통합 |
| Dimensity 9500 | 2025 | TSMC 3nm (N3P) | 1 × C1-Ultra + 3 × C1-Premium + 4 × C1-Pro | Mali-G1-Ultra MC12 | LPDDR5X 10667 MT/s | 통합 |
| Dimensity 9600 Pro | 2026 | TSMC 2nm (N2P, 추정) | 2 × C2-Ultra + 6 × C2-Pro (3 + 3, 클럭 다름) | G2-Ultra NX | LPDDR6 | 통합 |

Dimensity 9300은 Android 플래그십 가운데 효율 코어(A5xx) 없이 큰 코어만으로 구성한 초기 사례입니다. 2026년 세대는 이름에 "Pro"가 붙은 9600 Pro가 최상위이고, MediaTek은 LPDDR6 지원을 이 칩에서 처음 발표했습니다. LPDDR5T는 SK hynix가 고속 LPDDR5X 계열 제품에 붙인 이름이며, 별도의 JEDEC 세대 이름은 아닙니다.

## Apple A 시리즈 { .l2 }

Apple은 코어 이름·메모리 종류·정확한 공정 이름을 공식으로 밝히지 않는 경우가 많습니다. 아래 표의 "P"는 고성능 코어, "E"는 고효율 코어이며, 괄호 안 공정 이름과 LPDDR 종류는 분해 분석·보도 기준의 **추정**입니다.

| 칩셋 | 발표 | 공정 | CPU 구성 | GPU | LPDDR | 모뎀 |
|---|---|---|---|---|---|---|
| A13 Bionic | 2019 | TSMC 7nm (N7P, 추정) | 2P + 4E | 자체 4코어 | LPDDR4X (추정) | 외장 |
| A14 Bionic | 2020 | TSMC 5nm (N5, 추정) | 2P + 4E | 자체 4코어 | LPDDR4X (추정) | 외장 |
| A15 Bionic | 2021 | TSMC 5nm (N5P, 추정) | 2P + 4E | 자체 4코어 / 5코어 (Pro 모델) | LPDDR4X (추정) | 외장 |
| A16 Bionic | 2022 | TSMC 4nm (N4, 추정) | 2P + 4E | 자체 5코어 | LPDDR5 (추정) | 외장 |
| A17 Pro | 2023 | TSMC 3nm (N3B, 추정) | 2P + 4E | 자체 6코어 (하드웨어 레이 트레이싱) | LPDDR5 (추정) | 외장 |
| A18 / A18 Pro | 2024 | TSMC 3nm (N3E, 추정) | 2P + 4E | 자체 5코어 / 6코어 | LPDDR5X (추정) | 외장 |
| A19 / A19 Pro | 2025 | TSMC 3nm (N3P, 추정) | 2P + 4E | 자체 5코어 / 6코어 (iPhone Air의 A19 Pro는 5코어) | LPDDR5X (추정) | 외장 |
| A20 Pro | 2026 | 2nm (TSMC N2, 분해 분석 보도) | 2P + 4E | 자체 7코어 | LPDDR5X (96비트, 분해 분석 초기 보도) | 외장 (자체 C2) |

Apple은 이 표의 모든 세대에서 2P + 4E 구성을 유지하며 코어 자체를 키워 왔습니다. Apple이 직접 밝힌 공정은 "5나노"(A14·A15), "4나노"(A16), "3나노"(A17 Pro), "2세대 3나노"(A18), "2나노"(A20 Pro) 같은 숫자 수준이며, TSMC 세부 노드 이름은 보도 기준입니다. 모뎀은 SoC 밖의 별도 칩이며, 공급원은 Qualcomm에서 자체 C 시리즈로 옮겨 가고 있습니다(2025년 iPhone Air의 C1X, 2026년 iPhone 18 Pro의 C2). A20 Pro는 A10부터 이어 온 InFO-PoP(SoC 위에 DRAM 적층)를 버리고 다이와 DRAM을 나란히 놓는 패키지로 바꿨습니다(Apple 발표, [패키징](../design/packaging.md#모바일-패키지의-방열-경쟁)).

## Google Tensor { .l2 }

Google은 CPU 코어 구성 일부만 공식으로 밝혀 왔습니다. 아래 CPU·GPU 구성은 Google 발표와 공개 분석을 함께 본 값이며, 회사가 직접 밝히지 않은 항목은 **추정**으로 읽으십시오.

| 칩셋 | 발표 | 공정 | CPU 구성 | GPU | LPDDR | 모뎀 |
|---|---|---|---|---|---|---|
| Tensor (G1) | 2021 | 삼성 5nm | 2 × Cortex-X1 + 2 × A76 + 4 × A55 | Mali-G78 MP20 | LPDDR5 | 외장 (삼성) |
| Tensor G2 | 2022 | 삼성 5nm | 2 × Cortex-X1 + 2 × A78 + 4 × A55 | Mali-G710 MP7 | LPDDR5 | 외장 (삼성) |
| Tensor G3 | 2023 | 삼성 4nm | 1 × Cortex-X3 + 4 × A715 + 4 × A510 (9코어) | Mali-G715 계열 (추정) | LPDDR5X | 외장 (삼성) |
| Tensor G4 | 2024 | 삼성 4nm | 1 × Cortex-X4 + 3 × A720 + 4 × A520 | Mali-G715 계열 (추정) | LPDDR5X | 외장 (삼성) |
| Tensor G5 | 2025 | TSMC 3nm (N3E, 추정) | 1 × Cortex-X4 + 5 × A725 + 2 × A520 (추정) | Imagination PowerVR DXT-48-1536 (추정) | LPDDR5X | 외장 (삼성) |
| Tensor G6 | 2026 | TSMC 3nm (N3P, 추정) | 1 × C1-Ultra + 4 × C1-Pro + 2 × C1-Pro (7코어, 추정) | Imagination PowerVR 계열 (추정) | — | 외장 (MediaTek, 추정) |

Tensor는 G4까지 삼성과 공동 개발·삼성 파운드리 생산이었고, G5부터 Google 주도 설계·TSMC 생산으로 바뀌었습니다. Google이 직접 밝힌 공정은 "TSMC 3nm"(G5는 블로그, G6는 Google 하드웨어 임원 인터뷰)까지입니다. G6의 모뎀은 FCC 인증 문서와 보도에서 MediaTek 제품으로 알려졌지만 Google이 공식으로 밝히지는 않았습니다([주요 제조사와 생태계](../getting-started/ecosystem.md)).

??? expert "전문가 노트 — 이 표를 쓸 때 주의할 점"
    **같은 이름, 다른 칩.** 같은 세대에도 클럭만 올린 변형(예: "for Galaxy" 판), 코어 수를 줄인 변형, 지역별로 다른 칩을 쓰는 기기가 있습니다. 측정이나 비교를 할 때는 기기의 부품 번호(`ro.board.platform`, 디바이스 트리 `compatible`)로 실제 칩을 확인합니다([칩셋 이름 읽는 법](../getting-started/naming.md)).

    **공정 이름은 상표에 가깝습니다.** "3nm"는 어떤 구조의 실제 치수가 아니며, 같은 파운드리 안에서도 N3B·N3E·N3P처럼 설계 규칙이 다른 변형이 있습니다. 서로 다른 파운드리의 같은 숫자 노드를 같은 성능으로 보면 안 됩니다([파운드리와 공정](../design/foundry.md)).

    **메모리 속도는 "지원 최대"입니다.** 표의 LPDDR 속도는 SoC 메모리 컨트롤러가 지원하는 최대값이고, 실제 기기는 그보다 낮은 속도의 DRAM을 쓰기도 합니다. 반대로 같은 SoC라도 출시 시점에 따라 더 빠른 DRAM을 붙인 기기가 나오기도 합니다.

    **GPU 코어 수는 비교 단위가 아닙니다.** Mali의 MC 수, Apple GPU 코어 수, Adreno 내부 구성은 단위 크기가 서로 달라서 숫자끼리 비교할 수 없습니다([주요 GPU 계열](../gpu/families.md)).

## 출처

2026년 10월 20일에 다시 확인했습니다. 회사 사이트 주소는 바뀔 수 있으므로 이름으로도 찾을 수 있게 적었습니다.

- Qualcomm: Snapdragon 865 / 888 / 8 Gen 1 / 8+ Gen 1 / 8 Gen 2 / 8 Gen 3 / 8 Elite / 8 Elite Gen 5 / 8 Elite Gen 6 / 8 Elite Extreme Gen 6 Mobile Platform 제품 소개 자료(Product Brief)
    - Snapdragon 8 Elite Product Brief — <https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Platform-Product-Brief.pdf>
    - Snapdragon 8 Elite Gen 5 Product Brief — <https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Gen-5-product-brief.pdf>
    - Snapdragon 8 Elite Gen 6 Product Brief — <https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Gen-6-Product-Brief.pdf>
    - Snapdragon 8 Elite Extreme Gen 6 Product Brief — <https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Extreme-Gen-6-Product-Brief.pdf>
- Samsung Semiconductor: Exynos 990 / 2100 / 2200 / 2400 / 2500 / 2600 제품 페이지와 발표 자료
    - Exynos 2500 — <https://semiconductor.samsung.com/processor/mobile-processor/exynos-2500/>
    - Exynos 2600 — <https://semiconductor.samsung.com/processor/mobile-processor/exynos-2600/>
- MediaTek: Dimensity 1000 / 9000 / 9200 / 9300 / 9400 / 9500 / 9600 Pro 제품 페이지와 발표 자료
    - Dimensity 9500 — <https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500>
    - Dimensity 9600 Pro — <https://www.mediatek.com/products/smartphones/mediatek-dimensity-9600-pro>
- Apple: 각 연도 iPhone 발표 보도 자료(Newsroom)와 iPhone 기술 사양 페이지
    - iPhone Air 기술 사양(A19 Pro 5코어 GPU, C1X) — <https://www.apple.com/iphone-air/specs/>
    - Apple debuts iPhone 18 Pro and iPhone 18 Pro Max (2026-09) — <https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/>
- Google: 각 연도 Pixel 발표 자료와 Tensor 소개 블로그
    - 5 reasons why Google Tensor G5 is a game-changer for Pixel (2025-08) — <https://blog.google/products-and-platforms/devices/pixel/tensor-g5-pixel-10/>
    - Google introduces Pixel 11, Pixel 11 Pro and Pixel 11 Pro XL (2026-08) — <https://blog.google/products-and-platforms/devices/pixel/google-pixel-11-pro-xl/>
- Arm: Cortex-A·X 및 C1 CPU, Mali·Immortalis GPU 제품 발표 자료
- 추정 값: 공개 분해 분석(다이 사진·패키지 분석)과 기술 매체 보도(Exynos 2600 외장 모뎀, Tensor G5·G6 CPU·GPU 구성, Tensor G6 모뎀, A20 Pro 공정·메모리 인터페이스 등)
    - TechInsights 분해 분석 보도(A20 Pro TSMC N2·WMCM 패키지, 2026-09) — <https://www.techtimes.com/articles/327936/20260923/techinsights-teardown-confirms-tsmc-2nm-nanosheet-transistors-now-inside-iphone-18-pro.htm>

## 관련 페이지

- [모바일 SoC의 역사](../getting-started/history.md) — 이 표의 세대들이 나온 흐름
- [제조사별 비교](vendor-compare.md) — 회사별 전략을 한 표에서
- [Arm 코어 계보](../cpu/arm-cores.md) — 표에 나오는 Cortex·C1 코어의 차이
- [LPDDR](../memory/lpddr.md) — 메모리 세대와 대역폭 계산
- [계산기](calculators.md) — 표의 LPDDR 속도를 대역폭으로 환산
