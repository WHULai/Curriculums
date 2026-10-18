"""Reproducible vector figures for Chapter 6; run with NumPy and Matplotlib.

Frequency axes use Hz unless explicitly normalized by the DFT spacing.
All time grids are arange(N)/fs: the end point N/fs is not sampled twice.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'img'
BLUE, RED, GRAY, GREEN = '#2d6fb1', '#b34145', '#757575', '#568651'
plt.rcParams.update({
    'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
    'font.size': 9, 'axes.titlesize': 10, 'axes.labelsize': 10,
    'lines.linewidth': 1.35, 'pdf.fonttype': 42,
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
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=.1)
    plt.close(fig)


def aliasing():
    fig, ax = plt.subplots(figsize=(7.2, 2.0), constrained_layout=True)
    fs = 200
    t = np.linspace(0, .05, 1800)
    ts = np.arange(11) / fs
    ax.plot(t * 1000, np.cos(2*np.pi*70*t), color=BLUE,
            label=r'$70\,\mathrm{Hz}$')
    ax.plot(t * 1000, np.cos(2*np.pi*130*t), color=RED, ls='--',
            label=r'$130\,\mathrm{Hz}$')
    ax.plot(ts * 1000, np.cos(2*np.pi*70*ts), 'o', color='black', ms=3,
            label=r'Samples: $f_s=200\,\mathrm{Hz}$')
    ax.legend(frameon=False, ncol=3, loc='upper right', fontsize=8)
    ax.set_ylim(-1.2, 1.65)
    style(ax, '$t$ (ms)', '$x(t)$')
    save(fig, 'ch6-aliasing.pdf')


def windows():
    n = np.arange(256)
    rect = np.ones(n.size)
    hann = .5-.5*np.cos(2*np.pi*n/n.size)  # Periodic Hann.
    m = 65536
    fbin = np.fft.rfftfreq(m) * n.size
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.1), constrained_layout=True)
    for w, color, label in [(rect, BLUE, 'Rectangular'), (hann, RED, 'Hann')]:
        aa[0].plot(n/n.size, w, color=color, label=label)
        h = abs(np.fft.rfft(w, m)) / sum(w)
        aa[1].plot(fbin, 20*np.log10(np.maximum(h, 1e-5)), color=color,
                   label=label)
    aa[0].legend(frameon=False, fontsize=8, loc='lower center')
    aa[0].set_ylim(-.05, 1.15)
    aa[1].set_xlim(0, 8)
    aa[1].set_ylim(-85, 3)
    aa[1].set_xticks([0, 1, 2, 4, 6, 8])
    style(aa[0], '$n/N$', '$w[n]$')
    style(aa[1], r'$f/(f_s/N)$', 'Normalized magnitude (dB)')
    aa[0].set_title('(a) Time window')
    aa[1].set_title('(b) Window spectrum')
    save(fig, 'ch6-windows.pdf')


def leakage():
    fs, n = 5120., 1024
    t = np.arange(n)/fs
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.2), constrained_layout=True)
    for ax, f0 in zip(aa, [100, 102]):
        x = np.sin(2*np.pi*f0*t)
        freq = np.fft.rfftfreq(n, 1/fs)
        amp = 2*abs(np.fft.rfft(x))/n
        dense_f = np.fft.rfftfreq(n*32, 1/fs)
        dense_a = 2*abs(np.fft.rfft(x, n*32))/n
        ax.plot(dense_f, dense_a, color=GRAY, lw=1,
                label='Same record, zero-padded')
        ax.vlines(freq, 0, amp, colors=BLUE, lw=1)
        ax.plot(freq, amp, 'o', ms=3, color=BLUE, label='1024-point DFT')
        ax.axvline(f0, color=RED, ls='--', lw=.8)
        ax.set_xlim(75, 130)
        ax.set_ylim(0, 1.15)
        ax.set_title(rf'$f_0={f0}\,\mathrm{{Hz}},\quad f_0T={f0*n/fs:g}$')
        style(ax, '$f$ (Hz)', 'One-sided amplitude')
    aa[1].legend(frameon=False, fontsize=7.5, loc='lower right')
    save(fig, 'ch6-leakage.pdf')


def correlations():
    lag = np.linspace(-.7, .7, 1800)
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.1), constrained_layout=True)
    aa[0].plot(lag, np.cos(2*np.pi*6*lag), color=GRAY, lw=1,
               label='Sinusoid')
    aa[0].plot(lag, np.exp(-abs(lag)/.22)*np.cos(2*np.pi*6*lag),
               color=BLUE, label='Narrow-band example')
    aa[0].plot(lag, np.exp(-abs(lag)/.025), color=RED,
               label='Broad-band example')
    aa[0].legend(frameon=False, fontsize=7, loc='upper right')
    aa[0].set_ylim(-1.1, 1.5)
    style(aa[0], r'Lag $\tau$ (s)', r'$R_x(\tau)/R_x(0)$')
    lag2 = np.linspace(-.03, .04, 1000)
    aa[1].plot(lag2*1000, np.exp(-abs(lag2-.012)/.004), color=BLUE)
    aa[1].axvline(12, color=RED, ls='--', lw=.8)
    aa[1].annotate(r'$\tau_d=12\,\mathrm{ms}$', (12, 1), xytext=(-18, .72),
                   arrowprops={'arrowstyle': '->', 'lw': .7}, fontsize=9)
    style(aa[1], r'Lag $\tau$ (ms)', r'$R_{xy}(\tau)/R_x(0)$')
    aa[0].set_title('(a) Auto-correlation shapes')
    aa[1].set_title(r'(b) $y(t)=x(t-\tau_d)$')
    save(fig, 'ch6-correlation.pdf')


def periodogram(x, fs):
    n = len(x)
    w = .5-.5*np.cos(2*np.pi*np.arange(n)/n)
    p = abs(np.fft.rfft((x-x.mean())*w))**2/(fs*sum(w*w))
    p[1:-1] *= 2
    return np.fft.rfftfreq(n, 1/fs), p


def psd_average():
    rng = np.random.default_rng(20261018)
    fs, n = 1024., 16384
    t = np.arange(n)/fs
    x = np.sin(2*np.pi*100*t)+rng.normal(0, 1, n)
    f, p = periodogram(x, fs)
    seg, hop = 1024, 512
    spectra = [periodogram(x[i:i+seg], fs)[1]
               for i in range(0, n-seg+1, hop)]
    fa = np.fft.rfftfreq(seg, 1/fs)
    pa = np.mean(spectra, axis=0)
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.1), constrained_layout=True)
    for a, fi, pi, title in zip(aa, [f, fa], [p, pa],
             [r'Full record: $\Delta f=0.0625\,\mathrm{Hz}$',
              r'31 overlapping segments: $\Delta f=1\,\mathrm{Hz}$']):
        a.plot(fi, 10*np.log10(np.maximum(pi, 1e-9)), color=BLUE, lw=.6)
        a.axhline(10*np.log10(2/fs), color=RED, ls='--', lw=.9)
        a.set_xlim(60, 140)
        a.set_ylim(-65, 12)
        a.set_title(title, fontsize=9)
        style(a, '$f$ (Hz)', r'PSD (dB re $1\,\mathrm{unit}^2/\mathrm{Hz}$)')
    save(fig, 'ch6-psd-average.pdf')


if __name__ == '__main__':
    aliasing()
    windows()
    leakage()
    correlations()
    psd_average()
