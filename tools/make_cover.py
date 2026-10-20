"""위키독스 책 표지 (1200 × 1600 PNG)를 만든다.

    python tools/make_cover.py            # → docs/assets/cover.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Arc, FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "cover.png"

KO = next((f for f in ("NanumSquare", "NanumBarunGothic", "NanumGothic", "Noto Sans CJK KR")
           if any(f in x.name for x in font_manager.fontManager.ttflist)), "DejaVu Sans")

BG_TOP = np.array([0x0b, 0x2a, 0x6f]) / 255     # 짙은 파랑
BG_BOT = np.array([0x0a, 0x1a, 0x2e]) / 255     # 남색
TEAL = "#2dd4bf"
WHITE = "#ffffff"
SOFT = "#cfe9e5"
CH = ["#2a78d6", "#1baf7a", "#eda100", "#eb6834", "#4a3aa7", "#e87ba4"]


def main() -> None:
    W, H = 12, 16
    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_axis_off()

    # 배경 그라데이션
    grad = np.linspace(0, 1, 512)[:, None, None]
    img = BG_BOT * grad + BG_TOP * (1 - grad)
    ax.imshow(np.repeat(img, 2, axis=1), extent=[0, W, 0, H], aspect="auto", zorder=0)

    # 칩 심볼 (패키지 + 핀 + 다이 안의 블록)
    cx, cy = W / 2, 8.2
    s = 2.6
    for k in range(7):  # 사방의 핀
        off = -s + 0.45 + k * (2 * s - 0.9) / 6
        for (x0, y0, w, h) in ((cx + off - 0.09, cy + s, 0.18, 0.55), (cx + off - 0.09, cy - s - 0.55, 0.18, 0.55),
                               (cx - s - 0.55, cy + off - 0.09, 0.55, 0.18), (cx + s, cy + off - 0.09, 0.55, 0.18)):
            ax.add_patch(Rectangle((x0, y0), w, h, color=TEAL, alpha=0.9, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - s, cy - s), 2 * s, 2 * s, boxstyle="round,pad=0,rounding_size=0.35",
                                facecolor="#1d4ed8", edgecolor=TEAL, lw=4, zorder=3))
    blocks = [  # (x, y, w, h, 색, 라벨) — 다이 안 블록 배치 (단위: s 기준 상대 좌표)
        (-0.85, 0.15, 0.95, 0.7, CH[0], "CPU"), (0.2, 0.15, 0.65, 0.7, CH[1], "GPU"),
        (-0.85, -0.45, 0.55, 0.5, CH[2], "NPU"), (-0.2, -0.45, 0.5, 0.5, CH[3], "ISP"),
        (0.4, -0.45, 0.45, 0.5, CH[4], "DSP"), (-0.85, -0.85, 1.7, 0.3, CH[5], "SLC"),
    ]
    for bx, by, bw, bh, col, lab in blocks:
        ax.add_patch(Rectangle((cx + bx * s, cy + by * s), bw * s, bh * s, facecolor=col, edgecolor=WHITE,
                               lw=2, zorder=4))
        ax.text(cx + (bx + bw / 2) * s, cy + (by + bh / 2) * s, lab, ha="center", va="center", color=WHITE,
                fontsize=22, fontweight="bold", family="DejaVu Sans", zorder=5)

    # 주변으로 퍼지는 옅은 회로 선
    for r in np.arange(3.9, 9.5, 0.75):
        ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=20, theta2=160, lw=1.2,
                         color=TEAL, alpha=max(0.05, 0.35 - (r - 3.9) * 0.06), zorder=2))

    # 제목
    ax.text(cx, 13.55, "SoC Handbook", ha="center", va="center", color=WHITE, fontsize=72,
            fontweight="bold", family="DejaVu Sans", zorder=4)
    ax.text(cx, 12.45, "Snapdragon  ·  Exynos  ·  Dimensity  ·  Apple", ha="center", va="center", color=TEAL,
            fontsize=32, family="DejaVu Sans", zorder=4)
    ax.text(cx, 3.05, "모바일 SoC 핸드북", ha="center", va="center", color=WHITE, fontsize=62,
            fontweight="bold", family=KO, zorder=4)
    ax.text(cx, 2.05, "기초부터 전문가까지 · 한글 칩셋 구조 해설", ha="center", va="center", color=SOFT,
            fontsize=30, family=KO, zorder=4)

    # 블록 칩
    chips = ["CPU", "GPU", "NPU", "LPDDR", "UFS"]
    cw, gap = 1.6, 0.25
    total = len(chips) * cw + (len(chips) - 1) * gap
    for i, c in enumerate(chips):
        x = cx - total / 2 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, 0.75), cw, 0.62, boxstyle="round,pad=0,rounding_size=0.31",
                                    facecolor="none", edgecolor=TEAL, lw=2.5, zorder=4))
        ax.text(x + cw / 2, 1.06, c, ha="center", va="center", color=WHITE, fontsize=22,
                family="DejaVu Sans", zorder=5)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=100)
    plt.close(fig)
    print(f"→ {OUT.relative_to(ROOT)} ({KO})")


if __name__ == "__main__":
    main()
