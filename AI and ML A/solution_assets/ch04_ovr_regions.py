from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def scores(x1, x2):
    return np.stack(
        [
            -x1 - x2 + 5,
            -x1 + 3,
            -x1 + x2,
        ],
        axis=0,
    )


plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.size": 10,
    }
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

fig, ax = plt.subplots(figsize=(5.2, 4.6))
cmap = ListedColormap(["#f0f0f0", "#f8d7da", "#d8f3dc", "#dbeafe"])
ax.contourf(xx, yy, region, levels=[-0.5, 0.5, 1.5, 2.5, 3.5], cmap=cmap, alpha=0.78)

line_x = np.linspace(-1.0, 7.0, 300)
ax.plot(line_x, 5 - line_x, color="#b91c1c", linewidth=2, label=r"$g_1=0$")
ax.axvline(3, color="#15803d", linewidth=2, label=r"$g_2=0$")
ax.plot(line_x, line_x, color="#1d4ed8", linewidth=2, label=r"$g_3=0$")

ax.scatter([1, 4], [3, 5], color="black", zorder=5)
ax.annotate("(1, 3)", (1, 3), xytext=(6, 6), textcoords="offset points")
ax.annotate("(4, 5)", (4, 5), xytext=(6, 6), textcoords="offset points")
ax.text(4.4, -1.1, r"$\omega_1$", color="#7f1d1d", fontsize=13)
ax.text(2.63, 2.86, r"$\omega_2$", color="#14532d", fontsize=13)
ax.text(4.8, 5.8, r"$\omega_3$", color="#1e3a8a", fontsize=13)
ax.text(-0.85, 6.25, "ambiguous / reject", color="0.35", fontsize=9)

ax.set_xlim(-1.0, 7.0)
ax.set_ylim(-2.0, 7.0)
ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")
ax.set_aspect("equal", adjustable="box")
ax.grid(True, alpha=0.2)
ax.legend(loc="lower left", frameon=True)
fig.tight_layout()
fig.savefig(Path(__file__).with_suffix(".pdf"))
