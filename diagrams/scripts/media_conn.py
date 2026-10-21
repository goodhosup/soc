"""멀티미디어·연결 그림

1. media_isp_pipeline        : 센서 → CSI-2 → ISP 단계(raw 영역 → YUV 영역) → NPU/GPU 보조 → 인코더·디스플레이
2. media_data_rates          : 카메라·비디오·디스플레이 비압축 데이터 속도와 D-PHY·C-PHY 링크 용량
3. media_display_composition : 레이어 → DPU 평면 합성 vs GPU 합성 → DSC → DSI → 패널
4. conn_soc_map              : SoC 안의 연결 블록과 외부 칩, 그 사이 버스 이름 (개념도)
5. conn_link_bandwidth       : PCIe·USB·SDIO·UART 한 방향 이론 대역폭 (로그 축)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import style as s

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import soc_numbers as n  # noqa: E402


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, round_=True):
    if round_:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=fc, edgecolor=ec, linewidth=lw))
    else:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, x0, y0, x1, y1, color=None, lw=1.3, style="-|>", ls="-", both=False):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="<|-|>" if both else style, color=color or s.INK2,
                                lw=lw, linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=11))


def region(ax, x, y, w, h, label, fc=None, ec=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=fc or s.EMPTY, edgecolor=ec or s.GRID, linewidth=1.2))
    ax.text(x + 0.12, y + h - 0.2, label, fontsize=9, color=s.INK2, va="center", fontweight="bold")


def legend(ax, items, x0, y, step):
    for i, (c, lab) in enumerate(items):
        x = x0 + i * step
        ax.add_patch(Rectangle((x, y), 0.3, 0.3, color=c))
        ax.text(x + 0.42, y + 0.15, lab, fontsize=9, va="center", color=s.INK2)


# ---------------------------------------------------------------- 1. ISP 파이프라인
def isp_pipeline():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    s.bare(ax)
    ax.set_xlim(-0.2, 14.2)
    ax.set_ylim(-1.3, 6.2)

    RAW, YUV, STAT, AIC, OUT, SRC = s.UL, s.DL, s.SPECIAL, s.CTRL, s.SYNC, s.INK2
    y, h = 3.2, 1.1

    # 센서·수신기
    box(ax, 0.0, y, 1.3, h, SRC, "Image\nsensor", fs=9, bold=True)
    box(ax, 1.75, y, 1.2, h, SRC, "CSI-2\nRX", fs=9)
    arrow(ax, 1.3, y + h / 2, 1.75, y + h / 2)
    ax.text(1.52, y + h + 0.18, "D-/C-PHY", fontsize=7.5, color=s.MUTED, ha="center")

    # raw 영역
    region(ax, 3.25, 2.55, 5.05, 3.25, "raw (Bayer) domain")
    raw = [("BLC ·\ndefect ·\nlens shading", 3.4), ("HDR\nmerge", 5.0), ("Demosaic", 6.55)]
    ws = [1.4, 1.35, 1.6]
    for (lab, x), w in zip(raw, ws):
        box(ax, x, y, w, h, RAW, lab, fs=8.5)
    arrow(ax, 2.95, y + h / 2, 3.4, y + h / 2)
    arrow(ax, 4.8, y + h / 2, 5.0, y + h / 2)
    arrow(ax, 6.35, y + h / 2, 6.55, y + h / 2)

    # 3A 통계 (raw에서 탭)
    box(ax, 3.4, 1.0, 1.4, 0.8, STAT, "3A stats\n(AE·AF·AWB)", fs=8)
    arrow(ax, 4.1, y, 4.1, 1.8, ls="--")
    # 3A 피드백 → 센서
    ax.plot([3.4, 0.65, 0.65], [1.4, 1.4, y], color=s.INK2, lw=1.2, ls="--")
    arrow(ax, 0.65, y - 0.4, 0.65, y, lw=1.2)
    ax.text(1.95, 1.55, "exposure · gain · focus\n(firmware, via I2C/I3C)", fontsize=7.5,
            color=s.INK2, ha="center", va="bottom")

    # YUV 영역
    region(ax, 8.55, 2.55, 3.35, 3.25, "RGB / YUV domain")
    box(ax, 8.7, y, 1.35, h, YUV, "Noise\nreduction", fs=8.5)
    box(ax, 10.25, y, 1.5, h, YUV, "Color ·\ntone map ·\nscale", fs=8.5)
    arrow(ax, 8.15, y + h / 2, 8.7, y + h / 2)
    arrow(ax, 10.05, y + h / 2, 10.25, y + h / 2)

    # 출력
    outs = [("Video encoder", 4.75), ("Display / preview", 3.75), ("JPEG / HEIF\nstill", 2.55)]
    for lab, oy in outs:
        box(ax, 12.45, oy, 1.7, 0.8, OUT, lab, fs=8.2)
        arrow(ax, 11.75, y + h / 2, 12.45, oy + 0.4, lw=1.1)
    ax.text(13.3, 5.75, "YUV streams", fontsize=8, color=s.INK2, ha="center")

    # NPU / GPU 보조 (메모리 경유)
    box(ax, 5.0, -0.25, 7.0, 0.8, s.EMPTY, "", ec=s.GRID)
    ax.text(8.5, 0.15, "DRAM / SLC frame buffers (multi-frame ring buffer)", fontsize=8.5,
            color=s.INK2, ha="center", va="center")
    box(ax, 8.7, 1.0, 3.05, 0.8, AIC, "NPU / GPU assist\n(segmentation · AI denoise)", fs=8)
    arrow(ax, 6.0, y, 6.0, 0.55, ls="--", both=True)   # HDR merge ↔ 메모리 (버스트 프레임)
    arrow(ax, 10.2, 1.0, 10.2, 0.55, both=True)
    arrow(ax, 9.35, y, 9.35, 1.8, ls="--", both=True)
    arrow(ax, 11.0, y, 11.0, 1.8, ls="--", both=True)

    legend(ax, [(RAW, "raw stages"), (YUV, "RGB/YUV stages"), (STAT, "3A statistics"),
                (AIC, "NPU/GPU"), (OUT, "consumers")], 0.0, -1.15, 2.6)
    ax.text(0.0, 5.95, "typical stage order; varies by vendor (conceptual)", fontsize=8.5, color=s.MUTED)
    s.save(fig, "media_isp_pipeline")


# ---------------------------------------------------------------- 2. 데이터 속도
def data_rates():
    cam, vid, disp = s.UL, s.ALT, s.DL
    rows = [
        ("12MP 10b 30fps sensor", n.pixel_rate_gbps(4000, 3000, 10, 30), cam),
        ("4K 10b 60fps sensor readout", n.pixel_rate_gbps(3840, 2160, 10, 60), cam),
        ("50MP 10b 30fps sensor", n.pixel_rate_gbps(8192, 6144, 10, 30), cam),
        ("4K60 10b 4:2:0 video", n.pixel_rate_gbps(3840, 2160, 15, 60), vid),
        ("8K30 10b 4:2:0 video", n.pixel_rate_gbps(7680, 4320, 15, 30), vid),
        ("QHD+ 120Hz DSC 8bpp", n.pixel_rate_gbps(1440, 3120, 8, 120), disp),
        ("QHD+ 120Hz 24b uncompressed", n.pixel_rate_gbps(1440, 3120, 24, 120), disp),
        ("4K 120Hz 30b (external out)", n.pixel_rate_gbps(3840, 2160, 30, 120), disp),
    ]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    ys = range(len(rows))
    ax.barh(list(ys), [r[1] for r in rows], color=[r[2] for r in rows], height=0.62)
    for yy, (lab, v, _) in zip(ys, rows):
        ax.text(v + 0.5, yy, f"{v:.1f}", va="center", fontsize=9, color=s.INK)
    ax.set_yticks(list(ys), [r[0] for r in rows])
    links = [("D-PHY 4 lanes", n.dphy_gbps(4), s.INK2, "--"),
             ("C-PHY 1 trio", n.cphy_gbps(1), s.MUTED, ":"),
             ("C-PHY 3 trios", n.cphy_gbps(3), s.INK2, "-.")]
    top = len(rows) - 0.4
    for lab, v, c, ls in links:
        ax.axvline(v, color=c, ls=ls, lw=1.4)
        left = lab == "C-PHY 1 trio"
        ax.text(v - 0.4 if left else v + 0.4, top, f"{lab}\n{v:.1f} Gbps", fontsize=8.5, color=c,
                va="bottom", ha="right" if left else "left")
    ax.set_xlim(0, 46)
    ax.set_ylim(-0.6, len(rows) + 0.6)
    ax.set_xlabel("uncompressed active-pixel data rate (Gbps)")
    ax.grid(True, axis="x", color=s.GRID, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cam, label="camera sensor"), Patch(color=vid, label="video (YUV)"),
                       Patch(color=disp, label="display")],
              loc="lower right", frameon=False, fontsize=9)
    ax.set_title("blanking and packet overhead excluded; PHY lines are v2.x per-link maxima",
                 fontsize=8.5, color=s.MUTED, loc="left", pad=6)
    s.save(fig, "media_data_rates")


# ---------------------------------------------------------------- 3. 디스플레이 합성
def display_composition():
    fig, ax = plt.subplots(figsize=(11, 5.4))
    s.bare(ax)
    ax.set_xlim(-0.2, 15.3)
    ax.set_ylim(-1.2, 6.4)

    LAY, GPU, DPU, LINK, PANEL = s.SYNC, s.UL, s.DL, s.CTRL, s.INK2

    region(ax, 0.0, 0.0, 2.6, 6.0, "DRAM buffers")
    layers = [("Status bar", 4.6), ("Nav bar", 3.6), ("Wallpaper", 2.6), ("App UI", 1.6), ("Video (YUV)", 0.6)]
    for lab, ly in layers:
        box(ax, 0.2, ly, 2.2, 0.75, LAY, lab, fs=8.5)

    # GPU 합성 경로
    box(ax, 3.4, 3.7, 1.8, 1.4, GPU, "GPU\n(client\ncomposition)", fs=8.5, bold=True)
    for _, ly in layers[:3]:
        arrow(ax, 2.4, ly + 0.375, 3.4, 4.4, lw=1.1)
    box(ax, 5.9, 3.95, 1.6, 0.9, s.EMPTY, "client target\nbuffer (DRAM)", fs=8, ec=GPU, lw=1.5)
    arrow(ax, 5.2, 4.4, 5.9, 4.4)
    ax.text(4.3, 5.35, "extra DRAM write + read,\nGPU must wake", fontsize=8, color=s.INK2, ha="center")

    # DPU
    region(ax, 8.0, 0.0, 4.15, 6.0, "DPU", fc="#ffffff", ec=DPU)
    planes = [("plane 0", 4.0), ("plane 1", 2.6), ("plane 2", 1.2)]
    for lab, py in planes:
        box(ax, 8.2, py, 1.25, 0.75, DPU, lab, fs=8.5)
    arrow(ax, 7.5, 4.4, 8.2, 4.375)
    arrow(ax, 2.4, 1.975, 8.2, 2.975, lw=1.1)
    arrow(ax, 2.4, 0.975, 8.2, 1.575, lw=1.1)
    ax.text(5.3, 2.1, "direct scan-out (overlay)", fontsize=8, color=s.INK2, ha="center", rotation=8)
    box(ax, 9.75, 1.2, 1.0, 3.55, DPU, "blend\n(z-order\n+ alpha)", fs=8.2)
    for _, py in planes:
        arrow(ax, 9.45, py + 0.375, 9.75, py + 0.375, lw=1.1)
    box(ax, 11.0, 3.15, 1.0, 1.6, DPU, "color ·\nHDR\ntone\nmap", fs=8)
    box(ax, 11.0, 1.2, 1.0, 1.6, s.SPECIAL, "DSC\nenc.", fs=8.5, bold=True)
    arrow(ax, 10.75, 3.95, 11.0, 3.95, lw=1.1)
    arrow(ax, 11.5, 3.15, 11.5, 2.8, lw=1.1)

    # 링크·패널
    box(ax, 12.6, 1.4, 1.0, 1.2, LINK, "DSI\nD-/C-PHY", fs=8)
    arrow(ax, 12.0, 2.0, 12.6, 2.0)
    box(ax, 13.9, 0.9, 1.25, 2.2, PANEL, "Panel\nDDIC\n(DSC dec.)", fs=8)
    arrow(ax, 13.6, 2.0, 13.9, 2.0)
    ax.text(13.1, 0.95, "~1/3 link\nbits", fontsize=8, color=s.INK2, ha="center", va="top")

    legend(ax, [(LAY, "layer buffers"), (GPU, "GPU path"), (DPU, "DPU (HWC) path"),
                (s.SPECIAL, "compression"), (LINK, "link")], 0.0, -1.0, 2.75)
    ax.text(0.0, 6.2, "example split: HWC assigns 3 planes, GPU pre-merges the rest (conceptual)",
            fontsize=8.5, color=s.MUTED)
    s.save(fig, "media_display_composition")


# ---------------------------------------------------------------- 4. 연결 블록 배치
def soc_map():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    s.bare(ax)
    ax.set_xlim(-0.2, 14.4)
    ax.set_ylim(-1.3, 8.3)

    SOC_C, CTRL_C, EXT, PMC, RF = s.DL, s.CTRL, s.SYNC, s.SPECIAL, s.UL

    ax.add_patch(FancyBboxPatch((0, 0), 5.6, 7.6, boxstyle="round,pad=0,rounding_size=0.15",
                                facecolor=s.EMPTY, edgecolor=s.INK2, linewidth=1.6))
    ax.text(0.2, 7.35, "SoC die", fontsize=10, color=s.INK2, va="center", fontweight="bold")
    box(ax, 0.25, 0.3, 1.25, 6.7, SOC_C, "AP\nCPU\n(OS)", fs=9.5, bold=True)
    box(ax, 1.7, 0.3, 0.45, 6.7, s.INK2, "", round_=False)
    ax.text(1.925, 3.65, "NoC / shared DRAM", rotation=90, fontsize=8.5, color="#ffffff",
            ha="center", va="center")

    cx, cw, ch = 2.4, 3.0, 0.75
    ctrls = {  # 이름: (y, 색)
        "modem": (6.0, SOC_C, "Modem baseband\n(DSP + protocol CPU)"),
        "pcie": (4.85, CTRL_C, "PCIe root complex"),
        "qup": (3.55, CTRL_C, "Serial engines\n(QUP / USI: I2C·SPI·UART)"),
        "usb": (2.4, CTRL_C, "USB ctrl + combo PHY"),
        "ufs": (1.4, CTRL_C, "UFS host (M-PHY)"),
        "spmi": (0.4, CTRL_C, "SPMI master"),
    }
    for k, (cy, c, lab) in ctrls.items():
        hh = 1.0 if k in ("modem", "qup") else ch
        box(ax, cx, cy, cw, hh, c, lab, fs=8.3)

    ex, ew, eh = 8.2, 2.3, 0.7
    exts = {
        "trx": (7.1, RF, "RF transceiver"),
        "wifi": (5.15, EXT, "Wi-Fi / BT combo"),
        "uwb": (4.05, EXT, "UWB"),
        "gnss": (3.15, EXT, "GNSS receiver"),
        "usbc": (2.25, s.INK2, "USB-C port"),
        "ufsd": (1.3, s.INK2, "UFS storage"),
        "pmic": (0.35, PMC, "PMIC"),
    }
    for k, (ey, c, lab) in exts.items():
        box(ax, ex, ey, ew, eh, c, lab, fs=8.6)
    box(ax, 11.4, 5.95, 2.6, eh, RF, "RF front-end\n(PA · LNA · switch)", fs=8)
    box(ax, 11.4, 7.1, 2.6, eh, s.EMPTY, "antennas", fs=8.5, ec=s.GRID)
    arrow(ax, 10.5, 7.45, 11.4, 6.5, both=True, lw=1.1)
    ax.text(10.95, 7.1, "RF", fontsize=7.5, color=s.INK2, ha="center")
    arrow(ax, 12.7, 6.65, 12.7, 7.1, both=True, lw=1.1)

    xe = cx + cw  # 5.4
    def link(y0, y1, lab, lx=None, ls="-", both=True, x1=ex):
        arrow(ax, xe, y0, x1, y1, ls=ls, both=both, lw=1.2)
        lx = lx or (xe + x1) / 2
        ly = y0 + (y1 - y0) * (lx - xe) / (x1 - xe)
        ax.text(lx, ly, lab, fontsize=8, color=s.INK, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="#ffffff", ec="none"))

    link(6.75, 7.45, "digital IQ", lx=6.9)
    # RFFE 제어선 (모뎀 → 프런트엔드), 점선
    arrow(ax, xe, 6.3, 11.4, 6.3, ls="--", lw=1.2)
    ax.text(9.35, 6.42, "MIPI RFFE (control)", fontsize=8, color=s.INK, ha="center", va="bottom")
    link(5.22, 5.5, "PCIe (Wi-Fi)", lx=6.9)
    link(4.35, 5.2, "UART (BT)", lx=6.5)
    link(4.05, 4.4, "SPI", lx=6.9)
    link(3.75, 3.5, "UART / I2C", lx=6.9)
    link(2.775, 2.6, "USB 3.x / eUSB2", lx=6.8)
    link(1.775, 1.65, "UFS", lx=6.8)
    link(0.775, 0.7, "SPMI", lx=6.8)

    ax.text(10.7, 3.5, "GNSS engine is often\ninside the SoC instead", fontsize=7.5, color=s.MUTED, va="center")
    ax.text(10.7, 4.4, "may share a combo\nchip with Wi-Fi", fontsize=7.5, color=s.MUTED, va="center")

    legend(ax, [(SOC_C, "compute / baseband"), (CTRL_C, "I/O controller"), (RF, "cellular RF"),
                (EXT, "wireless chips"), (PMC, "power")], 0.0, -1.1, 2.75)
    ax.text(0.0, 8.05, "typical arrangement, not a specific chip (conceptual)", fontsize=8.5, color=s.MUTED)
    s.save(fig, "conn_soc_map")


# ---------------------------------------------------------------- 5. 링크 대역폭
def link_bandwidth():
    PC, US, SD, UA = s.DL, s.UL, s.SYNC, s.CTRL
    rows = []
    for g in (2, 3, 4, 5):
        for l in (1, 2):
            rows.append((f"PCIe Gen{g} x{l}", n.pcie_gbs(g, l) * 1e3, PC))
    rows += [
        ("USB 2.0 High-Speed (raw)", 480 / 8, US),
        ("USB 3.2 Gen 1", n.usb_gbs("USB 3.2 Gen 1") * 1e3, US),
        ("USB 3.2 Gen 2", n.usb_gbs("USB 3.2 Gen 2") * 1e3, US),
        ("SDIO 3.0 SDR104 4-bit", n.sdio_mbs(208), SD),
        ("UART 3 Mbaud 8N1", n.uart_kbs(3e6) / 1e3, UA),
    ]
    rows.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    ys = list(range(len(rows)))
    ax.barh(ys, [r[1] for r in rows], color=[r[2] for r in rows], height=0.62)

    def fmt(v):
        return f"{v / 1e3:.2f} GB/s" if v >= 1e3 else f"{v:.0f} MB/s" if v >= 10 else f"{v:.1f} MB/s"
    for yy, (lab, v, _) in zip(ys, rows):
        ax.text(v * 1.12, yy, fmt(v), va="center", fontsize=8.8, color=s.INK)
    ax.set_yticks(ys, [r[0] for r in rows])
    ax.set_xscale("log")
    ax.set_xlim(0.1, 3e4)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xticks([0.1, 1, 10, 100, 1e3, 1e4], ["0.1 MB/s", "1 MB/s", "10 MB/s", "100 MB/s", "1 GB/s", "10 GB/s"])
    ax.set_xlabel("one-direction theoretical bandwidth after line coding (log)")
    ax.grid(True, axis="x", which="major", color=s.GRID, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=PC, label="PCIe"), Patch(color=US, label="USB"),
                       Patch(color=SD, label="SDIO"), Patch(color=UA, label="UART")],
              loc="lower right", frameon=False, fontsize=9)
    s.save(fig, "conn_link_bandwidth")


if __name__ == "__main__":
    s.setup()
    isp_pipeline()
    data_rates()
    display_composition()
    soc_map()
    link_bandwidth()
