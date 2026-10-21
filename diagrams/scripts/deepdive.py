"""3차 보강 그림 — Mermaid 하나만 있던 페이지에 구조·데이터 그림 추가

1.  history_timeline        : 2007–2025 모바일 SoC 주요 전환점
2.  arch_parallelism        : ILP · DLP · TLP 세 가지 병렬성
3.  coherence_mesi          : MESI 상태 전이 (로컬 읽기·쓰기, 다른 캐시의 읽기·쓰기)
4.  sched_capacity          : CPU capacity와 작업 배치 (EAS, misfit) — 예시 값
5.  codec_block_sizes       : 코덱 세대별 최대 부호화 블록 크기
6.  mte_tags                : MTE의 메모리 태그와 포인터 태그 비교
7.  power_domain_boundary   : 파워 도메인 경계의 전원 스위치·아이솔레이션·레벨 시프터·리텐션
8.  crypto_locations        : SoC 안 암호 하드웨어의 위치
9.  lowspeed_wiring         : I2C · SPI · UART 배선
10. modem_placement         : 통합 모뎀과 외장 모뎀 배치
11. bench_efficiency        : 전력 대비 성능(가상 칩 A·B)과 Amdahl 법칙(90% 병렬)
12. rt_bvh                  : BVH 순회와 광선–삼각형 교차
13. license_spectrum        : Arm 라이선스 세 형태의 자유도와 개발 부담
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, x0, y0, x1, y1, c=None, lw=1.4, style="-|>", rad=0.0, z=1, ls="-"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=12,
                                 color=c or s.INK2, linewidth=lw, zorder=z, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    s.bare(ax)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return fig, ax


# ---------------------------------------------------------------- 1. 연표
def history_timeline():
    ev = [(2007, "first smartphone APs\n(ARM11, single core)", s.GRID),
          (2010, "Cortex-A8/A9\ndual → quad core", s.DL),
          (2013, "big.LITTLE +\nfirst 64-bit (Apple A7)", s.DL),
          (2015, "14/16nm FinFET", s.CTRL),
          (2017, "NPUs appear\n(A11, Kirin 970)\nDynamIQ", s.UL),
          (2019, "7nm EUV,\nintegrated 5G modem", s.SYNC),
          (2020, "Cortex-X1", s.DL),
          (2021, "Armv9", s.DL),
          (2022, "3nm GAA\nproduction", s.CTRL),
          (2023, "on-device gen-AI,\ncustom CPUs (2023–24)", s.UL),
          (2025, "2nm race,\nArm C1 cores, SME2", s.CTRL)]
    fig, ax = canvas(13, 5.2, (2005.6, 2026.6), (-3.3, 3.4))
    ax.plot([2006.6, 2025.8], [0, 0], color=s.INK2, lw=2)
    for yr in range(2007, 2026, 2):
        ax.plot([yr, yr], [-0.08, 0.08], color=s.INK2, lw=1.2)
        ax.text(yr, -0.32, str(yr), ha="center", va="top", fontsize=8.5, color=s.INK2)
    levels = [0.55, 1.65, -1.45, -2.55]
    for i, (yr, t, c) in enumerate(ev):
        y = levels[i % 4]
        lc = c if c != s.GRID else s.MUTED
        ax.plot([yr, yr], [0, y] if y > 0 else [y + 0.9, 0], color=lc, lw=1.2, zorder=1)
        ax.add_patch(Circle((yr, 0), 0.12, color=lc, zorder=3))
        box(ax, yr - 1.4, y, 2.8, 0.9, c, t, fs=6.9, bold=True, tc=s.INK if c == s.GRID else None, z=3)
    for i, (c, t) in enumerate(((s.DL, "CPU / architecture"), (s.CTRL, "process"), (s.UL, "AI / design shift"),
                                (s.SYNC, "connectivity"))):
        ax.add_patch(Rectangle((2007 + i * 3.2, 3.0), 0.3, 0.22, facecolor=c, edgecolor="none"))
        ax.text(2007.4 + i * 3.2, 3.11, t, va="center", fontsize=8.5, color=s.INK2)
    s.save(fig, "start_history_timeline")


# ---------------------------------------------------------------- 2. 병렬성
def arch_parallelism():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    for ax in axes:
        s.bare(ax)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
    ax = axes[0]
    ops = ["add r1", "ldr r2", "mul r3", "sub r4"]
    for i, o in enumerate(ops):
        box(ax, 0.6 + i * 2.25, 4.6, 2.0, 1.0, s.DL, o, fs=8.5)
        ax.plot([1.6 + i * 2.25, 1.6 + i * 2.25], [4.6, 3.4], color=s.INK2, lw=1)
    ax.text(5, 6.6, "one thread, cycle t", ha="center", fontsize=9, color=s.INK2)
    box(ax, 0.6, 2.2, 8.75, 1.1, s.EMPTY, "4 independent instructions issue together", fs=8.5, tc=s.INK, ec=s.MUTED)
    ax.set_title("ILP — instruction level\n(superscalar, out-of-order)", fontsize=10.5, fontweight="bold")
    ax = axes[1]
    box(ax, 0.6, 5.6, 8.8, 0.9, s.ALT, "one instruction: multiply-add", fs=8.8, bold=True)
    for i in range(8):
        box(ax, 0.6 + i * 1.1, 3.4, 1.0, 1.4, s.CTRL, f"px\n{i}", fs=8)
        arrow(ax, 1.1 + i * 1.1, 5.55, 1.1 + i * 1.1, 4.85, lw=1)
    box(ax, 0.6, 1.6, 8.8, 1.0, s.EMPTY, "same op on many data lanes", fs=8.5, tc=s.INK, ec=s.MUTED)
    ax.set_title("DLP — data level\n(SIMD NEON/SVE2, GPU, NPU)", fontsize=10.5, fontweight="bold")
    ax = axes[2]
    th = [("UI thread", s.UL), ("render", s.DL), ("network", s.SYNC), ("decode", s.SPECIAL)]
    for i, (t, c) in enumerate(th):
        box(ax, 0.6 + i * 2.25, 4.8, 2.0, 1.1, s.INK2, f"core {i}", fs=8.5, bold=True)
        box(ax, 0.6 + i * 2.25, 3.4, 2.0, 1.1, c, t, fs=8.2)
    box(ax, 0.6, 1.6, 8.75, 1.0, s.EMPTY, "different threads on different cores", fs=8.5, tc=s.INK, ec=s.MUTED)
    ax.set_title("TLP — thread level\n(multicore)", fontsize=10.5, fontweight="bold")
    s.save(fig, "basics_parallelism")


# ---------------------------------------------------------------- 3. MESI
def coherence_mesi():
    fig, ax = canvas(9.5, 6.4, (0, 10), (0, 8.4))
    pos = {"M": (2.2, 6.4), "E": (7.8, 6.4), "S": (7.8, 1.8), "I": (2.2, 1.8)}
    col = {"M": s.UL, "E": s.SYNC, "S": s.DL, "I": s.GRID}
    desc = {"M": "Modified\nonly copy, dirty", "E": "Exclusive\nonly copy, clean",
            "S": "Shared\nclean, others too", "I": "Invalid\nno data"}
    for k, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.95, facecolor=col[k], edgecolor="white", lw=2, zorder=3))
        ax.text(x, y + 0.2, k, ha="center", va="center", fontsize=18, fontweight="bold", zorder=4,
                color=s.INK if k == "I" else "white")
        ax.text(x, y - 0.45, desc[k], ha="center", va="center", fontsize=6.6, zorder=4,
                color=s.INK if k == "I" else "white")

    def tr(a, b, label, rad, lx, ly, c=s.INK2):
        (x0, y0), (x1, y1) = pos[a], pos[b]
        v = np.array([x1 - x0, y1 - y0])
        v = v / np.linalg.norm(v)
        arrow(ax, x0 + v[0] * 1.0, y0 + v[1] * 1.0, x1 - v[0] * 1.0, y1 - v[1] * 1.0, c=c, lw=1.5, rad=rad)
        ax.text(lx, ly, label, ha="center", va="center", fontsize=7.8, color=c,
                bbox=dict(facecolor=s.SURFACE, edgecolor="none", pad=1.2))

    local, remote = s.INK2, s.RS
    tr("I", "E", "local read,\nno other copy", 0.2, 3.4, 3.0)
    tr("I", "S", "local read,\nothers have it", 0.0, 5.0, 1.45)
    tr("E", "M", "local write\n(no bus traffic)", 0.0, 5.0, 6.75)
    tr("S", "M", "local write:\ninvalidate others", 0.2, 4.6, 5.3)
    tr("I", "M", "local write\n(read-for-ownership)", 0.0, 1.05, 4.1)
    tr("M", "S", "other cache reads:\nwrite back, share", 0.3, 6.55, 4.9, remote)
    tr("E", "S", "other cache\nreads", 0.0, 8.95, 4.1, remote)
    tr("S", "I", "other cache\nwrites", 0.25, 5.0, 0.35, remote)
    ax.text(5.0, 8.1, "black = this core's access   red = snoop caused by another cache", ha="center",
            fontsize=8.5, color=s.INK2)
    ax.text(5.0, 7.7, "(M/E → I on another cache's write omitted for clarity)", ha="center", fontsize=7.8,
            color=s.MUTED)
    s.save(fig, "cpu_mesi")


# ---------------------------------------------------------------- 4. capacity
def sched_capacity():
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    cpus = ["cpu0", "cpu1", "cpu2", "cpu3", "cpu4", "cpu5", "cpu6", "cpu7"]
    cap = [260, 260, 260, 260, 700, 700, 700, 1024]
    col = [s.SYNC] * 4 + [s.DL] * 3 + [s.UL]
    ax.bar(cpus, cap, color=col, width=0.62, alpha=0.35)
    ax.bar(cpus, [c * 0.8 for c in cap], color="none", edgecolor=col, width=0.62, lw=1.2, ls="--")
    tasks = {0: (90, "bg sync"), 1: (60, "music"), 4: (420, "app"), 7: (900, "game main")}
    for i, (u, n) in tasks.items():
        ax.bar(i, u, color=col[i], width=0.42)
        ax.text(i, u + 18, f"{n}\nu={u}", ha="center", fontsize=8)
    ax.annotate("misfit: task u=300 > 80 % of 260\n→ moved to a bigger core", xy=(4, 320), xytext=(1.3, 640),
                fontsize=8.5, color=s.RS, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=s.RS, lw=1.4, connectionstyle="arc3,rad=-0.2"))
    ax.set_ylim(0, 1150)
    ax.set_ylabel("capacity / utilisation (max core = 1024)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("EAS places each task where it fits at the lowest energy (example capacities)", fontsize=10.5,
                 fontweight="bold")
    ax.text(5.0, 960, "dashed line = ~80 % fit margin", fontsize=8, color=s.INK2, ha="center")
    s.save(fig, "cpu_sched_capacity")


# ---------------------------------------------------------------- 5. 코덱 블록
def codec_block_sizes():
    fig, ax = canvas(12, 4.4, (0, 12.4), (-0.9, 3.4))
    items = [("H.264/AVC\nmacroblock", 16, s.GRID), ("H.265/HEVC\nCTU", 64, s.DL), ("VP9\nsuperblock", 64, s.SYNC),
             ("AV1\nsuperblock", 128, s.UL), ("H.266/VVC\nCTU", 128, s.CTRL)]
    sc = 2.4 / 128
    x = 0.3
    for name, n, c in items:
        w = n * sc
        ax.add_patch(Rectangle((x, 0), w, w, facecolor=c, edgecolor=s.INK2, lw=1, alpha=0.9))
        if n >= 64:
            for k in range(1, n // 16):
                ax.plot([x + k * 16 * sc] * 2, [0, w], color="white", lw=0.4, alpha=0.6)
                ax.plot([x, x + w], [k * 16 * sc] * 2, color="white", lw=0.4, alpha=0.6)
        ax.text(x + max(w, 0.3) / 2, -0.15, f"{name}\n{n}×{n}", ha="center", va="top", fontsize=8.5)
        x += max(w, 0.5) + 0.35
    ax.text(6.2, 3.1, "largest coding block per generation (drawn to scale; white grid = 16×16)", ha="center",
            fontsize=9.5, fontweight="bold")
    s.save(fig, "media_codec_blocks")


# ---------------------------------------------------------------- 6. MTE
def mte_tags():
    fig, ax = canvas(12, 4.4, (0, 12.4), (-0.5, 5.8))
    ax.text(0.2, 5.3, "64-bit pointer", fontsize=9.5, fontweight="bold")
    box(ax, 0.2, 4.2, 1.2, 0.8, s.INK2, "top bits", fs=8)
    box(ax, 1.4, 4.2, 0.8, 0.8, s.UL, "tag\n0x3", fs=8, bold=True)
    box(ax, 2.2, 4.2, 4.6, 0.8, s.DL, "virtual address", fs=8.5)
    ax.text(0.2, 2.65, "memory: 16-byte granules, each with a 4-bit tag", fontsize=9.5, fontweight="bold")
    tags = ["0x3", "0x3", "0x3", "0x3", "0x7", "0x7", "0x1", "0x1"]
    for i, t in enumerate(tags):
        c = s.UL if t == "0x3" else (s.ALT if t == "0x7" else s.GRID)
        box(ax, 0.2 + i * 1.5, 1.2, 1.4, 1.2, s.EMPTY, f"16 B", fs=8, tc=s.INK, ec=s.MUTED)
        box(ax, 0.2 + i * 1.5, 0.55, 1.4, 0.55, c, t, fs=8, bold=True, tc=s.INK if c == s.GRID else None)
    ax.add_patch(FancyBboxPatch((0.1, 0.45), 5.95, 2.05, boxstyle="round,pad=0,rounding_size=0.05",
                                facecolor="none", edgecolor=s.UL, lw=1.6, ls="--"))
    ax.text(3.1, -0.25, "64-byte buffer allocated with tag 0x3", ha="center", fontsize=8.5, color=s.UL)
    arrow(ax, 4.5, 4.2, 2.2, 2.45, c=s.SYNC, lw=1.8)
    ax.text(1.6, 3.55, "access inside buffer:\ntag 0x3 = 0x3 → OK", fontsize=8.5, color=s.SYNC, ha="center")
    arrow(ax, 6.0, 4.2, 7.1, 2.45, c=s.RS, lw=1.8)
    ax.text(8.6, 3.75, "overflow into next object:\ntag 0x3 ≠ 0x7 → fault", fontsize=8.5, color=s.RS, ha="center")
    s.save(fig, "memory_mte_tags")


# ---------------------------------------------------------------- 7. 파워 도메인 경계
def power_domain_boundary():
    fig, ax = canvas(12, 4.8, (0, 12.4), (-0.4, 6.2))
    ax.plot([0.3, 12.0], [5.6, 5.6], color=s.INK, lw=2)
    ax.text(0.3, 5.85, "VDD (always-on rail)", fontsize=9, fontweight="bold")
    ax.add_patch(FancyBboxPatch((0.3, 0.4), 3.6, 4.3, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=s.EMPTY, edgecolor=s.SYNC, lw=1.8))
    ax.text(2.1, 4.35, "always-on (AON) domain", ha="center", fontsize=9, fontweight="bold", color=s.SYNC)
    box(ax, 0.7, 2.6, 2.8, 1.2, s.SYNC, "power controller\n(sequencing)", fs=8.5, bold=True)
    box(ax, 0.7, 1.0, 2.8, 1.1, s.SYNC, "wake-up logic,\ntimers", fs=8.5)
    ax.add_patch(FancyBboxPatch((6.6, 0.4), 5.4, 4.3, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=s.EMPTY, edgecolor=s.UL, lw=1.8))
    ax.text(9.3, 4.35, "switchable domain (e.g. GPU)", ha="center", fontsize=9, fontweight="bold", color=s.UL)
    box(ax, 7.0, 2.6, 2.4, 1.2, s.UL, "logic", fs=9, bold=True)
    box(ax, 9.6, 2.6, 2.1, 1.2, s.CTRL, "retention\nflip-flops", fs=8.2, bold=True)
    ax.text(10.65, 2.25, "keep state on a\nsmall separate supply", ha="center", fontsize=7.5, color=s.INK2)
    box(ax, 8.6, 4.95, 1.6, 0.5, s.INK2, "power switch", fs=7.8)
    ax.plot([9.4, 9.4], [5.45, 5.6], color=s.INK, lw=1.5)
    ax.plot([9.4, 9.4], [4.7, 4.95], color=s.INK, lw=1.5)
    box(ax, 4.4, 2.75, 1.7, 0.9, s.SPECIAL, "isolation\ncell", fs=8.2, bold=True)
    box(ax, 4.4, 1.15, 1.7, 0.9, s.ALT, "level\nshifter", fs=8.2, bold=True)
    arrow(ax, 7.0, 3.2, 6.1, 3.2, lw=1.4)
    arrow(ax, 4.4, 3.2, 3.5, 3.2, lw=1.4)
    arrow(ax, 3.5, 1.6, 4.4, 1.6, lw=1.4)
    arrow(ax, 6.1, 1.6, 8.2, 2.6, lw=1.4, rad=0.25)
    ax.text(5.25, 4.0, "clamps outputs of the\nOFF domain to 0/1", ha="center", fontsize=7.6, color=s.INK2)
    ax.text(5.25, 0.6, "only if the domains run\nat different voltages", ha="center", fontsize=7.6, color=s.INK2)
    ax.annotate("", xy=(8.6, 5.2), xytext=(3.5, 3.6),
                arrowprops=dict(arrowstyle="-|>", color=s.SYNC, lw=1.3, ls="--", connectionstyle="arc3,rad=-0.25"))
    ax.text(5.2, 5.1, "enable / sequence", fontsize=8, color=s.SYNC)
    s.save(fig, "power_domain_boundary")


# ---------------------------------------------------------------- 8. 암호 하드웨어 위치
def crypto_locations():
    fig, ax = canvas(12.5, 4.8, (0, 12.8), (-0.4, 6.2))
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 9.6, 5.4, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.6))
    ax.text(0.45, 5.5, "SoC", fontsize=10, fontweight="bold", color=s.INK2)
    box(ax, 0.6, 3.4, 2.8, 1.6, s.DL, "CPU\nAES · PMULL · SHA\ninstructions, RNDR", fs=8.2, bold=True)
    box(ax, 3.7, 3.4, 2.8, 1.6, s.CTRL, "crypto engine\n(DMA-based,\nbulk / secure jobs)", fs=8.2, bold=True)
    box(ax, 6.8, 3.4, 2.7, 1.6, s.SYNC, "secure subsystem\nAES, public-key\naccelerator, keys", fs=8.2, bold=True)
    box(ax, 0.6, 1.0, 2.8, 1.6, s.SPECIAL, "TRNG\n(noise source +\npost-processing)", fs=8.2, bold=True)
    box(ax, 3.7, 1.0, 5.8, 1.6, s.UL, "UFS host controller\nwith inline crypto engine (AES-256-XTS)", fs=8.5,
        bold=True)
    box(ax, 10.4, 1.0, 2.1, 1.6, s.GRID, "UFS storage\n(only ciphertext)", fs=8.2, tc=s.INK)
    arrow(ax, 9.5, 1.8, 10.4, 1.8, lw=2.0, c=s.UL)
    ax.text(8.45, 0.65, "", fontsize=8)
    ax.text(11.45, 3.0, "file contents encrypted\non the fly, no extra\ncopy through memory",
            ha="center", fontsize=7.8, color=s.INK2)
    s.save(fig, "sec_crypto_locations")


# ---------------------------------------------------------------- 9. 저속 버스 배선
def lowspeed_wiring():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
    for ax in axes:
        s.bare(ax)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
    # I2C
    ax = axes[0]
    box(ax, 0.3, 3.0, 2.2, 2.0, s.DL, "SoC", fs=9, bold=True)
    for k, (y, n) in enumerate(((4.4, "SCL"), (3.6, "SDA"))):
        ax.plot([2.5, 9.6], [y, y], color=s.INK, lw=1.6)
        ax.text(9.7, y, n, va="center", fontsize=8.5)
    for i, n in enumerate(("touch", "charger", "sensor")):
        x = 3.3 + i * 2.2
        box(ax, x, 1.0, 1.7, 1.2, s.SYNC, n, fs=7.6)
        ax.plot([x + 0.55, x + 0.55], [2.2, 4.4], color=s.INK2, lw=1)
        ax.plot([x + 1.15, x + 1.15], [2.2, 3.6], color=s.INK2, lw=1)
    ax.plot([3.0, 3.0, 3.0], [4.4, 5.6, 5.6], color=s.INK2, lw=1)
    ax.plot([3.4, 3.4], [3.6, 5.6], color=s.INK2, lw=1)
    ax.text(3.2, 6.0, "pull-ups", ha="center", fontsize=7.8, color=s.INK2)
    ax.set_title("I²C / I3C — 2 shared wires,\naddress selects the device", fontsize=10, fontweight="bold")
    # SPI
    ax = axes[1]
    box(ax, 0.3, 2.6, 2.2, 3.0, s.DL, "SoC", fs=9, bold=True)
    for y, n in ((5.2, "SCLK"), (4.6, "MOSI"), (4.0, "MISO")):
        ax.plot([2.5, 9.6], [y, y], color=s.INK, lw=1.6)
        ax.text(9.7, y, n, va="center", fontsize=8)
    for i, n in enumerate(("UWB", "FP sensor")):
        x = 4.0 + i * 3.0
        box(ax, x, 0.8, 2.0, 1.2, s.SYNC, n, fs=8.2)
        for dx, y in ((0.4, 5.2), (1.0, 4.6), (1.6, 4.0)):
            ax.plot([x + dx, x + dx], [2.0, y], color=s.INK2, lw=1)
        cs_y = 3.3 - i * 0.5
        ax.plot([2.5, x + 1.0 + 0.05], [cs_y, cs_y], color=s.RS, lw=1.4)
        ax.plot([x + 1.0 + 0.05, x + 1.0 + 0.05], [cs_y, 2.0], color=s.RS, lw=1.4)
        ax.text(2.7, cs_y + 0.12, f"CS{i}", fontsize=7.6, color=s.RS)
    ax.set_title("SPI — shared clock/data,\none chip-select per device", fontsize=10, fontweight="bold")
    # UART
    ax = axes[2]
    box(ax, 0.5, 2.6, 2.6, 2.6, s.DL, "SoC\nUART", fs=8.8, bold=True)
    box(ax, 6.9, 2.6, 2.6, 2.6, s.SYNC, "Bluetooth\nchip", fs=8.8, bold=True)
    arrow(ax, 3.1, 4.6, 6.9, 4.6, lw=1.6)
    arrow(ax, 6.9, 3.2, 3.1, 3.2, lw=1.6)
    ax.text(5.0, 4.8, "TX → RX", ha="center", fontsize=8.5)
    ax.text(5.0, 3.4, "RX ← TX", ha="center", fontsize=8.5)
    ax.text(5.0, 1.6, "+ optional RTS/CTS flow control\nno clock wire: both sides agree on baud rate",
            ha="center", fontsize=8, color=s.INK2)
    ax.set_title("UART — point to point,\nasynchronous", fontsize=10, fontweight="bold")
    s.save(fig, "conn_lowspeed_wiring")


# ---------------------------------------------------------------- 10. 모뎀 배치
def modem_placement():
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
    for ax in axes:
        s.bare(ax)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
    ax = axes[0]
    ax.add_patch(FancyBboxPatch((0.3, 1.9), 6.2, 4.2, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.6))
    ax.text(0.5, 5.75, "SoC die", fontsize=9, fontweight="bold", color=s.INK2)
    box(ax, 0.6, 3.6, 2.5, 1.8, s.DL, "AP\nCPU·GPU·NPU", fs=8, bold=True)
    box(ax, 3.6, 3.6, 2.6, 1.8, s.UL, "modem\nbaseband", fs=8.5, bold=True)
    box(ax, 0.6, 2.2, 5.6, 0.9, s.INK2, "on-chip interconnect · shared DRAM", fs=8.2)
    box(ax, 7.2, 3.6, 2.4, 1.8, s.CTRL, "RF\ntransceiver", fs=8.5)
    arrow(ax, 6.2, 4.5, 7.2, 4.5, style="<|-|>")
    box(ax, 0.6, 0.4, 5.6, 0.9, s.SYNC, "LPDDR (shared)", fs=8.5)
    arrow(ax, 3.4, 1.3, 3.4, 2.2, style="<|-|>")
    ax.set_title("Integrated modem\n(e.g. Snapdragon 8, Dimensity flagship)", fontsize=10.5, fontweight="bold")
    ax = axes[1]
    ax.add_patch(FancyBboxPatch((0.3, 1.9), 3.6, 4.2, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.6))
    ax.text(0.5, 5.75, "SoC die", fontsize=9, fontweight="bold", color=s.INK2)
    box(ax, 0.6, 3.6, 3.0, 1.8, s.DL, "AP", fs=9, bold=True)
    box(ax, 0.6, 2.2, 3.0, 0.9, s.INK2, "PCIe root port", fs=8.2)
    ax.add_patch(FancyBboxPatch((4.8, 1.9), 2.4, 4.2, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.UL, lw=1.6))
    box(ax, 5.0, 3.6, 2.0, 1.8, s.UL, "modem\nchip", fs=8.5, bold=True)
    box(ax, 5.0, 2.2, 2.0, 0.9, s.SPECIAL, "own memory\n(if needed)", fs=7.6)
    arrow(ax, 3.6, 2.65, 5.0, 4.0, style="<|-|>", c=s.RS, lw=1.8)
    ax.text(4.4, 1.0, "chip-to-chip link\n(e.g. PCIe)", ha="center", fontsize=7.8, color=s.RS)
    box(ax, 7.9, 3.6, 1.8, 1.8, s.CTRL, "RF\ntransceiver", fs=8.2)
    arrow(ax, 7.0, 4.5, 7.9, 4.5, style="<|-|>")
    box(ax, 0.6, 0.4, 3.0, 0.9, s.SYNC, "LPDDR", fs=8.5)
    ax.set_title("Discrete modem\n(e.g. iPhone, Tensor, Exynos 2600)", fontsize=10.5, fontweight="bold")
    s.save(fig, "conn_modem_placement")


# ---------------------------------------------------------------- 11. 벤치마크
def bench_efficiency():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.4))
    fig.subplots_adjust(wspace=0.5)
    chips = ["chip A\n8 W", "chip B\n6 W"]
    score = [5000, 4500]
    ppw = [625, 750]
    x = np.arange(2)
    ax.bar(x - 0.2, score, 0.36, color=s.DL, label="score")
    ax2 = ax.twinx()
    ax2.bar(x + 0.2, ppw, 0.36, color=s.SYNC, label="score per watt")
    for i in range(2):
        ax.text(x[i] - 0.2, score[i] + 80, f"{score[i]:,}", ha="center", fontsize=9)
        ax2.text(x[i] + 0.2, ppw[i] + 10, f"{ppw[i]}", ha="center", fontsize=9, color=s.SYNC)
    ax.set_xticks(x, chips)
    ax.set_ylim(0, 6000)
    ax2.set_ylim(0, 900)
    ax.set_ylabel("score", color=s.DL)
    ax2.set_ylabel("score / W", color=s.SYNC, labelpad=10)
    for a in (ax, ax2):
        a.spines["top"].set_visible(False)
    ax.set_title("Higher score ≠ more efficient (hypothetical)", fontsize=10.5, fontweight="bold")
    n = np.arange(1, 17)
    for p, c in ((0.5, s.GRID), (0.9, s.UL), (0.95, s.CTRL)):
        bx.plot(n, 1 / ((1 - p) + p / n), color=c if c != s.GRID else s.MUTED, lw=2.2, label=f"{int(p*100)} % parallel")
    bx.plot(n, n, color=s.INK2, lw=1, ls="--", label="ideal")
    sp = 1 / (0.1 + 0.9 / 8)
    bx.plot([8], [sp], "o", color=s.UL)
    bx.annotate(f"8 cores, 90 %: ≈{sp:.1f}×", xy=(8, sp), xytext=(9.5, 2.6), fontsize=9, color=s.UL,
                arrowprops=dict(arrowstyle="-|>", color=s.UL))
    bx.set_xlabel("cores")
    bx.set_ylabel("speed-up")
    bx.set_xticks([2, 4, 6, 8, 10, 12, 14, 16])
    bx.set_ylim(0, 12)
    bx.legend(frameon=False, fontsize=8.5)
    bx.spines[["top", "right"]].set_visible(False)
    bx.set_title("Amdahl's law limits multi-core scaling", fontsize=10.5, fontweight="bold")
    s.save(fig, "sw_bench_efficiency")


# ---------------------------------------------------------------- 12. BVH
def rt_bvh():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={"width_ratios": [1.2, 1]})
    s.bare(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.add_patch(Rectangle((0.5, 0.5), 9, 6, facecolor="none", edgecolor=s.INK2, lw=1.8))
    ax.text(0.6, 6.15, "root", fontsize=8, color=s.INK2)
    ax.add_patch(Rectangle((0.8, 0.8), 4.0, 5.2, facecolor=s.DL, alpha=0.12, edgecolor=s.DL, lw=1.6))
    ax.text(0.9, 5.65, "A", fontsize=10, color=s.DL, fontweight="bold")
    ax.add_patch(Rectangle((5.3, 1.0), 3.9, 4.8, facecolor=s.UL, alpha=0.12, edgecolor=s.UL, lw=1.6))
    ax.text(5.4, 5.45, "B", fontsize=10, color=s.UL, fontweight="bold")
    ax.add_patch(Rectangle((5.6, 3.3), 1.8, 2.2, facecolor="none", edgecolor=s.UL, lw=1.2, ls="--"))
    ax.text(5.65, 5.1, "B1", fontsize=8.5, color=s.UL)
    ax.add_patch(Rectangle((7.5, 1.3), 1.5, 1.8, facecolor="none", edgecolor=s.UL, lw=1.2, ls="--"))
    ax.text(7.55, 2.75, "B2", fontsize=8.5, color=s.UL)
    for tri, c in (([(1.3, 1.4), (2.6, 1.2), (2.0, 2.6)], s.DL), ([(3.0, 3.6), (4.4, 4.0), (3.4, 5.6)], s.DL),
                   ([(5.8, 3.6), (7.2, 3.9), (6.4, 5.3)], s.UL), ([(7.7, 1.5), (8.8, 1.6), (8.2, 2.9)], s.UL)):
        ax.add_patch(Polygon(tri, closed=True, facecolor=c, alpha=0.7, edgecolor="white"))
    arrow(ax, 5.55, 6.95, 6.5, 4.4, c=s.RS, lw=2.2, z=4)
    ax.plot([6.55], [4.3], "o", color=s.RS, ms=8, zorder=5)
    ax.text(5.0, 6.7, "ray", color=s.RS, fontsize=9, fontweight="bold")
    ax.text(6.75, 4.55, "hit", color=s.RS, fontsize=9, fontweight="bold")
    ax.set_title("Boxes (AABBs) around triangles", fontsize=10.5, fontweight="bold")
    s.bare(bx)
    bx.set_xlim(0, 10)
    bx.set_ylim(0, 7)
    nodes = {"root": (5, 6.0, s.INK2), "A": (2.5, 4.2, s.DL), "B": (7.5, 4.2, s.UL),
             "B1": (6.2, 2.4, s.UL), "B2": (8.8, 2.4, s.UL)}
    for a, b in (("root", "A"), ("root", "B"), ("B", "B1"), ("B", "B2")):
        bx.plot([nodes[a][0], nodes[b][0]], [nodes[a][1], nodes[b][1]], color=s.INK2, lw=1.2, zorder=1)
    for k, (x, y, c) in nodes.items():
        hit = k in ("root", "B", "B1")
        bx.add_patch(Circle((x, y), 0.55, facecolor=c if hit else s.SURFACE, edgecolor=c, lw=1.8, zorder=2))
        bx.text(x, y, k, ha="center", va="center", fontsize=9, fontweight="bold", zorder=3,
                color="white" if hit else c)
    bx.text(2.5, 3.2, "ray misses box A\n→ skip its triangles", ha="center", fontsize=8.2, color=s.INK2)
    bx.text(6.2, 1.2, "test triangles\nin B1 → hit", ha="center", fontsize=8.2, color=s.RS)
    bx.text(8.8, 1.2, "missed", ha="center", fontsize=8.2, color=s.INK2)
    bx.set_title("BVH traversal (filled = visited)", fontsize=10.5, fontweight="bold")
    s.save(fig, "gpu_rt_bvh")


# ---------------------------------------------------------------- 13. 라이선스
def license_spectrum():
    fig, ax = canvas(11, 4.2, (0, 11.4), (-0.6, 5.2))
    arrow(ax, 0.6, 1.0, 10.8, 1.0, lw=2.4, c=s.INK2)
    ax.text(5.7, 0.45, "more design freedom  ·  more cost, people and time", ha="center", fontsize=9.5,
            color=s.INK2)
    items = [(1.0, "CSS\n(Compute Subsystem)", "pre-verified cores + DSU +\ninterconnect, physical\nreference",
              s.SYNC),
             (4.3, "core licence", "finished Cortex / C1 cores;\nchoose caches, core count",
              s.DL),
             (7.6, "architecture licence", "ISA rights only;\ndesign your own core\n(Apple, Qualcomm Oryon)",
              s.UL)]
    for x, t, d, c in items:
        box(ax, x, 3.1, 2.9, 1.0, c, t, fs=9.5, bold=True)
        ax.text(x + 1.45, 2.2, d, ha="center", va="center", fontsize=8.3, color=s.INK)
    ax.text(5.7, 4.75, "Arm licensing models (fastest to market → most differentiation)", ha="center",
            fontsize=10, fontweight="bold")
    s.save(fig, "start_license_spectrum")


if __name__ == "__main__":
    s.setup()
    history_timeline()
    arch_parallelism()
    coherence_mesi()
    sched_capacity()
    codec_block_sizes()
    mte_tags()
    power_domain_boundary()
    crypto_locations()
    lowspeed_wiring()
    modem_placement()
    bench_efficiency()
    rt_bvh()
    license_spectrum()
