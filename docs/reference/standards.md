# 표준 인덱스

!!! spec "규격 · 버전"
    Arm(아키텍처·AMBA·펌웨어 인터페이스) · JEDEC(LPDDR·UFS) · MIPI Alliance(카메라·디스플레이·저속 버스·UFS 물리 계층) · PCI-SIG · USB-IF · VESA · ITU-T/ISO/IEC·AOMedia(비디오 코덱) · Khronos(그래픽·연산 API) · 3GPP·IEEE(무선) · IEEE 1801(UPF) · ISO 26262(기능 안전)
    버전과 연도는 **이 책 본문이 다루는 범위**만 적었습니다. 표준은 계속 개정되므로 인용할 때는 문서 번호와 개정판을 함께 확인하십시오(기준 시점 2026년 10월).

!!! basic "한눈에 보기"
    SoC 하나는 수십 개의 표준이 만나는 곳입니다. 표준을 정하는 단체를 알면 문서를 어디서 찾을지 바로 알 수 있습니다.

    1. **Arm**은 명령어 집합(아키텍처), 칩 안 버스(AMBA), 전원 제어 펌웨어 인터페이스(PSCI·SCMI)를 정합니다.
    2. **JEDEC**은 메모리(LPDDR)와 저장장치(UFS)를, **MIPI Alliance**는 카메라·디스플레이·센서·PMIC 연결 같은 모바일 인터페이스를 정합니다.
    3. **PCI-SIG·USB-IF·VESA**는 고속 외부 연결과 화면 압축, **ITU-T·ISO/IEC·AOMedia**는 비디오 코덱을 정합니다.
    4. 일부 표준(MIPI 대부분, JEDEC 일부)은 회원사만 원문을 볼 수 있어, 공개된 요약·백서로 공부하게 됩니다([참고 자료](resources.md)).

## 아키텍처·인터커넥트·펌웨어 (Arm) { .l2 }

| 표준 | 주요 버전 | 내용 | 이 책 페이지 |
|---|---|---|---|
| Arm A-profile 아키텍처 (Arm ARM) | Armv8-A (AArch64) → v8.x → Armv9-A → v9.x | 명령어 집합, 예외 수준(EL0–EL3), 메모리 모델, SVE2·SME·MTE·포인터 인증 | [Arm 아키텍처](../cpu/arm-architecture.md), [컴퓨터 구조 기초](../basics/computer-architecture.md) |
| Arm SMMU 아키텍처 | SMMUv2 → SMMUv3 | 장치 DMA 주소 변환과 격리 | [메모리 보호와 IOMMU](../memory/iommu.md) |
| Arm TrustZone (아키텍처 보안 확장) | Armv8-A 이후 EL3·Secure 상태 | 일반 세계와 보안 세계 분리 | [TrustZone과 TEE](../security/trustzone.md) |
| AMBA AXI·ACE | AMBA 3 AXI → AMBA 4 AXI4·ACE·ACE-Lite → AXI5 | 칩 안 주 버스와 캐시 일관성 확장 | [버스와 인터커넥트](../basics/interconnect.md), [캐시와 일관성](../cpu/cache-coherence.md) |
| AMBA CHI | AMBA 5 CHI (여러 개정판) | 패킷 기반 일관성 프로토콜, 메시·링 인터커넥트 | [버스와 인터커넥트](../basics/interconnect.md), [메모리 컨트롤러와 SLC](../memory/controller-slc.md) |
| AMBA AHB·APB | AMBA 2 이후 | 저속 주변장치 버스 | [버스와 인터커넥트](../basics/interconnect.md) |
| PSCI (Power State Coordination Interface) | Arm DEN0022, 1.0 이후 OS 주도 모드 | 코어·클러스터 켜기·끄기·수면 요청 | [대기 전력과 저전력 상태](../power/idle.md), [파워 도메인과 게이팅](../power/power-domains.md) |
| SCMI (System Control and Management Interface) | Arm DEN0056 | 성능(DVFS)·클럭·전원 도메인·센서 제어 메시지 | [DVFS와 전력 관리](../power/dvfs.md), [클럭과 전압](../basics/clock-voltage.md), [열 관리와 스로틀링](../power/thermal.md) |
| TBBR · FF-A (참조 구현 TF-A) | — | 보안 부팅 단계(BL1–BL33), 보안 세계 파티션 인터페이스 | [부팅 과정](../security/boot.md), [TrustZone과 TEE](../security/trustzone.md) |
| PMUv3 · AMU · SPE · CoreSight | Armv8-A 이후 확장 | 성능 카운터, 통계 프로파일링, 추적·디버그 | [성능 분석 도구](../software/profiling.md), [IP와 통합](../design/ip-integration.md) |
| UCIe | 1.0 (2022) → 1.1 → 2.0 | 칩렛 사이 다이 간 연결 | [버스와 인터커넥트](../basics/interconnect.md), [패키징](../design/packaging.md) |

## 메모리·저장장치 (JEDEC) { .l2 }

| 표준 | 문서 번호 | 주요 버전 | 이 책 페이지 |
|---|---|---|---|
| LPDDR4 / LPDDR4X | JESD209-4 계열 | LPDDR4(2014), LPDDR4X(I/O 전압 하향) | [LPDDR](../memory/lpddr.md) |
| LPDDR5 / LPDDR5X | JESD209-5 계열 | LPDDR5(2019), LPDDR5X(2021, 이후 개정으로 최대 속도 확장) | [LPDDR](../memory/lpddr.md), [온디바이스 LLM](../npu/llm.md) |
| LPDDR6 | JESD209-6 | 2025 발표 | [LPDDR](../memory/lpddr.md) |
| UFS | JESD220 계열 | UFS 3.0(2018) → 3.1(2020) → 4.0(2022) → 4.1 | [UFS 저장장치](../memory/ufs.md) |
| eMMC | JESD84 계열 | 5.1 | [UFS 저장장치](../memory/ufs.md) |

## 모바일 인터페이스 (MIPI Alliance) { .l2 }

| 표준 | 계층 | 주요 버전 | 이 책 페이지 |
|---|---|---|---|
| CSI-2 | 카메라 프로토콜 | 여러 개정판 (v1.x → v4.x) | [이미지 센서 인터페이스](../media/camera-interface.md), [ISP와 카메라 파이프라인](../media/isp.md) |
| DSI / DSI-2 | 디스플레이 프로토콜 | DSI → DSI-2 (2016, C-PHY 지원) | [디스플레이 파이프라인](../media/display.md) |
| D-PHY | 물리 계층 (클럭 + 데이터 레인) | v1.0 (2009) → v2.x | [이미지 센서 인터페이스](../media/camera-interface.md) |
| C-PHY | 물리 계층 (3선 trio, 클럭 내장) | v1.0 (2014) → v2.x | [이미지 센서 인터페이스](../media/camera-interface.md), [디스플레이 파이프라인](../media/display.md) |
| M-PHY | 고속 직렬 물리 계층 | HS-G4 → M-PHY 5.0 (HS-G5) | [UFS 저장장치](../memory/ufs.md) |
| UniPro | 링크 계층 (UFS) | UniPro 2.0 (UFS 4.0) | [UFS 저장장치](../memory/ufs.md) |
| I3C / I3C Basic | 센서·카메라 제어 버스 | v1.0 (2016), I3C Basic (2018), v1.1 | [저속 주변장치 (I2C·I3C·SPI·UART)](../connectivity/low-speed.md), [센서 허브](../media/sensor-hub.md) |
| SPMI | SoC–PMIC 전원 제어 버스 | 1.0 → 2.0 | [PMIC와 전원 공급](../power/pmic.md), [저속 주변장치 (I2C·I3C·SPI·UART)](../connectivity/low-speed.md) |
| RFFE | RF 프런트엔드 제어 버스 | — | [모뎀의 통합](../connectivity/modem.md) |
| SoundWire | 오디오 코덱·앰프 연결 | 2014 발표 | [오디오와 DSP](../media/audio-dsp.md) |

## 외부 연결·디스플레이·코덱 { .l2 }

| 표준 | 기관 | 주요 버전 | 이 책 페이지 |
|---|---|---|---|
| PCI Express | PCI-SIG | 2.0 (5 GT/s) → 3.0 (8 GT/s) → 4.0 (16 GT/s) → 5.0 → 6.0 | [PCIe·USB](../connectivity/pcie-usb.md), [Wi-Fi·Bluetooth 콤보](../connectivity/wifi-bt.md) |
| USB | USB-IF | USB 2.0 · eUSB2 · USB 3.2 (Gen 1·Gen 2·Gen 2x2) · USB4 · USB Type-C · USB Power Delivery | [PCIe·USB](../connectivity/pcie-usb.md), [PMIC와 전원 공급](../power/pmic.md) |
| DisplayPort (USB-C Alt Mode) | VESA | HBR3 등 | [PCIe·USB](../connectivity/pcie-usb.md), [디스플레이 파이프라인](../media/display.md) |
| DSC (Display Stream Compression) | VESA | 1.1 → 1.2 계열 | [디스플레이 파이프라인](../media/display.md) |
| SD / SDIO | SD Association | SDIO 3.0 | [PCIe·USB](../connectivity/pcie-usb.md) |
| H.264/AVC · H.265/HEVC · H.266/VVC | ITU-T · ISO/IEC | 2003 · 2013 · 2020 | [비디오 코덱](../media/video-codec.md) |
| VP9 · AV1 | Google · AOMedia | 2013 · 2018 | [비디오 코덱](../media/video-codec.md) |
| HDR (PQ·HLG) | SMPTE ST 2084 · ITU-R BT.2100 | HDR10·HLG 및 HDR10+·Dolby Vision | [비디오 코덱](../media/video-codec.md), [디스플레이 파이프라인](../media/display.md) |
| JTAG | IEEE 1149.1 | — | [저속 주변장치 (I2C·I3C·SPI·UART)](../connectivity/low-speed.md), [시험과 양산](../design/test.md) |

## API·무선 { .l2 }

| 표준 | 기관 | 주요 버전 | 이 책 페이지 |
|---|---|---|---|
| OpenGL ES · Vulkan · SPIR-V · OpenCL | Khronos | OpenGL ES 3.2, Vulkan 1.0 (2016) → 1.4 (2024) | [그래픽 API와 드라이버](../gpu/apis.md), [GPU 연산](../gpu/compute.md) |
| 5G NR | 3GPP | Rel-15 → Rel-16 → Rel-17 (NTN) → Rel-18 (5G-Advanced) | [모뎀의 통합](../connectivity/modem.md), [GNSS·UWB·위성](../connectivity/gnss-uwb.md) |
| Wi-Fi | IEEE 802.11 · Wi-Fi Alliance | 802.11ax (Wi-Fi 6·6E) → 802.11be (Wi-Fi 7) | [Wi-Fi·Bluetooth 콤보](../connectivity/wifi-bt.md) |
| Bluetooth Core · LE Audio (LC3) | Bluetooth SIG | Core 5.x → 6.0 | [Wi-Fi·Bluetooth 콤보](../connectivity/wifi-bt.md), [오디오와 DSP](../media/audio-dsp.md) |
| UWB | IEEE 802.15.4z · FiRa | 2020 | [GNSS·UWB·위성](../connectivity/gnss-uwb.md) |

## 설계·시험·안전·소프트웨어 { .l2 }

| 표준 | 기관 | 주요 버전 | 이 책 페이지 |
|---|---|---|---|
| SystemVerilog · UVM | IEEE 1800 · IEEE 1800.2 | — | [SoC 설계 흐름](../design/flow.md), [검증과 에뮬레이션](../design/verification.md) |
| UPF (Unified Power Format) | IEEE 1801 | — | [파워 도메인과 게이팅](../power/power-domains.md), [SoC 설계 흐름](../design/flow.md) |
| IP-XACT | IEEE 1685 | 2009 → 2014 → 2022 | [IP와 통합](../design/ip-integration.md) |
| JTAG · 코어 테스트 래퍼 · IJTAG | IEEE 1149.1 · IEEE 1500 · IEEE 1687 | — | [시험과 양산](../design/test.md), [저속 주변장치 (I2C·I3C·SPI·UART)](../connectivity/low-speed.md) |
| 신뢰성 인증 | JEDEC JESD47 · AEC-Q100 (차량용) | — | [시험과 양산](../design/test.md), [차량용 SoC](../next/automotive.md) |
| 기능 안전 · 차량 사이버 보안 | ISO 26262 · ISO/SAE 21434 | ISO 26262: 2011 초판 → 2018 2판 | [차량용 SoC](../next/automotive.md) |
| TEE API · Secure Element | GlobalPlatform | TEE Client·Internal Core API | [TrustZone과 TEE](../security/trustzone.md), [하드웨어 보안 모듈](../security/secure-element.md) |
| Devicetree Specification | devicetree.org | — | [Linux 커널과 SoC 지원](../software/linux-kernel.md) |
| RISC-V ISA · 프로파일 | RISC-V International | 비특권 ISA (2019 비준), V 1.0 (2021), RVA23 (2024) | [RISC-V의 부상](../next/riscv.md) |

??? expert "전문가 노트 — 표준 원문을 다룰 때"
    **공개 범위가 다릅니다.** Arm 아키텍처 매뉴얼과 AMBA·PSCI·SCMI 문서는 Arm 개발자 사이트에서 공개로 받을 수 있습니다. JEDEC 표준은 계정을 만들면 상당수를 무료로 받을 수 있지만 일부는 유료이고, MIPI 규격 원문은 대부분 회원사 전용입니다. 그래서 MIPI 관련 숫자는 공개 백서·발표 자료와 Linux 드라이버 코드로 교차 확인하는 경우가 많습니다.

    **문서 번호 뒤의 글자가 개정판입니다.** JEDEC 문서는 JESD209-5, JESD209-5A, JESD209-5B처럼 뒤에 글자를 붙여 개정합니다. LPDDR5X처럼 "새 세대"로 불리는 것이 실제로는 기존 문서의 개정판인 경우도 있으므로, 인용할 때는 마케팅 이름보다 문서 번호와 개정 글자를 적는 편이 정확합니다.

    **SoC 사양표의 "지원"은 부분 지원일 수 있습니다.** "UFS 4.0 지원", "Vulkan 1.3 지원"이라고 해도 선택 기능 전부를 구현했다는 뜻은 아닙니다. 드라이버가 보고하는 기능 목록(예: Vulkan의 `vkGetPhysicalDeviceFeatures2`, UFS의 디스크립터)이 실제 판단 근거입니다.

## 관련 페이지

- [참고 자료](resources.md) — 표준 단체와 공식 문서 사이트
- [칩셋 세대 인덱스](chipset-index.md) — 표준이 어느 세대 칩에 들어갔는지
- [학습 로드맵](../getting-started/roadmap.md) — 규격 박스와 표준 인덱스를 활용하는 방법
- [약어 사전](glossary.md) — 표준 이름 속 약어
