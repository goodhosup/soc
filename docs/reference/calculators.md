# 계산기

!!! spec "계산식 출처"
    LPDDR 데이터 레이트·채널 폭: JEDEC JESD209-4/-5/-6 (LPDDR4·5·5X·6) · 동적 전력 $P = \alpha C V^2 f$: CMOS 전력 모델 · 웨이퍼당 다이 수 근사식과 푸아송 수율 모델 $Y = e^{-A D_0}$: 반도체 제조 교과서의 표준 근사 · 피크 연산 = 연산기 수 × 2(곱셈·덧셈, FMA/MAC) × 클럭 · 화소 데이터 속도: MIPI CSI-2·DSI의 비압축 화소 형식 · 배터리 에너지: 공칭 전압 × 용량

!!! basic "사용법"
    값을 바꾸면 결과가 바로 갱신됩니다. 모든 계산은 브라우저에서만 이루어집니다. 공식과 기본값은 `tools/soc_numbers.py`와 같으며, 기본값을 그대로 두면 본문의 예제 값(예: LPDDR5X-8533 → 68.3 GB/s, 7B INT4 → 19.5 tok/s, 120 mm² → 528개·88.7%·468개)이 나옵니다.

## LPDDR 피크 대역폭 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>세대 예시
      <select id="bw-preset">
        <option value="">직접 입력</option>
        <option value="4266">LPDDR4X-4266</option>
        <option value="6400">LPDDR5-6400</option>
        <option value="8533" selected>LPDDR5X-8533</option>
        <option value="9600">LPDDR5X-9600</option>
        <option value="10667">LPDDR5X-10667</option>
      </select>
    </label>
    <label>핀당 데이터 레이트 (MT/s)
      <input id="bw-rate" type="number" min="0" step="1" value="8533">
    </label>
    <label>총 버스 폭 (비트) — 스마트폰은 보통 64
      <input id="bw-bus" type="number" min="1" step="16" value="64">
    </label>
  </div>
  <div class="calc-result">
    <div>16비트 채널 <b id="bw-ch">—</b>개 기준</div>
    <div class="calc-big"><span id="bw-out">—</span> GB/s <small>(피크 이론값, 10<sup>9</sup> 바이트)</small></div>
  </div>
</div>

## 온디바이스 LLM 생성 속도 상한 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>LPDDR 데이터 레이트 (MT/s)
      <input id="llm-rate" type="number" min="0" value="8533">
    </label>
    <label>버스 폭 (비트)
      <input id="llm-bus" type="number" min="1" step="16" value="64">
    </label>
    <label>매개변수 수 (십억, B)
      <input id="llm-params" type="number" min="0.1" step="0.1" value="7">
    </label>
    <label>가중치 비트 수
      <select id="llm-bits">
        <option value="16">16 (FP16)</option>
        <option value="8">8 (INT8)</option>
        <option value="4" selected>4 (INT4)</option>
        <option value="3">3</option>
        <option value="2">2</option>
      </select>
    </label>
    <label>대역폭 활용률 (%) — 참고용
      <input id="llm-eff" type="number" min="1" max="100" value="100">
    </label>
  </div>
  <div class="calc-result">
    <div>대역폭 <b id="llm-bw">—</b> GB/s · 가중치 크기 <b id="llm-model">—</b> GB</div>
    <div class="calc-big"><span id="llm-out">—</span> tok/s <small>(토큰마다 가중치 전체를 한 번 읽는다고 가정한 상한)</small></div>
    <div>활용률 반영 시 <b id="llm-real">—</b> tok/s</div>
  </div>
</div>

## DVFS 동적 전력과 에너지 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>기준 클럭 f₀ (GHz)
      <input id="dv-f0" type="number" min="0.01" step="0.1" value="3.0">
    </label>
    <label>기준 전압 V₀ (V)
      <input id="dv-v0" type="number" min="0.01" step="0.01" value="1.0">
    </label>
    <label>새 클럭 f₁ (GHz)
      <input id="dv-f1" type="number" min="0.01" step="0.1" value="1.5">
    </label>
    <label>새 전압 V₁ (V)
      <input id="dv-v1" type="number" min="0.01" step="0.01" value="0.7">
    </label>
  </div>
  <div class="calc-result">
    <div>같은 일을 끝내는 시간 <b id="dv-t">—</b>배</div>
    <div class="calc-big">전력 비 <span id="dv-p">—</span> · 에너지 비 <span id="dv-e">—</span></div>
    <div>동적 전력 <b id="dv-psave">—</b>% 감소 · 같은 일의 동적 에너지 <b id="dv-esave">—</b>% 감소 <small>(누설 전력 제외)</small></div>
  </div>
</div>

## 웨이퍼당 다이 수와 수율 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>다이 면적 (mm²)
      <input id="dw-area" type="number" min="1" step="1" value="120">
    </label>
    <label>웨이퍼 지름 (mm)
      <select id="dw-wafer">
        <option value="200">200</option>
        <option value="300" selected>300</option>
      </select>
    </label>
    <label>결함 밀도 D₀ (개/cm²)
      <input id="dw-d0" type="number" min="0" step="0.01" value="0.1">
    </label>
  </div>
  <div class="calc-result">
    <div>웨이퍼당 다이 <b id="dw-n">—</b>개 · 푸아송 수율 <b id="dw-y">—</b>%</div>
    <div class="calc-big">양품 다이 약 <span id="dw-good">—</span>개 <small>(가장자리 손실 근사식, 스크라이브 라인 제외)</small></div>
  </div>
</div>

## NPU·GPU 피크 연산 성능 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>MAC 또는 ALU 수
      <input id="tp-units" type="number" min="1" step="1" value="4096">
    </label>
    <label>클럭 (GHz)
      <input id="tp-ghz" type="number" min="0.01" step="0.05" value="1.0">
    </label>
    <label>정밀도 배율 (INT4·FP16 2배속 설계면 2, 희소성까지 4)
      <input id="tp-rate" type="number" min="0.25" step="1" value="1">
    </label>
    <label>이용률 (%)
      <input id="tp-util" type="number" min="1" max="100" value="40">
    </label>
    <label>전력 (W)
      <input id="tp-watt" type="number" min="0.01" step="0.1" value="2">
    </label>
  </div>
  <div class="calc-result">
    <div>NPU면 TOPS, GPU FP 연산이면 TFLOPS로 읽습니다.</div>
    <div class="calc-big">피크 <span id="tp-out">—</span> TOPS · 유효 <span id="tp-eff">—</span> TOPS</div>
    <div>피크 기준 효율 <b id="tp-pw">—</b> TOPS/W</div>
  </div>
</div>

## 카메라·디스플레이 raw 데이터 속도 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>예시
      <select id="px-preset">
        <option value="">직접 입력</option>
        <option value="4000,3000,10,30" selected>12MP 센서 10bit 30fps</option>
        <option value="8192,6144,10,30">50MP 센서 10bit 30fps</option>
        <option value="3840,2160,15,60">4K60 10bit 4:2:0 영상</option>
        <option value="1440,3120,24,120">QHD+ 패널 24bit 120Hz</option>
        <option value="1440,3120,8,120">QHD+ 120Hz DSC 8bpp</option>
      </select>
    </label>
    <label>가로 (화소)
      <input id="px-w" type="number" min="1" value="4000">
    </label>
    <label>세로 (화소)
      <input id="px-h" type="number" min="1" value="3000">
    </label>
    <label>화소당 비트
      <input id="px-bits" type="number" min="1" step="1" value="10">
    </label>
    <label>프레임 속도 (fps·Hz)
      <input id="px-fps" type="number" min="1" value="30">
    </label>
  </div>
  <div class="calc-result">
    <div><b id="px-mp">—</b> MP · 한 프레임 <b id="px-frame">—</b> MB</div>
    <div class="calc-big"><span id="px-out">—</span> Gbps <small>(블랭킹·패킷 헤더 제외)</small></div>
    <div>바이트로 환산 <b id="px-gbs">—</b> GB/s</div>
  </div>
</div>

## 배터리 사용 시간 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>배터리 용량 (mAh)
      <input id="bat-mah" type="number" min="1" value="5000">
    </label>
    <label>공칭 전압 (V)
      <input id="bat-v" type="number" min="0.1" step="0.01" value="3.87">
    </label>
    <label>평균 소비 전력 (W)
      <input id="bat-w" type="number" min="0.001" step="0.1" value="1.5">
    </label>
  </div>
  <div class="calc-result">
    <div>배터리 에너지 <b id="bat-wh">—</b> Wh</div>
    <div class="calc-big">약 <span id="bat-h">—</span>시간 <small>(<span id="bat-d">—</span>일)</small></div>
  </div>
</div>

??? expert "계산기 사용 시 주의"
    - **LPDDR 대역폭**은 피크 이론값입니다. 리프레시, 뱅크 충돌, 읽기·쓰기 전환 때문에 실제 유효 대역폭은 이보다 낮고, CPU·GPU·NPU·디스플레이가 함께 나눠 씁니다([LPDDR](../memory/lpddr.md), [메모리 컨트롤러와 SLC](../memory/controller-slc.md)).
    - **LLM 토큰 속도**는 생성(디코드) 단계에서 가중치를 토큰마다 한 번씩 읽는다는 가정의 상한입니다. KV 캐시 읽기, 다른 블록과의 대역폭 경쟁, 열 제한을 빼지 않았으므로 실제 값은 더 낮습니다. 프리필 단계는 연산 성능이 좌우합니다([온디바이스 LLM](../npu/llm.md)).
    - **DVFS 비율**은 동적 전력만 봅니다. 낮은 전압에서도 누설 전력은 남고, 작업 시간이 길어지면 그동안 다른 블록도 깨어 있으므로 "느리게 오래"가 항상 이득은 아닙니다([DVFS와 전력 관리](../power/dvfs.md)).
    - **다이 수·수율**은 교과서식 근사입니다. 실제 양산 수율은 공정 성숙도, 설계의 결함 민감 면적, 리던던시(예: SRAM 예비 행·열)에 따라 다르고, 결함 밀도 값은 파운드리가 공개하지 않는 경우가 많습니다([파운드리와 공정](../design/foundry.md)).
    - **피크 TOPS**는 모든 MAC이 매 클럭 일할 때의 값입니다. 회사 발표 TOPS는 정밀도(INT8·INT4)와 희소성 포함 여부가 제각각이므로 같은 기준으로 맞춘 뒤 비교합니다([TOPS와 정밀도](../npu/tops.md)).
    - **raw 데이터 속도**는 화소만 센 값이라 실제 링크에는 블랭킹·헤더·부호화 여유가 더 필요합니다([이미지 센서 인터페이스](../media/camera-interface.md), [디스플레이 파이프라인](../media/display.md)).
    - **배터리 사용 시간**은 평균 전력 하나로 본 단순 모델입니다. 실제로는 배터리 노화, 온도, 변환 손실, 화면 밝기에 따라 달라집니다([전력 측정과 분석](../power/measurement.md)).

<script src="../../javascripts/calculators.js"></script>
