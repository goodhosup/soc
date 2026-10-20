# 약어 사전

!!! basic "이 페이지의 용도"
    핸드북에서 쓰는 약어를 알파벳순으로 정리했습니다. 이 표는 사이트 전체 **약어 툴팁**의 원본이기도 합니다(`tools/gen_abbreviations.py`가 이 표에서 `includes/abbreviations.md`를 생성). 뜻이 여러 개인 약어는 툴팁에서 제외하고 아래 별도 표에만 적었습니다. 집필이 진행되면서 계속 추가합니다.

| 약어 | 풀네임 | 설명 |
|---|---|---|
| AABB | Axis-Aligned Bounding Box | 좌표축에 나란한 경계 상자 |
| ACE | AXI Coherency Extensions | AMBA 4의 캐시 일관성 확장 |
| ADC | Analog-to-Digital Converter | 아날로그 값을 디지털로 바꾸는 변환기 |
| ADPF | Android Dynamic Performance Framework | 앱이 성능 목표를 시스템에 알리는 Android API |
| AFBC | Arm Frame Buffer Compression | Arm의 무손실 프레임버퍼 압축 |
| AICore | Android AICore | Android의 시스템 온디바이스 AI 모델 서비스 |
| ALSA | Advanced Linux Sound Architecture | Linux 오디오 서브시스템 |
| ALU | Arithmetic Logic Unit | 산술·논리 연산 장치 |
| AMAT | Average Memory Access Time | 평균 메모리 접근 시간 |
| AMBA | Advanced Microcontroller Bus Architecture | Arm의 온칩 버스 규격 묶음 |
| AMU | Activity Monitors Unit | Arm 코어의 활동 카운터 |
| ANE | Apple Neural Engine | Apple SoC의 신경망 가속기 |
| ANGLE | Almost Native Graphics Layer Engine | OpenGL ES를 Vulkan 등 다른 API 위에서 구현하는 변환 계층 |
| AoA | Angle of Arrival | 도래각, 방향 측정 |
| AON | Always-On | 항상 켜진 전원 영역 |
| AOT | Ahead-Of-Time compilation | 실행 전에 미리 컴파일 |
| AP | Application Processor | 운영체제와 앱을 돌리는 프로세서 |
| APB | Advanced Peripheral Bus | 저속 주변장치용 AMBA 버스 |
| API | Application Programming Interface | 응용 프로그램 인터페이스 |
| ASoC | ALSA System on Chip | SoC 오디오용 ALSA 계층 |
| ASTC | Adaptive Scalable Texture Compression | Khronos 표준 가변 블록 텍스처 압축 |
| AV1 | AOMedia Video 1 | AOMedia의 로열티 프리 비디오 코덱 |
| AVC | Advanced Video Coding | H.264 비디오 코덱 |
| AVS | Adaptive Voltage Scaling | 칩 특성에 맞춰 전압을 미세 조정하는 기법 |
| AWB | Auto White Balance | 자동 화이트 밸런스 |
| AXI | Advanced eXtensible Interface | 고성능 AMBA 버스 프로토콜 |
| BF16 | bfloat16 | 지수 8비트의 16비트 부동소수점 형식 |
| BLAS | Bottom-Level Acceleration Structure | 물체 단위 레이 트레이싱 가속 구조 |
| BTB | Branch Target Buffer | 분기 목표 주소 캐시 |
| BTI | Branch Target Identification | 분기 대상 표시로 코드 재사용 공격을 막는 Arm 확장 |
| BVH | Bounding Volume Hierarchy | 경계 상자 계층 구조 (레이 트레이싱 가속) |
| CCCI | Cross Core Communication Interface | MediaTek 모뎀–AP 통신 계층 |
| CCI | Camera Control Interface | I2C·I3C 기반 카메라 센서 제어 버스 |
| CDC | Clock Domain Crossing | 클럭 도메인 사이 신호 전달 |
| CFS | Completely Fair Scheduler | Linux의 이전 기본 스케줄러 |
| CHI | Coherent Hub Interface | AMBA 5의 패킷 기반 일관성 프로토콜 |
| CHRE | Context Hub Runtime Environment | Android 센서 허브용 nanoapp 런타임 |
| CHUB | Context Hub | Exynos의 센서 허브 영역 |
| CMOS | Complementary Metal-Oxide-Semiconductor | NMOS·PMOS를 짝지은 논리 회로 방식 |
| CPP | Contacted Poly Pitch | 이웃한 게이트 사이 간격 |
| CPU | Central Processing Unit | 중앙 처리 장치 |
| CRTC | CRT Controller | Linux DRM에서 화면 스캔아웃 파이프를 뜻하는 객체 |
| CSI | Camera Serial Interface | 카메라 센서와 SoC를 잇는 MIPI 직렬 인터페이스 (CSI-2) |
| CSS | Compute Subsystem | Arm이 코어·인터커넥트를 묶어 제공하는 검증된 서브시스템 |
| CTU | Coding Tree Unit | HEVC·VVC의 기본 부호화 블록 |
| DAC | Digital-to-Analog Converter | 디지털-아날로그 변환기 |
| DMA | Direct Memory Access | 장치가 CPU를 거치지 않고 메모리에 직접 접근 |
| DPU | Display Processing Unit | 화면 레이어를 합성해 패널로 내보내는 블록 |
| DRAM | Dynamic Random Access Memory | 커패시터 기반 메인 메모리 |
| DRX | Discontinuous Reception | 단말이 주기적으로만 수신하는 절전 방식 |
| DSC | Display Stream Compression | VESA의 시각적 무손실 디스플레이 압축 |
| DSI | Display Serial Interface | 패널과 SoC를 잇는 MIPI 직렬 인터페이스 |
| DSP | Digital Signal Processor | 신호 처리용 프로세서 |
| DSU | DynamIQ Shared Unit | DynamIQ 클러스터의 공유 L3·스누프 필터·전력 관리 블록 |
| DTCO | Design-Technology Co-Optimization | 설계와 공정을 함께 최적화 |
| DVFS | Dynamic Voltage and Frequency Scaling | 부하에 따라 전압과 클럭을 함께 바꾸는 기법 |
| DWC3 | DesignWare USB3 Controller | Synopsys USB3 컨트롤러 IP |
| EAS | Energy Aware Scheduling | 에너지 모델로 작업 배치를 정하는 Linux 스케줄러 기능 |
| EDA | Electronic Design Automation | 칩 설계 자동화 도구 |
| EEVDF | Earliest Eligible Virtual Deadline First | Linux 6.6부터의 기본 스케줄링 알고리즘 |
| EMI | Electromagnetic Interference | 전자기 간섭 |
| eMMC | embedded MultiMediaCard | 병렬 버스 기반 내장 플래시 저장장치 |
| eSE | embedded Secure Element | 내장 보안 요소 |
| ETC2 | Ericsson Texture Compression 2 | OpenGL ES 3.0 필수 텍스처 압축 |
| eUSB2 | Embedded USB2 | 저전압 USB 2.0 변형 |
| EUV | Extreme Ultraviolet | 13.5 nm 파장 극자외선 노광 |
| FEM | Front-End Module | RF 프런트엔드 모듈 |
| FinFET | Fin Field-Effect Transistor | 지느러미형 채널의 3면을 게이트가 감싸는 트랜지스터 |
| FLOPS | Floating-point Operations Per Second | 초당 부동소수점 연산 수 |
| FMA | Fused Multiply-Add | 곱셈과 덧셈을 한 번에 하는 연산 |
| FOWLP | Fan-Out Wafer Level Package | 재배선층으로 다이 바깥까지 배선을 펼친 패키지 |
| FP16 | 16-bit Floating Point | IEEE 754 반정밀도 부동소수점 |
| FP8 | 8-bit Floating Point | E4M3·E5M2 등 8비트 부동소수점 형식 |
| GAA | Gate-All-Around | 게이트가 채널 네 면을 모두 감싸는 트랜지스터 |
| GENI | Generic Interface | QUP v3의 범용 직렬 엔진 |
| GLSL | OpenGL Shading Language | OpenGL·OpenGL ES 셰이더 언어 |
| GMEM | Graphics Memory | Adreno의 칩 안 타일 메모리 |
| GNSS | Global Navigation Satellite System | 위성 항법 시스템 (GPS·Galileo·BeiDou 등) |
| GPGPU | General-Purpose computing on GPU | GPU를 이용한 범용 연산 |
| GPIO | General-Purpose Input/Output | 범용 입출력 핀 |
| GPU | Graphics Processing Unit | 그래픽·병렬 연산 프로세서 |
| GSR | Game Super Resolution | Snapdragon의 게임 업스케일링 기술 |
| HAL | Hardware Abstraction Layer | Android 하드웨어 추상화 계층 |
| HCI | Host Controller Interface | Bluetooth 호스트–컨트롤러 인터페이스 |
| HEVC | High Efficiency Video Coding | H.265 비디오 코덱 |
| HKMG | High-k Metal Gate | 고유전율 절연막과 금속 게이트 |
| HLG | Hybrid Log-Gamma | 방송용 HDR 전달 함수 (ITU-R BT.2100) |
| HLSL | High-Level Shading Language | Direct3D 셰이더 언어 |
| HMP | Heterogeneous Multi-Processing | 이종 코어를 동시에 쓰는 초기 스케줄링 방식 |
| HSR | Hidden Surface Removal | 가려진 면의 셰이딩을 하드웨어로 제거 |
| HVX | Hexagon Vector eXtensions | Hexagon DSP의 넓은 벡터 확장 |
| HWC | Hardware Composer | Android의 DPU 합성 HAL |
| I2C | Inter-Integrated Circuit | 2선 저속 직렬 버스 |
| I2S | Inter-IC Sound | 칩 간 디지털 오디오 직렬 버스 |
| I3C | Improved Inter-Integrated Circuit | MIPI의 I2C 후속 버스 |
| IBI | In-Band Interrupt | I3C 대역 내 인터럽트 |
| ILP | Instruction-Level Parallelism | 명령 수준 병렬성 |
| IMR | Immediate Mode Rendering | 즉시 렌더링 방식 |
| INT4 | 4-bit Integer | 4비트 정수 (LLM 가중치 양자화) |
| INT8 | 8-bit Integer | 8비트 정수 (추론 양자화의 표준) |
| IOMMU | I/O Memory Management Unit | 장치용 주소 변환·격리 장치 |
| IOVA | I/O Virtual Address | 장치가 쓰는 가상 주소 |
| IP | Intellectual Property | 라이선스로 거래되는 회로 설계 블록 |
| IPC | Instructions Per Cycle | 사이클당 처리 명령 수 |
| ISA | Instruction Set Architecture | 명령어 집합 아키텍처 |
| ISP | Image Signal Processor | 이미지 센서 데이터를 사진·영상으로 바꾸는 블록 |
| JEDEC | JEDEC Solid State Technology Association | 메모리·저장장치 표준 단체 |
| KGSL | Kernel Graphics Support Layer | Qualcomm Adreno 커널 드라이버 |
| KMD | Kernel Mode Driver | 커널 모드 드라이버 |
| KMS | Kernel Mode Setting | Linux DRM의 화면 모드·평면 설정 인터페이스 |
| KV | Key-Value cache | 어텐션 키·값을 저장하는 LLM 캐시 |
| LC3 | Low Complexity Communication Codec | LE Audio의 기본 오디오 코덱 |
| LDO | Low-Dropout Regulator | 입출력 전압 차가 작은 선형 레귤레이터 |
| LLM | Large Language Model | 대규모 언어 모델 |
| LNA | Low-Noise Amplifier | 수신 저잡음 증폭기 |
| LPDDR | Low Power Double Data Rate | 모바일용 저전력 DRAM |
| LSE | Large System Extensions | Armv8.1의 원자 연산 확장 |
| LTPO | Low-Temperature Polycrystalline Oxide | 저주사율 구동이 가능한 OLED 백플레인 |
| MAC | Multiply-Accumulate | 곱셈 후 누적 합에 더하는 연산 |
| MCU | Microcontroller Unit | 저전력 마이크로컨트롤러 |
| MHI | Modem Host Interface | PCIe 외장 모뎀용 Qualcomm 호스트 인터페이스 |
| MIPI | MIPI Alliance | 모바일 인터페이스 표준 단체 (CSI-2, DSI, M-PHY, UniPro 등) |
| MLO | Multi-Link Operation | Wi-Fi 7 다중 링크 동시 동작 |
| MLP | Memory-Level Parallelism | 메모리 수준 병렬성 |
| MMP | Minimum Metal Pitch | 최소 금속 배선 간격 |
| MOSFET | Metal-Oxide-Semiconductor Field-Effect Transistor | 금속 산화막 반도체 전계 효과 트랜지스터 |
| MPS | Metal Performance Shaders | Apple의 GPU 연산 라이브러리 |
| MSAA | Multisample Anti-Aliasing | 다중 샘플 안티앨리어싱 |
| MSL | Metal Shading Language | Metal 셰이더 언어 |
| MTE | Memory Tagging Extension | 메모리·포인터 태그로 메모리 오류를 잡는 Arm 확장 |
| NEON | Arm Advanced SIMD | Arm의 128비트 SIMD 확장 |
| NNAPI | Neural Networks API | Android의 (폐기 발표된) 신경망 API |
| NoC | Network on Chip | 패킷 기반 온칩 인터커넥트 |
| NPU | Neural Processing Unit | 신경망 연산 가속기 |
| NTN | Non-Terrestrial Network | 위성 등 비지상 네트워크 (3GPP Rel-17) |
| NVMe | Non-Volatile Memory Express | PCIe 기반 저장장치 프로토콜 |
| ODPM | On-Device Power Monitor | 기기 안 레일별 전력 계측 (Pixel 등) |
| OLED | Organic Light-Emitting Diode | 유기 발광 디스플레이 |
| ONNX | Open Neural Network Exchange | 신경망 모델 교환 형식 |
| OPP | Operating Performance Point | 주파수와 전압의 동작점 |
| PAC | Pointer Authentication Code | 포인터 서명으로 위조를 막는 Arm 확장 |
| PCIe | PCI Express | 고속 직렬 확장 버스 |
| PCM | Pulse Code Modulation | 비압축 디지털 오디오 표현 |
| PDAF | Phase Detection Auto Focus | 위상차 화소를 이용한 자동 초점 |
| PDM | Pulse Density Modulation | 디지털 마이크 출력 방식 |
| PELT | Per-Entity Load Tracking | Linux의 작업별 부하 추적 |
| PHY | Physical Layer | 물리 계층 회로 |
| PLL | Phase-Locked Loop | 기준 클럭을 곱해 고속 클럭을 만드는 회로 |
| PMIC | Power Management IC | 전원 관리 칩 |
| PoP | Package on Package | 패키지 위에 패키지를 쌓는 구조 |
| PPA | Performance, Power, Area | 성능·전력·면적 |
| PQ | Perceptual Quantizer | HDR10의 전달 함수 (SMPTE ST 2084) |
| PSCI | Power State Coordination Interface | Arm의 코어·클러스터·시스템 전원 상태 요청 표준 |
| PTA | Packet Traffic Arbitration | Wi-Fi·Bluetooth 시간 분할 중재 |
| QMI | Qualcomm MSM Interface | Qualcomm 모뎀 제어 메시지 프로토콜 |
| QNN | Qualcomm AI Engine Direct SDK | Qualcomm의 AI 가속 SDK |
| QoS | Quality of Service | 트래픽 우선순위·대역폭 보장 |
| QUP | Qualcomm Universal Peripheral | Qualcomm 직렬 엔진 묶음 |
| RDL | Redistribution Layer | 재배선층 |
| RDNA | Radeon DNA | AMD의 GPU 아키텍처 계열 |
| RFFE | RF Front-End Control Interface | RF 프런트엔드 제어용 MIPI 버스 |
| RIL | Radio Interface Layer | Android 셀룰러 제어 계층 |
| ROB | Reorder Buffer | 비순차 실행 명령을 원래 순서로 추적하는 버퍼 |
| RTK | Real-Time Kinematic | 반송파 위상 기반 정밀 측위 |
| SCMI | System Control and Management Interface | Arm의 전원·성능·클럭 관리 메시지 규격 |
| SDIO | Secure Digital Input Output | SD 규격 기반 주변장치 인터페이스 |
| SDK | Software Development Kit | 소프트웨어 개발 도구 모음 |
| SIMD | Single Instruction, Multiple Data | 한 명령으로 여러 데이터를 처리 |
| SIMT | Single Instruction, Multiple Threads | 한 명령을 여러 스레드가 함께 실행 |
| SLC | System Level Cache | SoC 전체가 공유하는 마지막 계층 캐시 |
| SLPI | Sensor Low Power Island | Qualcomm SoC의 상시 저전력 센서 처리 영역 |
| SME | Scalable Matrix Extension | Arm의 행렬 연산 확장 |
| SME2 | Scalable Matrix Extension 2 | SME의 후속 Arm 행렬 확장 |
| SMEM | Shared Memory | Qualcomm 프로세서 간 공유 메모리 영역 |
| SMMU | System Memory Management Unit | Arm의 IOMMU 아키텍처 |
| SNPE | Snapdragon Neural Processing Engine | QNN 이전의 Qualcomm AI SDK |
| SoC | System on Chip | 시스템 전체를 한 칩에 모은 집적 회로 |
| SPI | Serial Peripheral Interface | 4선 동기 직렬 버스 |
| SPIR-V | Standard Portable Intermediate Representation V | Vulkan·OpenCL 셰이더 중간 표현 |
| SPMI | System Power Management Interface | MIPI의 SoC–PMIC 전원 제어 버스 |
| SRAM | Static Random Access Memory | 캐시에 쓰는 고속 메모리 |
| STS | Scrambled Timestamp Sequence | 802.15.4z 보안 거리 측정 시퀀스 |
| SVE2 | Scalable Vector Extension 2 | Arm의 가변 길이 벡터 확장 |
| TBDR | Tile-Based Deferred Rendering | 타일 기반 지연 렌더링 |
| TBR | Tile-Based Rendering | 타일 기반 렌더링 |
| TCXO | Temperature-Compensated Crystal Oscillator | 온도 보상 수정 발진기 |
| TEE | Trusted Execution Environment | 보안 세계의 격리된 실행 환경 |
| TF-A | Trusted Firmware-A | Arm 보안 펌웨어 참조 구현 (PSCI 처리) |
| TFLite | TensorFlow Lite | LiteRT의 이전 이름 |
| TFT | Thin-Film Transistor | 패널 화소를 구동하는 박막 트랜지스터 |
| Tj | Junction Temperature | 다이 내부 접합 온도 |
| TLAS | Top-Level Acceleration Structure | 장면 단위 레이 트레이싱 가속 구조 |
| TLB | Translation Lookaside Buffer | 주소 변환 캐시 |
| TLMM | Top Level Mode Multiplexer | Qualcomm 핀 다중화 블록 |
| TLP | Thread-Level Parallelism | 스레드 수준 병렬성 |
| ToF | Time of Flight | 신호 왕복 시간 |
| TOPS | Tera Operations Per Second | 초당 조 단위 연산 수 |
| TPU | Tensor Processing Unit | Google의 신경망 가속기 |
| UART | Universal Asynchronous Receiver-Transmitter | 비동기 직렬 통신 |
| UBWC | Universal Bandwidth Compression | Qualcomm의 무손실 대역폭 압축 |
| UFS | Universal Flash Storage | 모바일용 직렬 플래시 저장장치 |
| UFSHCI | UFS Host Controller Interface | UFS 호스트 컨트롤러 표준 레지스터 인터페이스 |
| UMD | User Mode Driver | 사용자 모드 드라이버 |
| UPF | Unified Power Format | IEEE 1801 전원 의도 기술 형식 |
| UPIU | UFS Protocol Information Unit | UFS 전송 계층 패킷 |
| USB | Universal Serial Bus | 범용 직렬 버스 |
| USI | Universal Serial Interface | Exynos 범용 직렬 블록 |
| UTP | UFS Transport Protocol | UFS 전송 계층 |
| UWB | Ultra-Wideband | 초광대역 거리·방향 측정 무선 |
| VESA | Video Electronics Standards Association | 디스플레이 표준 단체 (DisplayPort, DSC 등) |
| VVC | Versatile Video Coding | H.266 비디오 코덱 |
| WCI-2 | Wireless Coexistence Interface 2 | 모뎀–콤보 칩 공존 신호 규격 |
| WCK | Write Clock | LPDDR5 이후의 데이터용 고속 클럭 |
| WFE | Wait For Event | 이벤트까지 코어를 대기시키는 Arm 명령 |
| WFI | Wait For Interrupt | 인터럽트까지 코어를 대기시키는 Arm 명령 |
| xHCI | eXtensible Host Controller Interface | USB 호스트 컨트롤러 표준 |

## 여러 뜻이 있는 약어

| 약어 | 뜻 | 쓰는 곳 |
|---|---|---|
| L1·L2·L3 | 캐시 계층 번호 | 이 책의 CPU·메모리 장 |
| CS | Chip Select / Compute Subsystem 등 | 문맥에 따라 다름 |
| PD | Power Domain / Power Delivery | 전력 관리 / USB 충전 |
| APU | AI Processing Unit (MediaTek) / Accelerated Processing Unit (AMD) | NPU 장 / PC 칩 |
| DRM | Direct Rendering Manager / Digital Rights Management | Linux 디스플레이 / 콘텐츠 보호 |
| HDR | High Dynamic Range / High Data Rate (I3C) | 카메라·디스플레이 / 저속 버스 |
| SDR | Standard Dynamic Range / Single Data Rate (I3C) | 디스플레이 / 저속 버스 |
| PA | Power Amplifier / Physical Address | RF 프런트엔드 / 메모리 |
| SCP | System Companion Processor (MediaTek) / Secure Copy | 센서 허브 / 파일 전송 |
