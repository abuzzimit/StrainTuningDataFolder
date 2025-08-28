import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import Model
from scipy.interpolate import interp1d
import matplotlib as mpl

# -----------------------
# Style & Colors
# -----------------------
COLOR_DATA = "#21295C"
COLOR_ERROR = "#067BC2"
COLOR_INTERP = "#067BC2"   # blue line + fill
COLOR_FIT = "#FFAD69"      # fit line
COLOR_FILL = "#84BCDA"     # fill color
COLOR_REF = "#BA2D0B"      # reference line color

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'font.size': 10,
    'axes.linewidth': 1,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.minor.visible': True,
    'ytick.minor.visible': True,
})
mpl.rc('text.latex', preamble=r'\usepackage{siunitx}\sisetup{detect-all}'
                              r'\usepackage{helvet}\usepackage[T1]{fontenc}'
                              r'\usepackage{sansmath}\sansmath')


def g2_blinking(x, amp, a, Gamma1, b, Gamma2, t0):
    return amp - (1 - a) * ((1 + b) * np.exp(-np.abs(x - t0)/Gamma1)
                            - b * np.exp(-np.abs(x - t0)/Gamma2))


def main():
    # Load pre-converted NPZ
    d = np.load('solo_rider_first_g2.npz')
    corr_delay = d['corr_delay']

    # Histogram (binning in ps for convenience)
    binwidth = 0.7e-9
    edges_ps = np.arange(-200e-9, 200e-9 + binwidth, binwidth) * 1e12  # ps
    centers_ps = edges_ps[1:] - binwidth * 1e12 / 2
    counts, _ = np.histogram(corr_delay, bins=edges_ps)
    errors = np.sqrt(counts)

    # Normalize by baseline (adjust slice if needed)
    norm = np.mean(counts[:50])
    y = counts / norm
    err = errors / norm

    # Shift x so the minimum bin is at tau=0, convert ps -> ns
    min_delay_ps = centers_ps[np.argmin(counts)]
    x_ns = (centers_ps - min_delay_ps) * 1e-3  # ns

    # Fit window
    mask = (x_ns >= -30) & (x_ns <= 30)
    x_fit, y_fit, err_fit = x_ns[mask], y[mask], err[mask]

    # Fit model (amp and t0 fixed)
    mod = Model(g2_blinking)
    pars = mod.make_params(amp=1, a=0.1, Gamma1=2, b=2, Gamma2=8, t0=0)
    pars['amp'].set(vary=False)
    pars['t0'].set(vary=False)
    result = mod.fit(y_fit, params=pars, x=x_fit, weights=1/np.clip(err_fit, 1e-9, None))

    # Smooth fit (2001 points)
    x_smooth = np.linspace(-30, 30, 2001)
    y_smooth = mod.eval(params=result.params, x=x_smooth)

    # Linear interpolation through the data (2001 points)
    f_lin = interp1d(x_fit, y_fit, kind='linear', bounds_error=False, fill_value='extrapolate')
    x_lin = np.linspace(x_fit.min(), x_fit.max(), 2001)
    y_lin = f_lin(x_lin)

    # Plot
    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    ax.errorbar(x_fit, y_fit, yerr=err_fit, fmt='o', ms=3, lw=1.5,
                color=COLOR_DATA, ecolor=COLOR_ERROR, capsize=0, label='Data')
    ax.plot(x_lin, y_lin, '-', lw=1.5, color=COLOR_INTERP, alpha=1)
    ax.fill_between(x_lin, 0, y_lin, color=COLOR_FILL, alpha=1)
    ax.plot(x_smooth, y_smooth, '-', color=COLOR_FIT, lw=3, label='Fit', zorder=10)
    ax.axhline(0.5, color=COLOR_REF, linestyle='--', linewidth=2, alpha=0.8, zorder=9)
    ax.set_xlim(-25, 25)
    ax.set_ylim(0, 2.6)
    ax.set_xlabel(r'Delay $\\tau$ (ns)')
    ax.set_ylabel(r'$g^{(2)}(\\tau)$')
    ax.legend(frameon=False, loc='upper right')
    plt.tight_layout()
    # keep saving behavior consistent with original
    plt.savefig("g2_clean_filled.png", dpi=300)
    plt.savefig("g2_clean_filled.pdf")
    plt.show()


if __name__ == "__main__":
    main()

