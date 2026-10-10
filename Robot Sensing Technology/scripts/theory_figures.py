"""Compact vector diagrams for the signal-analysis review text.

Plot coordinates are dimensionless drawing coordinates. Labels give the
actual symbolic time, frequency, amplitude, and Fourier-series coefficients.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'img'
BLUE, RED, GRAY = '#2d6fb1', '#b34145', '#757575'
plt.rcParams.update({
    'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
    'font.size': 10, 'axes.titlesize': 10, 'axes.labelsize': 10,
    'lines.linewidth': 1.6, 'pdf.fonttype': 42,
})


def axes(ax, xlim, ylim, xlabel, ylabel):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(length=3, width=.6, pad=4, labelsize=9)
    ax.annotate('', (xlim[1], 0), (xlim[0], 0),
                arrowprops={'arrowstyle': '->', 'color': '#383838', 'lw': .8}, zorder=0)
    ax.annotate('', (0, ylim[1]), (0, ylim[0]),
                arrowprops={'arrowstyle': '->', 'color': '#383838', 'lw': .8}, zorder=0)
    ax.text(1.01, (0-ylim[0])/(ylim[1]-ylim[0])-.035, xlabel,
            transform=ax.transAxes, ha='left', va='top')
    ax.text((0-xlim[0])/(xlim[1]-xlim[0])+.02, 1.0, ylabel,
            transform=ax.transAxes, ha='left', va='bottom')


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=.10)
    plt.close(fig)


def square_wave():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 1.65))
    fig.subplots_adjust(left=.065, right=.955, top=.80, bottom=.22, wspace=.45)
    a = aa[0]
    axes(a, (-1.17, 1.2), (-1.35, 1.45), '$t$', '$x(t)$')
    # q=t/T0; vertical lines denote the periodic jumps, not finite slopes.
    ts = [-1.12, -1, -.5, 0, .5, 1, 1.12]
    vals = [-1, 1, -1, 1, -1, 1]
    for left, right, value in zip(ts[:-1], ts[1:], vals):
        a.plot([left, right], [value, value], color=BLUE)
    for k in [-1, -.5, 0, .5, 1]:
        a.plot([k, k], [-1, 1], color=BLUE, lw=.7)
    a.set_xticks([-.5, 0, .5], ['$-T_0/2$', '0', '$T_0/2$'])
    a.set_yticks([1], ['$A$'])
    a.annotate('$-A$', (0, -1), xytext=(-8, -12),
               textcoords='offset points', ha='right', fontsize=9)
    a.set_title('(a) $x(t)$', pad=19)
    a = aa[1]
    axes(a, (-7.7, 7.8), (-.12, 1.32), '$f$', '$|C_n|$')
    for n in [-7, -5, -3, -1, 1, 3, 5, 7]:
        v=1/abs(n)
        a.plot([n, n], [0, v], color=BLUE, lw=1)
        a.plot(n, v, 'o', color=BLUE, ms=3)
    a.set_xticks([-5, -3, -1, 0, 1, 3, 5],
                 ['$-5f_0$', '$-3f_0$', '$-f_0$', '0', '$f_0$', '$3f_0$', '$5f_0$'])
    a.set_yticks([])
    a.annotate(r'$2A/\pi$', (1, 1), xytext=(8, 4),
               textcoords='offset points', fontsize=9)
    a.set_title(r'(b) $|C_n|=2A/(\pi|n|)$, $n$ odd', pad=19)
    save(fig, 'review-square-wave.pdf')


def sine_strength():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 1.7))
    fig.subplots_adjust(left=.075, right=.945, top=.76, bottom=.21, wspace=.45)
    th = np.linspace(0, 2*np.pi, 1000)
    a=aa[0]
    axes(a, (-.13, 2*np.pi+.32), (-1.28, 1.32), r'$\theta=\omega t$', '$x(t)$')
    a.plot(th, np.sin(th), color=BLUE)
    a.set_xticks([0, np.pi, 2*np.pi], ['0', r'$\pi$', r'$2\pi$'])
    a.set_yticks([-1, 1], ['$-x_0$', '$x_0$'])
    a.set_title(r'(a) $x_0>0$, $\mu_x=0$', pad=19)
    a=aa[1]
    axes(a, (-.13, 2*np.pi+.32), (-.17, 1.43), r'$\theta=\omega t$', '$|x(t)|$')
    a.fill_between(th, 0, abs(np.sin(th)), color=BLUE, alpha=.09)
    a.plot(th, abs(np.sin(th)), color=BLUE)
    a.hlines(2/np.pi, 0, 2*np.pi, color=RED, ls='--', lw=1)
    a.hlines(1/np.sqrt(2), 0, 2*np.pi, color=GRAY, ls=':', lw=1)
    a.set_xticks([0, np.pi, 2*np.pi], ['0', r'$\pi$', r'$2\pi$'])
    a.set_yticks([1], ['$x_0$'])
    a.text(.5, 1.29, r'$\mu_{|x|}=2x_0/\pi$  (--) ', color=RED, transform=a.transAxes, ha='center', fontsize=9)
    a.text(.5, 1.12, r'$x_{\mathrm{rms}}=x_0/\sqrt{2}$  ($\cdots$)', color=GRAY, transform=a.transAxes, ha='center', fontsize=9)
    save(fig, 'review-sine-strength.pdf')


def rectangular_window():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 1.75))
    fig.subplots_adjust(left=.06, right=.945, top=.79, bottom=.26, wspace=.40)
    a=aa[0]
    axes(a, (-.95, .99), (-.23, 1.42), '$t$', '$w_L(t)$')
    a.plot([-.85, -.5, -.5, .5, .5, .88], [0, 0, 1, 1, 0, 0], color=BLUE)
    a.set_xticks([-.5, 0, .5], ['$-L/2$', '0', '$L/2$'])
    a.set_yticks([1], ['1'])
    a.annotate('', (.5, 1.2), (-.5, 1.2), arrowprops={'arrowstyle':'<->','lw':.7,'color':GRAY})
    a.text(-.22, 1.23, '$L$', ha='center', fontsize=9)
    a.set_title('(a) $w_L(t)$', pad=20)
    a=aa[1]
    axes(a, (-3.7, 3.8), (-.5, 1.42), '$f$', '$W_L(f)$')
    q=np.linspace(-3.6, 3.6, 1800)
    a.plot(q, np.sinc(q), color=BLUE)
    a.set_xticks([-2, -1, 0, 1, 2], ['$-2/L$', '$-1/L$', '0', '$1/L$', '$2/L$'])
    a.set_yticks([1], ['$L$'])
    a.plot([-1, 1], [0, 0], 'o', ms=3, color=RED)
    a.annotate('', (1, -.70), (-1, -.70), annotation_clip=False,
               arrowprops={'arrowstyle':'<->','lw':.7,'color':GRAY})
    a.text(0, -.77, '$2/L$', ha='center', va='top', fontsize=9)
    a.set_title(r'(b) $W_L(f)=L\,\mathrm{Sa}(\pi Lf)$', pad=20)
    save(fig, 'review-rectangular-window.pdf')


def generate_all():
    square_wave()
    sine_strength()
    rectangular_window()


if __name__ == '__main__':
    generate_all()
