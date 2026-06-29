from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "red_strong": "#B64342",
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

samples = [
    ("s1", 0.80, 1),
    ("s2", 0.70, 1),
    ("s3", 0.56, 0),
    ("s4", 0.50, 1),
    ("s5", 0.50, 0),
    ("s6", 0.30, 1),
    ("s7", 0.20, 0),
    ("s8", 0.15, 0),
]

scores = sorted({score for _, score, _ in samples}, reverse=True)
p = sum(label for _, _, label in samples)
n = len(samples) - p

roc_points = [(0.0, 0.0)]
for threshold in scores:
    tp = sum(label == 1 and score >= threshold for _, score, label in samples)
    fp = sum(label == 0 and score >= threshold for _, score, label in samples)
    roc_points.append((fp / n, tp / p))

xs = np.array([point[0] for point in roc_points])
ys = np.array([point[1] for point in roc_points])
auc = np.trapezoid(ys, xs)

fig, ax = plt.subplots(figsize=(3.2, 3.0))
ax.fill_between(xs, ys, alpha=0.12, color=PALETTE["blue_main"])
ax.plot(xs, ys, marker="o", markersize=4, color=PALETTE["blue_main"],
        linewidth=1.5, markeredgecolor="white", markeredgewidth=0.5,
        label=f"AUC = {auc:.3f}")
ax.plot([0, 1], [0, 1], "--", color=PALETTE["neutral_mid"], linewidth=0.8)

for (x, y), label in zip(roc_points[1:], [f"{s:g}" for s in scores]):
    ax.annotate(label, (x, y), xytext=(4, -8), textcoords="offset points",
                fontsize=5.5, color=PALETTE["neutral_dark"])

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_xticks(np.linspace(0, 1, 5))
ax.set_yticks(np.linspace(0, 1, 5))
ax.set_xlabel("False positive rate", fontsize=7)
ax.set_ylabel("True positive rate", fontsize=7)
ax.set_title(f"ROC curve", fontsize=8, fontweight="bold", color=PALETTE["neutral_black"])
ax.legend(loc="lower right", fontsize=6)
ax.grid(True, alpha=0.15, linewidth=0.5)

fig.tight_layout(pad=1.5)
fig.savefig(Path(__file__).with_suffix(".pdf"), bbox_inches="tight")
plt.close(fig)
