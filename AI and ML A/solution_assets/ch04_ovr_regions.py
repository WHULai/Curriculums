from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "red_strong": "#B64342",
    "green_3": "#8BCF8B",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "red_1": "#F6CFCB",
    "green_1": "#DDF3DE",
}

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})


def scores(x1, x2):
    return np.stack(
        [
            -x1 - x2 + 5,
            -x1 + 3,
            -x1 + x2,
        ],
        axis=0,
    )


x = np.linspace(-1.0, 7.0, 500)
y = np.linspace(-2.0, 7.0, 500)
xx, yy = np.meshgrid(x, y)
g = scores(xx, yy)
positive = g > 0
region = np.zeros_like(xx, dtype=int)
for idx in range(3):
    region[(positive[idx]) & (positive.sum(axis=0) == 1)] = idx + 1
region[positive.sum(axis=0) != 1] = 0

fig, ax = plt.subplots(figsize=(3.6, 3.2))
cmap = ListedColormap(["#f5f5f5", PALETTE["red_1"], PALETTE["green_1"], "#dbeafe"])
ax.contourf(xx, yy, region, levels=[-0.5, 0.5, 1.5, 2.5, 3.5], cmap=cmap, alpha=0.85)

line_x = np.linspace(-1.0, 7.0, 300)
ax.plot(line_x, 5 - line_x, color=PALETTE["red_strong"], linewidth=1.5,
        label=r"$g_1=0$")
ax.axvline(3, color=PALETTE["green_3"], linewidth=1.5, label=r"$g_2=0$")
ax.plot(line_x, line_x, color=PALETTE["blue_main"], linewidth=1.5,
        label=r"$g_3=0$")

ax.scatter([1, 4], [3, 5], color=PALETTE["neutral_black"], s=16, zorder=5)
ax.annotate("(1, 3)", (1, 3), xytext=(5, 5), textcoords="offset points",
            fontsize=6, color=PALETTE["neutral_dark"])
ax.annotate("(4, 5)", (4, 5), xytext=(5, 5), textcoords="offset points",
            fontsize=6, color=PALETTE["neutral_dark"])

ax.text(4.4, -1.1, r"$\omega_1$", color=PALETTE["red_strong"], fontsize=8,
        fontweight="bold")
ax.text(2.63, 2.86, r"$\omega_2$", color=PALETTE["green_3"], fontsize=8,
        fontweight="bold")
ax.text(4.8, 5.8, r"$\omega_3$", color=PALETTE["blue_main"], fontsize=8,
        fontweight="bold")
ax.text(-0.85, 6.25, "ambiguous / reject", color=PALETTE["neutral_mid"],
        fontsize=6, style="italic")

ax.set_xlim(-1.0, 7.0)
ax.set_ylim(-2.0, 7.0)
ax.set_xlabel(r"$x_1$", fontsize=7)
ax.set_ylabel(r"$x_2$", fontsize=7)
ax.set_aspect("equal", adjustable="box")
ax.grid(True, alpha=0.15, linewidth=0.5)
ax.legend(loc="lower left", fontsize=5.5, frameon=True, framealpha=0.9,
          edgecolor=PALETTE["neutral_mid"], fancybox=False)

fig.tight_layout(pad=1.5)
fig.savefig(Path(__file__).with_suffix(".pdf"), bbox_inches="tight")
plt.close(fig)
