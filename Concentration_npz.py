import numpy as np
import matplotlib.pyplot as plt


def main():
    d = np.load('Concentration_processed.npz', allow_pickle=True)
    depth_C = d['depth_C']
    conc_C = d['conc_C']
    depth_O = d['depth_O']
    conc_O = d['conc_O']
    depth_Si = d['depth_Si']
    conc_Si = d['conc_Si']

    fig, ax = plt.subplots(figsize=(8, 5))

    # Carbon on log scale (left axis)
    line_c, = ax.plot(depth_C, conc_C, color='#1f77b4', linewidth=2, label="Carbon")
    ax.set_yscale("log")
    ax.set_xlabel("Depth (nm)")
    ax.set_ylabel("Carbon Concentration (atoms/cc)")

    lines = [line_c]; labels = ["Carbon"]
    ax2 = ax.twinx()
    if depth_O.size and conc_O.size:
        line_o, = ax2.plot(depth_O, conc_O, color='#ff7f0e', linewidth=2, linestyle="-", label="Oxygen")
        lines.append(line_o); labels.append("Oxygen")
    if depth_Si.size and conc_Si.size:
        line_si, = ax2.plot(depth_Si, conc_Si, color='#2ca02c', linewidth=2, linestyle="-", label="Silicon")
        lines.append(line_si); labels.append("Silicon")
    ax2.set_ylabel("Silicon and Oxygen Intensity (arbitrary units)")

    xmin = np.inf; xmax = -np.inf
    for arr in [depth_C, depth_O, depth_Si]:
        if arr.size:
            xmin = min(xmin, np.min(arr))
            xmax = max(xmax, np.max(arr))
    if np.isfinite(xmin) and np.isfinite(xmax):
        ax.set_xlim(xmin, xmax)

    if depth_C.size and conc_C.size:
        c_pos = conc_C[conc_C > 0]
        if c_pos.size:
            c_min = np.min(c_pos)
            c_max = np.max(conc_C)
            ax.set_ylim(c_min * 0.5, c_max * 3)

    y2_vals = []
    for arr in [conc_O, conc_Si]:
        if arr.size:
            y2_vals.append(np.max(arr))
    if y2_vals:
        ax2.set_ylim(-5, max(y2_vals) * 1.2)

    ax.grid(True, which="both", alpha=0.3)
    ax.legend(lines, labels, loc="upper center", frameon=True, fontsize=11,
              fancybox=True, shadow=True, ncol=3)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

