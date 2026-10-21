"""계보·구성·이름 그림 (2차 보강)

1. cpu_arm_core_timeline   : Arm 모바일 코어 세대표 (2012–2026, 등급별)
2. cpu_cluster_cache       : Arm DSU 클러스터(코어 전용 L2 + 공유 L3) vs 자체 코어 클러스터(공유 대형 L2)
3. gpu_family_lineage      : 모바일 GPU 계열별 아키텍처 계보
4. npu_design_styles       : DSP 확장형(Hexagon) 진화 경로와 전용 설계형 NPU 구조
5. conn_wifi_bt_links      : 콤보 칩과 SoC·모뎀·오디오 DSP 사이 연결
6. design_ip_sources       : SoC 블록별 IP 출처(라이선스·자체·기초 IP)와 통합 작업
7. sec_attack_map          : 필요한 접근 수준별 하드웨어 공격과 대응
8. naming_anatomy          : 칩셋 이름에서 등급·세대·변형 읽기
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, x0, y0, x1, y1, c=None, lw=1.4, style="-|>", rad=0.0, z=1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=12,
                                 color=c or s.INK2, linewidth=lw, zorder=z,
                                 connectionstyle=f"arc3,rad={rad}"))


def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    s.bare(ax)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return fig, ax


# ---------------------------------------------------------------- 1. Arm 코어 세대표
def arm_core_timeline():
    # (연도 시작, 연도 끝, 이름) — docs/cpu/arm-cores.md 표와 같음
    top = [(2020, 2020, "X1"), (2021, 2021, "X2"), (2022, 2022, "X3"), (2023, 2023, "X4"),
           (2024, 2024, "X925"), (2025, 2025, "C1-Ultra"), (2026, 2026, "C2-Ultra")]
    mid = [(2012, 2012, "A57"), (2015, 2015, "A72"), (2016, 2016, "A73"), (2017, 2017, "A75"),
           (2018, 2018, "A76"), (2019, 2019, "A77"), (2020, 2020, "A78"), (2021, 2021, "A710"),
           (2022, 2022, "A715"), (2023, 2023, "A720"), (2024, 2024, "A725"), (2025, 2025, "C1-Premium\n/ C1-Pro"),
           (2026, 2026, "C2-Pro")]
    eff = [(2012, 2016, "A53"), (2017, 2020, "A55"), (2021, 2022, "A510"), (2023, 2024, "A520"),
           (2025, 2025, "C1-Nano")]
    arch = [(2012, 2016, "Armv8.0", s.GRID), (2017, 2020, "Armv8.2", s.EMPTY), (2021, 2022, "Armv9.0", s.GRID),
            (2023, 2024, "Armv9.2", s.EMPTY), (2025, 2026, "Armv9.3", s.GRID)]
    fig, ax = canvas(13, 4.6, (2011.4, 2026.7), (-0.9, 4.3))
    rows = [(3.0, "top performance\n(Cortex-X / Ultra)", top, s.UL),
            (2.0, "balanced\n(A7xx / Premium·Pro)", mid, s.DL),
            (1.0, "high efficiency\n(A5xx / Nano)", eff, s.SYNC)]
    for y, lab, items, c in rows:
        ax.text(2011.35, y, lab, ha="right", va="center", fontsize=8.8, color=s.INK2)
        for a, b, n in items:
            fs = 6.3 if "\n" in n else (7.0 if len(n) > 5 else 8.2)
            box(ax, a - 0.45, y - 0.36, b - a + 0.9, 0.72, c, n, fs=fs, bold=True)
    for a, b, n, c in arch:
        ax.add_patch(Rectangle((a - 0.5, -0.05), b - a + 1, 0.5, facecolor=c, edgecolor="none"))
        ax.text((a + b) / 2, 0.2, n, ha="center", va="center", fontsize=8.5, color=s.INK)
    for yr in range(2012, 2027, 2):
        ax.text(yr, -0.45, str(yr), ha="center", fontsize=8.5, color=s.INK2)
    ax.text(2026, 1.0, "none\nannounced", ha="center", va="center", fontsize=7.0, color=s.MUTED)
    ax.text(2019.0, 3.9, "announcement year (not phone shipping year); 2026 per Arm's announcement",
            ha="center", fontsize=8.5, color=s.MUTED)
    s.save(fig, "cpu_arm_core_timeline")


# ---------------------------------------------------------------- 2. 클러스터 캐시 구성
def cluster_cache():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for ax in axes:
        s.bare(ax)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
    ax = axes[0]
    cores = [("X / Ultra", s.UL), ("A7xx", s.DL), ("A7xx", s.DL), ("A7xx", s.DL), ("A5xx", s.SYNC), ("A5xx", s.SYNC)]
    for i, (n, c) in enumerate(cores):
        x = 0.3 + i * 1.6
        box(ax, x, 4.6, 1.4, 1.0, c, n, fs=8, bold=True)
        box(ax, x, 3.6, 1.4, 0.8, s.CTRL, "L2\n(private)", fs=7.4)
    box(ax, 0.3, 2.2, 9.4, 1.0, s.SPECIAL, "DSU: shared L3 + snoop control", fs=9, bold=True)
    box(ax, 0.3, 0.6, 9.4, 1.0, s.INK2, "interconnect → SLC → DRAM", fs=9)
    ax.set_title("Arm cores (DynamIQ / DSU)\nprivate L2 per core + shared L3", fontsize=10.5, fontweight="bold")
    ax = axes[1]
    for i in range(4):
        box(ax, 0.6 + i * 1.15, 4.6, 1.0, 1.0, s.UL, "P", fs=9, bold=True)
    for i in range(4):
        box(ax, 5.6 + i * 1.0, 4.6, 0.85, 1.0, s.SYNC, "E", fs=9, bold=True)
    box(ax, 0.6, 3.0, 4.45, 1.3, s.CTRL, "shared L2 (large, MB-class)\nfor the P cluster", fs=8.5, bold=True)
    box(ax, 5.6, 3.0, 3.85, 1.3, s.CTRL, "shared L2\nfor the E cluster", fs=8.5)
    box(ax, 0.3, 0.6, 9.4, 1.0, s.INK2, "fabric → SLC → DRAM", fs=9)
    ax.plot([2.8, 2.8], [1.6, 3.0], color=s.INK2, lw=1.4)
    ax.plot([7.5, 7.5], [1.6, 3.0], color=s.INK2, lw=1.4)
    ax.set_title("Custom cores (e.g. Apple, Oryon)\ncluster-shared large L2", fontsize=10.5, fontweight="bold")
    fig.text(0.5, 0.01, "conceptual; core counts and cache sizes vary by chip", ha="center", fontsize=8.5,
             color=s.MUTED)
    s.save(fig, "cpu_cluster_cache")


# ---------------------------------------------------------------- 3. GPU 계보
def gpu_family_lineage():
    fig, ax = canvas(13, 5.2, (-0.2, 13.4), (-0.4, 6.0))
    lanes = [
        ("Arm Mali", s.DL, ["Utgard\n(split shaders)", "Midgard\n(unified, SIMD)", "Bifrost\n(scalar quads)",
                            "Valhall", "5th gen\n(deferred vertex)", "Mali G1\n(2025)"]),
        ("Qualcomm Adreno", s.UL, ["2xx", "3xx … 6xx", "7xx", "8xx\n(sliced GPU,\n8 Elite era)"]),
        ("Samsung Xclipse", s.ALT, ["RDNA 2 based\n(Exynos 2200)", "RDNA 3 family\n(2400 · 2500)",
                                    "new arch\n(2600, Xclipse 960)"]),
        ("Apple GPU", s.SYNC, ["PowerVR licence\n(early iPhone)", "in-house\n(A11, 2017)",
                               "HW ray tracing +\nDynamic Caching\n(A17 Pro / M3, 2023)"]),
        ("Imagination PowerVR", s.CTRL, ["SGX", "Rogue", "Furian", "A · B · C · D", "E series\n(2025)"]),
    ]
    for r, (name, c, gens) in enumerate(lanes):
        y = 4.9 - r * 1.15
        ax.text(2.1, y, name, ha="right", va="center", fontsize=9.5, fontweight="bold", color=c)
        n = len(gens)
        w = (13.2 - 2.4) / n
        for i, g in enumerate(gens):
            x = 2.4 + i * w
            box(ax, x, y - 0.45, w - 0.25, 0.9, c, g, fs=7.4)
            if i:
                arrow(ax, x - 0.25, y, x, y, lw=1.1)
    ax.text(7.8, 5.75, "older  →  newer   (columns are not aligned in time)", ha="center", fontsize=9,
            color=s.MUTED)
    s.save(fig, "gpu_family_lineage")


# ---------------------------------------------------------------- 4. NPU 설계 방식
def npu_design_styles():
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    s.bare(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    steps = [("scalar\nDSP", s.GRID), ("+ vector\n(HVX)", s.DL),
             ("+ tensor\naccel.\n(SD 855)", s.CTRL), ("fused\nS · V · T\n(~SD 888)", s.UL),
             ("Hexagon\nNPU\n(INT4,\ntransformer)", s.UL)]
    for i, (t, c) in enumerate(steps):
        x = 0.1 + i * 2.0
        box(ax, x, 3.4, 1.75, 1.9, c, t, fs=7.4, bold=True, tc=s.INK if c == s.GRID else None)
        if i:
            arrow(ax, x - 0.25, 4.35, x, 4.35)
    ax.text(5.0, 6.2, "DSP-extension path (Qualcomm Hexagon)", ha="center", fontsize=10.5, fontweight="bold")
    ax.text(5.0, 2.2, "programmable vector units absorb new operators;\ngenerality costs some area/power",
            ha="center", fontsize=8.8, color=s.INK2)
    ax = axes[1]
    s.bare(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.text(5.0, 6.2, "dedicated design (ANE, TPU, Samsung, MediaTek)", ha="center", fontsize=10.5,
            fontweight="bold")
    box(ax, 0.5, 3.0, 4.2, 2.4, s.UL, "MAC array\n(fixed-function\ntensor engine)", fs=9, bold=True)
    box(ax, 5.0, 4.3, 4.4, 1.1, s.DL, "vector / activation unit", fs=8.5)
    box(ax, 5.0, 3.0, 4.4, 1.1, s.SPECIAL, "local SRAM + DMA", fs=8.5, bold=True)
    box(ax, 0.5, 1.3, 8.9, 1.0, s.EMPTY, "unsupported ops → handed to CPU / GPU / DSP", fs=8.5, tc=s.INK,
        ec=s.MUTED)
    arrow(ax, 4.95, 2.3, 4.95, 3.0, style="<|-")
    ax.text(5.0, 0.5, "best efficiency on supported ops; compiler-driven, mostly closed", ha="center", fontsize=8.8,
            color=s.INK2)
    s.save(fig, "npu_design_styles")


# ---------------------------------------------------------------- 5. Wi-Fi·BT 연결
def wifi_bt_links():
    fig, ax = canvas(12, 5.0, (0, 12.4), (-0.3, 6.4))
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 4.6, 5.6, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.6))
    ax.text(0.45, 5.7, "SoC", fontsize=10, fontweight="bold", color=s.INK2)
    box(ax, 0.6, 4.2, 3.0, 0.9, s.DL, "PCIe root port", fs=8.8)
    box(ax, 0.6, 3.0, 3.0, 0.9, s.CTRL, "UART (BT HCI)", fs=8.8)
    box(ax, 0.6, 1.8, 3.0, 0.9, s.ALT, "audio DSP", fs=8.8)
    box(ax, 0.6, 0.7, 3.0, 0.8, s.GRID, "GPIO", fs=8.8, tc=s.INK)
    box(ax, 7.0, 1.4, 2.8, 3.8, s.SYNC, "Wi-Fi + Bluetooth\ncombo chip\n\nPTA arbiter\n(2.4 GHz sharing)", fs=9,
        bold=True)
    links = [(4.65, "Wi-Fi data\nPCIe x1 (≈0.5–0.98 GB/s)", s.DL),
             (3.45, "BT commands/data\nUART (≈300 kB/s)", s.CTRL),
             (2.25, "BT voice/audio\nPCM·I²S, SoundWire", s.ALT),
             (1.1, "power on, host wake, reset", s.INK2)]
    for y, t, c in links:
        arrow(ax, 3.6, y, 7.0, y, c=c, lw=1.8, style="<|-|>")
        ax.text(5.3, y + 0.2, t, ha="center", va="bottom", fontsize=7.6, color=c, linespacing=1.1)
    box(ax, 10.4, 4.3, 1.8, 0.9, s.UL, "cellular\nmodem", fs=8.5, bold=True)
    arrow(ax, 9.8, 4.0, 10.4, 4.6, c=s.RS, lw=1.6, style="<|-|>")
    ax.text(11.3, 3.6, "coex link\n(TX timing)", ha="center", fontsize=8, color=s.RS)
    ax.plot([8.4, 8.4], [5.2, 5.8], color=s.INK2, lw=1.4)
    ax.plot([8.1, 8.4, 8.7], [6.15, 5.8, 6.15], color=s.INK2, lw=1.4)
    ax.text(8.9, 5.9, "shared antenna", fontsize=8, color=s.INK2, va="center")
    s.save(fig, "conn_wifi_bt_links")


# ---------------------------------------------------------------- 6. IP 출처
def ip_sources():
    fig, ax = canvas(12.5, 5.2, (0, 12.8), (-0.6, 6.4))
    lic, own, base = s.DL, s.UL, s.GRID
    ax.add_patch(FancyBboxPatch((0.2, 0.2), 8.6, 5.8, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.6))
    ax.text(0.45, 5.7, "SoC (example mix)", fontsize=10, fontweight="bold", color=s.INK2)
    blocks = [(0.5, 4.2, 2.5, 1.1, lic, "CPU cluster\n(Arm Cortex + DSU)"),
              (3.2, 4.2, 2.5, 1.1, lic, "GPU\n(Mali / PowerVR)"),
              (5.9, 4.2, 2.6, 1.1, own, "modem\n(in-house)"),
              (0.5, 2.8, 2.5, 1.1, own, "NPU\n(in-house)"),
              (3.2, 2.8, 2.5, 1.1, own, "ISP / media\n(in-house)"),
              (5.9, 2.8, 2.6, 1.1, lic, "NoC\n(Arteris, Arm NI)"),
              (0.5, 1.5, 8.0, 1.0, lic, "PHY + controllers: LPDDR, UFS (M-PHY), PCIe, USB, MIPI  (Synopsys, Cadence …)"),
              (0.5, 0.45, 8.0, 0.8, base, "foundation IP: standard cells, SRAM compiler, I/O cells, PLL")]
    for x, y, w, h, c, t in blocks:
        box(ax, x, y, w, h, c, t, fs=8.2, tc=s.INK if c == base else None)
    for i, (c, t) in enumerate(((lic, "licensed IP"), (own, "in-house design"), (base, "foundry / IP vendor basics"))):
        ax.add_patch(Rectangle((0.5 + i * 2.9, -0.45), 0.3, 0.3, facecolor=c, edgecolor="none"))
        ax.text(0.9 + i * 2.9, -0.3, t, va="center", fontsize=8.5, color=s.INK2)
    ax.text(10.8, 5.6, "integration work", ha="center", fontsize=10, fontweight="bold")
    tasks = ["bus & address map", "clocks + CDC", "reset sequence", "power domains (UPF)",
             "interrupts · DMA · IOMMU IDs", "register map → RTL / headers", "debug & trace (CoreSight)"]
    for i, t in enumerate(tasks):
        box(ax, 9.3, 4.8 - i * 0.72, 3.1, 0.6, s.CTRL, t, fs=7.8)
    arrow(ax, 9.3, 3.0, 8.8, 3.0, lw=1.6)
    s.save(fig, "design_ip_sources")


# ---------------------------------------------------------------- 7. 공격 지도
def attack_map():
    fig, ax = canvas(12.5, 5.0, (0, 12.8), (-0.4, 6.4))
    ax.text(3.1, 6.0, "needs physical access", ha="center", fontsize=10.5, fontweight="bold", color=s.UL)
    ax.text(9.6, 6.0, "needs code running on the same chip", ha="center", fontsize=10.5, fontweight="bold",
            color=s.DL)
    phys = [("voltage / clock glitch", "glitch sensors, redundant checks"),
            ("EM / laser fault injection", "shielding, light sensors, reset on fault"),
            ("power / EM side channel", "masking, constant-time hardware"),
            ("JTAG / debug port", "debug fuses, authenticated debug")]
    soft = [("cache timing", "constant-time code, cache partitioning"),
            ("Spectre-class speculation", "predictor isolation (CSV2), barriers"),
            ("Rowhammer (DRAM)", "TRR / RFM, data placement")]
    for i, (a, d) in enumerate(phys):
        y = 4.9 - i * 1.2
        box(ax, 0.2, y, 2.7, 0.9, s.UL, a, fs=8.2, bold=True)
        box(ax, 3.1, y, 3.0, 0.9, s.EMPTY, d.replace(", ", ",\n", 1), fs=7.6, tc=s.INK, ec=s.MUTED)
    for i, (a, d) in enumerate(soft):
        y = 4.9 - i * 1.2
        box(ax, 6.7, y, 2.7, 0.9, s.DL, a, fs=8.2, bold=True)
        box(ax, 9.6, y, 3.0, 0.9, s.EMPTY, d.replace(", ", ",\n", 1), fs=7.6, tc=s.INK, ec=s.MUTED)
    box(ax, 6.7, 1.3, 5.9, 0.9, s.SYNC, "memory-safety hardening: PAC · BTI · MTE · CCA", fs=8.6, bold=True)
    ax.plot([6.4, 6.4], [0.0, 5.9], color=s.GRID, lw=1.4, ls="--")
    ax.text(3.1, -0.2, "attack  →  typical countermeasure", ha="center", fontsize=8.5, color=s.MUTED)
    ax.text(9.6, -0.2, "attack  →  typical countermeasure", ha="center", fontsize=8.5, color=s.MUTED)
    s.save(fig, "sec_attack_map")


# ---------------------------------------------------------------- 8. 이름 해부
def naming_anatomy():
    fig, ax = canvas(12.5, 4.8, (0, 13.6), (-0.3, 6.2))
    tier, gen, var = s.UL, s.DL, s.SYNC
    examples = [
        ("Snapdragon", [("8", tier), (" Elite", var), (" Gen 5", gen)]),
        ("Exynos", [("2", tier), ("6", gen), ("00", s.GRID)]),
        ("Dimensity", [("9", tier), ("5", gen), ("00", s.GRID)]),
        ("Apple", [("A", s.GRID), ("19", gen), (" Pro", var)]),
    ]
    for r, (brand, parts) in enumerate(examples):
        y = 5.1 - r * 1.25
        ax.text(3.0, y, brand, ha="right", va="center", fontsize=13, color=s.INK2)
        x = 3.2
        for t, c in parts:
            w = 0.3 * len(t.strip()) + 0.4
            box(ax, x, y - 0.42, w, 0.84, c, t.strip(), fs=13, bold=True, tc=s.INK if c == s.GRID else None)
            x += w + 0.12
    notes = ["8 = flagship tier · Elite = top brand · Gen 5 = generation",
             "2 = flagship (1x80 = mid-range) · 6 = generation",
             "9 = flagship tier (8/7/6 below) · 5 = generation",
             "19 = generation · Pro = variant for Pro iPhones"]
    for r, t in enumerate(notes):
        ax.text(8.0, 5.1 - r * 1.25, t, va="center", fontsize=9, color=s.INK2)
    for i, (c, t) in enumerate(((tier, "tier"), (gen, "generation"), (var, "variant / brand"))):
        ax.add_patch(Rectangle((3.2 + i * 2.4, -0.15), 0.3, 0.3, facecolor=c, edgecolor="none"))
        ax.text(3.6 + i * 2.4, 0.0, t, va="center", fontsize=9, color=s.INK2)
    s.save(fig, "naming_anatomy")


if __name__ == "__main__":
    s.setup()
    arm_core_timeline()
    cluster_cache()
    gpu_family_lineage()
    npu_design_styles()
    wifi_bt_links()
    ip_sources()
    attack_map()
    naming_anatomy()
