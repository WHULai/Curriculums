"""Generate supplementary vector figures for the homework-centred review.

The windowed-cosine plot evaluates the exact analytical Fourier transform.
Its chosen dimensionless ratio f0*T=5/2 illustrates superposition only; it is
not an additional premise of the homework problem or its general solution.
Run with: python scripts/homework_figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[1] / "img"
BLUE = "#2d6fb1"
RED = "#c74440"


def windowed_cosine_total():
    """Plot Y/T and |Y|/T against frequency f, using q=f*T internally."""
    plt.rcParams.update({
        "font.family": "DejaVu Serif",
        "mathtext.fontset": "dejavuserif",
        "font.size": 9,
        "axes.titlesize": 9,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "pdf.fonttype": 42,
    })

    ratio = 2.5  # Illustration only: f0*T=5/2, not a supplied problem datum.
    q = np.linspace(-6.25, 6.25, 10001)
    # numpy.sinc(z)=sin(pi*z)/(pi*z), including the continuous value at zero.
    # Thus T*Sa[2*pi*T*(f +/- f0)] / T = sinc[2*(q +/- ratio)].
    positive = np.sinc(2 * (q - ratio))
    negative = np.sinc(2 * (q + ratio))
    total = positive + negative

    # Sanity checks independent of the graph's appearance.
    assert np.allclose(total, total[::-1], atol=1e-12)
    assert np.isclose(2 * np.sinc(2 * ratio), 0, atol=1e-12)
    assert np.isclose(1 + np.sinc(4 * ratio), 1, atol=1e-12)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.85), sharex=True)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.83, bottom=0.25,
                        wspace=0.24)
    fig.suptitle(r"Illustration only: $f_0T=5/2$", y=0.98, fontsize=10)

    ticks = [-2 * ratio, -ratio, 0, ratio, 2 * ratio]
    labels = [r"$-2f_0$", r"$-f_0$", r"$0$", r"$f_0$", r"$2f_0$"]
    for ax in axes:
        ax.set_xlim(q[0], q[-1])
        ax.set_xticks(ticks, labels)
        ax.set_yticks([0, 0.5, 1], [r"$0$", r"$1/2$", r"$1$"])
        ax.spines[["top", "right"]].set_visible(False)
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_color("#777777")
            ax.spines[spine].set_linewidth(0.7)
        ax.tick_params(width=0.7, length=3, color="#777777")
        ax.axhline(0, color="#999999", lw=0.65, zorder=0)
        ax.axvline(0, color="#dddddd", lw=0.55, zorder=0)
        ax.set_xlabel(r"Frequency $f$", labelpad=3)

    ax = axes[0]
    ax.plot(q, positive, color=BLUE, lw=1.0, ls="--", alpha=0.45,
            label=r"$Y_+/T$")
    ax.plot(q, negative, color=RED, lw=1.0, ls="--", alpha=0.45,
            label=r"$Y_-/T$")
    ax.plot(q, total, color=BLUE, lw=1.55, label=r"$Y/T$ (sum)")
    ax.set_ylim(-0.29, 1.18)
    ax.set_ylabel(r"$Y(f)/T$", labelpad=3)
    ax.set_title("(a) Signed spectrum: add before taking magnitude", pad=7,
                 fontsize=8.2)
    ax.legend(loc="upper center", frameon=False, handlelength=2.1,
              borderaxespad=0.15, labelspacing=0.22)

    ax = axes[1]
    ax.plot(q, np.abs(total), color=BLUE, lw=1.55)
    ax.set_ylim(-0.035, 1.18)
    ax.set_ylabel(r"$|Y(f)|/T$", labelpad=3)
    ax.set_title("(b) Magnitude of the total spectrum", pad=7, fontsize=8.2)

    fig.text(0.5, 0.025,
             r"The ratio $f_0T$ is fixed for this illustration only; "
             "the homework solution retains general parameters.",
             ha="center", va="bottom", fontsize=8)
    OUT.mkdir(exist_ok=True)
    destination = OUT / "homework-windowed-total.pdf"
    fig.savefig(destination, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(destination)


if __name__ == "__main__":
    windowed_cosine_total()
