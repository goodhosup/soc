"""GPU·NPU 장 그림

1. gpu_imr_vs_tbr   : IMR과 타일 기반 렌더링의 프레임버퍼 트래픽이 어디로 가는지 (DRAM 왕복 vs 칩 안 타일 메모리)
2. gpu_tile_binning : 화면을 타일로 나누고 삼각형을 타일별로 분류 → binning 패스 후 타일별 렌더 패스
3. npu_mac_array    : 가중치 고정(weight-stationary) MAC 배열 — 활성화는 흐르고 부분합은 누적, 로컬 SRAM이 공급
4. npu_roofline     : 가상의 8.2 TOPS NPU + LPDDR5X-8533 64비트 루프라인, 디코드(메모리 한계)와 프리필·CNN(연산 한계)
5. npu_llm_decode   : LPDDR5X-8533에서 1B/3B/7B, INT4/INT8 디코드 토큰/s 이론 상한
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

import style as s

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import soc_numbers as n  # noqa: E402

BW_8533 = n.dram_bw_gbs(n.LPDDR_RATES["LPDDR5X-8533"])
PEAK_TOPS = n.npu_peak_tops(4096, 1.0)


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, round_=True, ls="-"):
    if round_:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls))
    else:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, p0, p1, color, lw=1.4, style="-|>", rad=0.0, ms=12):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- 1. IMR vs TBR
def imr_vs_tbr():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.0))
    titles = ["IMR (immediate mode)", "TBR (tile-based)"]
    for ax, t in zip(axes, titles):
        s.bare(ax)
        ax.set_xlim(0, 6)
        ax.set_ylim(-0.9, 6.2)
        ax.text(3, 6.0, t, ha="center", fontsize=11, fontweight="bold", color=s.INK)
        # 칩 경계
        ax.add_patch(FancyBboxPatch((0.2, 2.9), 5.6, 2.75, boxstyle="round,pad=0,rounding_size=0.12",
                                    facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.2, ls="--"))
        ax.text(0.35, 5.42, "GPU (on chip)", fontsize=8.5, color=s.INK2, va="center")
        # DRAM
        ax.add_patch(FancyBboxPatch((0.2, -0.2), 5.6, 1.7, boxstyle="round,pad=0,rounding_size=0.12",
                                    facecolor=s.SURFACE, edgecolor=s.UL, lw=1.4))
        ax.text(5.65, 1.28, "DRAM (LPDDR)", fontsize=8.5, color=s.UL, va="center", ha="right", fontweight="bold")

    # --- IMR
    ax = axes[0]
    box(ax, 0.6, 3.3, 2.2, 1.6, s.DL, "raster +\npixel shader", fs=9, bold=True)
    box(ax, 3.4, 3.5, 2.1, 1.2, s.EMPTY, "small caches", fs=8.5, ec=s.GRID, tc=s.INK2)
    box(ax, 0.6, 0.05, 2.3, 0.95, s.UL, "color buffer\n(full screen)", fs=8.5)
    box(ax, 3.2, 0.05, 2.3, 0.95, s.UL, "depth buffer\n(full screen)", fs=8.5)
    arrow(ax, (1.5, 3.3), (1.5, 1.0), s.UL, lw=3.2, style="<|-|>", ms=14)
    ax.text(1.38, 2.15, "color W\n+ blend R", fontsize=8.5, color=s.UL, ha="right", va="center")
    arrow(ax, (2.5, 3.3), (4.0, 1.0), s.UL, lw=3.2, style="<|-|>", ms=14)
    ax.text(3.45, 2.45, "depth R/W", fontsize=8.5, color=s.UL, ha="left", va="center")
    ax.text(3.6, 1.98, "per fragment,\n× overdraw", fontsize=8, color=s.INK2, ha="left", va="center")
    ax.text(3, -0.65, "framebuffer traffic: many DRAM round-trips per pixel",
            ha="center", fontsize=8.5, color=s.INK2)

    # --- TBR
    ax = axes[1]
    box(ax, 0.6, 3.3, 2.2, 1.6, s.DL, "raster +\npixel shader", fs=9, bold=True)
    box(ax, 3.5, 3.3, 2.0, 1.6, s.SYNC, "tile memory\ncolor + depth\n(one tile)", fs=8.5, bold=False)
    arrow(ax, (2.85, 4.35), (3.45, 4.35), s.SYNC, lw=3.2, style="<|-|>", ms=14)
    arrow(ax, (2.85, 3.85), (3.45, 3.85), s.SYNC, lw=3.2, style="<|-|>", ms=14)
    ax.text(3.15, 5.08, "R/W stay on chip", fontsize=8.5, color=s.SYNC, ha="center", fontweight="bold")
    box(ax, 0.6, 0.05, 2.3, 0.95, s.EMPTY, "bin lists\n(per tile)", fs=8.5, ec=s.UL, tc=s.INK)
    box(ax, 3.2, 0.05, 2.3, 0.95, s.UL, "final frame\n(full screen)", fs=8.5)
    arrow(ax, (4.5, 3.3), (4.35, 1.0), s.UL, lw=1.2, ms=11)
    ax.text(4.55, 2.15, "1 write\nper tile", fontsize=8.5, color=s.UL, ha="left", va="center")
    arrow(ax, (1.75, 1.0), (1.7, 3.3), s.UL, lw=1.2, ms=11)
    ax.text(1.85, 2.15, "read bin list\n(from binning pass)", fontsize=8, color=s.INK2, ha="left", va="center")
    ax.text(3, -0.65, "depth discarded on chip; only finished color goes out",
            ha="center", fontsize=8.5, color=s.INK2)

    fig.text(0.5, 0.05, "conceptual data flow, not a specific GPU · arrow width ≈ relative DRAM traffic",
             ha="center", fontsize=8.5, color=s.MUTED)
    fig.subplots_adjust(wspace=0.06)
    s.save(fig, "gpu_imr_vs_tbr")


# ---------------------------------------------------------------- 2. 타일 binning
def _tri_hits(tri, x0, y0, w, h, k=24):
    """타일 안 격자점 중 하나라도 삼각형 안이면 해당 타일에 분류."""
    (ax_, ay), (bx, by), (cx, cy) = tri
    xs, ys = np.meshgrid(np.linspace(x0 + 0.01, x0 + w - 0.01, k), np.linspace(y0 + 0.01, y0 + h - 0.01, k))

    def side(px, py, qx, qy, rx, ry):
        return (px - rx) * (qy - ry) - (qx - rx) * (py - ry)

    d1 = side(xs, ys, ax_, ay, bx, by)
    d2 = side(xs, ys, bx, by, cx, cy)
    d3 = side(xs, ys, cx, cy, ax_, ay)
    neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
    pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
    return bool(np.any(~(neg & pos)))


def tile_binning():
    fig = plt.figure(figsize=(10, 5.6))
    ax = fig.add_axes([0.0, 0.33, 0.52, 0.65])
    at = fig.add_axes([0.55, 0.33, 0.45, 0.65])
    ab = fig.add_axes([0.0, 0.0, 1.0, 0.29])
    for a in (ax, at, ab):
        s.bare(a)

    cols, rows, tw, th = 4, 3, 1.0, 1.0
    ax.set_xlim(-0.1, cols * tw + 0.1)
    ax.set_ylim(-0.35, rows * th + 0.35)
    ax.set_aspect("equal")
    tris = {
        "A": ([(0.25, 0.2), (1.6, 0.4), (0.5, 1.85)], s.DL),
        "B": ([(1.3, 2.8), (2.8, 2.6), (2.1, 1.6)], s.UL),
        "C": ([(2.6, 0.25), (3.7, 0.35), (3.4, 1.3)], s.CTRL),
    }
    bins = {}
    for r in range(rows):
        for c in range(cols):
            tid = (rows - 1 - r) * cols + c
            x0, y0 = c * tw, r * th
            ax.add_patch(Rectangle((x0, y0), tw, th, facecolor=s.SURFACE, edgecolor=s.GRID, lw=1.2))
            ax.text(x0 + 0.06, y0 + th - 0.08, f"T{tid}", fontsize=8, color=s.INK2, va="top", zorder=5)
            bins[tid] = [k for k, (tri, _) in tris.items() if _tri_hits(tri, x0, y0, tw, th)]
    for k, (tri, col) in tris.items():
        ax.add_patch(Polygon(tri, closed=True, facecolor=col, alpha=0.55, edgecolor=col, lw=1.6))
        cx = sum(p[0] for p in tri) / 3
        cy = sum(p[1] for p in tri) / 3
        ax.text(cx, cy, k, ha="center", va="center", fontsize=11, fontweight="bold", color=s.INK)
    ax.add_patch(Rectangle((0, 0), cols * tw, rows * th, fill=False, edgecolor=s.INK2, lw=1.4))
    ax.text(cols * tw / 2, rows * th + 0.2, "screen split into tiles (T0–T11)", ha="center",
            fontsize=9.5, color=s.INK2)

    # 타일별 목록 (binning 결과)
    at.set_xlim(0, 4.6)
    at.set_ylim(0, 6.9)
    at.text(0.1, 6.6, "bin lists (written by binning pass)", fontsize=9.5, color=s.INK2, va="center")
    colmap = {k: c for k, (_, c) in tris.items()}
    for tid in range(12):
        col_i, row_i = tid % 2, tid // 2
        x = 0.1 + col_i * 2.3
        y = 5.55 - row_i * 0.95
        at.add_patch(FancyBboxPatch((x, y), 2.1, 0.72, boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=s.EMPTY, edgecolor=s.GRID, lw=1))
        at.text(x + 0.12, y + 0.36, f"T{tid}", fontsize=9, color=s.INK2, va="center", fontweight="bold")
        if bins[tid]:
            for j, k in enumerate(bins[tid]):
                bx = x + 0.75 + j * 0.45
                at.add_patch(Rectangle((bx, y + 0.14), 0.38, 0.44, facecolor=colmap[k], edgecolor="none"))
                at.text(bx + 0.19, y + 0.36, k, ha="center", va="center", fontsize=9,
                        color=s.text_on(colmap[k]), fontweight="bold")
        else:
            at.text(x + 0.75, y + 0.36, "empty → skip", fontsize=8, color=s.MUTED, va="center")

    # 아래: 두 패스 타임라인
    ab.set_xlim(0, 10)
    ab.set_ylim(-0.2, 1.9)
    box(ab, 0.15, 0.55, 2.3, 0.9, s.CTRL, "pass 1: binning\nall vertices (positions)", fs=8.5, bold=True)
    ab.text(1.3, 0.25, "→ bin lists to DRAM", fontsize=8, color=s.INK2, ha="center")
    arrow(ab, (2.55, 1.0), (2.95, 1.0), s.INK2, lw=1.2)
    ab.text(3.0, 1.68, "pass 2: render tile by tile (raster + shade in tile memory, then 1 write-out)",
            fontsize=8.5, color=s.INK2)
    x = 3.0
    shown = [0, 1, 2, 3, 4, 5]
    for tid in shown:
        w = 0.88
        box(ab, x, 0.55, w, 0.9, s.DL if bins[tid] else s.EMPTY, f"T{tid}", fs=8.5,
            ec=s.SURFACE if bins[tid] else s.GRID, tc=None if bins[tid] else s.MUTED)
        if bins[tid]:
            ab.add_patch(Rectangle((x + w - 0.16, 0.55), 0.16, 0.9, facecolor=s.UL, edgecolor="none"))
        x += w + 0.08
    ab.text(x + 0.05, 1.0, "…  T11", fontsize=9, color=s.INK2, va="center")
    ab.add_patch(Rectangle((3.0, 0.08), 0.16, 0.22, facecolor=s.UL, edgecolor="none"))
    ab.text(3.22, 0.19, "write tile to DRAM", fontsize=8, color=s.INK2, va="center")
    ab.add_patch(Rectangle((5.3, 0.08), 0.3, 0.22, facecolor=s.EMPTY, edgecolor=s.GRID))
    ab.text(5.68, 0.19, "empty tile: skipped", fontsize=8, color=s.INK2, va="center")
    ab.text(9.95, 0.19, "conceptual, not a specific GPU", fontsize=8, color=s.MUTED, ha="right", va="center")
    s.save(fig, "gpu_tile_binning")


# ---------------------------------------------------------------- 3. MAC 배열
def mac_array():
    N = 4
    fig, ax = plt.subplots(figsize=(10, 6.0))
    s.bare(ax)
    ax.set_xlim(-0.2, 11.2)
    ax.set_ylim(-1.7, 6.4)
    ax.set_aspect("equal")
    pe, gap = 0.95, 0.35
    x0, ytop = 4.0, 4.9   # 배열 왼쪽 위 기준

    # SRAM 블록
    box(ax, 0.0, 0.6, 1.5, 4.3, s.SYNC, "local\nSRAM\n\nactivation\nbuffer", fs=9, bold=False)
    box(ax, x0 - 0.05, 5.55, N * pe + (N - 1) * gap + 0.1, 0.65, s.SYNC, "weight buffer (SRAM) — loaded once", fs=8.5)

    # PE 격자
    for i in range(N):
        for j in range(N):
            x = x0 + j * (pe + gap)
            y = ytop - pe - i * (pe + gap)
            box(ax, x, y, pe, pe, s.DL, "", round_=True)
            ax.text(x + pe / 2, y + pe * 0.64, f"w{i}{j}", ha="center", va="center", fontsize=9,
                    color="#ffffff", fontweight="bold")
            ax.text(x + pe / 2, y + pe * 0.28, "×  +", ha="center", va="center", fontsize=8, color="#ffffff")
            # 활성화: 오른쪽으로
            if j < N - 1:
                arrow(ax, (x + pe + 0.02, y + pe * 0.62), (x + pe + gap - 0.02, y + pe * 0.62), s.UL, lw=1.4, ms=9)
            # 부분합: 아래로
            if i < N - 1:
                arrow(ax, (x + pe * 0.5, y - 0.02), (x + pe * 0.5, y - gap + 0.02), s.CTRL, lw=1.4, ms=9)
    # 가중치 버퍼 → 배열
    for j in range(N):
        xc = x0 + j * (pe + gap) + pe / 2
        arrow(ax, (xc, 5.53), (xc, ytop + 0.03), s.SYNC, lw=1.2, ms=9)

    # 활성화 입력 (기울어진 시간차)
    for i in range(N):
        yc = ytop - pe - i * (pe + gap) + pe * 0.62
        arrow(ax, (1.55, yc), (x0 - 0.03, yc), s.UL, lw=1.6, ms=10)
        for t in range(i + 1):
            ax.add_patch(plt.Circle((x0 - 0.45 - t * 0.42, yc), 0.13, color=s.UL, zorder=3))
        ax.text(1.75, yc + 0.08, f"row {i} acts", fontsize=8, color=s.UL, ha="left", va="bottom")
    ax.text(0.0, 0.2, "staggered: row i starts i cycles later", fontsize=8, color=s.INK2, ha="left")

    # 아래 누적기
    ybot = ytop - N * pe - (N - 1) * gap
    acc_y = ybot - 1.15
    for j in range(N):
        xc = x0 + j * (pe + gap) + pe / 2
        arrow(ax, (xc, ybot - 0.02), (xc, acc_y + 0.55), s.CTRL, lw=1.4, ms=9)
    box(ax, x0 - 0.05, acc_y, N * pe + (N - 1) * gap + 0.1, 0.55, s.CTRL, "accumulators (INT32) → vector engine → SRAM", fs=8)

    # 범례/설명 (오른쪽)
    lx = 9.75
    items = [
        (s.DL, "PE: holds one weight,\ndoes 1 MAC per cycle"),
        (s.UL, "activations flow →\n(reused by every column)"),
        (s.CTRL, "partial sums flow ↓\nand accumulate"),
        (s.SYNC, "SRAM feeds the array\n(DRAM only via DMA)"),
    ]
    for k, (c, lab) in enumerate(items):
        y = 4.6 - k * 1.15
        ax.add_patch(Rectangle((lx - 0.05, y - 0.15), 0.3, 0.3, color=c))
        ax.text(lx + 0.4, y, lab, fontsize=8.5, color=s.INK2, va="center")
    ax.text(5.6, -1.45, "conceptual 4×4 weight-stationary array (real arrays are far larger)",
            ha="center", fontsize=8.5, color=s.MUTED)
    s.save(fig, "npu_mac_array")


# ---------------------------------------------------------------- 4. 루프라인
def roofline():
    bw = BW_8533
    peak = PEAK_TOPS
    ridge = n.ridge_ops_per_byte(peak, bw)
    ai = np.logspace(np.log10(0.5), np.log10(4000), 400)
    att = np.minimum(peak, bw * ai / 1000)

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.axvspan(0.5, ridge, color=s.UL, alpha=0.07, lw=0)
    ax.axvspan(ridge, 4000, color=s.DL, alpha=0.07, lw=0)
    ax.plot(ai, att, color=s.INK, lw=2.2)
    ax.axvline(ridge, color=s.MUTED, lw=1, ls="--")
    ax.text(ridge * 1.08, 0.03, f"ridge ≈ {ridge:.0f} ops/byte", fontsize=9, color=s.INK2, va="bottom")
    ax.text(1.0, peak * 1.12, f"peak {peak:.1f} TOPS (INT8)", fontsize=9, color=s.INK2)
    ax.text(15, 0.17, f"slope = DRAM {bw:.1f} GB/s\n(LPDDR5X-8533, 64-bit)", fontsize=9,
            color=s.INK2, ha="left")

    # 디코드: INT4 (가중치 1바이트 = 2개 → MAC 2번 = 4 ops), INT8 (2 ops/byte)
    for ops_b, bits, xt, ha, dy in ((4, 4, 6.0, "left", 4.5), (2, 8, 1.6, "center", 9.0)):
        y = min(peak, bw * ops_b / 1000)
        ax.plot([ops_b], [y], marker="o", ms=8, color=s.UL, zorder=4)
        ax.annotate(f"LLM decode INT{bits}\n≈{ops_b} ops/byte → {y:.2f} TOPS", (ops_b, y),
                    xytext=(xt, y / dy), fontsize=9, color=s.UL, ha=ha,
                    arrowprops=dict(arrowstyle="-", color=s.UL, lw=0.8))

    # 프리필·CNN: 연산 한계 (개념적 구간)
    for x, lab in ((400, "CNN conv"), (1500, "LLM prefill")):
        ax.plot([x], [peak], marker="s", ms=8, color=s.DL, zorder=4)
        ax.text(x, peak * 0.62, lab, fontsize=9, color=s.DL, ha="center")
    ax.text(30, 0.012, "memory bound", ha="center", fontsize=10, color=s.UL, fontweight="bold")
    ax.text(np.sqrt(ridge * 4000), 0.012, "compute bound", ha="center", fontsize=10, color=s.DL, fontweight="bold")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.5, 4000)
    ax.set_ylim(0.008, 20)
    ax.set_xlabel("arithmetic intensity (ops per DRAM byte, log)")
    ax.set_ylabel("attainable TOPS (log)")
    ax.set_xticks([1, 10, 100, 1000], ["1", "10", "100", "1000"])
    ax.set_yticks([0.01, 0.1, 1, 10], ["0.01", "0.1", "1", "10"])
    ax.grid(True, which="major", color=s.GRID, lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("hypothetical NPU: 4096 INT8 MACs @ 1 GHz (not a specific chip); "
                 "workload positions are illustrative", fontsize=8.5, color=s.MUTED, loc="left")
    s.save(fig, "npu_roofline")


# ---------------------------------------------------------------- 5. 디코드 토큰/s
def llm_decode():
    bw = BW_8533
    models = [1, 3, 7]
    v4 = [n.llm_tokens_per_s(bw, m, 4) for m in models]
    v8 = [n.llm_tokens_per_s(bw, m, 8) for m in models]
    x = np.arange(len(models))
    w = 0.36
    fig, ax = plt.subplots(figsize=(9, 4.8))
    b4 = ax.bar(x - w / 2 - 0.01, v4, w, color=s.DL, label="INT4 weights")
    b8 = ax.bar(x + w / 2 + 0.01, v8, w, color=s.UL, label="INT8 weights")
    for bars, vals in ((b4, v4), (b8, v8)):
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}", ha="center", va="bottom",
                    fontsize=9.5, color=s.INK)
    ax.set_xticks(x, [f"{m}B" for m in models])
    ax.set_xlabel("model size (parameters)")
    ax.set_ylabel("decode tokens/s (upper bound)")
    ax.set_ylim(0, 155)
    ax.grid(True, axis="y", color=s.GRID, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(f"LPDDR5X-8533, 64-bit ({bw:.1f} GB/s peak) · all weights read once per token · "
                 "theoretical bound", fontsize=8.5, color=s.MUTED, loc="left")
    s.save(fig, "npu_llm_decode")


if __name__ == "__main__":
    s.setup()
    imr_vs_tbr()
    tile_binning()
    mac_array()
    roofline()
    llm_decode()
