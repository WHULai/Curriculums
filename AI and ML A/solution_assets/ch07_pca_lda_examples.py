from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def unit(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-12 else v


def pca_direction(x):
    centered = x - x.mean(axis=0)
    cov = centered.T @ centered / len(x)
    values, vectors = np.linalg.eigh(cov)
    return unit(vectors[:, np.argmax(values)])


def lda_direction(x, y):
    classes = np.unique(y)
    means = [x[y == c].mean(axis=0) for c in classes]
    sw = np.zeros((2, 2))
    for c, mean in zip(classes, means):
        z = x[y == c] - mean
        sw += z.T @ z
    diff = means[1] - means[0]
    if np.linalg.norm(diff) < 1e-12:
        return np.zeros(2)
    return unit(np.linalg.pinv(sw) @ diff)


rng = np.random.default_rng(7)
good_a = rng.normal(loc=(-2.0, 0.0), scale=(0.45, 0.55), size=(35, 2))
good_b = rng.normal(loc=(2.0, 0.0), scale=(0.45, 0.55), size=(35, 2))
good_x = np.vstack([good_a, good_b])
good_y = np.array([0] * len(good_a) + [1] * len(good_b))

offsets = np.array(
    [
        [-0.16, -0.10],
        [-0.11, 0.12],
        [0.08, -0.14],
        [0.19, 0.08],
    ]
)
bad_a = np.vstack([offsets + (-1, -1), offsets + (1, 1)])
bad_b = np.vstack([offsets + (-1, 1), offsets + (1, -1)])
bad_x = np.vstack([bad_a, bad_b])
bad_y = np.array([0] * len(bad_a) + [1] * len(bad_b))

plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.size": 10,
    }
)

fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.1))
for ax, x, y, title in [
    (axes[0], good_x, good_y, "PCA and LDA find the same useful direction"),
    (axes[1], bad_x, bad_y, "XOR: no good linear projection"),
]:
    ax.scatter(x[y == 0, 0], x[y == 0, 1], marker="o", facecolors="none", edgecolors="#2563eb", label="class 0")
    ax.scatter(x[y == 1, 0], x[y == 1, 1], marker="+", color="#dc2626", s=65, label="class 1")
    center = x.mean(axis=0)
    p_dir = pca_direction(x)
    l_dir = lda_direction(x, y)
    for direction, color, name, offset in [
        (p_dir, "#0f766e", "PCA", 0.10),
        (l_dir, "#9333ea", "LDA", -0.10),
    ]:
        if np.linalg.norm(direction) < 1e-12:
            ax.text(center[0] - 1.1, center[1] - 1.45, "LDA direction undefined", color=color)
            continue
        start = center - 1.5 * direction + offset * np.array([-direction[1], direction[0]])
        end = center + 1.5 * direction + offset * np.array([-direction[1], direction[0]])
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops=dict(arrowstyle="->", color=color, linewidth=2),
        )
        ax.text(*(end + 0.08), name, color=color, fontsize=10)
    ax.axhline(0, color="0.85", linewidth=0.8)
    ax.axvline(0, color="0.85", linewidth=0.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title)
    ax.grid(True, alpha=0.2)

axes[0].legend(loc="lower right", frameon=True)
fig.tight_layout()
fig.savefig(Path(__file__).with_suffix(".pdf"))
