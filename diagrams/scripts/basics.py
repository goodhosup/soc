"""시작하기·공통 기초 그림

1. soc_blocks        : 스마트폰 SoC의 일반적인 블록 구성과 인터커넥트, 외부 메모리
2. memory_hierarchy  : 메모리 계층별 용량과 접근 지연 (로그 축, 대표 범위)
3. dvfs_curve        : 동작점(OPP)별 주파수–전압과 상대 동적 전력 (개념도)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, round_=True):
    if round_:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=fc, edgecolor=ec, linewidth=lw))
    else:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


# ---------------------------------------------------------------- 1. SoC 블록
def soc_blocks():
    fig, ax = plt.subplots(figsize=(12, 6.6))
    s.bare(ax)
    ax.set_xlim(-0.3, 12.3)
    ax.set_ylim(-1.6, 6.4)

    # 다이 외곽
    ax.add_patch(FancyBboxPatch((0, 0), 10.2, 6.0, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, linewidth=1.6))
    ax.text(0.2, 5.75, "SoC die", fontsize=10, color=s.INK2, va="center", fontweight="bold")

    compute, media, conn, sys_, mem = s.DL, s.ALT, s.SYNC, s.CTRL, s.UL
    # 연산 블록 (윗줄)
    box(ax, 0.3, 3.9, 2.9, 1.5, compute, "CPU clusters\n(prime / perf / eff)\n+ shared L2/L3", fs=9, bold=True)
    box(ax, 3.4, 3.9, 2.1, 1.5, compute, "GPU", fs=10, bold=True)
    box(ax, 5.7, 3.9, 2.1, 1.5, compute, "NPU", fs=10, bold=True)
    box(ax, 8.0, 3.9, 1.9, 1.5, compute, "DSP", fs=10, bold=True)

    # 인터커넥트
    box(ax, 0.3, 2.95, 9.6, 0.65, s.INK2, "Interconnect / NoC  +  System Level Cache (SLC)", fs=9.5, round_=False)

    # 아랫줄: 멀티미디어·연결·시스템
    row = [("ISP", media), ("Video\ncodec", media), ("Display\n(DPU)", media), ("Audio", media),
           ("Modem", conn), ("Wi-Fi/BT\n(or ext.)", conn), ("Security\n(TEE/SE)", sys_),
           ("Power mgmt\nMCU", sys_)]
    w, g = 1.1, 0.114
    for i, (lab, c) in enumerate(row):
        box(ax, 0.3 + i * (w + g), 1.35, w, 1.3, c, lab, fs=8.2)

    # 메모리 컨트롤러·I/O
    box(ax, 0.3, 0.3, 4.6, 0.75, mem, "Memory controllers (LPDDR PHY)", fs=9)
    box(ax, 5.1, 0.3, 4.8, 0.75, sys_, "I/O: UFS · PCIe · USB · MIPI · I2C/I3C/SPI", fs=9)

    # 외부 칩
    box(ax, 10.6, 3.9, 1.6, 1.5, mem, "LPDDR\nDRAM\n(PoP)", fs=9, bold=True)
    box(ax, 10.6, 1.35, 1.6, 1.3, sys_, "UFS\nstorage", fs=9)
    box(ax, 10.6, 0.0, 1.6, 0.95, sys_, "PMIC", fs=9)
    ax.annotate("", xy=(10.6, 4.4), xytext=(9.9, 3.27),
                arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=1.2))
    ax.annotate("", xy=(10.6, 2.0), xytext=(9.9, 0.68),
                arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=1.2))

    # 범례
    items = [(compute, "compute"), (media, "multimedia"), (conn, "connectivity"),
             (sys_, "system / I/O"), (mem, "memory")]
    for i, (c, lab) in enumerate(items):
        x = 0.3 + i * 2.2
        ax.add_patch(Rectangle((x, -1.1), 0.35, 0.35, color=c))
        ax.text(x + 0.5, -0.92, lab, fontsize=9, va="center", color=s.INK2)
    s.save(fig, "basics_soc_blocks")


# ---------------------------------------------------------------- 2. 메모리 계층
def memory_hierarchy():
    # (이름, 용량 범위 바이트, 지연 범위 ns) — 대표 범위, 칩마다 다름
    levels = [
        ("Registers", (1e3, 4e3), (0.2, 0.4), s.CTRL),
        ("L1 cache", (6.4e4, 1.3e5), (0.8, 1.5), s.DL),
        ("L2 cache", (5e5, 1.6e7), (3, 6), s.DL),
        ("L3 / SLC", (4e6, 3.2e7), (8, 25), s.SYNC),
        ("LPDDR DRAM", (8e9, 2.4e10), (80, 150), s.UL),
        ("UFS storage", (1.28e11, 1e12), (5e4, 2e5), s.RS),
    ]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    for name, (c0, c1), (l0, l1), col in levels:
        ax.add_patch(Rectangle((c0, l0), c1 - c0, l1 - l0, facecolor=col, alpha=0.85, edgecolor="none"))
        ax.text(c1 * 1.25, (l0 * l1) ** 0.5, name, va="center", fontsize=9.5, color=s.INK)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(3e2, 3e13)
    ax.set_ylim(0.1, 1e6)
    ax.set_xlabel("capacity (bytes, log)")
    ax.set_ylabel("access latency (ns, log)")
    ax.grid(True, which="major", color=s.GRID, lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([1e3, 1e6, 1e9, 1e12], ["1 KB", "1 MB", "1 GB", "1 TB"])
    ax.set_yticks([1, 10, 100, 1e3, 1e4, 1e5, 1e6], ["1 ns", "10 ns", "100 ns", "1 µs", "10 µs", "100 µs", "1 ms"])
    s.save(fig, "basics_memory_hierarchy")


# ---------------------------------------------------------------- 3. DVFS 곡선
def dvfs_curve():
    # 개념용 OPP 표 (특정 칩 값 아님): 주파수 GHz, 전압 V
    opp = [(0.6, 0.55), (1.0, 0.60), (1.4, 0.66), (1.8, 0.73), (2.2, 0.82), (2.6, 0.92), (3.0, 1.05)]
    f = [o[0] for o in opp]
    v = [o[1] for o in opp]
    p = [vi * vi * fi for fi, vi in opp]
    pmax = p[-1]
    fig, ax1 = plt.subplots(figsize=(9, 4.6))
    ax1.plot(f, v, marker="o", color=s.DL, lw=2, label="voltage (V)")
    ax1.set_xlabel("frequency (GHz)")
    ax1.set_ylabel("voltage (V)", color=s.DL)
    ax1.set_ylim(0.4, 1.15)
    ax2 = ax1.twinx()
    ax2.bar(f, [x / pmax * 100 for x in p], width=0.18, color=s.UL, alpha=0.55, label="relative dynamic power (%)")
    ax2.set_ylabel("relative dynamic power (%)", color=s.UL)
    ax2.set_ylim(0, 110)
    for a in (ax1, ax2):
        a.spines["top"].set_visible(False)
    ax1.grid(True, axis="y", color=s.GRID, lw=0.6)
    ax1.set_zorder(ax2.get_zorder() + 1)
    ax1.patch.set_visible(False)
    ax1.text(0.6, 1.09, "conceptual OPP table (not a specific chip)", fontsize=9, color=s.MUTED)
    s.save(fig, "basics_dvfs_curve")


if __name__ == "__main__":
    s.setup()
    soc_blocks()
    memory_hierarchy()
    dvfs_curve()
