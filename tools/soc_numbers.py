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
