"""기초·CPU·메모리·보안·전력·연결·RISC-V 페이지 보강 그림

1.  basics_cmos_inverter     : CMOS 인버터의 충전·방전 경로 (동적 전력의 출처)
2.  basics_vth_tradeoff      : 문턱 전압에 따른 구동 전류와 누설 전류 (개념도, LVT/SVT/HVT)
3.  basics_dvfs_energy       : 클럭만 낮출 때와 전압도 함께 낮출 때의 전력·성능·에너지 (본문 표 값)
4.  basics_clock_tree        : 수정 발진기 → PLL → 분주·선택 → 클럭 게이트 → 클럭 트리
5.  basics_interconnect_topo : 공유 버스, 크로스바, NoC 메시 비교
6.  basics_axi_channels      : AXI의 다섯 채널
7.  basics_die_yield         : 다이 면적에 따른 웨이퍼당 다이 수·수율·양품 수 (300 mm, D0 = 0.1/cm²)
8.  cpu_ooo_pipeline         : 비순차 코어의 주요 구조 (프런트엔드 → 리네임 → 실행 → 리타이어)
9.  cpu_exception_levels     : Arm 예외 수준 EL0–EL3과 보안 세계
10. memory_controller_slc    : 블록 → 인터커넥트 → SLC → 메모리 컨트롤러 → PHY → LPDDR
11. memory_ufs_stack         : UFS 계층 구조와 세대별 레인당 속도
12. sec_hw_security_placement: TEE · iSE · eSE의 위치
13. power_measurement_setup  : 외부 측정기 · 레일 계측 · 연료 게이지의 측정 위치
14. conn_gnss_uwb_bands      : GNSS L1/L5와 UWB 채널 5·9의 주파수 위치
15. next_riscv_isa           : RISC-V 기본 ISA, 표준 확장, 프로파일의 관계
"""
from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, round_=True, z=2):
    if round_:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))
    else:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, x0, y0, x1, y1, c=None, lw=1.4, style="-|>", ls="-", z=1, rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=12,
                                 color=c or s.INK2, linewidth=lw, linestyle=ls, zorder=z,
                                 connectionstyle=f"arc3,rad={rad}"))


def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    s.bare(ax)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return fig, ax


# ---------------------------------------------------------------- 1. CMOS 인버터
def cmos_inverter():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, (title, charging) in zip(axes, (("input 0 → output rises: PMOS charges C from VDD", True),
                                            ("input 1 → output falls: NMOS discharges C to GND", False))):
        s.bare(ax)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        # 전원·접지 레일
        ax.plot([2, 8], [9.2, 9.2], color=s.INK, lw=2)
        ax.text(8.2, 9.2, "VDD", va="center", fontsize=10, fontweight="bold")
        ax.plot([2, 8], [0.8, 0.8], color=s.INK, lw=2)
        ax.text(8.2, 0.8, "GND", va="center", fontsize=10, fontweight="bold")
        on, off = s.SYNC, s.GRID
        # PMOS / NMOS 상자
        box(ax, 3.2, 6.0, 2.0, 1.8, on if charging else off, "PMOS\n" + ("ON" if charging else "OFF"), fs=9,
            tc="#ffffff" if charging else s.INK2, bold=True)
        box(ax, 3.2, 2.2, 2.0, 1.8, off if charging else on, "NMOS\n" + ("OFF" if charging else "ON"), fs=9,
            tc=s.INK2 if charging else "#ffffff", bold=True)
        ax.plot([4.2, 4.2], [7.8, 9.2], color=s.INK, lw=1.5)
        ax.plot([4.2, 4.2], [4.0, 6.0], color=s.INK, lw=1.5)
        ax.plot([4.2, 4.2], [0.8, 2.2], color=s.INK, lw=1.5)
        # 입력
        ax.plot([1.0, 2.6], [5.0, 5.0], color=s.INK, lw=1.5)
        ax.plot([2.6, 2.6], [3.1, 6.9], color=s.INK, lw=1.5)
        ax.plot([2.6, 3.2], [6.9, 6.9], color=s.INK, lw=1.5)
        ax.plot([2.6, 3.2], [3.1, 3.1], color=s.INK, lw=1.5)
        ax.text(0.9, 5.0, "in = " + ("0" if charging else "1"), ha="right", va="center", fontsize=10)
        # 출력과 부하 C
        ax.plot([4.2, 6.6], [5.0, 5.0], color=s.INK, lw=1.5)
        ax.add_patch(Circle((4.2, 5.0), 0.09, color=s.INK, zorder=3))
        ax.plot([6.6, 6.6], [5.0, 4.0], color=s.INK, lw=1.5)
        ax.plot([6.0, 7.2], [4.0, 4.0], color=s.INK, lw=2.4)
        ax.plot([6.0, 7.2], [3.6, 3.6], color=s.INK, lw=2.4)
        ax.plot([6.6, 6.6], [3.6, 0.8], color=s.INK, lw=1.5)
        ax.text(7.4, 3.8, "load C\n(wires + next gates)", va="center", fontsize=8.5, color=s.INK2)
        ax.text(6.0, 5.35, "out = " + ("1" if charging else "0"), fontsize=10)
        # 전류 경로
        c = s.UL
        if charging:
            ax.annotate("", xy=(6.3, 4.3), xytext=(4.7, 8.7),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2, connectionstyle="arc3,rad=-0.3"))
            ax.text(5.7, 7.6, "charge\n½CV² stored,\n½CV² lost", fontsize=8.5, color=c, fontweight="bold")
        else:
            ax.annotate("", xy=(4.7, 1.3), xytext=(6.3, 4.3),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2, connectionstyle="arc3,rad=-0.3"))
            ax.text(7.0, 1.6, "discharge\n½CV² lost", fontsize=8.5, color=c, fontweight="bold")
        ax.set_title(title, fontsize=10.5, fontweight="bold", color=s.INK)
    fig.text(0.5, 0.01, "one full 0→1→0 cycle draws CV² from the supply  →  P_dyn = α·C·V²·f",
             ha="center", fontsize=10, color=s.INK2)
    s.save(fig, "basics_cmos_inverter")


# ---------------------------------------------------------------- 2. Vth 트레이드오프
def vth_tradeoff():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    vth = np.linspace(0.15, 0.55, 200)
    vdd = 0.75
    ion = (vdd - vth) ** 1.3
    ion = ion / ion.max()
    s_slope = 0.085  # 약 85 mV/decade (가정)
    ioff = 10 ** (-(vth - vth.min()) / s_slope)
    ax.plot(vth, ion, color=s.DL, lw=2.4, label="drive current I_on (speed), linear, normalised")
    ax.set_xlabel("threshold voltage Vth (V)  —  assumed VDD = 0.75 V")
    ax.set_ylabel("relative I_on", color=s.DL)
    ax.set_ylim(0, 1.1)
    ax2 = ax.twinx()
    ax2.semilogy(vth, ioff, color=s.RS, lw=2.4, label="leakage I_off, log scale")
    ax2.set_ylabel("relative I_off (log)", color=s.RS)
    ax2.set_ylim(1e-5, 3)
    for name, v in (("LVT", 0.22), ("SVT", 0.33), ("HVT", 0.45)):
        ax.axvline(v, color=s.GRID, lw=1, ls="--", zorder=0)
        ax.text(v, 1.04, name, ha="center", fontsize=9.5, fontweight="bold", color=s.INK2)
    for a in (ax, ax2):
        a.spines["top"].set_visible(False)
    l1, n1 = ax.get_legend_handles_labels()
    l2, n2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, n1 + n2, loc="lower left", fontsize=8.5, frameon=False)
    ax.set_title("Lower Vth: faster but leakage rises exponentially (conceptual)", fontsize=11, fontweight="bold")
    s.save(fig, "basics_vth_tradeoff")


# ---------------------------------------------------------------- 3. DVFS 에너지
def dvfs_energy():
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    cases = ["baseline\n(f, V)", "clock ½\n(f/2, V)", "clock ½ + voltage 0.7×\n(f/2, 0.7V)"]
    power = [1.0, 0.5, 0.245]
    perf = [1.0, 0.5, 0.5]
    energy = [1.0, 1.0, 0.49]
    x = np.arange(3)
    w = 0.25
    for i, (vals, c, lab) in enumerate(((power, s.UL, "power"), (perf, s.DL, "performance"),
                                        (energy, s.SYNC, "energy for the same work"))):
        bars = ax.bar(x + (i - 1) * w, vals, w * 0.92, color=c, label=lab)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:g}", ha="center", fontsize=9)
    ax.set_xticks(x, cases)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel("relative to baseline")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=9, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    ax.text(2, 0.75, "only lowering V\nsaves energy (V²)", ha="center", fontsize=9, color=s.SYNC,
            fontweight="bold")
    s.save(fig, "basics_dvfs_energy")


# ---------------------------------------------------------------- 4. 클럭 트리
def clock_tree():
    fig, ax = canvas(12, 4.6, (-0.2, 12.4), (-0.6, 5.2))
    box(ax, 0.0, 2.2, 1.7, 1.2, s.EMPTY, "crystal\n(tens of MHz)", fs=8.5, ec=s.INK2)
    box(ax, 2.3, 3.4, 1.6, 1.0, s.CTRL, "PLL A\n(×N → GHz)", fs=8.5)
    box(ax, 2.3, 2.2, 1.6, 1.0, s.CTRL, "PLL B", fs=8.5)
    box(ax, 2.3, 1.0, 1.6, 1.0, s.CTRL, "PLL C", fs=8.5)
    box(ax, 4.6, 1.6, 1.6, 2.4, s.DL, "divider\n+ mux\n(select /\ndivide)", fs=8.5)
    for y in (3.9, 2.7, 1.5):
        arrow(ax, 1.7, 2.8, 2.3, y)
        arrow(ax, 3.9, y, 4.6, min(max(y, 1.9), 3.7))
    box(ax, 6.9, 3.3, 1.4, 0.9, s.SPECIAL, "clock gate", fs=8.5)
    box(ax, 6.9, 1.4, 1.4, 0.9, s.SPECIAL, "clock gate", fs=8.5)
    arrow(ax, 6.2, 3.3, 6.9, 3.75)
    arrow(ax, 6.2, 2.3, 6.9, 1.85)
    ax.text(7.6, 2.75, "enable = 0\n→ no switching", ha="center", fontsize=8, color=s.INK2)

    def tree(x0, y0, label):
        arrow(ax, 8.3, y0, x0, y0)
        ax.plot([x0, x0], [y0 - 0.55, y0 + 0.55], color=s.SYNC, lw=1.6)
        for dy in (-0.55, 0, 0.55):
            ax.plot([x0, x0 + 0.7], [y0 + dy, y0 + dy], color=s.SYNC, lw=1.6)
            for k in range(3):
                ax.add_patch(Rectangle((x0 + 0.8 + k * 0.45, y0 + dy - 0.15), 0.32, 0.3, facecolor=s.EMPTY,
                                       edgecolor=s.INK2, lw=0.8))
        ax.text(x0 + 1.6, y0 + 0.95, label, ha="center", fontsize=8.5, color=s.INK2)

    tree(9.0, 3.75, "clock tree → flip-flops (CPU cluster)")
    tree(9.0, 1.85, "clock tree → flip-flops (GPU)")
    box(ax, 0.0, 0.0, 1.7, 0.9, s.EMPTY, "32.768 kHz", fs=8.5, ec=s.INK2)
    arrow(ax, 1.7, 0.45, 4.0, 0.45)
    ax.text(4.1, 0.45, "RTC, deep-sleep timers (always-on domain)", va="center", fontsize=8.5, color=s.INK2)
    ax.text(6.2, 4.95, "generate → select / divide → gate → distribute", ha="center", fontsize=10,
            fontweight="bold", color=s.INK)
    s.save(fig, "basics_clock_tree")


# ---------------------------------------------------------------- 5. 인터커넥트 토폴로지
def interconnect_topo():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
    names = ["CPU", "GPU", "NPU", "ISP", "DMA", "MC"]
    cols = [s.DL, s.ALT, s.CTRL, s.SYNC, s.SPECIAL, s.UL]
    # 공유 버스
    ax = axes[0]
    s.bare(ax); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.add_patch(Rectangle((0.5, 3.7), 9, 0.6, facecolor=s.INK2, edgecolor="none"))
    ax.text(5, 4.0, "shared bus", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    for i, (n, c) in enumerate(zip(names, cols)):
        x = 0.9 + (i % 3) * 3.1
        y = 6.0 if i < 3 else 0.9
        box(ax, x, y, 2.0, 1.1, c, n, fs=9, bold=True)
        ax.plot([x + 1.0, x + 1.0], [y if i < 3 else y + 1.1, 4.3 if i < 3 else 3.7], color=s.INK2, lw=1.4)
    ax.set_title("Shared bus\none transfer at a time", fontsize=10.5, fontweight="bold")
    # 크로스바
    ax = axes[1]
    s.bare(ax); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    mast = names[:4]
    slv = ["MC 0", "MC 1", "SRAM", "regs"]
    for i, (n, c) in enumerate(zip(mast, cols)):
        box(ax, 0.2, 6.2 - i * 1.6, 2.0, 1.1, c, n, fs=9, bold=True)
        for j in range(4):
            ax.plot([2.2, 7.8], [6.75 - i * 1.6, 6.75 - j * 1.6], color=s.GRID, lw=1.1, zorder=0)
    for j, n in enumerate(slv):
        box(ax, 7.8, 6.2 - j * 1.6, 2.0, 1.1, s.UL, n, fs=9, bold=True)
    ax.plot([2.2, 7.8], [6.75, 5.15], color=s.DL, lw=2.4)
    ax.plot([2.2, 7.8], [3.55, 6.75], color=s.CTRL, lw=2.4)
    ax.set_title("Crossbar\nparallel pairs, wires grow ~N²", fontsize=10.5, fontweight="bold")
    # NoC 메시
    ax = axes[2]
    s.bare(ax); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    pts = [(2.2 + 2.8 * i, 1.6 + 2.6 * j) for j in range(3) for i in range(3)]
    for (x, y) in pts:
        if x + 2.8 < 9.5:
            ax.plot([x, x + 2.8], [y, y], color=s.INK2, lw=1.6, zorder=1)
        if y + 2.6 < 8.0:
            ax.plot([x, x], [y, y + 2.6], color=s.INK2, lw=1.6, zorder=1)
    blocks = ["CPU", "GPU", "NPU", "ISP", "DSP", "DPU", "MC 0", "MC 1", "SLC"]
    bc = [s.DL, s.ALT, s.CTRL, s.SYNC, s.SYNC, s.ALT, s.UL, s.UL, s.SPECIAL]
    for (x, y), n, c in zip(pts, blocks, bc):
        ax.add_patch(Rectangle((x - 0.32, y - 0.32), 0.64, 0.64, facecolor=s.SURFACE, edgecolor=s.INK2,
                               lw=1.2, zorder=2))
        box(ax, x - 1.15, y + 0.35, 1.2, 0.7, c, n, fs=7.5, bold=True, z=3)
    ax.annotate("", xy=(7.8, 6.8), xytext=(2.2, 1.6),
                arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=1.8, connectionstyle="angle,angleA=0,angleB=90"))
    ax.text(5.0, 0.5, "□ router   packets hop router to router", ha="center", fontsize=8.5, color=s.INK2)
    ax.set_title("Network-on-Chip (mesh)\nscales, QoS per route", fontsize=10.5, fontweight="bold")
    s.save(fig, "basics_interconnect_topo")


# ---------------------------------------------------------------- 6. AXI 채널
def axi_channels():
    fig, ax = canvas(9.5, 4.4, (0, 10), (0, 6.6))
    box(ax, 0.3, 0.6, 2.2, 5.4, s.DL, "manager\n(master)\ne.g. CPU, DMA", fs=10, bold=True)
    box(ax, 7.5, 0.6, 2.2, 5.4, s.UL, "subordinate\n(slave)\ne.g. memory\ncontroller", fs=10, bold=True)
    rows = [("AR  read address", True, s.CTRL), ("R   read data + response", False, s.CTRL),
            ("AW  write address", True, s.SYNC), ("W   write data + byte strobes", True, s.SYNC),
            ("B   write response", False, s.SYNC)]
    for i, (lab, fwd, c) in enumerate(rows):
        y = 5.3 - i * 1.05
        if fwd:
            arrow(ax, 2.6, y, 7.4, y, c=c, lw=2.2)
        else:
            arrow(ax, 7.4, y, 2.6, y, c=c, lw=2.2)
        ax.text(5.0, y + 0.18, lab, ha="center", va="bottom", fontsize=9.5, color=c, fontweight="bold")
    ax.text(5.0, 0.15, "5 independent channels, each with its own VALID/READY handshake; IDs allow out-of-order responses",
            ha="center", fontsize=8.5, color=s.INK2)
    s.save(fig, "basics_axi_channels")


# ---------------------------------------------------------------- 7. 다이 면적과 수율
def die_yield():
    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    d = 300.0
    r = d / 2
    A = np.linspace(40, 250, 300)  # mm²
    n = math.pi * r ** 2 / A - math.pi * d / np.sqrt(2 * A)
    y = np.exp(-A / 100 * 0.1)
    good = n * y
    ax.plot(A, n, color=s.DL, lw=2.2, label="dies per wafer (gross)")
    ax.plot(A, good, color=s.SYNC, lw=2.6, label="good dies (× Poisson yield)")
    for a in (100, 120, 150):
        nn = math.pi * r ** 2 / a - math.pi * d / math.sqrt(2 * a)
        g = nn * math.exp(-a / 100 * 0.1)
        ax.plot([a], [g], "o", color=s.SYNC)
        ax.text(a + 3, g + 25, f"{a} mm²: ≈{g:.0f}", fontsize=8.5, color=s.INK)
    ax.set_xlabel("die area (mm²)")
    ax.set_ylabel("dies per 300 mm wafer")
    ax.set_ylim(0, 1700)
    ax2 = ax.twinx()
    ax2.plot(A, y * 100, color=s.UL, lw=1.8, ls="--", label="yield (%)")
    ax2.set_ylim(70, 100)
    ax2.set_ylabel("yield (%)", color=s.UL)
    for a in (ax, ax2):
        a.spines["top"].set_visible(False)
    l1, n1 = ax.get_legend_handles_labels()
    l2, n2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, n1 + n2, frameon=False, fontsize=9, loc="upper right")
    ax.set_title("Bigger die → fewer dies and lower yield (assumed D0 = 0.1 /cm²)", fontsize=11,
                 fontweight="bold")
    s.save(fig, "basics_die_yield")


# ---------------------------------------------------------------- 8. 비순차 파이프라인
def ooo_pipeline():
    fig, ax = canvas(13, 5.0, (-0.2, 13.4), (-0.8, 5.6))
    fe, mid, ex, mem = s.DL, s.CTRL, s.SYNC, s.UL
    box(ax, 0.0, 3.8, 2.2, 1.0, fe, "branch predictor\n+ BTB", fs=8.5)
    box(ax, 0.0, 2.5, 2.2, 1.0, fe, "L1 I-cache\n/ µop cache", fs=8.5)
    box(ax, 2.7, 2.5, 1.6, 2.3, fe, "decode\n(N wide)", fs=9, bold=True)
    box(ax, 4.8, 2.5, 1.8, 2.3, mid, "rename\n+ dispatch", fs=9, bold=True)
    box(ax, 7.1, 3.6, 2.0, 1.2, mid, "schedulers\n(issue queues)", fs=8.5)
    box(ax, 7.1, 0.3, 6.0, 1.0, mid, "ROB (reorder buffer) — hundreds of entries, retire in program order", fs=9)
    ex_units = ["ALU", "ALU", "ALU", "branch", "FP/SIMD", "FP/SIMD", "load", "store"]
    for i, n in enumerate(ex_units):
        c = mem if n in ("load", "store") else ex
        box(ax, 9.6 + (i % 4) * 0.9, 3.9 - (i // 4) * 1.0, 0.82, 0.8, c, n, fs=7.5)
    box(ax, 9.6, 1.6, 1.7, 0.75, mem, "load/store\nqueues", fs=7.5)
    box(ax, 11.5, 1.6, 1.7, 0.75, mem, "L1 D-cache\n+ TLB", fs=7.5)
    arrow(ax, 1.1, 3.8, 1.1, 3.5)
    arrow(ax, 2.2, 3.0, 2.7, 3.0)
    arrow(ax, 4.3, 3.65, 4.8, 3.65)
    arrow(ax, 6.6, 4.2, 7.1, 4.2)
    arrow(ax, 9.1, 4.2, 9.6, 4.2)
    arrow(ax, 5.7, 2.5, 7.1, 0.8, rad=0.2)
    arrow(ax, 11.3, 1.97, 11.5, 1.97)
    ax.text(1.1, 5.15, "front end", ha="center", fontsize=10, fontweight="bold", color=fe)
    ax.text(5.7, 5.15, "in order", ha="center", fontsize=10, fontweight="bold", color=mid)
    ax.text(11.2, 5.15, "out of order execution", ha="center", fontsize=10, fontweight="bold", color=ex)
    ax.text(10.1, -0.5, "results written back; ROB retires them in order", ha="center", fontsize=8.5, color=s.INK2)
    s.save(fig, "cpu_ooo_pipeline")


# ---------------------------------------------------------------- 9. 예외 수준
def exception_levels():
    fig, ax = canvas(10, 5.4, (0, 10), (0, 7.4))
    ax.text(2.6, 7.0, "Normal world", ha="center", fontsize=11, fontweight="bold", color=s.DL)
    ax.text(7.4, 7.0, "Secure world", ha="center", fontsize=11, fontweight="bold", color=s.CTRL)
    rows = [("EL0", "apps, system services", "trusted apps (TAs)", 5.4),
            ("EL1", "OS kernel (Linux)", "trusted OS (e.g. Trusty, QTEE)", 3.9),
            ("EL2", "hypervisor (e.g. pKVM)", "secure partition manager\n(S-EL2, Armv8.4+)", 2.4)]
    for el, nl, sl, y in rows:
        box(ax, 0.6, y, 4.0, 1.2, s.DL, nl, fs=9)
        box(ax, 5.4, y, 4.0, 1.2, s.CTRL, sl, fs=9)
        ax.text(0.45, y + 0.6, el, ha="right", va="center", fontsize=10, fontweight="bold", color=s.INK)
    box(ax, 0.6, 0.6, 8.8, 1.3, s.INK2, "EL3 — secure monitor (e.g. Trusted Firmware-A): switches between worlds",
        fs=9.5, bold=True)
    ax.text(0.45, 1.25, "EL3", ha="right", va="center", fontsize=10, fontweight="bold")
    arrow(ax, 9.75, 1.0, 9.75, 6.4, c=s.RS, lw=1.4, style="<|-")
    ax.text(9.9, 3.7, "privilege", rotation=90, va="center", fontsize=8.5, color=s.RS)
    ax.plot([5.0, 5.0], [2.2, 6.8], color=s.GRID, lw=1.4, ls="--")
    s.save(fig, "cpu_exception_levels")


# ---------------------------------------------------------------- 10. 메모리 컨트롤러와 SLC
def controller_slc():
    fig, ax = canvas(12.5, 4.8, (-0.2, 12.8), (-0.6, 5.4))
    masters = [("CPU", s.DL), ("GPU", s.ALT), ("NPU", s.CTRL), ("ISP", s.SYNC), ("display", s.SPECIAL)]
    for i, (n, c) in enumerate(masters):
        box(ax, 0.0, 4.2 - i * 1.0, 1.6, 0.8, c, n, fs=9, bold=True)
        arrow(ax, 1.6, 4.6 - i * 1.0, 2.3, 2.6)
    box(ax, 2.3, 0.7, 1.4, 3.8, s.INK2, "inter-\nconnect\n/ NoC", fs=9, bold=True)
    box(ax, 4.3, 0.7, 2.0, 3.8, s.SPECIAL, "SLC\n(system-level\ncache)\nshared by all", fs=9, bold=True)
    box(ax, 6.9, 0.7, 2.4, 3.8, s.UL, "", fs=9)
    ax.text(8.1, 4.15, "memory controller", ha="center", fontsize=9, color="white", fontweight="bold")
    for i, n in enumerate(("request queues\n+ reorder", "QoS / priority", "refresh · power")):
        box(ax, 7.1, 2.85 - i * 1.0, 2.0, 0.8, s.SURFACE, n, fs=7.8, tc=s.INK, z=3)
    box(ax, 9.9, 0.7, 1.0, 3.8, s.CTRL, "PHY", fs=9, bold=True)
    for i in range(4):
        box(ax, 11.4, 4.0 - i * 1.05, 1.3, 0.8, s.DL, f"LPDDR\nch {i}", fs=7.8)
        arrow(ax, 10.9, 2.6, 11.4, 4.4 - i * 1.05, style="<|-|>", lw=1.1)
    arrow(ax, 3.7, 2.6, 4.3, 2.6, style="<|-|>")
    arrow(ax, 6.3, 2.6, 6.9, 2.6, style="<|-|>")
    arrow(ax, 9.3, 2.6, 9.9, 2.6, style="<|-|>")
    ax.annotate("", xy=(1.6, 0.5), xytext=(5.3, 0.6),
                arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=1.8, ls="--", connectionstyle="arc3,rad=-0.25"))
    ax.text(3.4, -0.45, "SLC hit: e.g. static frame for display — DRAM can stay asleep", ha="center", fontsize=8.5,
            color=s.RS)
    s.save(fig, "memory_controller_slc")


# ---------------------------------------------------------------- 11. UFS
def ufs_stack():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})
    s.bare(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    layers = [("application", "UFS command set (SCSI based), logical units", s.DL),
              ("transport", "UTP — commands / data / responses as UPIU packets", s.CTRL),
              ("link", "MIPI UniPro — reliable delivery, flow control", s.SYNC),
              ("physical", "MIPI M-PHY — high-speed differential lanes, gears", s.UL)]
    for i, (n, d, c) in enumerate(layers):
        y = 5.4 - i * 1.3
        box(ax, 0.2, y, 1.9, 1.1, c, n, fs=9, bold=True)
        box(ax, 2.3, y, 7.4, 1.1, c, d, fs=8.2)
    ax.text(6.0, 0.55, "host (SoC) ⇄ device (UFS controller + NAND): same layers on both sides\nM-PHY: 2 lanes each way, full duplex",
            ha="center", fontsize=8, color=s.INK2)
    ax.set_title("UFS layers", fontsize=11, fontweight="bold")
    gens = ["UFS 2.1\nHS-G3", "UFS 3.1\nHS-G4", "UFS 4.0/4.1\nHS-G5"]
    lane = [5.8, 11.7, 23.3]
    two = [11.7, 23.3, 46.6]
    bars = bx.bar(gens, lane, color=[s.GRID, s.DL, s.UL], width=0.6)
    for b, v, t in zip(bars, lane, two):
        bx.text(b.get_x() + b.get_width() / 2, v + 0.5, f"≈{v} Gbps/lane\n(2 lanes ≈{t})",
                ha="center", fontsize=8.5)
    bx.set_ylim(0, 30)
    bx.set_ylabel("raw rate per lane, Rate B (Gbps)")
    bx.spines[["top", "right"]].set_visible(False)
    bx.set_title("Link rate doubles each gear", fontsize=11, fontweight="bold")
    s.save(fig, "memory_ufs_stack")


# ---------------------------------------------------------------- 12. 하드웨어 보안 위치
def hw_security_placement():
    fig, ax = canvas(12, 5.0, (0, 12.4), (-0.4, 6.4))
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 8.4, 5.6, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.6))
    ax.text(0.45, 5.7, "SoC die", fontsize=10, fontweight="bold", color=s.INK2)
    box(ax, 0.6, 2.6, 4.2, 2.7, s.DL, "", fs=9)
    ax.text(2.7, 5.0, "application CPU", ha="center", color="white", fontsize=9.5, fontweight="bold")
    box(ax, 0.8, 2.8, 1.8, 1.8, s.SURFACE, "normal world\nAndroid / Linux", fs=8, tc=s.INK, z=3)
    box(ax, 2.8, 2.8, 1.8, 1.8, s.CTRL, "TEE\n(secure world)\nshares CPU,\ncache, DRAM", fs=7.8, z=3)
    box(ax, 5.3, 2.6, 3.0, 2.7, s.SYNC, "iSE\nisolated security\nsubsystem\nown core, ROM, RAM,\ncrypto, TRNG", fs=8.2,
        bold=False)
    box(ax, 0.6, 0.7, 7.7, 1.3, s.INK2, "interconnect · shared DRAM controller", fs=9)
    box(ax, 9.4, 2.6, 2.8, 2.7, s.UL, "eSE / discrete\nsecurity chip\n(e.g. Titan M2)", fs=8.5, bold=True)
    arrow(ax, 8.6, 3.95, 9.4, 3.95, style="<|-|>", lw=1.6)
    ax.text(9.0, 4.25, "SPI / I²C", ha="center", fontsize=8, color=s.INK2)
    for x, t in ((2.7, "fast, no extra chip\nsoftware/side-channel exposure"),
                 (6.8, "on-die but isolated\nfast internal link"),
                 (10.8, "physically separate\nslow bus, extra part")):
        ax.text(x, -0.25, t, ha="center", fontsize=8.2, color=s.INK2)
    ax.text(6.2, 6.15, "more isolation →", ha="center", fontsize=10, color=s.RS, fontweight="bold")
    s.save(fig, "sec_hw_security_placement")


# ---------------------------------------------------------------- 13. 전력 측정 위치
def measurement_setup():
    fig, ax = canvas(12, 4.8, (0, 12.4), (-0.4, 6.0))
    box(ax, 0.2, 2.0, 2.4, 2.0, s.UL, "external power\nmonitor\n(replaces battery)", fs=8.8, bold=True)
    box(ax, 3.4, 2.0, 1.6, 2.0, s.SPECIAL, "battery\n+ fuel\ngauge", fs=8.8, bold=True)
    box(ax, 5.8, 2.0, 1.6, 2.0, s.CTRL, "PMIC\n(rails)", fs=9, bold=True)
    rails = [("CPU rail", s.DL), ("GPU rail", s.ALT), ("DRAM rail", s.SYNC), ("display / other", s.GRID)]
    for i, (n, c) in enumerate(rails):
        y = 4.5 - i * 1.15
        box(ax, 9.2, y, 2.6, 0.85, c, n, fs=8.5, tc=s.INK if c == s.GRID else None)
        ax.add_patch(Rectangle((8.2, y + 0.25), 0.5, 0.35, facecolor=s.SURFACE, edgecolor=s.INK2, lw=1))
        ax.plot([7.4, 8.2], [3.0, y + 0.42], color=s.INK2, lw=1.2)
        ax.plot([8.7, 9.2], [y + 0.42, y + 0.42], color=s.INK2, lw=1.2)
    ax.text(8.45, 5.55, "shunt / on-device\nrail meter (ODPM)", ha="center", fontsize=8, color=s.INK2)
    arrow(ax, 2.6, 3.0, 3.4, 3.0, lw=2, c=s.UL)
    arrow(ax, 5.0, 3.0, 5.8, 3.0, lw=2, c=s.UL)
    notes = [(1.4, "whole device,\nhigh sample rate"), (4.2, "any device,\nlow resolution"),
             (10.0, "per rail,\nsynced with Perfetto")]
    for x, t in notes:
        ax.text(x, 0.55, t, ha="center", fontsize=8.5, color=s.INK2)
    ax.text(6.2, -0.3, "energy (J) = average power (W) × time (s)", ha="center", fontsize=9.5, fontweight="bold")
    s.save(fig, "power_measurement_setup")


# ---------------------------------------------------------------- 14. GNSS·UWB 대역
def gnss_uwb_bands():
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.set_xscale("log")
    ax.set_xlim(900, 13000)
    ax.set_ylim(0, 3.2)
    ax.set_yticks([])
    for sp in ("left", "right", "top"):
        ax.spines[sp].set_visible(False)
    bands = [("GNSS L5 / E5a / B2a\n1176.45 MHz", 1176.45, 20, s.DL, 1.0, "right"),
             ("GNSS L1 / E1 / B1\n1575.42 MHz", 1575.42, 20, s.DL, 1.0, "left"),
             ("UWB ch 5\n≈6.5 GHz\n499.2 MHz wide", 6489.6, 499.2, s.UL, 2.0, "right"),
             ("UWB ch 9\n≈8.0 GHz\n499.2 MHz wide", 7987.2, 499.2, s.UL, 2.0, "left")]
    for lab, fc, bw, c, h, side in bands:
        ax.add_patch(Rectangle((fc - bw / 2, 0), bw, h, facecolor=c, edgecolor="none", alpha=0.85))
        x = fc - bw / 2 - fc * 0.03 if side == "right" else fc + bw / 2 + fc * 0.03
        ax.text(x, h * 0.55, lab, ha=side, va="center", fontsize=8.5, color=s.INK)
    ax.set_xticks([1000, 1500, 2000, 3000, 5000, 7000, 10000],
                  ["1 GHz", "1.5", "2", "3", "5", "7", "10 GHz"])
    ax.minorticks_off()
    ax.set_xlabel("frequency (log scale)")
    ax.text(1360, 2.6, "narrow GNSS signals\n(receive only)", ha="center", fontsize=9, color=s.DL,
            fontweight="bold")
    ax.text(7200, 2.75, "UWB: very wide channels\n→ fine time (distance) resolution",
            ha="center", fontsize=9, color=s.UL, fontweight="bold")
    s.save(fig, "conn_gnss_uwb_bands")


# ---------------------------------------------------------------- 15. RISC-V ISA
def riscv_isa():
    fig, ax = canvas(11.5, 4.8, (0, 12.0), (-0.4, 6.2))
    box(ax, 0.4, 0.4, 8.95, 1.1, s.INK2, "base integer ISA: RV32I / RV64I (small, frozen core)", fs=9.5, bold=True)
    ext = [("M", "mul/div"), ("A", "atomics"), ("F", "single FP"), ("D", "double FP")]
    for i, (k, d) in enumerate(ext):
        box(ax, 0.4 + i * 1.3, 1.8, 1.2, 1.3, s.DL, f"{k}\n{d}", fs=8.5, bold=True)
    ax.add_patch(FancyBboxPatch((0.3, 1.7), 5.2, 1.5, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor="none", edgecolor=s.DL, lw=1.6, ls="--"))
    ax.text(2.9, 3.35, "IMAFD (+Zicsr, Zifencei) = \"G\" general purpose", ha="center", fontsize=8.5, color=s.DL)
    for i, (k, d, c) in enumerate((("C", "compressed\n16-bit", s.SYNC), ("V", "vector\n(VLA)", s.CTRL),
                                   ("H", "hyper-\nvisor", s.CTRL))):
        box(ax, 5.7 + i * 1.25, 1.8, 1.15, 1.3, c, f"{k}\n{d}", fs=8, bold=True)
    box(ax, 0.4, 4.0, 8.95, 1.0, s.SURFACE, "vendor custom extensions (allowed — flexibility and fragmentation)", fs=8.8,
        tc=s.INK, ec=s.MUTED)
    box(ax, 9.7, 0.4, 2.2, 4.6, s.UL, "profile\n(e.g. RVA23)\n\nthe set an\napplication\nprocessor must\nimplement\n(V and H\nmandatory)",
        fs=8.8, bold=True)
    arrow(ax, 9.35, 2.45, 9.7, 2.45, lw=1.6)
    ax.text(6.0, 5.6, "small base + optional standard extensions + profiles for OS/app compatibility",
            ha="center", fontsize=10, fontweight="bold")
    s.save(fig, "next_riscv_isa")


if __name__ == "__main__":
    s.setup()
    cmos_inverter()
    vth_tradeoff()
    dvfs_energy()
    clock_tree()
    interconnect_topo()
    axi_channels()
    die_yield()
    ooo_pipeline()
    exception_levels()
    controller_slc()
    ufs_stack()
    hw_security_placement()
    measurement_setup()
    gnss_uwb_bands()
    riscv_isa()
