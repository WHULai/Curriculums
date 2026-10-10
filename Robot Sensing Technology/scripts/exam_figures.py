"""Generate symbolic exam sketches for the chapter's Fourier examples.

Coordinates used for drawing are dimensionless geometry, not assigned physical
parameters. Exact tick labels retain the problem's symbols. The damped and
modulated signal outlines are explicitly schematic because their free ratios
or their underlying waveform have not been specified.
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "img"
BLUE, RED, GREEN, PINK = "#2d6fb1", "#c74440", "#388c46", "#f8a3bc"
plt.rcParams.update({
    "font.family": "DejaVu Serif", "mathtext.fontset": "dejavuserif",
    "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
    "legend.fontsize": 8, "lines.linewidth": 1.5, "pdf.fonttype": 42,
})


def _axes(ax, xlim, ylim, ylabel, xlabel=r"$f$", baseline=0.0):
    """Draw unlatticed arrow axes; the caller supplies all symbolic ticks."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    props = dict(arrowstyle="->", color="#333333", lw=0.8,
                 mutation_scale=8, shrinkA=0, shrinkB=0)
    ax.annotate("", (xlim[1], baseline), (xlim[0], baseline),
                arrowprops=props)
    ax.annotate("", (0, ylim[1]), (0, baseline), arrowprops=props)
    ax.text(xlim[1], baseline + 0.035 * (ylim[1] - ylim[0]), xlabel,
            ha="right", va="bottom")
    ax.text(0.05 * (xlim[1] - xlim[0]), ylim[1], ylabel,
            ha="left", va="top")


def _xtick(ax, x, label, y=0.0, offset=-0.045, va="top"):
    height = ax.get_ylim()[1] - ax.get_ylim()[0]
    ax.plot([x, x], [y, y + 0.014 * height], color="#444444", lw=0.7)
    ax.text(x, y + offset * height, label, ha="center", va=va, fontsize=9)


def _ytick(ax, y, label, side=-1, distance=0.025):
    width = ax.get_xlim()[1] - ax.get_xlim()[0]
    ax.plot([-0.01 * width, 0.01 * width], [y, y], color="#444444", lw=0.7)
    ax.text(side * distance * width, y, label,
            ha="right" if side < 0 else "left", va="center", fontsize=9)


def _save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def exponential():
    # q = 2*pi*f/a; this normalized shape is universal for a>0, A != 0.
    q = np.linspace(-4, 4, 1801)
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.4))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.83, bottom=0.13, wspace=0.3)
    ax = axs[0]
    _axes(ax, (-4.3, 4.3), (-0.27, 1.25), r"$|X(f)|$")
    ax.plot(q, 1 / np.sqrt(1 + q*q), color=BLUE)
    for sign in [-1, 1]:
        ax.plot([sign, sign], [0, 1/np.sqrt(2)], color="#aaaaaa", lw=0.6, ls="--")
        ax.plot([sign], [1/np.sqrt(2)], "o", color=RED, ms=3)
        _xtick(ax, sign, r"$-\frac{a}{2\pi}$" if sign < 0 else r"$\frac{a}{2\pi}$")
    _xtick(ax, 0, "$0$", offset=-0.14)
    ax.annotate(r"$\frac{|A|}{a}$", xy=(0, 1), xytext=(1.9, 1.05),
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax.annotate(r"$\frac{|A|}{a\sqrt{2}}$", xy=(-1, 1/np.sqrt(2)),
                xytext=(-2.9, 0.98), ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax.set_title(r"(a) Magnitude, $a>0,\ A\ne0$", pad=8)

    ax = axs[1]
    baseline = -2.1
    _axes(ax, (-4.3, 4.3), (-2.63, 2.0), r"$\phi(f)$", baseline=baseline)
    ax.plot(q, -np.arctan(q), color=BLUE)
    for value, label in [
        (np.pi/2, r"$\alpha+\frac{\pi}{2}$"),
        (np.pi/4, r"$\alpha+\frac{\pi}{4}$"),
        (0, r"$\alpha$"),
        (-np.pi/4, r"$\alpha-\frac{\pi}{4}$"),
        (-np.pi/2, r"$\alpha-\frac{\pi}{2}$"),
    ]:
        # The +pi/4 point lies on the negative-frequency branch; label it
        # on the empty side rather than directly across that branch.
        _ytick(ax, value, label, side=1 if value == np.pi/4 else -1,
               distance=0.032)
    for value in [-np.pi/2, np.pi/2]:
        # Leave space for the symbolic asymptote labels beside the axis.
        ax.plot([-4, -1.7], [value, value], color=RED, lw=0.65, ls="--")
        ax.plot([0.12, 4], [value, value], color=RED, lw=0.65, ls="--")
    for sign in [-1, 1]:
        ax.plot([sign, sign], [baseline, -np.arctan(sign)], color="#aaaaaa", lw=0.6, ls="--")
        _xtick(ax, sign, r"$-\frac{a}{2\pi}$" if sign < 0 else r"$\frac{a}{2\pi}$", y=baseline)
    _xtick(ax, 0, "$0$", y=baseline, offset=-0.11)
    ax.set_title(r"(b) Phase, $\alpha=\arg A$ (mod $2\pi$)", pad=8)
    _save(fig, "hw02-exponential.pdf")


def generalized():
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 4.0))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.91, bottom=0.07,
                        wspace=0.3, hspace=0.43)
    # Both branches continue beyond the viewport near zero: a renderer clip
    # must not suggest a finite value at the principal-value singularity.
    neg, pos = np.linspace(-2.3, -0.025, 1000), np.linspace(0.025, 2.3, 1000)
    ax = axs[0, 0]
    _axes(ax, (-2.5, 2.5), (-0.38, 2.75), r"$|S|,\ |U_c|$")
    for f in [neg, pos]:
        ax.plot(f, 1/(np.pi*np.abs(f)), color=RED)
        ax.plot(f, 1/(2*np.pi*np.abs(f)), color=BLUE)
    ax.text(-2.4, 2.18, r"$|S(f)|=1/(\pi|f|)$", color=RED, va="top")
    ax.text(0.28, 1.72, r"$|U_c(f)|=1/(2\pi|f|)$", color=BLUE, va="top")
    _xtick(ax, 0, "$0$")
    ax.set_title(r"(a) Regular parts, $f\ne0$", pad=5)

    ax = axs[0, 1]
    _axes(ax, (-2.5, 2.5), (-2.3, 2.3), r"$\phi(f)$")
    ax.plot([-2.3, 0], [np.pi/2, np.pi/2], color=BLUE)
    ax.plot([0, 2.3], [-np.pi/2, -np.pi/2], color=BLUE)
    ax.plot([0, 0], [np.pi/2, -np.pi/2], "o", mfc="white", mec=BLUE, ms=4)
    _ytick(ax, np.pi/2, r"$+\pi/2$", side=1)
    _ytick(ax, -np.pi/2, r"$-\pi/2$", side=-1)
    _xtick(ax, 0, "$0$")
    ax.set_title(r"(b) Both phases, $f\ne0$", pad=5)

    ax = axs[1, 0]
    _axes(ax, (-2.5, 2.5), (-0.26, 1.4), r"$\mathrm{Re}\,U(f)$")
    ax.annotate("", (0, 1.0), (0, 0),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2, mutation_scale=11))
    ax.text(0.23, 0.82, r"$\frac{1}{2}\delta(f)$"+"\nweight = 1/2\nheight schematic", va="top")
    _xtick(ax, 0, "$0$")
    ax.set_title("(c) Separate zero-frequency impulse", pad=5)

    ax = axs[1, 1]
    _axes(ax, (-2.5, 2.5), (-2.5, 2.5), r"$\mathrm{Im}\,U(f)$")
    for f in [neg, pos]:
        ax.plot(f, -1/(2*np.pi*f), color=BLUE)
    ax.text(-2.35, -1.95, r"$-\mathrm{PV}\,[1/(2\pi f)]$", va="top")
    _xtick(ax, 0, "$0$", offset=-0.025)
    ax.set_title("(d) Principal-value imaginary part", pad=5)
    _save(fig, "hw03-generalized.pdf")


def windowed():
    # q=2T(f-centre), so sinc(q) is a universal individual window component.
    q = np.linspace(-2.35, 2.35, 1801)
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.4))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.80, bottom=0.10, wspace=0.3)
    for ax, sign in zip(axs, [1, -1]):
        name = r"Y_-(f)" if sign < 0 else r"Y_+(f)"
        centre = r"-f_0" if sign < 0 else r"f_0"
        _axes(ax, (-2.55, 2.55), (-0.80, 1.36), "$"+name+"$")
        ax.plot(q, np.sinc(q), color=BLUE)
        _ytick(ax, 1, "$T$", side=-1)
        _xtick(ax, -1, "$"+centre+r"-\frac{1}{2T}$", offset=-0.145)
        _xtick(ax, 1, "$"+centre+r"+\frac{1}{2T}$", offset=-0.145)
        _xtick(ax, 0, "$"+centre+"$", offset=-0.275)
        title = (r"(b) $Y_-=T\,\mathrm{Sa}[2\pi T(f+f_0)]$" if sign < 0
                 else r"(a) $Y_+=T\,\mathrm{Sa}[2\pi T(f-f_0)]$")
        ax.set_title(title, pad=9)
    fig.text(0.5, 0.017, r"Individual components in local coordinates; $Y(f)=Y_-(f)+Y_+(f)$.",
             ha="center", fontsize=9)
    _save(fig, "hw04-windowed.pdf")


def damped():
    # Dimensionless outlines represent the two regimes, not chosen physical
    # values of a or omega. Free a/omega ratios mean no universal exact shape.
    z = np.linspace(-2.7, 2.7, 2001)
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.5))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.81, bottom=0.20, wspace=0.32)
    ax = axs[0]
    rho = 0.25
    shape = 2*rho / np.sqrt((1+rho*rho-z*z)**2+4*rho*rho*z*z)
    peak = np.sqrt(1-rho*rho)
    centre = 2*rho/(1+rho*rho)
    _axes(ax, (-2.85, 2.85), (-0.31, 1.39), r"$|X(f)|$")
    ax.plot(z, shape, color=BLUE)
    for sign in [-1, 1]:
        ax.plot([sign*peak, sign*peak], [0, 1], color="#aaaaaa", ls="--", lw=0.7)
        ax.plot([sign*peak], [1], "o", color=RED, ms=3)
        _xtick(ax, sign*peak, "$-f_p$" if sign < 0 else "$f_p$")
    _xtick(ax, 0, "$0$", offset=-0.115)
    ax.text(-peak, 1.09, r"$\frac{1}{2a}$", ha="center", va="bottom")
    ax.annotate(r"$\frac{\omega}{a^2+\omega^2}$", xy=(0, centre), xytext=(-2.1, 0.45),
                ha="left", va="center", arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax.set_title(r"(a) $\omega>a$: two peaks", pad=9)

    ax = axs[1]
    rho = 1.4
    shape = (1+rho*rho) / np.sqrt((1+rho*rho-z*z)**2+4*rho*rho*z*z)
    _axes(ax, (-2.85, 2.85), (-0.31, 1.39), r"$|X(f)|$")
    ax.plot(z, shape, color=BLUE)
    ax.plot([0], [1], "o", color=RED, ms=3)
    ax.text(-0.16, 1.13, r"$\frac{\omega}{a^2+\omega^2}$", ha="right", va="center")
    _xtick(ax, 0, "$0$")
    ax.set_title(r"(b) $0<\omega\leq a$: centre peak", pad=9)
    fig.text(0.5, 0.055, r"$f_p=\sqrt{\omega^2-a^2}/(2\pi)$; shape schematic, not to scale.",
             ha="center", fontsize=9)
    _save(fig, "hw05-damped.pdf")


def modulation():
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 4.3))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.89, bottom=0.12,
                        wspace=0.3, hspace=0.53)

    # Smooth bell-shaped outlines only; neither a new exact m(t) nor M(f) is
    # asserted. For the frequency panels, sum the same shifted outline so
    # the half-coefficients and overlap are nevertheless drawn consistently.
    def outline(q):
        value = np.zeros_like(q)
        inside = np.abs(q) < 1
        value[inside] = np.cos(np.pi*q[inside]/2)**2
        return value

    ax = axs[0, 0]
    t = np.linspace(-2.8, 2.8, 2001)
    envelope = np.exp(-np.abs(t)**1.5)
    _axes(ax, (-3.0, 3.0), (-1.22, 1.34), "$s(t)$", "$t$")
    ax.plot(t, envelope*np.cos(2*np.pi*1.8*t), color=BLUE, lw=1.1)
    ax.plot(t, envelope, color=RED, ls="--", lw=0.85)
    ax.plot(t, -envelope, color=RED, ls="--", lw=0.85)
    ax.text(1.05, 0.6, r"$|m(t)|$", color=RED)
    ax.text(1.05, -0.75, r"$-|m(t)|$", color=RED)
    _xtick(ax, 0, "$0$", offset=-0.08)
    ax.set_title(r"(a) $s(t)=m(t)\cos(2\pi f_ct)$", pad=7)

    ax = axs[0, 1]
    q = np.linspace(-1.5, 1.5, 1601)
    _axes(ax, (-1.62, 1.62), (-0.31, 1.36), "$M(f)$")
    ax.plot(q, outline(q), color=BLUE)
    _xtick(ax, -1, "$-f_m$")
    _xtick(ax, 1, "$f_m$")
    _xtick(ax, 0, "$0$", offset=-0.13)
    _ytick(ax, 1, "$M(0)$", side=-1)
    ax.set_title("(b) Given baseband outline", pad=7)

    ax = axs[1, 0]
    q = np.linspace(-3.6, 3.6, 2001)
    c = 2.15  # drawing separation only, with symbolic physical tick labels
    _axes(ax, (-3.7, 3.7), (-0.45, 0.88), "$S(f)$")
    ax.plot(q, 0.5*(outline(q-c)+outline(q+c)), color=BLUE)
    endpoints = [(-c-1, r"$-f_c-f_m$"), (-c+1, r"$-f_c+f_m$"),
                 (c-1, r"$f_c-f_m$"), (c+1, r"$f_c+f_m$")]
    for x, label in endpoints:
        _xtick(ax, x, label, offset=-0.05)
    for x, label in [(-c, "$-f_c$"), (c, "$f_c$")]:
        _xtick(ax, x, label, offset=-0.21)
    _xtick(ax, 0, "$0$", offset=-0.05)
    ax.text(-c, 0.56, r"$\frac{1}{2}M(f+f_c)$", ha="center")
    ax.text(c, 0.56, r"$\frac{1}{2}M(f-f_c)$", ha="center")
    ax.set_title(r"(c) $f_c>f_m$: separated copies", pad=7)

    ax = axs[1, 1]
    q = np.linspace(-1.95, 1.95, 2001)
    c = 0.56  # drawing overlap only; no specified physical ratio
    _axes(ax, (-2.02, 2.02), (-0.45, 0.88), "$S(f)$")
    left, right = 0.5*outline(q+c), 0.5*outline(q-c)
    ax.fill_between([-(1-c), 1-c], 0, 0.72, color=PINK, alpha=0.3, zorder=0)
    ax.plot(q, left, color=GREEN, ls="--", lw=0.8)
    ax.plot(q, right, color=RED, ls="--", lw=0.8)
    ax.plot(q, left+right, color=BLUE)
    _xtick(ax, -(1-c), r"$-(f_m-f_c)$", offset=-0.22)
    _xtick(ax, 1-c, r"$f_m-f_c$", offset=-0.22)
    _xtick(ax, -1-c, r"$-f_c-f_m$", offset=-0.05)
    _xtick(ax, 1+c, r"$f_c+f_m$", offset=-0.05)
    _xtick(ax, 0, "$0$", offset=-0.05)
    ax.text(-c, 0.59, r"$\frac{1}{2}M(f+f_c)$", color=GREEN, ha="right")
    ax.text(c, 0.59, r"$\frac{1}{2}M(f-f_c)$", color=RED, ha="left")
    ax.text(-0.05, 0.78, "overlap", ha="right", fontsize=9)
    ax.set_title(r"(d) $0<f_c<f_m$: overlapping copies", pad=7)
    fig.text(0.5, 0.03, "Shape schematic; bandwidth alone does not determine the time waveform.",
             ha="center", fontsize=9)
    _save(fig, "hw06-modulation.pdf")


def generate_all():
    exponential()
    generalized()
    windowed()
    damped()
    modulation()


if __name__ == "__main__":
    generate_all()
