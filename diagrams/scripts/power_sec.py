"""전력·보안·CPU 장 그림

1. power_thermal_throttle : 30분 지속 부하에서 성능·전력·표면 온도 (개념도, 가정값)
2. power_idle_breakeven   : 얕은/깊은 대기 상태의 체류 시간별 에너지와 손익분기점 (가정값)
3. power_rail_tree        : 배터리 → PMIC 벅/LDO → 레일 → 게이팅 스위치가 달린 파워 도메인
4. sec_boot_chain         : Boot ROM에서 커널까지의 신뢰 사슬과 예외 레벨(EL)
5. cpu_cluster_layout     : 이기종 CPU 클러스터 (전용 L1/L2, DSU 공유 L3, 인터커넥트·SLC·DRAM)
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


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, round_=True,
        z=2):
    if round_:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))
    else:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, x0, y0, x1, y1, color=None, lw=1.3, style="-|>", ls="-", z=1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=z,
                arrowprops=dict(arrowstyle=style, color=color or s.INK2, lw=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0))


def clean(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(True, color=s.GRID, lw=0.6)


# ---------------------------------------------------------------- 1. 열 스로틀링
def thermal_throttle():
    t_lim, t_amb, r_th = 43.0, 25.0, 4.0
    p_sus = n.sustained_power_w(t_lim, t_amb, r_th)      # 4.5 W
    p_peak = 2 * p_sus                                    # 가정: 순간 최대 9 W
    tau = 6.0                                             # 가정: 열 시정수(분)
    k = 2.0                                               # 가정: 제어 이득 W/°C
    dt = 0.02
    t = np.arange(0, 30 + dt, dt)
    temp = np.empty_like(t)
    pw = np.empty_like(t)
    T = t_amb
    for i in range(len(t)):
        P = float(np.clip(p_sus + k * (t_lim - T), 0, p_peak))
        temp[i], pw[i] = T, P
        T += dt * (P * r_th - (T - t_amb)) / tau
    perf = (pw / p_peak) ** (1 / 2.5) * 100              # 전력 ∝ 성능^2.5 근사 (DVFS)
    perf_sus = (p_sus / p_peak) ** (1 / 2.5) * 100

    fig, axes = plt.subplots(3, 1, figsize=(9, 7.2), sharex=True,
                             gridspec_kw=dict(hspace=0.25))
    a0, a1, a2 = axes
    a0.plot(t, perf, color=s.DL, lw=2.2)
    a0.axhline(perf_sus, color=s.MUTED, lw=1, ls="--")
    a0.set_ylabel("performance (%)")
    a0.set_ylim(50, 108)
    a0.text(29.8, perf_sus - 3, f"sustained ≈ {perf_sus:.0f}% of peak", ha="right", va="top",
            fontsize=9, color=s.INK2)
    a0.text(0.3, 103, "peak (burst)", fontsize=9, color=s.INK2, va="center")

    a1.plot(t, pw, color=s.UL, lw=2.2)
    a1.axhline(p_sus, color=s.MUTED, lw=1, ls="--")
    a1.set_ylabel("power (W)")
    a1.set_ylim(0, p_peak * 1.15)
    a1.text(29.8, p_sus + 0.35, f"P_sustained = (T_limit − T_amb) / Rθ = ({t_lim:.0f} − {t_amb:.0f}) / "
            f"{r_th:.0f} = {p_sus:.1f} W", ha="right", va="bottom", fontsize=9, color=s.INK2)

    a2.plot(t, temp, color=s.RS, lw=2.2)
    a2.axhline(t_lim, color=s.RS, lw=1, ls="--", alpha=0.7)
    a2.axhline(t_amb, color=s.MUTED, lw=1, ls=":")
    a2.text(29.8, t_lim + 0.6, f"skin limit T_limit = {t_lim:.0f} °C", ha="right", va="bottom",
            fontsize=9, color=s.INK2)
    a2.text(29.8, t_amb + 0.6, f"ambient T_amb = {t_amb:.0f} °C", ha="right", va="bottom",
            fontsize=9, color=s.INK2)
    a2.set_ylabel("skin temp (°C)")
    a2.set_ylim(22, 48)
    a2.set_xlim(0, 30)
    a2.set_xlabel("time under continuous load (min)")

    # 스로틀링 시작 지점
    i_thr = int(np.argmax(pw < p_peak - 1e-6))
    for a in axes:
        clean(a)
        a.axvspan(0, t[i_thr], color=s.EMPTY, zorder=0)
    a1.text(t[i_thr] / 2, 6.4, "burst:\nheat capacity\nabsorbs heat", ha="center", va="center",
            fontsize=8.5, color=s.INK2)
    a2.text(t[i_thr] + 0.5, 30, "throttling: governor caps OPP\nto hold skin temp at the limit",
            fontsize=8.5, color=s.INK2, va="center")
    a0.set_title("hypothetical: Rθ = 4 °C/W, 9 W burst, thermal time constant 6 min, "
                 "perf ∝ P^0.4 (not a specific phone)", fontsize=9, color=s.MUTED, loc="left")
    s.save(fig, "power_thermal_throttle")


# ---------------------------------------------------------------- 2. 대기 손익분기
def idle_breakeven():
    e_uj, p_sh, p_dp = 30.0, 50.0, 5.0
    t_be = n.idle_breakeven_ms(e_uj, p_sh, p_dp)          # ≈ 0.67 ms
    t = np.linspace(0, 2.0, 400)
    e_sh = p_sh * t                                       # mW·ms = µJ
    e_dp = e_uj + p_dp * t
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.axvspan(0, t_be, color=s.EMPTY, zorder=0)
    ax.plot(t, e_sh, color=s.DL, lw=2.2, label=f"shallow (WFI): {p_sh:.0f} mW, no entry/exit cost")
    ax.plot(t, e_dp, color=s.UL, lw=2.2,
            label=f"deep (core power-down): {p_dp:.0f} mW + {e_uj:.0f} µJ entry/exit")
    e_be = p_sh * t_be
    ax.plot([t_be], [e_be], "o", color=s.INK, zorder=5)
    ax.axvline(t_be, color=s.INK2, lw=1, ls="--")
    ax.annotate(f"break-even\nt_be = {e_uj:.0f} / ({p_sh:.0f} − {p_dp:.0f}) ≈ {t_be:.2f} ms",
                xy=(t_be, e_be), xytext=(t_be + 0.25, 12), fontsize=9.5, color=s.INK,
                arrowprops=dict(arrowstyle="-", color=s.INK2, lw=1))
    ax.text(t_be / 2, 92, "short idle:\nstay shallow", ha="center", va="top", fontsize=9.5,
            color=s.DL, fontweight="bold")
    ax.text(1.55, 92, "long idle:\ngo deep", ha="center", va="top", fontsize=9.5,
            color=s.UL, fontweight="bold")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0, 100)
    ax.set_xlabel("idle residency (ms)")
    ax.set_ylabel("energy over the idle period (µJ)")
    clean(ax)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=9, frameon=False)
    ax.set_title("assumed values (not a specific core)", fontsize=9, color=s.MUTED, loc="left")
    s.save(fig, "power_idle_breakeven")


# ---------------------------------------------------------------- 3. 레일 트리
def switch_glyph(ax, x, y, color=s.INK2):
    """작은 전원 스위치 기호 (열린 접점)."""
    ax.plot([x, x + 0.12], [y, y], color=color, lw=1.2, zorder=3)
    ax.plot([x + 0.12, x + 0.34], [y, y + 0.14], color=color, lw=1.2, zorder=3)
    ax.plot([x + 0.38, x + 0.5], [y, y], color=color, lw=1.2, zorder=3)
    ax.plot([x + 0.12, x + 0.38], [y, y], "o", ms=2.6, color=color, zorder=3)


def rail_tree():
    compute, mem, aon, io = s.DL, s.UL, s.SYNC, s.SPECIAL
    buck, ldo = s.CTRL, s.ALT
    # (레귤레이터 라벨, 종류, PMIC, 레일 이름, 색, [(도메인, 게이팅 여부)])
    rails = [
        ("multi-phase\nbuck", buck, "sub", "VDD_CPU_BIG", compute,
         [("prime core", True), ("big cores ×N", True)]),
        ("multi-phase\nbuck", buck, "sub", "VDD_GPU", compute,
         [("GPU top", True), ("shader cores ×N", True)]),
        ("buck", buck, "main", "VDD_CPU_MID", compute, [("mid cores ×N", True), ("DSU / L3", True)]),
        ("buck", buck, "main", "VDD_CPU_LIT", compute, [("little cores ×N", True)]),
        ("buck", buck, "main", "VDD_NPU", compute, [("NPU cores", True), ("NPU SRAM", True)]),
        ("buck", buck, "main", "VDD_DDR", mem, [("MC + DDR PHY", True), ("LPDDR (ext.)", False)]),
        ("LDO", ldo, "main", "VDD_AON", aon, [("AON / PMU MCU", False), ("RTC, wake IRQ", False)]),
        ("LDO", ldo, "main", "VDD_IO 1.8V", io, [("UFS / USB PHY", True), ("GPIO, I2C/I3C", False)]),
    ]
    nr = len(rails)
    rh, gap = 0.9, 0.16          # 레일 한 줄의 높이(도메인 두 개가 위아래로 분기)
    top = nr * (rh + gap)
    fig, ax = plt.subplots(figsize=(11, 8.6))
    s.bare(ax)
    ax.set_xlim(-0.2, 13.6)
    ax.set_ylim(-1.6, top + 0.9)

    ys = [top - (i + 1) * (rh + gap) + gap for i in range(nr)]
    # PMIC 외곽: sub = 첫 2개, main = 나머지
    x_reg, w_reg = 3.0, 1.9
    sub_y0, sub_y1 = ys[1] + 0.06, ys[0] + rh - 0.06
    main_y0, main_y1 = ys[-1] + 0.06, ys[2] + rh - 0.06
    for (y0, y1, lab) in ((sub_y0, sub_y1, "sub PMIC"), (main_y0, main_y1, "main PMIC")):
        ax.add_patch(FancyBboxPatch((x_reg - 0.95, y0), w_reg + 1.1, y1 - y0,
                                    boxstyle="round,pad=0,rounding_size=0.12",
                                    facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.3, zorder=1))
        ax.text(x_reg - 0.5, (y0 + y1) / 2, lab, rotation=90, ha="center", va="center",
                fontsize=9.5, color=s.INK2, fontweight="bold")

    # 배터리 → 충전 IC → VSYS
    yb = (sub_y1 + main_y0) / 2
    box(ax, 0.0, yb + 0.55, 1.4, 0.9, s.EMPTY, "Li-ion\nbattery\n3.4–4.4 V", fs=8.5, ec=s.INK2,
        tc=s.INK)
    box(ax, 0.0, yb - 1.25, 1.4, 0.9, s.EMPTY, "charger IC\n(USB in)", fs=8.5, ec=s.INK2, tc=s.INK)
    arrow(ax, 0.7, yb + 0.55, 0.7, yb - 0.35, style="<|-|>")
    ax.text(1.55, yb + 0.15, "VSYS", fontsize=9, color=s.INK2, fontweight="bold")
    # VSYS 버스
    xbus = 1.75
    ax.plot([1.4, xbus], [yb - 0.1, yb - 0.1], color=s.INK2, lw=1.8)
    ax.plot([xbus, xbus], [ys[-1] + rh / 2, ys[0] + rh / 2], color=s.INK2, lw=1.8)

    x_rail, x_j = 5.3, 8.4        # x_j: 레일이 도메인 갈래로 나뉘는 분기점
    bh, dw = 0.36, 3.3            # 도메인 박스 높이·너비
    x_box = x_j + 1.0
    rgh = 0.6                     # 레귤레이터 박스 높이
    for (rl, rc, _pm, rname, col, doms), y in zip(rails, ys):
        cy = y + rh / 2
        ax.plot([xbus, x_reg], [cy, cy], color=s.INK2, lw=1.2, zorder=0.5)
        box(ax, x_reg, cy - rgh / 2, w_reg - 0.2, rgh, rc, rl, fs=8, z=3)
        # 레일 선 (분기점까지)
        ax.plot([x_reg + w_reg - 0.2, x_j], [cy, cy], color=col, lw=3, zorder=1,
                solid_capstyle="butt")
        ax.text(x_rail + 1.4, cy + 0.08, rname, ha="center", va="bottom", fontsize=8.5,
                color=s.INK, family="DejaVu Sans Mono")
        # 도메인: 분기점에서 갈래마다 자기 스위치를 거쳐 블록으로 (병렬)
        bys = [cy] if len(doms) == 1 else [cy + 0.22, cy - 0.22]
        if len(doms) > 1:
            ax.plot([x_j, x_j], [bys[-1], bys[0]], color=col, lw=3, zorder=1,
                    solid_capstyle="projecting")
            ax.plot([x_j], [cy], "o", ms=5, color=col, zorder=2)
        for (dname, gated), by in zip(doms, bys):
            if gated:
                ax.plot([x_j, x_j + 0.2], [by, by], color=col, lw=3, zorder=1, solid_capstyle="butt")
                switch_glyph(ax, x_j + 0.2, by)
                ax.plot([x_j + 0.7, x_box], [by, by], color=col, lw=3, zorder=1,
                        solid_capstyle="butt")
            else:
                ax.plot([x_j, x_box], [by, by], color=col, lw=3, zorder=1, solid_capstyle="butt")
            box(ax, x_box, by - bh / 2, dw, bh, col, dname + ("" if gated else "  (not gated)"),
                fs=8.2, z=3)

    # 열 제목
    hy = top + 0.45
    for x, lab in ((0.7, "source"), (x_reg + 0.85, "regulator"), (x_rail + 1.4, "rail"),
                   (x_j + 2.6, "power domains (own switch each)")):
        ax.text(x, hy, lab, ha="center", va="center", fontsize=10, color=s.INK2, fontweight="bold")

    # 범례
    items = [(buck, "buck (switching)"), (ldo, "LDO"), (compute, "compute"), (mem, "memory"),
             (aon, "always-on"), (io, "I/O")]
    for i, (c, lab) in enumerate(items):
        x = 0.0 + i * 1.85 + (0.45 if i else 0)
        ax.add_patch(Rectangle((x, -0.75), 0.32, 0.32, color=c))
        ax.text(x + 0.45, -0.59, lab, fontsize=9, va="center", color=s.INK2)
    switch_glyph(ax, 11.75, -0.59)
    ax.text(12.35, -0.59, "power switch", fontsize=9, va="center", color=s.INK2)
    ax.text(0.0, -1.35, "conceptual rail map, not a specific phone; rail names, count and PMIC split "
            "vary by design", fontsize=9, color=s.MUTED)
    s.save(fig, "power_rail_tree")


# ---------------------------------------------------------------- 4. 부팅 신뢰 사슬
def boot_chain():
    lanes = [("EL3", "secure monitor", s.RS),
             ("S-EL1", "secure world", s.SPECIAL),
             ("NS-EL2 / EL1", "normal world", s.DL)]
    lh = 1.5
    fig, ax = plt.subplots(figsize=(11, 6.0))
    s.bare(ax)
    ax.set_xlim(-2.4, 13.4)
    ax.set_ylim(-1.25, len(lanes) * lh + 0.75)
    ly = {}
    for i, (name, sub, col) in enumerate(lanes):
        y0 = (len(lanes) - 1 - i) * lh
        ly[name] = y0
        ax.add_patch(Rectangle((-0.3, y0 + 0.05), 13.6, lh - 0.1, facecolor=s.EMPTY,
                               edgecolor="none", zorder=0))
        ax.add_patch(Rectangle((-0.3, y0 + 0.05), 0.12, lh - 0.1, facecolor=col, edgecolor="none"))
        ax.text(-0.45, y0 + lh / 2 + 0.17, name, ha="right", va="center", fontsize=10,
                fontweight="bold", color=s.INK)
        ax.text(-0.45, y0 + lh / 2 - 0.2, sub, ha="right", va="center", fontsize=8.5, color=s.INK2)

    bw, bh = 2.0, 0.95

    def stage(x, lane, label, col, sub=None):
        y = ly[lane] + (lh - bh) / 2
        box(ax, x, y, bw, bh, col, label, fs=9, bold=True)
        if sub:
            ax.text(x + bw / 2, y - 0.08, sub, ha="center", va="top", fontsize=7.8, color=s.INK2)
        return x, y

    rom = stage(0.2, "EL3", "Boot ROM\n(BL1 / PBL)", s.RS)
    bl2 = stage(2.9, "S-EL1", "BL2\nearly loader", s.SPECIAL, "DRAM training")
    bl31 = stage(6.4, "EL3", "BL31\nEL3 runtime", s.RS, "PSCI, world switch")
    bl32 = stage(6.4, "S-EL1", "BL32\nTEE OS", s.SPECIAL)
    bl33 = stage(8.2, "NS-EL2 / EL1", "BL33\nbootloader", s.DL, "ABL / U-Boot / UEFI")
    kern = stage(11.25, "NS-EL2 / EL1", "kernel +\nAndroid", s.DL)

    # 퓨즈
    box(ax, -0.1, len(lanes) * lh + 0.02, 2.6, 0.6, s.CTRL, "OTP fuses\nroot key hash", fs=8.5)
    arrow(ax, 1.2, len(lanes) * lh + 0.02, 1.2, rom[1] + bh, color=s.CTRL)

    def link(a, b, label, side_out="r", lx=None, ly_=None, ha="center"):
        ax_, ay = a
        bx, by = b
        if side_out == "r":
            x0, y0 = ax_ + bw, ay + bh / 2
        elif side_out == "b":
            x0, y0 = ax_ + bw * 0.75, ay
        else:  # top
            x0, y0 = ax_ + bw * 0.75, ay + bh
        x1, y1 = bx, by + bh / 2
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=s.INK, lw=1.4, shrinkA=0, shrinkB=0,
                                    connectionstyle="arc3,rad=0"), zorder=4)
        mx = lx if lx is not None else (x0 + x1) / 2
        my = ly_ if ly_ is not None else (y0 + y1) / 2
        ax.text(mx, my, label, ha=ha, va="center", fontsize=7.8, color=s.INK, zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc=s.SURFACE, ec="none"))

    link(rom, bl2, "verify sig")
    link(bl2, bl31, "verify sig")
    link(bl2, bl32, "verify sig")
    link(bl2, bl33, "verify sig", side_out="b")
    link(bl33, kern, "AVB\nvbmeta")
    # 실행 순서 메모 (BL31이 BL32·BL33으로 넘김)
    ax.text(10.5, ly["EL3"] + lh / 2, "BL31 hands off to BL32,\nthen to BL33",
            ha="center", va="center", fontsize=8, color=s.INK2)
    ax.text(kern[0] + bw / 2, kern[1] - 0.08, "dm-verity on\nsystem partitions", ha="center",
            va="top", fontsize=7.8, color=s.INK2)

    ax.text(-0.3, -0.5, "root of trust: ROM code is immutable; each stage verifies the next "
            "before running it (signature chained to the fused key hash)", fontsize=9,
            color=s.INK2)
    ax.text(-0.3, -1.0, "generic TF-A naming; stage count, ELs and vendor names differ "
            "(e.g. BL2 may run at EL3, kernel at EL1 or EL2)", fontsize=9, color=s.MUTED)
    s.save(fig, "sec_boot_chain")


# ---------------------------------------------------------------- 5. CPU 클러스터
def cluster_layout():
    fig, ax = plt.subplots(figsize=(11, 6.4))
    s.bare(ax)
    ax.set_xlim(-0.2, 13.2)
    ax.set_ylim(-2.4, 6.9)

    # DSU 클러스터 외곽
    ax.add_patch(FancyBboxPatch((0, 1.55), 13.0, 5.1, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, lw=1.5, zorder=0))
    ax.text(0.2, 6.4, "CPU cluster (DSU)", fontsize=10, color=s.INK2, fontweight="bold", va="center")

    cores = [("prime", 1, 2.0, s.RS), ("big", 3, 1.5, s.UL), ("little", 4, 1.05, s.SYNC)]
    x = 0.25
    gapc = 0.15
    for kind, cnt, w, col in cores:
        x_start = x
        for i in range(cnt):
            hh = 3.2 if kind == "prime" else (2.9 if kind == "big" else 2.5)
            y0 = 2.85
            ax.add_patch(FancyBboxPatch((x, y0), w, hh, boxstyle="round,pad=0,rounding_size=0.08",
                                        facecolor=s.SURFACE, edgecolor=col, lw=1.8, zorder=1))
            box(ax, x + 0.08, y0 + hh - 0.95, w - 0.16, 0.85, col, f"{kind}\ncore", fs=8.5, bold=True)
            box(ax, x + 0.08, y0 + hh - 1.55, w - 0.16, 0.5, s.DL, "L1 I/D", fs=8)
            l2h = hh - 1.75
            box(ax, x + 0.08, y0 + 0.1, w - 0.16, l2h, s.CTRL, "L2", fs=8.5)
            x += w + gapc
        ax.text((x_start + x - gapc) / 2, 2.62, f"{cnt}× {kind}" if cnt > 1 else f"1× {kind}",
                ha="center", va="top", fontsize=9, color=s.INK2)
        x += 0.25

    # 공유 L3
    box(ax, 0.25, 1.75, 12.5, 0.55, s.SYNC, "shared L3  +  snoop filter  (DSU)", fs=9.5, bold=True,
        round_=False)

    # 인터커넥트
    box(ax, 0.0, 0.3, 13.0, 0.6, s.INK2, "coherent interconnect / NoC  (e.g. CHI)", fs=9.5,
        round_=False)
    arrow(ax, 6.5, 1.75, 6.5, 0.9, style="<|-|>", lw=1.6)

    # 다른 마스터, SLC, DRAM
    for i, lab in enumerate(["GPU", "NPU", "ISP / media"]):
        box(ax, 0.0 + i * 1.6, -1.25, 1.45, 0.85, s.DL, lab, fs=8.5)
        arrow(ax, 0.72 + i * 1.6, -0.4, 0.72 + i * 1.6, 0.3, style="<|-|>")
    box(ax, 6.0, -1.25, 2.4, 0.85, s.SYNC, "SLC\n(system cache)", fs=8.5, bold=True)
    box(ax, 8.9, -1.25, 1.9, 0.85, s.UL, "memory\ncontrollers", fs=8.5)
    box(ax, 11.3, -1.25, 1.7, 0.85, s.UL, "LPDDR\nDRAM", fs=8.5, bold=True)
    arrow(ax, 7.2, -0.4, 7.2, 0.3, style="<|-|>")
    arrow(ax, 8.4, -0.83, 8.9, -0.83, style="<|-|>")
    arrow(ax, 10.8, -0.83, 11.3, -0.83, style="<|-|>")

    ax.text(0.0, -1.85, "private per core: L1, L2 (+ own clock/power domain);  shared in cluster: "
            "L3;  shared SoC-wide: SLC, DRAM", fontsize=9, color=s.INK2)
    ax.text(0.0, -2.25, "conceptual 1+3+4 layout, not a specific chip; box sizes are not to "
            "scale; some designs pair little cores to share L2", fontsize=9, color=s.MUTED)
    s.save(fig, "cpu_cluster_layout")


if __name__ == "__main__":
    s.setup()
    thermal_throttle()
    idle_breakeven()
    rail_tree()
    boot_chain()
    cluster_layout()
