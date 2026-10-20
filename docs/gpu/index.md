# GPU

이 섹션은 스마트폰 SoC에서 화면을 그리는 **GPU**를 다룹니다. GPU는 게임만을 위한 블록이 아니라, 홈 화면 애니메이션·스크롤·카메라 미리보기·영상 효과까지 매 프레임 픽셀을 만들어 내는 SoC의 주요 연산 장치입니다. 모바일 GPU는 데스크톱 GPU보다 훨씬 적은 전력과 메모리 대역폭 안에서 일해야 하므로, **데이터를 칩 밖으로 덜 보내는 구조**가 설계의 중심에 있습니다.

| 페이지 | 핵심 질문 |
|---|---|
| [모바일 GPU 구조](architecture.md) | 타일 기반 렌더링은 왜 쓰고, 셰이더 코어·워프·대역폭 압축은 어떻게 동작하나? |
| [주요 GPU 계열](families.md) | Adreno·Mali/Immortalis·Xclipse·Apple GPU·PowerVR은 어디서 왔고 무엇이 다른가? |
| [그래픽 API와 드라이버](apis.md) | OpenGL ES·Vulkan·Metal은 무엇이 다르고, Android GPU 드라이버는 어떻게 구성되나? |
| [레이 트레이싱과 업스케일링](raytracing.md) | 모바일에서 하드웨어 레이 트레이싱은 무엇을 가속하고, 업스케일링·프레임 생성은 어떻게 전력을 아끼나? |
| [GPU 연산](compute.md) | OpenCL·Vulkan compute로 GPU를 범용 연산에 쓸 때, NPU와는 어떻게 역할을 나누나? |

!!! basic "GPU 연산 능력 미리 보기"
    GPU의 이론 연산 성능은 간단한 곱셈으로 어림합니다.

    **FLOPS = ALU 수 × 2 × 클럭**

    ALU 하나는 한 클럭에 곱셈과 덧셈을 묶은 FMA 한 번(연산 2개로 셈)을 할 수 있다고 봅니다. 예를 들어 FP32 ALU가 1024개이고 1 GHz로 돈다면 1024 × 2 × 1 GHz ≈ **2.05 TFLOPS**입니다. 이 값은 가상의 입력으로 계산한 이론 상한이며, 실제 성능은 메모리 대역폭·발열·드라이버에 따라 크게 낮아집니다. (수치는 `tools/soc_numbers.py`에서 계산)

!!! tip "다른 섹션과의 연결"
    GPU가 쓰는 DRAM 대역폭은 [LPDDR](../memory/lpddr.md)과 [메모리 컨트롤러와 SLC](../memory/controller-slc.md), 게임 중 GPU 클럭이 떨어지는 원리는 [DVFS와 전력 관리](../power/dvfs.md)와 [열 관리와 스로틀링](../power/thermal.md), 완성된 프레임을 화면에 내보내는 과정은 [디스플레이 파이프라인](../media/display.md), AI 연산의 분담은 [NPU란 무엇인가](../npu/what-is-npu.md)에서 다룹니다.
