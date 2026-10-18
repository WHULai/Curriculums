"""Vector illustrations for the signal-conditioning chapter.

Line spectra use the explicitly labelled peak-amplitude or complex-line
convention. Symbolic spectra are schematic in the vertical direction.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'img'
BLUE, RED, GRAY = '#2d6fb1', '#b34145', '#757575'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
                     'font.size': 9, 'axes.labelsize': 10, 'axes.titlesize': 10,
                     'lines.linewidth': 1.4, 'pdf.fonttype': 42})


def style(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=.17, linewidth=.5)
    ax.tick_params(labelsize=8)


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=.12)
    plt.close(fig)


def am_waveform():
    fig, aa = plt.subplots(3, 1, figsize=(7.2, 3.65), sharex=True, constrained_layout=True)
    t = np.linspace(0, 2, 5000)
    x = .8*np.cos(2*np.pi*t)
    carrier = np.cos(2*np.pi*18*t)
    for ax, y, lab in zip(aa, [x, x*carrier, (1+x)*carrier],
                          ['$x(t)$', '$x(t)c(t)$', '$[1+x(t)]c(t)$']):
        ax.plot(t, y, color=BLUE, lw=.85)
        style(ax, '', lab)
        ax.axhline(0, color=GRAY, lw=.6)
    aa[1].plot(t, x, color=RED, ls='--', lw=.8)
    aa[1].plot(t, -x, color=RED, ls='--', lw=.8)
    aa[1].text(.015, .88, 'Signed envelope; carrier reverses phase', transform=aa[1].transAxes, fontsize=8)
    aa[2].plot(t, 1+x, color=RED, ls='--', lw=.8)
    aa[2].plot(t, -(1+x), color=RED, ls='--', lw=.8)
    aa[2].set_xlabel('Time / modulation period')
    save(fig, 'ch5-am-waveforms.pdf')


def bridge_spectra():
    fig, aa = plt.subplots(2, 2, figsize=(7.2, 3.7), constrained_layout=True)
    ax = aa[0, 0]
    for v, h, label in [(-100, .55, '$B/2$'), (-10, .9, '$A/2$'),
                         (10, .9, '$A/2$'), (100, .55, '$B/2$')]:
        ax.vlines(v, 0, h, color=BLUE, lw=1.5)
        ax.plot(v, h, 'o', color=BLUE, ms=3)
        if abs(v) == 100:
            ax.text(v, h+.06, label, ha='center', fontsize=8)
    ax.text(0, 1.08, '$A/2$ (each)', ha='center', fontsize=8)
    for v in [-10, 10]:
        ax.annotate('', (v, .91), (0, 1.045),
                    arrowprops={'arrowstyle': '->', 'lw': .5, 'color': GRAY})
    ax.set_xlim(-130, 130)
    ax.set_xticks([-100, -10, 10, 100])
    ax.set_title('(a) Strain')
    ax = aa[0, 1]
    ax.vlines([-10000, 10000], 0, .85, color=RED, lw=1.5)
    for v in [-10000, 10000]:
        ax.text(v, .91, '$E/2$', ha='center', fontsize=8)
    ax.set_xlim(-14000, 14000)
    ax.set_xticks([-10000, 0, 10000])
    ax.set_title('(b) Excitation')
    for ax, sign in zip(aa[1], [-1, 1]):
        vs = np.array([9900, 9990, 10010, 10100])*sign
        labs = [r'$S_gEB/4$', r'$S_gEA/4$', r'$S_gEA/4$', r'$S_gEB/4$']
        for v, h, lab in zip(vs, [.55, .9, .9, .55], labs):
            ax.vlines(v, 0, h, color=BLUE, lw=1.5)
            if abs(v) in [9900, 10100]:
                ax.text(v, h+.07, lab, ha='center', fontsize=7)
        ax.text(sign*10000, 1.08, '$S_gEA/4$ (each)', ha='center', fontsize=7)
        for v in [sign*9990, sign*10010]:
            ax.annotate('', (v, .91), (sign*10000, 1.045),
                        arrowprops={'arrowstyle': '->', 'lw': .5, 'color': GRAY})
        ax.axvline(sign*10000, color=GRAY, ls=':', lw=.7)
        ax.set_xlim((9870, 10130) if sign > 0 else (-10130, -9870))
        ax.set_xticks(sorted(vs))
        ax.tick_params(axis='x', rotation=90, labelsize=7)
        ax.set_title('(d) Output, positive frequencies' if sign > 0 else '(c) Output, negative frequencies')
    for ax in aa.flat:
        ax.set_ylim(0, 1.2)
        ax.set_yticks([])
        style(ax, r'$\omega$ (rad/s)', r'$|C_{\omega}|$')
    save(fig, 'ch5-bridge-spectra.pdf')


def conventional_spectra():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.45), constrained_layout=True)
    for ax, fs, amps, title in [
            (aa[0], [0, .5, 1.5], [100, 30, 20], '(a) Envelope $q(t)=100+m(t)$'),
            (aa[1], [8.5, 9.5, 10, 10.5, 11.5], [10, 15, 100, 15, 10], '(b) AM signal')]:
        ax.vlines(fs, 0, amps, color=BLUE, lw=1.6)
        ax.plot(fs, amps, 'o', color=BLUE, ms=3)
        for f, a in zip(fs, amps):
            ax.text(f, a+4, f'{a}', ha='center', fontsize=8)
        ax.set_ylim(0, 120)
        ax.set_xticks(fs)
        ax.set_title(title)
        style(ax, '$f$ (kHz)', 'Peak amplitude (one-sided)')
    aa[0].set_xlim(-.18, 1.75)
    aa[1].set_xlim(8.2, 11.8)
    save(fig, 'ch5-am-spectra.pdf')


def filters():
    fig, aa = plt.subplots(2, 2, figsize=(7.2, 3.3), constrained_layout=True)
    vals = [([0, 1, 1, 3], [1, 1, 0, 0], 'Low-pass'),
            ([0, 1, 1, 3], [0, 0, 1, 1], 'High-pass'),
            ([0, 1, 1, 2, 2, 3], [0, 0, 1, 1, 0, 0], 'Band-pass'),
            ([0, 1, 1, 2, 2, 3], [1, 1, 0, 0, 1, 1], 'Band-stop')]
    for ax, (x, y, title) in zip(aa.flat, vals):
        ax.plot(x, y, color=BLUE)
        ax.set_ylim(-.08, 1.2)
        ax.set_xticks([0, 1, 2, 3], ['0', '$f_{c1}$' if 'pass' not in title[:4].lower() else '$f_c$', '$f_{c2}$', ''])
        if title in ['Low-pass', 'High-pass']:
            ax.set_xticks([0, 1], ['0', '$f_c$'])
        ax.set_yticks([0, 1])
        ax.set_title(title)
        style(ax, '$f$', '$A/A_0$')
    save(fig, 'ch5-filter-types.pdf')


def rc_curves():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.35), constrained_layout=True)
    q = np.logspace(-2, 2, 800)
    lp = 1/(1+1j*q)
    hp = 1j*q/(1+1j*q)
    for h, name, color in [(lp, 'Low-pass', BLUE), (hp, 'High-pass', RED)]:
        aa[0].semilogx(q, 20*np.log10(abs(h)), color=color, label=name)
        aa[1].semilogx(q, np.angle(h)*180/np.pi, color=color, label=name)
    aa[0].axhline(-3.0103, color=GRAY, ls=':', lw=.8)
    aa[0].set_ylim(-43, 3)
    aa[0].legend(frameon=False, fontsize=8)
    aa[1].set_yticks([-90, -45, 0, 45, 90])
    for ax, label in zip(aa, ['Gain (dB)', 'Phase (deg)']):
        ax.axvline(1, color=GRAY, ls=':', lw=.8)
        style(ax, r'$q=\omega\tau=f/f_c$', label)
    save(fig, 'ch5-rc-frequency.pdf')


def bandwidths():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.35), constrained_layout=True)
    for i, (a, b) in enumerate([(1, 2), (2, 4), (4, 8)]):
        aa[0].plot([a, a, b, b], [0, 1, 1, 0], color=[BLUE, RED, '#568651'][i])
        aa[0].text(np.sqrt(a*b), 1.04, f'$B={b-a}$', ha='center', fontsize=8)
    for i, a in enumerate([1, 2, 3, 4, 5, 6, 7]):
        aa[1].plot([a, a, a+1, a+1], [0, 1, 1, 0], color=BLUE if i%2==0 else RED)
    aa[1].text(4.5, 1.04, '$B=1$ for every channel', ha='center', fontsize=8)
    for ax, title in zip(aa, ['Constant relative bandwidth', 'Constant absolute bandwidth']):
        style(ax, 'Normalized frequency', '$A/A_0$')
        ax.set_title(title)
        ax.set_ylim(-.05, 1.25)
        ax.set_xticks([1, 2, 4, 8])
        ax.set_yticks([0, 1])
    save(fig, 'ch5-filter-bank.pdf')


def lowpass_example():
    fig = plt.figure(figsize=(7.2, 3.1), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.13])
    aa = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[:, 1])]
    t = np.linspace(0, 1, 2000)
    x1, x2 = .5*np.cos(10*t), .2*np.cos(100*t-np.pi/4)
    y1 = .5/np.sqrt(1+.5**2)*np.cos(10*t-np.arctan(.5))
    y2 = .2/np.sqrt(1+5**2)*np.cos(100*t-np.pi/4-np.arctan(5))
    for ax, x, y, label in zip(aa, [x1, x2, x1+x2], [y1, y2, y1+y2],
                              [r'$\omega=10$', r'$\omega=100$', 'Sum']):
        ax.plot(t, x, color=GRAY, ls='--', lw=.9, label='Input')
        ax.plot(t, y, color=BLUE, label='Output')
        style(ax, '$t$ (s)', label)
    aa[0].set_xlabel('')
    aa[0].tick_params(labelbottom=False)
    aa[2].legend(frameon=False, fontsize=8, loc='upper right')
    save(fig, 'ch5-lowpass-example.pdf')


if __name__ == '__main__':
    am_waveform()
    bridge_spectra()
    conventional_spectra()
    filters()
    rc_curves()
    bandwidths()
    lowpass_example()
