from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


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

plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.size": 10,
    }
)

fig, (ax_fit, ax_tree) = plt.subplots(
    1, 2, figsize=(10.5, 4.3), gridspec_kw={"width_ratios": [1.05, 1.35]}
)

ax_fit.scatter(x, y, color="#1f77b4", zorder=3, label="samples")
for left, right, value in leaf_intervals:
    ax_fit.hlines(value, left, right, colors="#d62728", linewidth=2.2)
for threshold in [1.5, 3.5, 4.5, 5.5, 6.5, 8.5, 9.5]:
    ax_fit.axvline(threshold, color="0.75", linestyle="--", linewidth=0.8)
ax_fit.set_xlabel(r"$x$")
ax_fit.set_ylabel(r"$y$")
ax_fit.set_xlim(0.7, 10.3)
ax_fit.set_ylim(4.2, 9.8)
ax_fit.set_title("Piecewise constant prediction")
ax_fit.grid(True, alpha=0.2)

ax_tree.axis("off")
for parent, child, label in edges:
    x0, y0, _ = nodes[parent]
    x1, y1, _ = nodes[child]
    ax_tree.plot([x0, x1], [y0 - 0.03, y1 + 0.03], color="0.35", linewidth=1)
    ax_tree.text((x0 + x1) / 2, (y0 + y1) / 2, label, fontsize=8, color="0.35")

for name, (nx, ny, text) in nodes.items():
    is_leaf = name in list("abcdefgh")
    bbox = dict(
        boxstyle="round,pad=0.25",
        facecolor="#fff7ed" if is_leaf else "#e0f2fe",
        edgecolor="#334155",
        linewidth=1,
    )
    ax_tree.text(nx, ny, text, ha="center", va="center", bbox=bbox)
ax_tree.set_title("Least-squares regression tree, max_depth=3")

fig.tight_layout()
fig.savefig(Path(__file__).with_suffix(".pdf"))
