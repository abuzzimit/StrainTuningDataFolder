import os
import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import Model

# ---------------- config ----------------
FNAME   = 'Saturation_spectrometer_B.npz'
WL_MIN, WL_MAX = 1275.0, 1279.0
BG_CONST = 60.0
FIT_SLICE = slice(4, -1)  # [4:-1]

# ---------------- model ----------------
def pwr_saturation_lin(x, Iinf, Psat):
    # I(x) = Iinf / (1 + Psat/x)
    return Iinf * (1.0 / (1.0 + Psat / x))

# ---------------- io ----------------
def load_real_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found!")
    d = np.load(filename)
    wl     = d['wavelength']
    counts = d['counts']       # shape (nPowers, nWavelengths)
    powers = d['power_in']     # μW
    return wl, counts, powers

# ---------------- processing ----------------
def process_spectral_data(wl, counts, powers):
    # window
    m = (wl > WL_MIN) & (wl < WL_MAX)
    wl_fit = wl[m]
    Y = counts[:, m] - BG_CONST  # background subtraction

    # integrate around the row-wise maximum using ±4 points
    nP, nL = Y.shape
    int_1 = np.zeros(nP, dtype=float)
    for k in range(nP):
        c = int(np.argmax(Y[k, :]))
        a = c - 4
        b = c + 4               # slice is [a:b)
        int_1[k] = np.sum(Y[k, a:b])

    # identical power scaling
    P = powers * 5.0  
    return P, int_1

# ---------------- fitting ----------------
def fit_saturation_curve(P, int_1):
    mod = Model(pwr_saturation_lin)
    pars = mod.make_params()
    pars['Psat'].set(value=20, vary=True, min=0, max=float(np.max(P * 1e6)))
    pars['Iinf'].set(value=float(np.max(int_1)), vary=True)
    result = mod.fit(int_1[FIT_SLICE], params=pars, x=P[FIT_SLICE] * 1e6)
    return result

# ---------------- plotting ----------------
def plot_saturation_curve(P, int_1, result):
    plt.figure()
    xfit = P[FIT_SLICE] * 1e6
    yfit = int_1[FIT_SLICE]
    plt.semilogy(xfit, yfit, 'o', ms=8, label='Data')
    plt.semilogy(xfit, result.best_fit, lw=1.5, label='Fit', zorder=0)
    plt.legend(loc='lower right')
    psat = result.params['Psat'].value
    iinf = result.params['Iinf'].value
    plt.xlabel('CW excitation power (μW)')
    plt.ylabel('Intensity (counts/min)')
    plt.title('Power saturation')
    plt.tight_layout()
    plt.savefig('powersweep_solo.png', dpi=300, bbox_inches='tight')
    plt.show()

# ---------------- main ----------------
def main():
    wl, counts, powers = load_real_data(FNAME)
    P, int_1 = process_spectral_data(wl, counts, powers)
    result = fit_saturation_curve(P, int_1)
    plot_saturation_curve(P, int_1, result)

if __name__ == '__main__':
    main()
