from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "red_strong": "#B64342",
    "neutral_light": "#CFCECE",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "green_3": "#8BCF8B",
    "teal": "#42949E",
    "gold": "#FFD700",
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

x = np.arange(1, 11, dtype=float)
y = np.array([4.50, 4.75, 4.91, 5.34, 5.80, 7.05, 7.90, 8.23, 8.70, 9.50])

leaf_intervals = [
    (1.0, 1.5, 4.50),
    (1.5, 3.5, 4.83),
    (3.5, 4.5, 5.34),
    (4.5, 5.5, 5.80),
    (5.5, 6.5, 7.05),
    (6.5, 8.5, 8.065),
    (8.5, 9.5, 8.70),
    (9.5, 10.0, 9.50),
]

nodes = {
    "root": (0.50, 0.94, r"$x\leq 5.5$"),
    "l": (0.25, 0.72, r"$x\leq 3.5$"),
    "r": (0.75, 0.72, r"$x\leq 8.5$"),
    "ll": (0.125, 0.50, r"$x\leq 1.5$"),
    "lr": (0.375, 0.50, r"$x\leq 4.5$"),
    "rl": (0.625, 0.50, r"$x\leq 6.5$"),
    "rr": (0.875, 0.50, r"$x\leq 9.5$"),
    "a": (0.055, 0.25, r"$4.50$"),
    "b": (0.195, 0.25, r"$4.83$"),
    "c": (0.305, 0.25, r"$5.34$"),
    "d": (0.445, 0.25, r"$5.80$"),
    "e": (0.555, 0.25, r"$7.05$"),
    "f": (0.695, 0.25, r"$8.065$"),
    "g": (0.805, 0.25, r"$8.70$"),
    "h": (0.945, 0.25, r"$9.50$"),
}
edges = [
    ("root", "l", "yes"),
    ("root", "r", "no"),
    ("l", "ll", "yes"),
    ("l", "lr", "no"),
    ("r", "rl", "yes"),
    ("r", "rr", "no"),
    ("ll", "a", "yes"),
    ("ll", "b", "no"),
    ("lr", "c", "yes"),
    ("lr", "d", "no"),
    ("rl", "e", "yes"),
    ("rl", "f", "no"),
    ("rr", "g", "yes"),
    ("rr", "h", "no"),
]

fig, (ax_fit, ax_tree) = plt.subplots(
    2, 1, figsize=(3.5, 6.0), gridspec_kw={"height_ratios": [1.0, 1.2]}
)

ax_fit.scatter(x, y, color=PALETTE["blue_main"], s=20, zorder=3, label="samples",
               edgecolors="white", linewidths=0.4)
for left, right, value in leaf_intervals:
    ax_fit.hlines(value, left, right, colors=PALETTE["red_strong"], linewidth=1.8)
for threshold in [1.5, 3.5, 4.5, 5.5, 6.5, 8.5, 9.5]:
    ax_fit.axvline(threshold, color=PALETTE["neutral_light"], linestyle="--",
                   linewidth=0.6)
ax_fit.set_xlabel(r"$x$", fontsize=7)
ax_fit.set_ylabel(r"$y$", fontsize=7)
ax_fit.set_xlim(0.7, 10.3)
ax_fit.set_ylim(4.2, 9.8)
ax_fit.set_title("Piecewise constant prediction", fontsize=8, fontweight="bold",
                  color=PALETTE["neutral_black"])
ax_fit.legend(fontsize=6)
ax_fit.grid(True, alpha=0.15, linewidth=0.5)

ax_tree.axis("off")
for parent, child, label in edges:
    x0, y0, _ = nodes[parent]
    x1, y1, _ = nodes[child]
    ax_tree.plot([x0, x1], [y0 - 0.03, y1 + 0.03], color=PALETTE["neutral_mid"],
                 linewidth=0.8)
    ax_tree.text((x0 + x1) / 2, (y0 + y1) / 2, label, fontsize=5.5,
                 color=PALETTE["neutral_mid"], ha="center", va="center")

for name, (nx, ny, text) in nodes.items():
    is_leaf = name in list("abcdefgh")
    bbox = dict(
        boxstyle="round,pad=0.2",
        facecolor="#FFF7ED" if is_leaf else "#E8F0FE",
        edgecolor=PALETTE["neutral_dark"],
        linewidth=0.6,
    )
    ax_tree.text(nx, ny, text, ha="center", va="center", fontsize=6, bbox=bbox)
ax_tree.set_title("Regression tree (max depth = 3)", fontsize=8,
                   fontweight="bold", color=PALETTE["neutral_black"])

fig.tight_layout(pad=1.5)
fig.savefig(Path(__file__).with_suffix(".pdf"), bbox_inches="tight")
plt.close(fig)
