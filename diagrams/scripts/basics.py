"""시작하기·공통 기초 그림

1. soc_blocks        : 스마트폰 SoC의 일반적인 블록 구성과 인터커넥트, 외부 메모리
2. memory_hierarchy  : 메모리 계층별 용량과 접근 지연 (로그 축, 대표 범위)
3. dvfs_curve        : 동작점(OPP)별 주파수–전압과 상대 동적 전력 (개념도)
4. transistor_3d     : 평면 · FinFET · GAA 나노시트 · CFET 입체 개념도
5. transistor_xsec   : 채널 단면에서 본 게이트 감싸기 (1면 · 3면 · 4면 · 적층)
"""
from __future__ import annotations

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


# ---------------------------------------------------------------- 4–5. 트랜지스터 구조
def _shade(c, f):
    r, g, b = mcolors.to_rgb(c)
    if f >= 1:
        return (r + (1 - r) * (f - 1), g + (1 - g) * (f - 1), b + (1 - b) * (f - 1))
    return (r * f, g * f, b * f)


def _cuboid(ax, x0, y0, z0, dx, dy, dz, c, kx=0.55, ky=0.42):
    """사투영(oblique) 직육면체: 앞면·윗면·오른쪽 면만 그린다. 그리는 순서는 호출하는 쪽이 정한다."""
    def P(x, y, z):
        return (x + kx * y, z + ky * y)
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    front = [P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)]
    top = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
    side = [P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)]
    for pts, f in ((front, 1.0), (top, 1.35), (side, 0.78)):
        ax.add_patch(Polygon(pts, closed=True, facecolor=_shade(c, f), edgecolor="#ffffff", lw=0.8))


def transistor_3d():
    sub, ch, gate, pch = "#c9c7c1", s.DL, s.UL, s.ALT
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.9))
    titles = ["Planar MOSFET\n(gate on 1 side)", "FinFET\n(gate on 3 sides)",
              "GAA nanosheet\n(gate on all 4 sides)", "CFET (research)\n(nFET + pFET stacked)"]
    L, W = 6.0, 3.0           # 채널 방향(x) 길이, 폭 방향(y) 깊이
    gx0, gx1 = 2.3, 3.7       # 게이트 위치(x)
    for ax, t in zip(axes, titles):
        s.bare(ax)
        ax.set_xlim(-0.3, 8.2)
        ax.set_ylim(-0.6, 5.6)
        ax.set_aspect("equal")
        ax.set_title(t, fontsize=10, color=s.INK, pad=4)

    # (a) 평면: 기판 위 얕은 채널, 그 위에 게이트
    ax = axes[0]
    _cuboid(ax, 0, 0, 0, L, W, 1.4, sub)
    _cuboid(ax, 0, 0.6, 1.4, gx0, 1.8, 0.15, ch)
    _cuboid(ax, gx0, 0.6, 1.4, gx1 - gx0, 1.8, 0.15, ch)
    _cuboid(ax, gx1, 0.6, 1.4, L - gx1, 1.8, 0.15, ch)
    _cuboid(ax, gx0, 0.3, 1.55, gx1 - gx0, 2.4, 0.9, gate)

    # (b) FinFET: 세운 핀을 게이트가 위·양옆에서 감쌈
    ax = axes[1]
    fy0, fw, fh = 1.25, 0.5, 2.0
    _cuboid(ax, 0, 0, 0, L, W, 1.0, sub)
    _cuboid(ax, 0, fy0, 1.0, gx0, fw, fh, ch)
    _cuboid(ax, gx0, 0.3, 1.0, gx1 - gx0, 2.4, fh + 0.6, gate)
    _cuboid(ax, gx1, fy0, 1.0, L - gx1, fw, fh, ch)

    # (c) GAA: 가로로 누운 얇은 판 3장을 게이트가 완전히 감쌈
    ax = axes[2]
    _cuboid(ax, 0, 0, 0, L, W, 1.0, sub)
    sheets = [1.5, 2.25, 3.0]
    for z in sheets:
        _cuboid(ax, 0, 0.75, z, gx0, 1.5, 0.3, ch)
    _cuboid(ax, gx0, 0.3, 1.0, gx1 - gx0, 2.4, 3.0, gate)
    for z in sheets:
        _cuboid(ax, gx1, 0.75, z, L - gx1, 1.5, 0.3, ch)

    # (d) CFET: 아래 nFET 판, 위 pFET 판을 한 게이트가 감쌈
    ax = axes[3]
    _cuboid(ax, 0, 0, 0, L, W, 1.0, sub)
    stack = [(1.4, ch), (2.0, ch), (3.0, pch), (3.6, pch)]
    for z, c in stack:
        _cuboid(ax, 0, 0.75, z, gx0, 1.5, 0.3, c)
    _cuboid(ax, gx0, 0.3, 1.0, gx1 - gx0, 2.4, 3.6, gate)
    for z, c in stack:
        _cuboid(ax, gx1, 0.75, z, L - gx1, 1.5, 0.3, c)
    ax.text(7.6, 2.6, "nFET", fontsize=8.5, color=ch, va="center", fontweight="bold")
    ax.text(7.6, 4.2, "pFET", fontsize=8.5, color=pch, va="center", fontweight="bold")

    for ax in axes:
        ax.text(0.0, -0.25, "source", fontsize=8, color=s.INK2, va="top")
        ax.text(5.2, -0.25, "drain", fontsize=8, color=s.INK2, va="top")
    # 범례
    for i, (lab, c) in enumerate((("gate", gate), ("channel (n)", ch), ("channel (p, CFET)", pch), ("substrate / isolation", sub))):
        fig.patches.append(Rectangle((0.30 + i * 0.12, 0.06), 0.012, 0.03, transform=fig.transFigure,
                                     facecolor=c, edgecolor="none"))
        fig.text(0.315 + i * 0.12, 0.075, lab, fontsize=8.5, color=s.INK2, va="center")
    fig.text(0.5, 0.0, "conceptual 3D sketches, not to scale; spacers, contacts and source/drain epitaxy omitted",
             ha="center", fontsize=8.8, color=s.MUTED)
    s.save(fig, "basics_transistor_3d")


def transistor_xsec():
    """전류가 흐르는 방향으로 본 단면: 게이트(주황)가 채널(파랑)을 몇 면에서 누르는지."""
    sub, ch, gate, pch, ox = "#c9c7c1", s.DL, s.UL, s.ALT, s.SPECIAL
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.9))
    specs = [("Planar", "1 side"), ("FinFET", "3 sides"), ("GAA nanosheet", "4 sides, per sheet"),
             ("CFET", "4 sides, n and p stacked")]
    for ax, (t, sub_t) in zip(axes, specs):
        s.bare(ax)
        ax.set_xlim(0, 5)
        ax.set_ylim(-0.2, 5.2)
        ax.set_aspect("equal")
        ax.set_title(f"{t}\ngate control: {sub_t}", fontsize=10, color=s.INK, pad=4)
        ax.add_patch(Rectangle((0.3, 0), 4.4, 1.0, facecolor=sub, edgecolor="none"))

    def R(ax, x, y, w, h, c):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=c, edgecolor="#ffffff", lw=0.8))

    # 평면
    ax = axes[0]
    R(ax, 0.3, 0.75, 4.4, 0.25, ch)
    R(ax, 0.8, 1.0, 3.4, 0.12, ox)
    R(ax, 0.8, 1.12, 3.4, 1.1, gate)
    # FinFET
    ax = axes[1]
    R(ax, 0.9, 1.0, 3.2, 3.0, gate)
    R(ax, 2.05, 1.0, 0.9, 2.5, ox)
    R(ax, 2.17, 1.0, 0.66, 2.38, ch)
    # GAA
    ax = axes[2]
    R(ax, 0.6, 1.0, 3.8, 3.4, gate)
    for y in (1.4, 2.4, 3.4):
        R(ax, 0.98, y - 0.12, 3.04, 0.64, ox)
        R(ax, 1.1, y, 2.8, 0.4, ch)
    # CFET
    ax = axes[3]
    R(ax, 0.6, 1.0, 3.8, 4.0, gate)
    for y, c in ((1.3, ch), (2.1, ch), (3.3, pch), (4.1, pch)):
        R(ax, 0.98, y - 0.12, 3.04, 0.6, ox)
        R(ax, 1.1, y, 2.8, 0.36, c)
    ax.text(4.5, 1.9, "n", fontsize=10, color=ch, va="center", fontweight="bold")
    ax.text(4.5, 3.9, "p", fontsize=10, color=pch, va="center", fontweight="bold")

    for i, (lab, c) in enumerate((("gate metal", gate), ("gate dielectric", ox), ("channel (n)", ch),
                                  ("channel (p)", pch), ("substrate", sub))):
        fig.patches.append(Rectangle((0.22 + i * 0.12, 0.07), 0.012, 0.03, transform=fig.transFigure,
                                     facecolor=c, edgecolor="none"))
        fig.text(0.235 + i * 0.12, 0.085, lab, fontsize=8.5, color=s.INK2, va="center")
    fig.text(0.5, 0.01, "cross-section across the channel (current flows into the page); conceptual, not to scale",
             ha="center", fontsize=8.8, color=s.MUTED)
    s.save(fig, "basics_transistor_xsec")


if __name__ == "__main__":
    s.setup()
    soc_blocks()
    memory_hierarchy()
    dvfs_curve()
    transistor_3d()
    transistor_xsec()
