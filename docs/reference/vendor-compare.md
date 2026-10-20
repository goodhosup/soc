# 제조사별 비교

!!! spec "기준 시점 · 출처"
    **기준 시점: 2026년 10월 20일**(2026년 10월까지의 공식 발표 기준이며, 막 발표된 세대의 세부는 보도에 기댄 부분이 있음) · 각 회사의 사업 보고와 제품 발표, Arm·파운드리의 공개 발표 · 소프트웨어 지원 기간은 SoC 회사가 아니라 **기기 제조사**의 공식 정책 기준
    흐름: Arm 코어 라이선스가 주류 → Apple(2012 A6부터 자체 코어, 2013 A7에서 64비트)·Qualcomm(2024 Oryon) 자체 코어 → GPU·NPU·모뎀의 자체 설계·통합 경쟁 → 3nm·2nm 세대에서 파운드리 선택이 차별점

!!! basic "한눈에 보기"
    다섯 회사는 모두 "스마트폰 두뇌"를 만들지만, 누구에게 팔고 무엇을 직접 만드는지가 다릅니다.

    1. **파는 회사**: Qualcomm과 MediaTek은 SoC를 여러 스마트폰 회사에 판매합니다. 삼성 System LSI는 주로 같은 그룹의 Galaxy에, 일부는 외부에 공급합니다.
    2. **쓰는 회사**: Apple과 Google은 자기 기기에만 넣을 칩을 직접 설계합니다. 칩 하나를 팔아서가 아니라 기기 전체로 이익을 냅니다.
    3. **직접 만드는 범위**: CPU·GPU·NPU·모뎀 가운데 무엇을 자체 설계하고 무엇을 Arm 같은 IP 회사에서 사 오는지가 회사마다 다릅니다.
    4. **생산**: 다섯 회사 모두 공장을 남(파운드리)에게 맡기거나, 삼성처럼 같은 그룹의 파운드리를 씁니다.

## 사업 모델과 생산 { .l2 }

| 항목 | Qualcomm | 삼성 System LSI | MediaTek | Apple | Google |
|---|---|---|---|---|---|
| 사업 형태 | 팹리스, SoC 외부 판매 + 특허 라이선스 | 종합 반도체 회사의 설계 사업부, 자사 기기 + 외부 공급 | 팹리스, SoC 외부 판매 | 기기 회사의 자체 칩 (외부 판매 없음) | 기기 회사의 자체 칩 (외부 판매 없음) |
| 주 고객 | 다수 Android 제조사, PC·차량 | Galaxy (지역·세대별로 Snapdragon과 혼용) | 다수 Android 제조사, TV·태블릿 | iPhone·iPad·Mac·Watch | Pixel |
| 플래그십 생산 | 주로 TSMC (888·8 Gen 1 등 일부 세대는 삼성) | 삼성 파운드리 | 주로 TSMC | TSMC | G4까지 삼성 파운드리, G5부터 TSMC |
| 제품 폭 | 플래그십 ~ 보급형 (8·7·6·4 계열) | 플래그십·중급 (2x00·1x80) | 플래그십 ~ 보급형 (9000·8000·7000 계열 등) | 연 1–2개 세대 + 이전 세대 재사용 | 연 1개 세대 |

삼성은 같은 그룹 안에 칩 설계(System LSI), 생산(파운드리), 메모리, 기기(MX)가 모두 있어, Exynos를 쓸지 Snapdragon을 쓸지는 기기 사업부가 세대마다 정합니다([주요 제조사와 생태계](../getting-started/ecosystem.md)).

## 블록별 전략 { .l2 }

| 블록 | Qualcomm | 삼성 System LSI | MediaTek | Apple | Google |
|---|---|---|---|---|---|
| CPU | Arm 코어 기반 Kryo → 2024년형부터 자체 **Oryon** (아키텍처 라이선스) | 자체 Mongoose (2019년형 Exynos 990까지) → Arm 코어 (Cortex → 2600부터 C1) | Arm 최신 코어를 빠르게 채택 | 자체 코어 (아키텍처 라이선스) | Arm 코어 (Cortex, G6는 C1 계열로 보도) |
| GPU | 자체 **Adreno** | Arm Mali → 2022년형부터 AMD RDNA 기반 **Xclipse** | Arm Mali·Immortalis | 자체 GPU (초기 세대는 PowerVR 기반) | Arm Mali (G1–G4) → Imagination PowerVR 계열 (G5부터) |
| NPU | 자체 **Hexagon** (DSP에서 출발) | 자체 NPU | 자체 APU·NPU | 자체 **Neural Engine** | 자체 **TPU** 계열 |
| 모뎀 | 자체 Snapdragon X, 플래그십 통합 | 자체 Exynos Modem, 2500까지 통합 → 2600은 외장 | 자체 모뎀, 통합 | 외장 (Qualcomm → 자체 C 시리즈로 전환 중, 2026년 iPhone 18 Pro는 C2) | 외장 (G5까지 삼성 Exynos Modem, G6는 MediaTek 모뎀으로 보도) |
| ISP | 자체 Spectra | 자체 | 자체 Imagiq | 자체 | 자체 (세부 구성은 비공개) |
| 다른 제품군 | Windows PC(Snapdragon X), 차량, XR | 차량(Exynos Auto) | Chromebook, TV, 차량 | Mac·iPad용 M 시리즈 | 데이터센터 TPU (별개 제품) |

CPU를 자체 설계하는 회사(Apple, Qualcomm)는 코어 폭·캐시 구조를 마음대로 정할 수 있는 대신 설계 인력과 기간이 크게 듭니다. Arm 코어를 쓰는 회사는 Arm의 연간 로드맵에 맞춰 빠르게 신제품을 낼 수 있고, 차별화는 클러스터 구성·클럭·캐시·GPU·NPU에서 합니다([자체 설계 코어](../cpu/custom-cores.md), [Arm 코어 계보](../cpu/arm-cores.md)).

## 소프트웨어 지원 { .l2 }

SoC 회사는 커널·드라이버·펌웨어를 기기 제조사에 공급하고, 실제 업데이트 약속은 **기기 제조사**가 합니다. 아래는 플래그십 기기 기준의 공식 정책입니다.

| 회사 | 기기 업데이트 정책 (공식 발표 기준) | SoC 측 지원 |
|---|---|---|
| Qualcomm | — (기기 제조사가 결정) | 2025년 2월 Google과 함께, Android 15로 출시되는 Snapdragon 8 Elite 기기부터 최대 8년간 Android OS·보안 업데이트를 제공할 수 있도록 지원한다고 발표 (실제 적용은 기기 제조사 결정) |
| 삼성 | Galaxy S24 시리즈부터 7년 OS·보안 업데이트 | Exynos BSP를 자사 기기에 직접 공급 |
| MediaTek | — (기기 제조사가 결정) | BSP를 고객사에 공급, 기간은 고객 계약에 따름 |
| Apple | OS 업데이트 기간은 명시하지 않음. 영국 PSTI 규정 신고에서 iPhone 15 계열은 최초 출시일로부터 최소 5년 보안 업데이트를 밝힘 | 칩·OS·기기 모두 자사 |
| Google | Pixel 8 시리즈부터 7년 OS·보안 업데이트 | Tensor BSP를 자사가 관리 |

업데이트 기간을 늘리려면 SoC 회사가 오래된 칩의 커널·드라이버를 새 Android 버전에 맞춰 계속 유지해야 합니다. Android의 GKI(Generic Kernel Image)와 벤더 모듈 분리는 이 부담을 줄이기 위한 구조입니다([Android BSP 구조](../software/android-bsp.md), [Linux 커널과 SoC 지원](../software/linux-kernel.md)).

??? expert "전문가 노트 — 비교표를 읽는 요령, 공개 정보의 차이, 같은 회사의 세대 차"
    **"자체 설계"의 범위.** 자체 GPU라도 셰이더 컴파일러·드라이버까지 자체인지, 일부 IP를 사 와서 고친 것인지는 회사마다 다릅니다. 예를 들어 Xclipse는 AMD의 GPU 아키텍처를 라이선스해 삼성이 SoC에 통합한 형태이고, Apple GPU는 초기 PowerVR 기반에서 자체 설계로 옮겨 갔습니다. "자체" 여부보다 **누가 드라이버를 유지하는가**가 실무에서는 더 중요합니다([그래픽 API와 드라이버](../gpu/apis.md)).

    **공개 정보 수준의 차이.** Qualcomm·MediaTek은 외부 고객에게 팔아야 하므로 제품 소개 자료에 코어 구성·메모리·모뎀 사양을 비교적 자세히 공개합니다. Apple과 Google은 기기 사양 위주로만 밝혀, 코어 이름·공정·메모리 종류는 분해 분석에 기대게 됩니다. 이 책의 [칩셋 세대 인덱스](chipset-index.md)가 Apple·Tensor 행에 "추정"을 많이 붙인 이유입니다.

    **모뎀 통합은 전력과 면적의 문제.** 모뎀을 SoC에 넣으면 칩 사이 링크와 별도 패키지가 사라져 전력·면적에 유리하지만, 다이가 커지고 모뎀 세대를 SoC와 같은 주기로 바꿔야 합니다. Apple·Google이 외장 모뎀을 쓰는 것은 SoC에 함께 넣을 자체 모뎀 IP가 없었거나(Google), 최근에야 갖추기 시작한(Apple) 사정과 관련이 깊습니다. 반대로 자체 모뎀이 있는 삼성도 2nm 첫 세대인 Exynos 2600에서는 모뎀을 별도 칩으로 뺐습니다. 이 경우 모뎀(Exynos Modem 5410)은 SoC와 다른 4nm 공정으로 만들어집니다([모뎀의 통합](../connectivity/modem.md)).

    **한 회사 안에서도 세대마다 바뀝니다.** Snapdragon의 생산 파운드리, Exynos의 GPU 공급원과 모뎀 통합 여부, Tensor의 파운드리·GPU·모뎀 공급원은 모두 최근 몇 세대 사이에 바뀌었습니다. 회사 이름만으로 특성을 단정하지 말고 세대를 함께 확인합니다.

## 관련 페이지

- [주요 제조사와 생태계](../getting-started/ecosystem.md) — 회사와 IP·파운드리의 관계를 이야기 형식으로
- [칩셋 세대 인덱스](chipset-index.md) — 세대별 구체 사양
- [파운드리와 공정](../design/foundry.md) — 생산 파운드리 선택의 배경
- [벤치마크 읽는 법](../software/benchmarks.md) — 회사 간 성능 비교를 할 때의 주의
