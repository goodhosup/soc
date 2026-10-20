# 참고 자료

!!! spec "규격 · 버전"
    표준 단체: Arm · JEDEC · MIPI Alliance · PCI-SIG · USB-IF · VESA · Khronos · 3GPP · IEEE · 제조사 개발자 포털과 오픈소스 프로젝트 문서 (주소는 2026년 기준 대표 도메인만 적었습니다. 세부 문서 위치는 자주 바뀌므로 사이트 안에서 문서 이름으로 검색하십시오)
    Arm 아키텍처·AMBA 문서와 Linux·Android 문서는 공개 · JEDEC은 계정 등록 후 상당수 무료 · MIPI 규격 원문은 대부분 회원사 전용

!!! basic "한눈에 보기"
    SoC 공부에 쓰는 1차 자료는 크게 다섯 가지입니다.

    1. **표준 문서** — 아키텍처, 메모리, 인터페이스 규격의 원문
    2. **제조사 자료** — 제품 소개 자료(product brief)와 개발자 문서
    3. **오픈소스 코드와 문서** — Linux 커널, Android, 펌웨어. 칩이 실제로 어떻게 움직이는지 가장 구체적으로 보여 줍니다
    4. **학회 발표** — Hot Chips, ISSCC 같은 학회에서 회사가 직접 설계를 설명합니다
    5. **참고서** — 컴퓨터 구조, 회로, 메모리의 기초를 잡는 교과서

## 표준 단체와 공식 문서 { .l2 }

| 기관 | 주소 | 이 책에서 쓰는 문서 |
|---|---|---|
| Arm Developer | <https://developer.arm.com/> | Arm Architecture Reference Manual, AMBA AXI·CHI, PSCI, SCMI, SMMU, 코어별 Technical Reference Manual ([표준 인덱스](standards.md)) |
| Arm Learning Paths | <https://learn.arm.com/> | 성능 분석·최적화 실습 문서 |
| JEDEC | <https://www.jedec.org/> | LPDDR(JESD209 계열), UFS(JESD220 계열), 신뢰성 시험 |
| MIPI Alliance | <https://www.mipi.org/> | CSI-2, DSI-2, D-PHY, C-PHY, I3C, SPMI, M-PHY, UniPro 개요와 백서 |
| PCI-SIG | <https://pcisig.com/> | PCI Express 규격 |
| USB-IF | <https://www.usb.org/> | USB 2.0·3.2·USB4, Type-C, Power Delivery |
| VESA | <https://vesa.org/> | DisplayPort, DSC |
| Khronos Group | <https://www.khronos.org/> | Vulkan, OpenGL ES, SPIR-V, OpenCL 규격과 레지스트리 |
| 3GPP | <https://www.3gpp.org/> | 5G NR 릴리스 규격 |
| IEEE Standards / IEEE Xplore | <https://standards.ieee.org/> · <https://ieeexplore.ieee.org/> | IEEE 1801(UPF), 1149.1(JTAG), 802.11, 학회 논문 |
| RISC-V International | <https://riscv.org/> | RISC-V ISA·프로파일 규격 |
| devicetree.org | <https://www.devicetree.org/> | Devicetree Specification |

## 제조사 자료 { .l2 }

| 회사 | 주소 | 볼 만한 자료 |
|---|---|---|
| Qualcomm | <https://www.qualcomm.com/> | Snapdragon 제품 소개 자료(Product Brief), 개발자 문서(Snapdragon Profiler, AI Engine Direct) |
| Samsung Semiconductor | <https://semiconductor.samsung.com/> | Exynos 제품 페이지, 파운드리 공정 발표, LPDDR·UFS 제품 정보 |
| MediaTek | <https://www.mediatek.com/> | Dimensity 제품 페이지, NeuroPilot 개발자 자료 |
| Apple Developer | <https://developer.apple.com/> | Metal, Core ML 문서, Apple Platform Security 가이드 |
| Google | <https://blog.google/> · <https://developer.android.com/> | Tensor 소개 글, Android 개발자 문서(성능·AI·Vulkan) |
| TSMC | <https://www.tsmc.com/> | 공정 기술 발표(Technology Symposium 요약) |

## 오픈소스와 플랫폼 문서 { .l2 }

| 자료 | 주소 | 내용 |
|---|---|---|
| Linux 커널 문서 | <https://www.kernel.org/doc/html/latest/> | cpufreq·cpuidle·thermal·devfreq·interconnect·IOMMU 등 프레임워크 설명, 디바이스 트리 바인딩 ([Linux 커널과 SoC 지원](../software/linux-kernel.md)) |
| Linux 커널 소스 | <https://git.kernel.org/> | `arch/arm64/boot/dts/` 아래 벤더별 디바이스 트리, `drivers/` 아래 SoC 드라이버 |
| Android 소스·플랫폼 문서 | <https://source.android.com/> | GKI, Treble, HAL, Verified Boot, 전력·열 관리 ([Android BSP 구조](../software/android-bsp.md)) |
| Trusted Firmware | <https://www.trustedfirmware.org/> | TF-A(부팅·PSCI 구현), OP-TEE ([부팅 과정](../security/boot.md)) |
| Linaro | <https://www.linaro.org/> | Arm SoC 업스트림 지원, 96Boards ([개발 보드로 실습](../software/dev-boards.md)) |
| Perfetto | <https://perfetto.dev/> | Android·Linux 시스템 추적 도구 ([성능 분석 도구](../software/profiling.md)) |
| Mesa 3D | <https://www.mesa3d.org/> | 오픈소스 GPU 드라이버(Adreno용 Freedreno·Turnip, Mali용 Panfrost·PanVK 등) |

## 학회와 참고서 { .l2 }

**학회·발표**

| 자료 | 주소 | 내용 |
|---|---|---|
| Hot Chips | <https://hotchips.org/> | 회사가 직접 발표하는 칩 구조 — CPU·GPU·NPU·SoC 설계의 1차 자료 |
| ISSCC | <https://www.isscc.org/> | 회로 수준 발표 — SRAM, PLL, 전원 회로, DRAM 인터페이스 |
| VLSI Symposium · IEDM | IEEE 학회 | 공정·소자 기술 발표 |
| ISCA · MICRO · HPCA | 컴퓨터 구조 학회 | 마이크로아키텍처·메모리 시스템 연구 |
| Linux Plumbers Conference · Linaro Connect | 각 행사 사이트 | 커널 전력 관리·스케줄러·SoC 지원 논의 |

**참고서**

| 책 | 저자 | 다루는 범위 |
|---|---|---|
| *Computer Architecture: A Quantitative Approach* | John L. Hennessy, David A. Patterson | 파이프라인, 캐시, 메모리 계층, 도메인 특화 가속기 |
| *Computer Organization and Design* (ARM Edition) | David A. Patterson, John L. Hennessy | Arm 명령어 기반 컴퓨터 구조 입문 |
| *CMOS VLSI Design* | Neil Weste, David Harris | CMOS 회로, 전력, 타이밍, 설계 흐름 |
| *Memory Systems: Cache, DRAM, Disk* | Bruce Jacob, Spencer Ng, David Wang | DRAM 동작과 메모리 컨트롤러 |
| *A Primer on Memory Consistency and Cache Coherence* | Vijay Nagarajan, Daniel J. Sorin, Mark D. Hill, David A. Wood | 일관성 프로토콜과 메모리 모델 |
| *Efficient Processing of Deep Neural Networks* | Vivienne Sze, Yu-Hsin Chen, Tien-Ju Yang, Joel S. Emer | NPU 데이터 흐름, 정밀도, 에너지 |

??? expert "전문가 노트 — 자료를 고르고 교차 확인하는 법"
    **1차 자료 우선.** 리뷰 기사와 커뮤니티 글은 빠르지만, 같은 숫자가 출처 없이 옮겨 다니면서 틀린 값이 굳어지기도 합니다. 칩 사양은 제조사 제품 소개 자료로, 동작 원리는 표준 원문과 학회 발표로, 실제 동작은 커널 소스로 확인합니다.

    **커널 소스는 공개된 사양서입니다.** 디바이스 트리에는 클러스터 구성, OPP(클럭·전압 표), 인터커넥트 경로, 전원 도메인 이름이 그대로 들어 있습니다. 회사가 공개하지 않은 구성을 확인할 때 가장 믿을 만한 공개 자료인 경우가 많습니다. 다만 업스트림에 올라간 값과 실제 출하 기기의 값은 다를 수 있습니다.

    **발표 자료의 비교 기준을 확인합니다.** "이전 세대 대비 30% 향상" 같은 수치는 비교 대상, 같은 전력인지 같은 클럭인지, 어떤 작업인지에 따라 뜻이 달라집니다. 이 책은 그런 수치를 옮길 때 기준을 함께 적거나 쓰지 않습니다([벤치마크 읽는 법](../software/benchmarks.md)).

    **자매 핸드북.** 무선 연결을 더 깊이 보려면 [Bluetooth 핸드북](https://goodhosup.github.io/bluetooth/), [Wi-Fi 핸드북](https://goodhosup.github.io/wifi/), [셀룰러 핸드북](https://goodhosup.github.io/cellular/)을 참고하십시오.

## 관련 페이지

- [표준 인덱스](standards.md) — 표준별 버전과 이 책 페이지
- [칩셋 세대 인덱스](chipset-index.md) — 제조사 자료에서 모은 세대별 사양
- [학습 로드맵](../getting-started/roadmap.md) — 무엇부터 읽을지
- [성능 분석 도구](../software/profiling.md) — 도구 사용법
