# NPU와 AI

이 섹션은 SoC 안의 **신경망 전용 가속기(NPU)**와 그 위에서 AI 모델을 돌리는 소프트웨어를 다룹니다. 카메라의 장면 인식과 음성 인식에서 시작한 NPU는 이제 온디바이스 LLM과 이미지 생성까지 맡고 있으며, 제조사 발표에서 가장 큰 숫자로 강조되는 블록이 되었습니다. 그러나 **사양표의 TOPS만으로는 실제 AI 성능을 알 수 없고**, 메모리 대역폭과 소프트웨어 스택이 체감 성능을 크게 좌우합니다.

| 페이지 | 핵심 질문 |
|---|---|
| [NPU란 무엇인가](what-is-npu.md) | 행렬 곱셈을 왜 CPU·GPU가 아닌 전용 블록에 맡기고, NPU 내부는 어떻게 생겼나? |
| [주요 NPU 계열](families.md) | Hexagon, Samsung NPU, MediaTek APU, Apple Neural Engine, Google TPU는 어디서 출발해 어떻게 바뀌었나? |
| [TOPS와 정밀도](tops.md) | TOPS는 어떻게 계산하고, INT8·INT4·FP16과 희소성 표기는 숫자를 어떻게 바꾸나? |
| [온디바이스 LLM](llm.md) | 스마트폰에서 LLM의 토큰 속도를 정하는 것은 연산일까 메모리일까? |
| [AI 소프트웨어 스택](software.md) | NNAPI 이후 앱은 어떤 경로로 NPU를 쓰고, 지원되지 않는 연산은 어디로 가나? |

!!! basic "TOPS 계산 미리 보기"
    NPU의 피크 성능은 간단한 곱셈입니다.

    **TOPS = MAC 수 × 2 × 클럭 ÷ 10¹²**

    MAC(곱셈-누적) 한 번을 곱셈 1회 + 덧셈 1회, 즉 **연산 2개**로 셉니다. 예를 들어 INT8 MAC 4096개가 1 GHz로 돌면 4096 × 2 × 10⁹ ≈ **8.2 TOPS**입니다. 같은 하드웨어가 INT4를 두 배 속도로 처리하면 사양표에는 **16.4 TOPS**로 적힐 수 있습니다. 숫자를 비교할 때는 항상 **어떤 정밀도 기준인지**를 확인해야 합니다. (수치는 `tools/soc_numbers.py`에서 계산)

!!! tip "다른 섹션과의 연결"
    NPU에 데이터를 공급하는 DRAM 대역폭은 [LPDDR](../memory/lpddr.md), GPU로 AI 연산을 돌리는 방법은 [GPU 연산](../gpu/compute.md), NPU의 전력·발열 한계는 [열 관리와 스로틀링](../power/thermal.md), 카메라 파이프라인 안의 AI 처리는 [ISP와 카메라 파이프라인](../media/isp.md)에서 다룹니다.
