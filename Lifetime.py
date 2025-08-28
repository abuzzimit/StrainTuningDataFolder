import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model, Parameters

# --- Mono-exponential model (τ parameterization) ---
def exp_decay(t, t0, tau, A, B):
    t = np.asarray(t, dtype=float)
    y = np.where(t >= t0, A * np.exp(-(t - t0) / tau), 0.0)
    return y + B

def fit_lifetime_minimal(filename="lifetime_sL20_us_.txt", tail_frac=0.15, skip_after_peak_bins=0):
    # Load CSV: time(ns), counts
    data = np.loadtxt(filename, delimiter=',')
    time = data[:, 0].astype(float)
    counts = data[:, 1].astype(float)

    # Peak and background
    i_peak = int(np.argmax(counts))
    t0 = float(time[i_peak])
    tail_start = int((1.0 - tail_frac) * len(counts))
    B0 = float(np.median(counts[max(0, tail_start):]))
    A0 = max(float(counts[i_peak] - B0), 1.0)

    # Initial τ guess from log-slope of tail
    dt = np.median(np.diff(time))
    tail_mask = (time > t0 + 3*dt) & (counts > B0 * 1.05)
    tau0 = 10.0
    if tail_mask.sum() >= 8:
        y = np.clip(counts[tail_mask] - B0, 1.0, None)
        x = time[tail_mask]
        m, _ = np.polyfit(x - t0, np.log(y), 1)
        if m < 0:
            tau0 = np.clip(-1.0/m, 0.05, 1e4)

    # Fit only the decaying part (post-peak)
    start_idx = min(i_peak + int(skip_after_peak_bins), len(time) - 1)
    mask = time >= time[start_idx]
    t_fit = time[mask]
    c_fit = counts[mask]

    # Model and parameters (t0 fixed)
    model = Model(exp_decay)
    pars = Parameters()
    pars.add('t0',  value=t0,  vary=False)
    pars.add('tau', value=tau0, min=0.02, max=1e4)
    pars.add('A',   value=A0,  min=0.0)
    pars.add('B',   value=B0,  min=0.0)

    # Poisson weights
    sigma = np.sqrt(np.clip(c_fit, 1.0, None))
    weights = 1.0 / sigma

    # Fit
    result = model.fit(c_fit, params=pars, t=t_fit, weights=weights)

    # Plot: data + fit (post-peak only), no extra text/legend/title/grid
    t_fine = np.linspace(time.min(), time.max(), 2000)
    y_fit = exp_decay(t_fine, result.params['t0'].value, result.params['tau'].value,
                      result.params['A'].value, result.params['B'].value)

    fig, ax = plt.subplots()
    ax.semilogy(time, counts, '.', ms=5, alpha=0.9)
    ax.semilogy(t_fine[t_fine >= t0], y_fit[t_fine >= t0], '-', lw=2)
    ax.set_title("Emitter $A_2$'s lifetime fit")
    ax.set_xlabel('Time (ns)')
    ax.set_ylabel('Counts')
    plt.tight_layout()
    plt.savefig('lifetime_fit_monoexp.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('lifetime_fit_monoexp.png', dpi=300, bbox_inches='tight')
    plt.show()

    return result

if __name__ == "__main__":
    fit_lifetime_minimal("lifetime_sL20_us_.txt", tail_frac=0.15, skip_after_peak_bins=0)
