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
    "teal": "#42949E",
    "violet": "#9A4D8E",
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

fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0))
for ax, x, y, title in [
    (axes[0], good_x, good_y, "PCA and LDA find the same direction"),
    (axes[1], bad_x, bad_y, "XOR: no good linear projection"),
]:
    ax.scatter(x[y == 0, 0], x[y == 0, 1], marker="o", facecolors="none",
               edgecolors=PALETTE["blue_main"], s=20, linewidths=0.8,
               label="class 0")
    ax.scatter(x[y == 1, 0], x[y == 1, 1], marker="+", color=PALETTE["red_strong"],
               s=35, linewidths=0.8, label="class 1")
    center = x.mean(axis=0)
    p_dir = pca_direction(x)
    l_dir = lda_direction(x, y)
    for direction, color, name, offset in [
        (p_dir, PALETTE["teal"], "PCA", 0.10),
        (l_dir, PALETTE["violet"], "LDA", -0.10),
    ]:
        if np.linalg.norm(direction) < 1e-12:
            ax.text(center[0] - 1.1, center[1] - 1.45,
                    "LDA direction undefined", color=color, fontsize=6)
            continue
        start = center - 1.5 * direction + offset * np.array([-direction[1], direction[0]])
        end = center + 1.5 * direction + offset * np.array([-direction[1], direction[0]])
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops=dict(arrowstyle="-|>", color=color, linewidth=1.5,
                            mutation_scale=8),
        )
        ax.text(*(end + 0.08), name, color=color, fontsize=6, fontweight="bold")
    ax.axhline(0, color=PALETTE["neutral_light"], linewidth=0.6)
    ax.axvline(0, color=PALETTE["neutral_light"], linewidth=0.6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title, fontsize=7.5, fontweight="bold", color=PALETTE["neutral_black"])
    ax.grid(True, alpha=0.15, linewidth=0.5)

axes[0].legend(loc="lower right", fontsize=5.5, frameon=True, framealpha=0.9,
               edgecolor=PALETTE["neutral_mid"], fancybox=False)
fig.tight_layout(pad=1.5)
fig.savefig(Path(__file__).with_suffix(".pdf"), bbox_inches="tight")
plt.close(fig)
