"""Vector figures for Chapter 3, using the equations in the notes.

Axes are normalized except the explicitly labelled homework time axis.
Run with Python, NumPy and Matplotlib; existing PDFs suffice for XeLaTeX.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'img'
BLUE, RED, GRAY = '#2d6fb1', '#b34145', '#757575'
COLORS = [RED, BLUE, '#c08835', '#568651']
plt.rcParams.update({
    'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
    'font.size': 9, 'axes.titlesize': 10, 'axes.labelsize': 10,
    'lines.linewidth': 1.5, 'pdf.fonttype': 42,
})


def style(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=.18, linewidth=.5)
    ax.tick_params(labelsize=8)


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=.12)
    plt.close(fig)


def second(r, z):
    h = 1 / (1-r*r+1j*2*z*r)
    return abs(h), np.angle(h)*180/np.pi


def static_characteristics():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.1), constrained_layout=True)
    x = np.linspace(0, 1, 400)
    ref = .05+.9*x
    actual = ref+.12*np.sin(np.pi*x)
    a = aa[0]
    a.plot(x, ref, '--', color=GRAY, label='Reference line')
    a.plot(x, actual, color=BLUE, label='Actual curve')
    a.annotate('', (.5, actual[200]), (.5, .5),
               arrowprops={'arrowstyle': '<->', 'color': RED, 'lw': 1})
    a.text(.53, .55, r'$\Delta_{\max}$', color=RED)
    a.legend(loc='upper left', frameon=False, fontsize=8)
    style(a, 'Normalized input', 'Normalized output')
    a.set_title('(a) Linearity')
    a = aa[1]
    up = ref-.08*np.sin(np.pi*x)
    down = ref+.08*np.sin(np.pi*x)
    a.plot(x, up, color=BLUE, label='Increasing input')
    a.plot(x, down, color=RED, label='Decreasing input')
    a.annotate('', (.5, .58), (.5, .42),
               arrowprops={'arrowstyle': '<->', 'color': GRAY, 'lw': 1})
    a.text(.53, .48, r'$h_{\max}$')
    a.legend(loc='upper left', frameon=False, fontsize=8)
    style(a, 'Normalized input', 'Normalized output')
    a.set_title('(b) Hysteresis')
    save(fig, 'ch3-static-characteristics.pdf')


def first_order():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.0), constrained_layout=True)
    q = np.linspace(0, 4, 600)
    a = aa[0]
    a.plot(q, 1/np.sqrt(1+q*q), color=BLUE)
    a.plot(1, 1/np.sqrt(2), 'o', color=RED, ms=3)
    a.axvline(1, color=GRAY, ls=':', lw=.7)
    a.annotate(r'$A/K=1/\sqrt{2}$', (1, 1/np.sqrt(2)),
               xytext=(1.45, .83), arrowprops={'arrowstyle':'->', 'lw':.6}, fontsize=9)
    style(a, r'$q=\omega\tau$', '$A/K$')
    a.set_ylim(0, 1.12)
    a = aa[1]
    a.plot(q, -np.arctan(q)*180/np.pi, color=BLUE)
    a.axvline(1, color=GRAY, ls=':', lw=.7)
    a.plot(1, -45, 'o', color=RED, ms=3)
    a.annotate(r'$-45^\circ$', (1, -45), xytext=(1.5, -32),
               arrowprops={'arrowstyle':'->', 'lw':.6}, fontsize=9)
    style(a, r'$q=\omega\tau$', r'$\phi$ (deg)')
    a.set_ylim(-90, 5)
    save(fig, 'ch3-first-order-frequency.pdf')

    fig, a = plt.subplots(figsize=(6.2, 1.75), constrained_layout=True)
    v = np.linspace(0, 5, 500)
    a.plot(v, 1-np.exp(-v), color=BLUE)
    a.axhline(1, color=GRAY, ls='--', lw=.8)
    for p, label, textpos in [(1, '0.632', (1.4, .48)),
                               (3, '0.950', (2.4, .78)),
                               (4, '0.982', (3.95, .83))]:
        y=1-np.exp(-p)
        a.plot(p, y, 'o', color=RED, ms=3)
        a.annotate(label, (p, y), xytext=textpos,
                   arrowprops={'arrowstyle':'->', 'lw':.6}, fontsize=8)
    style(a, r'$t/\tau$', '$y/(KX_0)$')
    a.set_ylim(0, 1.1)
    save(fig, 'ch3-first-order-step.pdf')


def second_order():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.2), constrained_layout=True)
    r = np.linspace(0, 2.5, 1300)
    for z, color in zip([.14, .6, .7, .8], COLORS):
        amp, phase = second(r, z)
        aa[0].plot(r, amp, color=color, label=rf'$\zeta={z}$')
        aa[1].plot(r, phase, color=color)
    aa[0].axhline(1, color=GRAY, ls=':', lw=.7)
    aa[0].legend(frameon=False, fontsize=8, loc='upper right')
    aa[0].set_ylim(0, 3.95)
    for a, ylabel in zip(aa, ['$A/K$', r'$\phi$ (deg)']):
        style(a, r'$r=\omega/\omega_n$', ylabel)
        a.axvline(1, color=GRAY, ls=':', lw=.7)
    aa[1].set_yticks([0, -45, -90, -135, -180])
    save(fig, 'ch3-second-order-frequency.pdf')

    fig, a = plt.subplots(figsize=(6.5, 2.0), constrained_layout=True)
    v = np.linspace(0, 16, 1200)
    for z, color in zip([.14, .6, .8, 1], COLORS):
        if z == 1:
            y=1-(1+v)*np.exp(-v)
        else:
            d=np.sqrt(1-z*z)
            y=1-np.exp(-z*v)*(np.cos(d*v)+z/d*np.sin(d*v))
        a.plot(v, y, color=color, label=rf'$\zeta={z}$')
    a.axhline(1, color=GRAY, ls=':', lw=.7)
    a.legend(frameon=False, fontsize=8, ncol=4, loc='lower right')
    style(a, r'$\omega_n t$', '$y/(KX_0)$')
    a.set_ylim(0, 1.8)
    save(fig, 'ch3-second-order-step.pdf')


def distortionless():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.0), constrained_layout=True)
    v=np.linspace(0, 2*np.pi, 600)
    x=lambda t: np.cos(t)+.35*np.cos(3*t+.3)
    gain, delay = .75, .6
    aa[0].plot(v, x(v), color=BLUE, label='$x(t)$')
    aa[0].plot(v, gain*x(v-delay), color=RED, ls='--', label='$A_0x(t-t_0)$')
    aa[0].legend(frameon=False, fontsize=8)
    aa[0].set_xticks([0, np.pi, 2*np.pi], ['0', r'$\pi$', r'$2\pi$'])
    style(aa[0], r'$\omega_0 t$', 'Amplitude')
    q=np.linspace(0, 4, 100)
    aa[1].plot(q, -delay*q, color=BLUE)
    aa[1].plot([1, 3], [-delay, -3*delay], 'o', color=RED, ms=3)
    aa[1].text(.18, .1, r'$\phi=-\omega t_0$', transform=aa[1].transAxes)
    style(aa[1], r'$\omega/\omega_0$', r'$\phi$ (rad)')
    save(fig, 'ch3-distortionless.pdf')


def homework_one():
    fig=plt.figure(figsize=(7.2, 2.9), constrained_layout=True)
    gs=fig.add_gridspec(2, 2, width_ratios=[1, 1.15])
    aa=[fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[:, 1])]
    t=np.linspace(0, .65, 1500)
    x1=.5*np.cos(10*t)
    x2=.2*np.cos(100*t-np.pi/4)
    y1=.5/np.sqrt(1+.05**2)*np.cos(10*t-np.arctan(.05))
    y2=.2/np.sqrt(1+.5**2)*np.cos(100*t-np.pi/4-np.arctan(.5))
    for a, x, y, label in zip(aa, [x1, x2, x1+x2], [y1, y2, y1+y2],
                              [r'$\omega=10$', r'$\omega=100$', 'Sum']):
        a.plot(t, x, color=GRAY, ls='--', lw=1, label='Input')
        a.plot(t, y, color=BLUE, label='Output')
        style(a, '$t$ (s)', label)
    aa[0].set_xlabel('')
    aa[0].tick_params(labelbottom=False)
    aa[2].legend(frameon=False, fontsize=8, loc='upper right')
    save(fig, 'ch3-hw01-response.pdf')


def homework_four():
    fig, aa=plt.subplots(1, 2, figsize=(7.2, 2.2), constrained_layout=True)
    r=np.linspace(0, 1.5, 1000)
    for z, color in zip([.14, .7], [RED, BLUE]):
        amp, phase=second(r, z)
        aa[0].plot(r, amp, color=color, label=rf'$\zeta={z}$')
        aa[1].plot(r, phase, color=color, label=rf'$\zeta={z}$')
        val, ph=second(.5, z)
        aa[0].plot(.5, val, 'o', color=color, ms=4)
        aa[1].plot(.5, ph, 'o', color=color, ms=4)
    aa[0].annotate('1.3107', (.5, second(.5,.14)[0]), xytext=(.08, 1.85),
                   color=RED, arrowprops={'arrowstyle':'->', 'lw':.6, 'color':RED})
    aa[0].annotate('0.9747', (.5, second(.5,.7)[0]), xytext=(.65, .55),
                   color=BLUE, arrowprops={'arrowstyle':'->', 'lw':.6, 'color':BLUE})
    aa[1].annotate(r'$-10.57^\circ$', (.5, second(.5,.14)[1]), xytext=(.63, -19),
                   color=RED, arrowprops={'arrowstyle':'->', 'lw':.6, 'color':RED}, fontsize=8)
    aa[1].annotate(r'$-43.03^\circ$', (.5, second(.5,.7)[1]), xytext=(.1, -88),
                   color=BLUE, arrowprops={'arrowstyle':'->', 'lw':.6, 'color':BLUE}, fontsize=8)
    aa[0].legend(frameon=False, fontsize=8, loc='upper left')
    for a, label in zip(aa, ['$A/K$', r'$\phi$ (deg)']):
        a.axvline(.5, color=GRAY, ls=':', lw=.7)
        style(a, '$r=f/f_n$', label)
    aa[0].set_ylim(0, 4)
    aa[1].set_yticks([0, -45, -90, -135, -180])
    save(fig, 'ch3-hw04-damping.pdf')


if __name__ == '__main__':
    static_characteristics()
    first_order()
    second_order()
    distortionless()
    homework_one()
    homework_four()
