"""본문에 들어가는 SoC 수치를 계산·검산하는 단일 출처.

메모리 대역폭, 동적 전력, 다이 수·수율, 지연 시간 환산, LLM 토큰 속도 상한을 여기서 계산하고
본문 표와 계산기는 이 값과 일치해야 한다.

    python tools/soc_numbers.py            # 주요 표 출력
    python tools/soc_numbers.py --check    # 본문에 적힌 대표 값 검산 (불일치 시 종료 코드 1)
"""
from __future__ import annotations

import argparse
import math
import sys
from fractions import Fraction as F

# ---------------------------------------------------------------- 메모리 대역폭
# 스마트폰 SoC는 보통 16비트 채널 4개 = 64비트 버스를 쓴다.
LPDDR_RATES = {  # 세대: 대표 최대 데이터 레이트 (MT/s)
    "LPDDR4X": 4266,
    "LPDDR5": 6400,
    "LPDDR5X-8533": 8533,
    "LPDDR5X-9600": 9600,
    "LPDDR5X-10667": 10667,
}


def dram_bw_gbs(mts: float, bus_bits: int = 64) -> float:
    """피크 대역폭 (GB/s, 10^9 바이트) = 데이터 레이트 × 버스 폭 / 8."""
    return mts * 1e6 * bus_bits / 8 / 1e9


# ---------------------------------------------------------------- UFS 레인 속도
# M-PHY HS 기어의 Rate B 기준 (Mbps/레인). UFS는 2레인.
UFS_GEAR_MBPS = {"HS-G3": 5830.4, "HS-G4": 11660.8, "HS-G5": 23321.6}


def ufs_raw_gbps(gear: str, lanes: int = 2) -> float:
    return UFS_GEAR_MBPS[gear] * lanes / 1000


# ---------------------------------------------------------------- 전력
def dyn_power_ratio(f0: float, v0: float, f1: float, v1: float) -> float:
    """P = αCV²f 에서 (f1, v1) 동작점의 전력 / (f0, v0) 동작점의 전력."""
    return (v1 / v0) ** 2 * (f1 / f0)


def energy_ratio(f0: float, v0: float, f1: float, v1: float) -> float:
    """같은 일(같은 사이클 수)을 끝내는 데 드는 동적 에너지 비 = V² 비."""
    return dyn_power_ratio(f0, v0, f1, v1) * (f0 / f1)


# ---------------------------------------------------------------- 다이와 수율
def dies_per_wafer(area_mm2: float, wafer_mm: float = 300) -> float:
    """웨이퍼당 다이 수 근사: πr²/A − πd/√(2A)."""
    r = wafer_mm / 2
    return math.pi * r * r / area_mm2 - math.pi * wafer_mm / math.sqrt(2 * area_mm2)


def poisson_yield(area_mm2: float, d0_per_cm2: float) -> float:
    """푸아송 수율 모델 Y = exp(−A·D0)."""
    return math.exp(-(area_mm2 / 100) * d0_per_cm2)


# ---------------------------------------------------------------- 시간 환산
def cycles_to_ns(cycles: float, ghz: float) -> float:
    return cycles / ghz


def amdahl(p: float, n: int) -> float:
    """병렬화 가능한 비율 p, 코어 n개일 때 속도 향상."""
    return 1 / ((1 - p) + p / n)


# ---------------------------------------------------------------- 온디바이스 LLM
def llm_tokens_per_s(bw_gbs: float, params_b: float, bits: int) -> float:
    """생성 단계 토큰 속도 상한: 토큰마다 가중치 전체를 한 번 읽는다고 가정."""
    model_gb = params_b * bits / 8
    return bw_gbs / model_gb


# ---------------------------------------------------------------- GPU
def gpu_tflops(alus: int, ghz: float, ops_per_alu: int = 2, rate: float = 1.0) -> float:
    """이론 연산량 (TFLOPS) = ALU 수 × 2(FMA) × 클럭 × 정밀도 배율 (FP16 2배 설계면 rate=2)."""
    return alus * ops_per_alu * ghz * rate / 1000


def framebuffer_gbs(w: int, h: int, bytes_pp: int, fps: float, passes: float = 1) -> float:
    """프레임버퍼 쓰기 대역폭 (GB/s, 10^9 바이트)."""
    return w * h * bytes_pp * fps * passes / 1e9


def render_pixel_ratio(axis_scale: float) -> float:
    """가로·세로를 axis_scale 배로 렌더링할 때 픽셀 수 비율."""
    return axis_scale ** 2


# ---------------------------------------------------------------- NPU
def npu_peak_tops(macs: int, ghz: float, ops_per_mac: int = 2) -> float:
    """피크 TOPS = MAC 수 × 2 × 클럭."""
    return macs * ops_per_mac * ghz * 1e9 / 1e12


def ridge_ops_per_byte(tops: float, bw_gbs: float) -> float:
    """루프라인 경계점 (ops/byte) = 피크 연산 / 메모리 대역폭."""
    return tops * 1e12 / (bw_gbs * 1e9)


def kv_cache_gb(layers: int, kv_heads: int, head_dim: int, ctx: int, bytes_per: float = 2) -> float:
    """KV 캐시 = 2(K,V) × 레이어 × KV 헤드 × 헤드 차원 × 문맥 × 바이트."""
    return 2 * layers * kv_heads * head_dim * ctx * bytes_per / 1e9


def prefill_s(params_b: float, tokens: int, eff_tops: float) -> float:
    """프리필 시간 근사 = 2 × 매개변수 × 토큰 / 유효 연산 성능 (어텐션 제외)."""
    return 2 * params_b * 1e9 * tokens / (eff_tops * 1e12)


def spec_decode_tokens(alpha: float, k: int) -> float:
    """추측 디코딩: 검증 1회당 기대 토큰 수 (채택 확률 α 독립 가정)."""
    return (1 - alpha ** (k + 1)) / (1 - alpha)


# ---------------------------------------------------------------- 멀티미디어
def pixel_rate_gbps(w: int, h: int, bits: float, fps: float) -> float:
    """비압축 화소 데이터 속도 (Gbps) = 가로 × 세로 × 화소당 비트 × fps. 블랭킹·헤더 제외."""
    return w * h * bits * fps / 1e9


def frame_mb(w: int, h: int, bits: float, frames: int = 1) -> float:
    """raw 프레임 버퍼 크기 (MB, 10^6 바이트)."""
    return w * h * bits / 8 * frames / 1e6


DPHY_LANE_GBPS = 4.5           # D-PHY v2.x 레인당 최대
CPHY_TRIO_GSPS = 6.0           # C-PHY v2.0 trio당 최대 심볼 레이트
CPHY_BITS_PER_SYMBOL = 16 / 7  # 7심볼에 16비트


def dphy_gbps(lanes: int = 4) -> float:
    return DPHY_LANE_GBPS * lanes


def cphy_gbps(trios: int = 1, gsps: float = CPHY_TRIO_GSPS) -> float:
    return gsps * CPHY_BITS_PER_SYMBOL * trios


def pcm_mbps(rate_hz: float, bits: int, ch: int) -> float:
    return rate_hz * bits * ch / 1e6


# ---------------------------------------------------------------- 연결 인터페이스
PCIE_GEN = {1: (2.5, F(8, 10)), 2: (5, F(8, 10)), 3: (8, F(128, 130)), 4: (16, F(128, 130)), 5: (32, F(128, 130))}


def pcie_gbs(gen: int, lanes: int = 1) -> float:
    """PCIe 한 방향 이론 대역폭 (GB/s) = GT/s × 부호화 효율 × 레인 / 8."""
    gts, enc = PCIE_GEN[gen]
    return float(gts * enc * lanes / 8)


USB_LINK = {"USB 3.2 Gen 1": (5, F(8, 10)), "USB 3.2 Gen 2": (10, F(128, 132))}


def usb_gbs(name: str) -> float:
    gbps, enc = USB_LINK[name]
    return float(gbps * enc / 8)


def sdio_mbs(clk_mhz: float, bits: int = 4) -> float:
    return clk_mhz * bits / 8


def uart_kbs(baud: float, bits_per_frame: int = 10) -> float:
    """8N1: 프레임 10비트 중 데이터 8비트."""
    return baud * 8 / bits_per_frame / 8 / 1e3


def dp_gbps(lane_gbps: float = 8.1, lanes: int = 4) -> float:
    return lane_gbps * lanes * 8 / 10


def iono_ratio(f_hi_mhz: float = 1575.42, f_lo_mhz: float = 1176.45) -> float:
    """전리층 지연 ∝ 1/f² → 낮은 주파수의 지연 / 높은 주파수의 지연."""
    return (f_hi_mhz / f_lo_mhz) ** 2


def uwb_sample_m(bw_hz: float = 499.2e6) -> float:
    return 299_792_458 / bw_hz


# ---------------------------------------------------------------- 배터리·전원·열·대기
def battery_wh(mah: float, v: float = 3.87) -> float:
    """배터리 에너지 (Wh) = 용량 × 공칭 전압."""
    return mah * v / 1000


def runtime_h(wh: float, watts: float) -> float:
    return wh / watts


def regulator_input_w(pout_w: float, eff: float) -> float:
    return pout_w / eff


def ldo_loss_w(vin: float, vout: float, amps: float) -> float:
    return (vin - vout) * amps


def sustained_power_w(t_limit: float, t_amb: float, r_theta: float) -> float:
    """ΔT = P × Rθ → P = (T_limit − T_amb) / Rθ."""
    return (t_limit - t_amb) / r_theta


def idle_breakeven_ms(e_uj: float, p_shallow_mw: float, p_deep_mw: float) -> float:
    """t_be = E_전환 / (P_얕은 − P_깊은). µJ / mW = ms."""
    return e_uj / (p_shallow_mw - p_deep_mw)


def energy_per_frame_mj(watts: float, fps: float) -> float:
    return watts / fps * 1000


# ---------------------------------------------------------------- 보안
def brute_force_hours(space: float, ms_per_try: float) -> float:
    """시도 제한 없이 전체 경우의 수를 시도하는 시간 (시간)."""
    return space * ms_per_try / 1000 / 3600


# ---------------------------------------------------------------- 제조 원가
def cost_per_good_die(wafer_cost: float, area_mm2: float, d0_per_cm2: float) -> float:
    """양품 다이 1개당 웨이퍼 원가 = 웨이퍼 가격 / (웨이퍼당 다이 수 × 수율)."""
    return wafer_cost / (dies_per_wafer(area_mm2) * poisson_yield(area_mm2, d0_per_cm2))


# ---------------------------------------------------------------- 벤치마크
def stability_pct(min_score: float, max_score: float) -> float:
    """지속 성능 안정성 = 최저 루프 ÷ 최고 루프 (%)."""
    return min_score / max_score * 100


def perf_per_watt(score: float, watts: float) -> float:
    return score / watts


def geomean(*xs: float) -> float:
    return math.prod(xs) ** (1 / len(xs))


def ipc(instructions: float, cycles: float) -> float:
    return instructions / cycles


# ---------------------------------------------------------------- 최신 동향
def die_cost_ratio(a0: float, d0_0: float, a1: float, d0_1: float, wafer_cost_ratio: float) -> float:
    """새 공정 다이(=같은 트랜지스터 수) 비용 / 이전 공정 다이 비용."""
    g0 = dies_per_wafer(a0) * poisson_yield(a0, d0_0)
    g1 = dies_per_wafer(a1) * poisson_yield(a1, d0_1)
    return wafer_cost_ratio * g0 / g1


def fit_failures(fit: float, hours: float, units: float) -> float:
    """FIT(10^9 시간당 고장 수) × 운행 시간 × 대수 → 기대 고장 수."""
    return fit * 1e-9 * hours * units


# ---------------------------------------------------------------- 출력·검산
def show() -> None:
    print("LPDDR 피크 대역폭 (64비트 버스, GB/s)")
    for k, v in LPDDR_RATES.items():
        print(f"  {k:>14}: {v:>6} MT/s → {dram_bw_gbs(v):5.1f}")
    print("\nUFS 원시 링크 속도 (2레인, Gbps)")
    for g in UFS_GEAR_MBPS:
        print(f"  {g}: {ufs_raw_gbps(g):5.1f}")
    print("\n동적 전력: 3.0 GHz·1.0 V → 1.5 GHz·0.7 V")
    print(f"  전력 비 {dyn_power_ratio(3.0, 1.0, 1.5, 0.7):.3f}, 에너지 비 {energy_ratio(3.0, 1.0, 1.5, 0.7):.3f}")
    print("\n웨이퍼당 다이 수와 수율 (300 mm, D0 = 0.1 /cm²)")
    for a in (100, 120, 150):
        print(f"  {a} mm²: {dies_per_wafer(a):5.0f}개, 수율 {poisson_yield(a, 0.1) * 100:4.1f}%")
    print("\n7B 모델 생성 속도 상한 (tok/s)")
    for k in ("LPDDR5", "LPDDR5X-8533", "LPDDR5X-10667"):
        bw = dram_bw_gbs(LPDDR_RATES[k])
        print(f"  {k:>14}: INT4 {llm_tokens_per_s(bw, 7, 4):5.1f}, INT8 {llm_tokens_per_s(bw, 7, 8):5.1f}")


# (설명, 계산값, 본문에 쓰는 값, 허용 오차)
def checks():
    return [
        ("LPDDR4X-4266 대역폭 (GB/s)", dram_bw_gbs(4266), 34.1, 0.05),
        ("LPDDR5-6400 대역폭 (GB/s)", dram_bw_gbs(6400), 51.2, 0.05),
        ("LPDDR5X-8533 대역폭 (GB/s)", dram_bw_gbs(8533), 68.3, 0.05),
        ("LPDDR5X-9600 대역폭 (GB/s)", dram_bw_gbs(9600), 76.8, 0.05),
        ("LPDDR5X-10667 대역폭 (GB/s)", dram_bw_gbs(10667), 85.3, 0.05),
        ("UFS 3.x HS-G4 2레인 (Gbps)", ufs_raw_gbps("HS-G4"), 23.3, 0.05),
        ("UFS 4.x HS-G5 2레인 (Gbps)", ufs_raw_gbps("HS-G5"), 46.6, 0.05),
        ("DVFS 전력 비 (3.0→1.5 GHz, 1.0→0.7 V)", dyn_power_ratio(3.0, 1.0, 1.5, 0.7), 0.245, 0.0005),
        ("DVFS 에너지 비", energy_ratio(3.0, 1.0, 1.5, 0.7), 0.49, 0.0005),
        ("120 mm² 웨이퍼당 다이 수", dies_per_wafer(120), 528, 1),
        ("120 mm² 수율 (D0 0.1)", poisson_yield(120, 0.1) * 100, 88.7, 0.05),
        ("100 mm² 웨이퍼당 다이 수", dies_per_wafer(100), 640, 1),
        ("100 mm² 수율 (D0 0.1)", poisson_yield(100, 0.1) * 100, 90.5, 0.05),
        ("150 mm² 웨이퍼당 다이 수", dies_per_wafer(150), 417, 1),
        ("150 mm² 수율 (D0 0.1)", poisson_yield(150, 0.1) * 100, 86.1, 0.05),
        ("100 mm² 양품 다이", dies_per_wafer(100) * poisson_yield(100, 0.1), 579, 1),
        ("120 mm² 양품 다이", dies_per_wafer(120) * poisson_yield(120, 0.1), 468, 1),
        ("150 mm² 양품 다이", dies_per_wafer(150) * poisson_yield(150, 0.1), 359, 1),
        ("4사이클 @3 GHz (ns)", cycles_to_ns(4, 3), 1.33, 0.005),
        ("암달 p=0.9, n=8", amdahl(0.9, 8), 4.71, 0.005),
        ("7B INT4 @LPDDR5X-8533 (tok/s)", llm_tokens_per_s(dram_bw_gbs(8533), 7, 4), 19.5, 0.05),
        ("GPU FP32 1024 ALU @1 GHz (TFLOPS)", gpu_tflops(1024, 1.0), 2.05, 0.005),
        ("GPU FP16 2배속 1024 ALU @1 GHz (TFLOPS)", gpu_tflops(1024, 1.0, rate=2), 4.10, 0.005),
        ("2400×1080 RGBA8 60 fps 1회 쓰기 (GB/s)", framebuffer_gbs(2400, 1080, 4, 60), 0.62, 0.005),
        ("업스케일 2/3 배율 픽셀 비 (%)", render_pixel_ratio(2/3) * 100, 44, 0.5),
        ("업스케일 1/2 배율 픽셀 비 (%)", render_pixel_ratio(0.5) * 100, 25, 0.001),
        ("NPU 4096 MAC @1 GHz INT8 (TOPS)", npu_peak_tops(4096, 1.0), 8.2, 0.05),
        ("같은 NPU INT4 2배 (TOPS)", npu_peak_tops(4096, 1.0) * 2, 16.4, 0.05),
        ("INT4 + 2배 희소성 (TOPS)", npu_peak_tops(4096, 1.0) * 4, 32.8, 0.05),
        ("이용률 40% 유효 (TOPS)", npu_peak_tops(4096, 1.0) * 0.4, 3.3, 0.05),
        ("8.2 TOPS / 2 W (TOPS/W)", npu_peak_tops(4096, 1.0) / 2, 4.1, 0.05),
        ("경계점 8.2 TOPS·LPDDR5X-8533 (ops/byte)", ridge_ops_per_byte(npu_peak_tops(4096, 1.0), dram_bw_gbs(8533)), 120, 0.5),
        ("1B INT4 @LPDDR5X-8533 (tok/s)", llm_tokens_per_s(dram_bw_gbs(8533), 1, 4), 136.5, 0.05),
        ("1B INT8 @LPDDR5X-8533 (tok/s)", llm_tokens_per_s(dram_bw_gbs(8533), 1, 8), 68.3, 0.05),
        ("3B INT4 @LPDDR5X-8533 (tok/s)", llm_tokens_per_s(dram_bw_gbs(8533), 3, 4), 45.5, 0.05),
        ("3B INT8 @LPDDR5X-8533 (tok/s)", llm_tokens_per_s(dram_bw_gbs(8533), 3, 8), 22.8, 0.05),
        ("7B INT8 @LPDDR5X-8533 (tok/s)", llm_tokens_per_s(dram_bw_gbs(8533), 7, 8), 9.8, 0.05),
        ("7B INT4 @LPDDR5X-10667 (tok/s)", llm_tokens_per_s(dram_bw_gbs(10667), 7, 4), 24.4, 0.05),
        ("KV 캐시 32L·8헤드·128·4096·FP16 (GB)", kv_cache_gb(32, 8, 128, 4096), 0.54, 0.005),
        ("7B 프리필 1000토큰 @유효 10 TOPS (s)", prefill_s(7, 1000, 10), 1.4, 0.005),
        ("추측 디코딩 α=0.7, k=4 (토큰)", spec_decode_tokens(0.7, 4), 2.77, 0.005),
        ("12MP 10bit 30fps 센서 (Gbps)", pixel_rate_gbps(4000, 3000, 10, 30), 3.6, 0.005),
        ("50MP(8192×6144) 10bit 30fps (Gbps)", pixel_rate_gbps(8192, 6144, 10, 30), 15.1, 0.05),
        ("4K 10bit 60fps 센서 읽기 (Gbps)", pixel_rate_gbps(3840, 2160, 10, 60), 4.98, 0.005),
        ("D-PHY 4레인 (Gbps)", dphy_gbps(4), 18, 0.05),
        ("C-PHY trio당 6 Gsps (Gbps)", cphy_gbps(1), 13.7, 0.05),
        ("C-PHY 3 trio (Gbps)", cphy_gbps(3), 41.1, 0.05),
        ("C-PHY v2.1 짧은 채널 8 Gsps (Gbps)", cphy_gbps(1, 8.0), 18.3, 0.05),
        ("D-PHY v3.0 레인 (Gbps)", 9.0, 9, 0.001),
        ("12MP 10bit raw 1장 (MB)", frame_mb(4000, 3000, 10), 15, 0.05),
        ("12MP 10bit raw 8장 (MB)", frame_mb(4000, 3000, 10, 8), 120, 0.5),
        ("4K60 10bit 4:2:0 원본 (Gbps)", pixel_rate_gbps(3840, 2160, 15, 60), 7.46, 0.005),
        ("4K60 원본 / 50 Mbps 압축 비", pixel_rate_gbps(3840, 2160, 15, 60) * 1e3 / 50, 150, 1),
        ("8K30 10bit 4:2:0 원본 (Gbps)", pixel_rate_gbps(7680, 4320, 15, 30), 14.9, 0.05),
        ("QHD+ 24bit 120Hz 비압축 (Gbps)", pixel_rate_gbps(1440, 3120, 24, 120), 12.9, 0.05),
        ("QHD+ 120Hz DSC 8bpp (Gbps)", pixel_rate_gbps(1440, 3120, 8, 120), 4.31, 0.005),
        ("4K 30bit 120Hz 비압축 (Gbps)", pixel_rate_gbps(3840, 2160, 30, 120), 29.9, 0.05),
        ("QHD+ 레이어 1장 DRAM 읽기 120Hz (GB/s)", 1440 * 3120 * 4 * 120 / 1e9, 2.16, 0.005),
        ("PCM 48kHz 24bit 스테레오 (Mbps)", pcm_mbps(48000, 24, 2), 2.3, 0.005),
        ("가속도 3축 16bit 100Hz (kbps)", 100 * 3 * 16 / 1e3, 4.8, 0.005),
        ("6축 16bit 100Hz 1분 버퍼 (KB)", 100 * 6 * 2 * 60 / 1e3, 72, 0.05),
        ("PCIe Gen2 x1 (GB/s)", pcie_gbs(2), 0.5, 0.005),
        ("PCIe Gen3 x1 (GB/s)", pcie_gbs(3), 0.98, 0.005),
        ("PCIe Gen4 x1 (GB/s)", pcie_gbs(4), 1.97, 0.005),
        ("PCIe Gen4 x2 (GB/s)", pcie_gbs(4, 2), 3.94, 0.005),
        ("USB 3.2 Gen 1 (GB/s)", usb_gbs("USB 3.2 Gen 1"), 0.5, 0.005),
        ("USB 3.2 Gen 2 (GB/s)", usb_gbs("USB 3.2 Gen 2"), 1.21, 0.005),
        ("USB 2.0 원시 (MB/s)", 480 / 8, 60, 0.5),
        ("SDIO 3.0 SDR104 4비트 (MB/s)", sdio_mbs(208), 104, 0.5),
        ("UART 3 Mbaud 8N1 (kB/s)", uart_kbs(3e6), 300, 0.5),
        ("DP HBR3 4레인 (Gbps)", dp_gbps(), 25.9, 0.05),
        ("GNSS L5/L1 전리층 지연 비", iono_ratio(), 1.79, 0.005),
        ("UWB 499.2 MHz 샘플당 거리 (m)", uwb_sample_m(), 0.60, 0.005),
        ("I3C SDR / I2C Fm 클럭 비", 12.5e6 / 400e3, 31, 0.5),
        ("5000 mAh·3.87 V 배터리 (Wh)", battery_wh(5000), 19.35, 0.005),
        ("평균 1.5 W 사용 시간 (h)", runtime_h(battery_wh(5000), 1.5), 12.9, 0.05),
        ("벅 입력 0.8 V·2 A·효율 85% (W)", regulator_input_w(1.6, 0.85), 1.88, 0.005),
        ("벅 손실 (W)", regulator_input_w(1.6, 0.85) - 1.6, 0.28, 0.005),
        ("LDO 효율 1.0→0.8 V (%)", 0.8 / 1.0 * 100, 80, 0.05),
        ("LDO 손실 0.1 A (mW)", ldo_loss_w(1.0, 0.8, 0.1) * 1000, 20, 0.05),
        ("지속 전력 43/25 °C, 4 °C/W (W)", sustained_power_w(43, 25, 4), 4.5, 0.005),
        ("idle 손익분기 30 µJ, 50→5 mW (ms)", idle_breakeven_ms(30, 50, 5), 0.67, 0.005),
        ("대기 20 mW (일)", runtime_h(battery_wh(5000), 0.020) / 24, 40.3, 0.05),
        ("대기 40 mW (일)", runtime_h(battery_wh(5000), 0.040) / 24, 20.2, 0.05),
        ("60 fps·3.0 W (mJ/frame)", energy_per_frame_mj(3.0, 60), 50, 0.05),
        ("120 fps·4.8 W (mJ/frame)", energy_per_frame_mj(4.8, 120), 40, 0.05),
        ("6자리 PIN 전수 시도, 80 ms/회 (시간)", brute_force_hours(10**6, 80), 22.2, 0.05),
        ("UFS 4.x HS-G5 2레인 (GB/s)", ufs_raw_gbps("HS-G5") / 8, 5.8, 0.05),
        ("110 mm² 웨이퍼당 다이 수", dies_per_wafer(110), 579, 1),
        ("110 mm² 수율 (D0 0.1)", poisson_yield(110, 0.1) * 100, 89.6, 0.05),
        ("110 mm² 수율 (D0 0.2)", poisson_yield(110, 0.2) * 100, 80.3, 0.05),
        ("110 mm² 수율 (D0 0.5)", poisson_yield(110, 0.5) * 100, 57.7, 0.05),
        ("110 mm² 양품 (D0 0.1)", dies_per_wafer(110) * poisson_yield(110, 0.1), 519, 1),
        ("110 mm² 양품 (D0 0.2)", dies_per_wafer(110) * poisson_yield(110, 0.2), 465, 1),
        ("110 mm² 양품 (D0 0.5)", dies_per_wafer(110) * poisson_yield(110, 0.5), 334, 1),
        ("양품당 원가 $20k·D0 0.1 ($)", cost_per_good_die(20000, 110, 0.1), 38.6, 0.05),
        ("양품당 원가 $20k·D0 0.2 ($)", cost_per_good_die(20000, 110, 0.2), 43.0, 0.05),
        ("양품당 원가 $20k·D0 0.5 ($)", cost_per_good_die(20000, 110, 0.5), 59.9, 0.05),
        ("200 mm² 웨이퍼당 다이 수", dies_per_wafer(200), 306, 1),
        ("200 mm² 수율 (D0 0.2)", poisson_yield(200, 0.2) * 100, 67.0, 0.05),
        ("200 mm² 양품 (D0 0.2)", dies_per_wafer(200) * poisson_yield(200, 0.2), 205, 1),
        ("100 mm² 수율 (D0 0.2)", poisson_yield(100, 0.2) * 100, 81.9, 0.05),
        ("100 mm² 양품 (D0 0.2)", dies_per_wafer(100) * poisson_yield(100, 0.2), 524, 1),
        ("100 mm² 2개 세트 (D0 0.2)", dies_per_wafer(100) * poisson_yield(100, 0.2) / 2, 262, 1),
        ("스트레스 안정성 3200/5000 (%)", stability_pct(3200, 5000), 64, 0.05),
        ("칩 A 와트당 점수 5000/8 W", perf_per_watt(5000, 8), 625, 0.5),
        ("칩 B 와트당 점수 4500/6 W", perf_per_watt(4500, 6), 750, 0.5),
        ("B/A 효율 비", perf_per_watt(4500, 6) / perf_per_watt(5000, 8), 1.2, 0.005),
        ("기하 평균 (2, 8)", geomean(2, 8), 4, 0.005),
        ("IPC 3e9/2e9", ipc(3e9, 2e9), 1.5, 0.005),
        ("87 mm² 웨이퍼당 다이 수", dies_per_wafer(87), 741, 1),
        ("87 mm² 수율 (D0 0.1)", poisson_yield(87, 0.1) * 100, 91.7, 0.05),
        ("87 mm² 수율 (D0 0.2)", poisson_yield(87, 0.2) * 100, 84.0, 0.05),
        ("87 mm² 양품 다이 (D0 0.1)", dies_per_wafer(87) * poisson_yield(87, 0.1), 679, 1),
        ("87 mm² 양품 다이 (D0 0.2)", dies_per_wafer(87) * poisson_yield(87, 0.2), 623, 1),
        ("2nm 트랜지스터당 비용 비 (성숙 수율)", die_cost_ratio(100, 0.1, 87, 0.1, 1.3), 1.11, 0.005),
        ("2nm 트랜지스터당 비용 비 (초기 수율)", die_cost_ratio(100, 0.1, 87, 0.2, 1.3), 1.21, 0.005),
        ("128비트 LPDDR5X-8533 (GB/s)", dram_bw_gbs(8533, 128), 136.5, 0.05),
        ("256비트 LPDDR5X-8533 (GB/s)", dram_bw_gbs(8533, 256), 273.1, 0.05),
        ("512비트 LPDDR5X-8533 (GB/s)", dram_bw_gbs(8533, 512), 546.1, 0.05),
        ("10 FIT·1만 시간·100만 대 고장", fit_failures(10, 1e4, 1e6), 100, 0.5),
        ("100 FIT·1만 시간·100만 대 고장", fit_failures(100, 1e4, 1e6), 1000, 0.5),
        ("7B INT4 가중치 크기 (GB)", 7 * 4 / 8, 3.5, 0.005),
        ("12MP 10bit 30fps 바이트 환산 (GB/s)", pixel_rate_gbps(4000, 3000, 10, 30) / 8, 0.45, 0.005),
    ]


def check() -> int:
    bad = 0
    for desc, got, want, tol in checks():
        ok = abs(F(got) - F(want)) <= F(tol)
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {desc}: {got:.4g} (본문 {want:g})")
    print("불일치", bad, "건" if bad else "— 모두 일치")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
