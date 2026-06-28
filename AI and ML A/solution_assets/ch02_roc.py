from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


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

plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.size": 10,
    }
)

fig, ax = plt.subplots(figsize=(4.2, 4.0))
ax.plot(xs, ys, marker="o", color="#1f77b4", linewidth=2)
ax.plot([0, 1], [0, 1], "--", color="0.65", linewidth=1)
for (x, y), label in zip(roc_points[1:], [f"score={s:g}" for s in scores]):
    ax.annotate(label, (x, y), xytext=(5, -12), textcoords="offset points", fontsize=8)

ax.set_xlim(-0.03, 1.03)
ax.set_ylim(-0.03, 1.03)
ax.set_xticks(np.linspace(0, 1, 5))
ax.set_yticks(np.linspace(0, 1, 5))
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.set_title(f"ROC curve, AUC = {auc:.5f}")
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(Path(__file__).with_suffix(".pdf"))
