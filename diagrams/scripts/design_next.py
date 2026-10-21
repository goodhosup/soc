"""설계·제조·메모리·차세대 공정 그림

1. design_flow            : SoC 설계 흐름 단계 (프론트엔드·백엔드 구간 표시)
2. design_yield_area      : 다이 면적에 따른 웨이퍼당 다이 수·푸아송 수율·양품 다이 수 (D0 0.1/0.2)
3. design_chiplet_yield   : 200 mm² 단일 다이 vs 100 mm² 칩렛 둘 — 웨이퍼당 양품 세트 (D0 0.2)
4. memory_lpddr_bandwidth : LPDDR 세대별 64비트 피크 대역폭 + 노트북용 128/256비트 LPDDR5X-8533
5. next_transistor_cost   : 2nm 가상 예의 트랜지스터당 상대 비용 (개념도)
6. design_mobile_package_thermal : 모바일 SoC 패키지 방열 구조 3종 단면 (PoP · HPB · 나란히 배치, 개념도)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

import style as s

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import soc_numbers as n  # noqa: E402


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def clean(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


# ---------------------------------------------------------------- 1. 설계 흐름
def design_flow():
    stages = [
        ("Spec /\narch", s.CTRL), ("RTL\ndesign", s.DL), ("Verification\n/ emulation", s.DL),
        ("Logic\nsynthesis", s.SYNC), ("Place &\nroute", s.SYNC),
        ("Signoff\nSTA · power\nIR · DRC/LVS", s.SYNC), ("Tapeout\n(GDS/OASIS)", s.UL),
        ("Silicon\nbring-up", s.UL),
    ]
    w, g, h, y = 1.45, 0.3, 1.35, 1.0
    fig, ax = plt.subplots(figsize=(11, 3.6))
    s.bare(ax)
    total = len(stages) * w + (len(stages) - 1) * g
    ax.set_xlim(-0.1, total + 0.1)
    ax.set_ylim(0.32, 3.2)
    xs = [i * (w + g) for i in range(len(stages))]
    for x, (lab, c) in zip(xs, stages):
        box(ax, x, y, w, h, c, lab, fs=8.6, bold=False)
    for x in xs[:-1]:
        ax.annotate("", xy=(x + w + g - 0.02, y + h / 2), xytext=(x + w + 0.02, y + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color=s.INK2, lw=1.2))

    # 구간 띠
    def band(x0, x1, label, c):
        ax.add_patch(Rectangle((x0, 2.65), x1 - x0, 0.42, facecolor=c, alpha=0.18, edgecolor="none"))
        ax.text((x0 + x1) / 2, 2.86, label, ha="center", va="center", fontsize=9.5, color=s.INK, fontweight="bold")

    band(xs[0], xs[2] + w, "front-end: correct behavior", s.DL)
    band(xs[3], xs[5] + w, "back-end: clock · power · area", s.SYNC)
    band(xs[6], xs[7] + w, "fab & lab", s.UL)

    # 반복 고리
    def loop(xa, xb, label):
        ax.annotate("", xy=(xa + w / 2, y - 0.02), xytext=(xb + w / 2, y - 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=1.1,
                                    connectionstyle="arc3,rad=-0.45"))
        ax.text((xa + xb + w) / 2, 0.45, label, ha="center", va="center", fontsize=8.3, color=s.RS)

    loop(xs[1], xs[2], "bug fix")
    loop(xs[4], xs[5], "ECO / timing fix")
    s.save(fig, "design_flow")


# ---------------------------------------------------------------- 2. 면적–수율
def design_yield_area():
    a = np.linspace(50, 300, 251)
    dpw = np.array([n.dies_per_wafer(x) for x in a])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.3), gridspec_kw=dict(wspace=0.28))

    ax1.plot(a, dpw, color=s.INK2, lw=2, label="dies per wafer")
    for d0, c in ((0.1, s.DL), (0.2, s.UL)):
        good = dpw * np.array([n.poisson_yield(x, d0) for x in a])
        ax1.plot(a, good, color=c, lw=2, label=f"good dies, D0 = {d0} /cm²")
        ax2.plot(a, [n.poisson_yield(x, d0) * 100 for x in a], color=c, lw=2, label=f"D0 = {d0} /cm²")

    for x in (100, 120, 150):
        g = n.dies_per_wafer(x) * n.poisson_yield(x, 0.1)
        y = n.poisson_yield(x, 0.1) * 100
        ax1.plot([x], [g], "o", color=s.DL, ms=6, zorder=5)
        ax1.annotate(f"{x} mm²: {g:.0f}", (x, g), xytext=(8, 6), textcoords="offset points",
                     fontsize=8.3, color=s.INK)
        ax2.plot([x], [y], "o", color=s.DL, ms=6, zorder=5)
        ax2.annotate(f"{y:.1f}%", (x, y), xytext=(6, 5), textcoords="offset points", fontsize=8.3, color=s.INK)

    # 파운드리 페이지의 110 mm² 예: 두 결함 밀도 모두 표시
    x = 110
    g1, g2 = (n.dies_per_wafer(x) * n.poisson_yield(x, d) for d in (0.1, 0.2))
    y1, y2 = (n.poisson_yield(x, d) * 100 for d in (0.1, 0.2))
    for ax, (a1, a2), top in ((ax1, (g1, g2), 1330), (ax2, (y1, y2), 98)):
        ax.plot([x], [a1], "D", color=s.DL, mec=s.INK, mew=0.8, ms=6.5, zorder=6)
        ax.plot([x], [a2], "D", color=s.UL, mec=s.INK, mew=0.8, ms=6.5, zorder=6)
    ax1.text(148, 720, f"\u25c6 110 mm² (foundry example)\n   good: {g1:.0f} (D0 0.1) / {g2:.0f} (D0 0.2)",
             fontsize=8.3, color=s.INK, va="center")
    ax2.text(115, 46, f"\u25c6 110 mm²: {y1:.1f}% (D0 0.1) / {y2:.1f}% (D0 0.2)", fontsize=8.3,
             color=s.INK, va="center")

    ax1.set_xlabel("die area (mm²)")
    ax1.set_ylabel("dies per 300 mm wafer")
    ax1.set_ylim(0, 1400)
    ax1.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax2.set_xlabel("die area (mm²)")
    ax2.set_ylabel("Poisson yield (%)")
    ax2.set_ylim(40, 100)
    ax2.legend(frameon=False, fontsize=8.5, loc="upper right")
    for ax in (ax1, ax2):
        ax.set_xlim(50, 300)
        ax.grid(True, color=s.GRID, lw=0.6)
        clean(ax)
    ax1.set_title("dies and good dies per wafer", fontsize=10, color=s.INK, loc="left")
    ax2.set_title("yield  Y = exp(−A·D0)", fontsize=10, color=s.INK, loc="left")
    fig.text(0.125, -0.04, "assumed D0 values; dots = D0 0.1 examples (basics/ppa), diamonds = 110 mm² example (D0 0.1 / 0.2)", fontsize=8.5, color=s.MUTED)
    s.save(fig, "design_yield_area")


# ---------------------------------------------------------------- 3. 칩렛 수율
def design_chiplet_yield():
    d0 = 0.2
    mono_dpw = n.dies_per_wafer(200)
    mono_good = mono_dpw * n.poisson_yield(200, d0)
    chip_dpw = n.dies_per_wafer(100)
    chip_good = chip_dpw * n.poisson_yield(100, d0)
    sets = chip_good / 2

    fig, ax = plt.subplots(figsize=(9, 4.0))
    labels = ["1 × 200 mm²\nmonolithic", "2 × 100 mm²\nchiplets"]
    yv = [1, 0]
    bh = 0.5
    # 전체 다이(세트 기준) 막대 뒤에 양품 막대
    ax.barh(yv, [mono_dpw, chip_dpw / 2], height=bh, color=s.EMPTY, edgecolor=s.GRID, label="candidate sets per wafer")
    ax.barh(yv, [mono_good, sets], height=bh, color=[s.UL, s.DL], label="good sets per wafer")
    ax.text(mono_good - 6, 1, f"{mono_good:.0f} good", ha="right", va="center", color="#ffffff", fontsize=10, fontweight="bold")
    ax.text(sets - 6, 0, f"{sets:.0f} good sets", ha="right", va="center", color="#ffffff", fontsize=10, fontweight="bold")
    ax.text(mono_dpw + 5, 1, f"of {mono_dpw:.0f} dies  (yield {n.poisson_yield(200, d0) * 100:.1f}%)",
            va="center", fontsize=9, color=s.INK2)
    ax.text(chip_dpw / 2 + 5, 0, f"of {chip_dpw / 2:.0f} pairs  ({chip_dpw:.0f} dies, yield {n.poisson_yield(100, d0) * 100:.1f}% each)",
            va="center", fontsize=9, color=s.INK2)
    ax.set_yticks(yv, labels)
    ax.set_xlim(0, 560)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel("per 300 mm wafer")
    ax.grid(True, axis="x", color=s.GRID, lw=0.6)
    ax.set_axisbelow(True)
    clean(ax)
    ax.set_title(f"same circuit, D0 = {d0} /cm²: +{(sets / mono_good - 1) * 100:.0f}% good sets "
            "(before die-to-die interface area and assembly yield)", fontsize=8.8, color=s.MUTED, loc="left")
    s.save(fig, "design_chiplet_yield")


# ---------------------------------------------------------------- 4. LPDDR 대역폭
def memory_lpddr_bandwidth():
    gens = list(n.LPDDR_RATES.items())
    names = [k if "-" in k else f"{k}-{v}" for k, v in gens]
    bw64 = [n.dram_bw_gbs(v) for _, v in gens]
    wide = [("128-bit", n.dram_bw_gbs(8533, 128)), ("256-bit", n.dram_bw_gbs(8533, 256))]

    fig, ax = plt.subplots(figsize=(10, 4.4))
    x1 = np.arange(len(gens))
    x2 = len(gens) + 0.8 + np.arange(len(wide))
    ax.bar(x1, bw64, width=0.62, color=s.DL)
    ax.bar(x2, [b for _, b in wide], width=0.62, color=s.UL)
    for x, b in list(zip(x1, bw64)) + list(zip(x2, [b for _, b in wide])):
        ax.text(x, b + 5, f"{b:.1f}", ha="center", va="bottom", fontsize=9, color=s.INK)
    ax.set_xticks(list(x1) + list(x2),
                  [nm.replace("-", "\n") for nm in names] + [f"{w}\nLPDDR5X-8533" for w, _ in wide], fontsize=8.6)
    ax.set_ylabel("peak bandwidth (GB/s)")
    ax.set_ylim(0, 340)
    ax.grid(True, axis="y", color=s.GRID, lw=0.6)
    ax.set_axisbelow(True)
    clean(ax)
    ax.axvline(len(gens) - 0.1, color=s.GRID, lw=1, ls="--")
    ax.text((len(gens) - 1) / 2, 322, "phone SoC: 64-bit bus (4 × 16-bit)", ha="center", fontsize=9.3, color=s.DL, fontweight="bold")
    ax.text(x2.mean(), 322, "laptop-class SoC: wider bus", ha="center", fontsize=9.3, color=s.UL, fontweight="bold")
    ax.text(-0.4, 280, "theoretical peak = MT/s × bus bits ÷ 8", fontsize=8.5, color=s.MUTED)
    s.save(fig, "memory_lpddr_bandwidth")


# ---------------------------------------------------------------- 5. 트랜지스터당 비용
def next_transistor_cost():
    mature = n.die_cost_ratio(100, 0.1, 87, 0.1, 1.3)
    early = n.die_cost_ratio(100, 0.1, 87, 0.2, 1.3)
    cases = [("previous node\n100 mm², D0 0.1", 1.0, s.MUTED),
             ("new node, mature yield\n87 mm², D0 0.1", mature, s.DL),
             ("new node, early yield\n87 mm², D0 0.2", early, s.UL)]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    x = np.arange(len(cases))
    ax.bar(x, [c[1] for c in cases], width=0.55, color=[c[2] for c in cases])
    for xi, (_, v, _) in zip(x, cases):
        lab = "1.00" if v == 1.0 else f"{v:.2f}  (+{(v - 1) * 100:.0f}%)"
        ax.text(xi, v + 0.02, lab, ha="center", va="bottom", fontsize=10, color=s.INK, fontweight="bold")
    ax.axhline(1.0, color=s.INK2, lw=1, ls="--")
    ax.set_xticks(x, [c[0] for c in cases], fontsize=9)
    ax.set_ylabel("relative cost per transistor")
    ax.set_ylim(0, 1.5)
    ax.grid(True, axis="y", color=s.GRID, lw=0.6)
    ax.set_axisbelow(True)
    clean(ax)
    ax.text(-0.35, 1.42, "conceptual example (assumed: wafer 1.3× price, 15% denser), not a specific process",
            fontsize=8.8, color=s.MUTED)
    s.save(fig, "next_transistor_cost")


# ---------------------------------------------------------------- 6. 모바일 패키지 방열 구조
def design_mobile_package_thermal():
    die, dram, cu, pkg, board, vc = s.UL, s.DL, s.SPECIAL, s.EMPTY, s.MUTED, s.SYNC
    panels = [
        ("(a) fan-out PoP\nDRAM stacked on SoC", "pop"),
        ("(b) PoP + heat path block\n(Samsung HPB, Exynos 2600)", "hpb"),
        ("(c) die and DRAM side by side\n(Apple A20 Pro)", "side"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.0))
    for ax, (title, kind) in zip(axes, panels):
        s.bare(ax)
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 5.2)
        ax.set_title(title, fontsize=10, color=s.INK, pad=6)
        box(ax, 0.2, 0.3, 5.6, 0.45, board, "board", fs=8.5)
        box(ax, 0.6, 0.85, 4.8, 0.35, pkg, "RDL / substrate", fs=8, ec=s.GRID, tc=s.INK2)
        box(ax, 0.2, 4.35, 5.6, 0.4, vc, "vapor chamber / graphite", fs=8.5)
        if kind == "side":
            box(ax, 0.9, 1.3, 2.2, 0.75, die, "SoC die", fs=9, bold=True)
            box(ax, 3.4, 1.3, 1.7, 0.75, dram, "DRAM", fs=9, bold=True)
            ax.annotate("", xy=(2.0, 4.3), xytext=(2.0, 2.1),
                        arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=2.4), zorder=0.5)
            ax.text(2.15, 3.2, "direct path\n(memory out of\nthermal path)", fontsize=8, color=s.RS, va="center")
        else:
            box(ax, 1.4, 1.3, 3.2, 0.75, die, "SoC die", fs=9, bold=True)
            box(ax, 0.6, 2.15, 4.8, 0.3, pkg, "top RDL / interposer", fs=7.5, ec=s.GRID, tc=s.INK2)
            if kind == "pop":
                box(ax, 0.8, 2.6, 4.4, 1.0, dram, "DRAM package", fs=9, bold=True)
                ax.annotate("", xy=(3.0, 4.3), xytext=(3.0, 2.1),
                            arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=1.2, ls="--"), zorder=0.5)
                ax.text(3.15, 3.95, "heat must pass\nthrough DRAM", fontsize=8, color=s.RS, va="center")
            else:
                box(ax, 0.8, 2.6, 2.2, 1.0, cu, "Cu heat\npath block", fs=8.5, bold=True)
                box(ax, 3.2, 2.6, 2.0, 1.0, dram, "DRAM\n(smaller)", fs=8.5, bold=True)
                ax.annotate("", xy=(1.9, 4.3), xytext=(1.9, 2.1),
                            arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=2.0), zorder=0.5)
                ax.text(2.05, 3.95, "via Cu block", fontsize=8, color=s.RS, va="center")
    fig.text(0.5, 0.04, "conceptual cross-sections, not to scale; exact stack-ups are not public",
             ha="center", fontsize=8.8, color=s.MUTED)
    s.save(fig, "design_mobile_package_thermal")


if __name__ == "__main__":
    s.setup()
    design_flow()
    design_yield_area()
    design_chiplet_yield()
    memory_lpddr_bandwidth()
    next_transistor_cost()
    design_mobile_package_thermal()
