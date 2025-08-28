import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Config
# ----------------------------
FILE_A = 'Tuning_emitter_A.npz'
FILE_B = 'Tuning_emitter_B.npz'

# Zoom windows
ZOOM_A = (1278.4, 1279.5)  # nm
ZOOM_B = (1277.1, 1277.7)  # nm

# If True, enforce equal data units inside each axes (1 nm == 1 V in physical size)
EQUAL_DATA_UNITS = False

# ----------------------------
# Load data
# ----------------------------
data_a = np.load(FILE_A)
data_b = np.load(FILE_B)

wavelength_a = data_a['wavelength']
voltage_a    = data_a['v_meas']
counts_a     = data_a['counts']   # shape ~ (nV, nLambda)

wavelength_b = data_b['wavelength']
voltage_b    = data_b['v_meas']
counts_b     = data_b['counts']

# ----------------------------
# Select zoomed regions
# ----------------------------
mask_a = (wavelength_a >= ZOOM_A[0]) & (wavelength_a <= ZOOM_A[1])
mask_b = (wavelength_b >= ZOOM_B[0]) & (wavelength_b <= ZOOM_B[1])

if mask_a.sum() < 2:
    raise ValueError(f"ZOOM_A selects too few wavelength points: {mask_a.sum()}")
if mask_b.sum() < 2:
    raise ValueError(f"ZOOM_B selects too few wavelength points: {mask_b.sum()}")

wz_a = wavelength_a[mask_a]
wz_b = wavelength_b[mask_b]
cz_a = counts_a[:, mask_a]
cz_b = counts_b[:, mask_b]

# Wavelength spans (for width ratios)
xr_a = float(np.ptp(wz_a))  # = wz_a.max() - wz_a.min()
xr_b = float(np.ptp(wz_b))

# Global voltage limits so both panels share identical vertical scale
vmin_a, vmax_a = float(voltage_a.min()), float(voltage_a.max())
vmin_b, vmax_b = float(voltage_b.min()), float(voltage_b.max())
vmin_all = min(vmin_a, vmin_b)
vmax_all = max(vmax_a, vmax_b)

# Shared color scale
cmin = float(min(np.nanmin(cz_a), np.nanmin(cz_b)))
cmax = float(max(np.nanmax(cz_a), np.nanmax(cz_b)))

# ----------------------------
# Plot
# ----------------------------
fig, axes = plt.subplots(
    1, 2, figsize=(16, 6), constrained_layout=True,
    gridspec_kw={'width_ratios': [xr_b, xr_a]}  # widths ∝ wavelength spans
)
fig.suptitle('Tuning Emitters A & B - First Measurement Comparison', fontsize=16, fontweight='bold')

# Left: Emitter B
im1 = axes[0].imshow(
    cz_b, origin='lower', aspect='auto',
    extent=[wz_b.min(), wz_b.max(), vmin_b, vmax_b],
    vmin=cmin, vmax=cmax, cmap='viridis'
)
axes[0].set_title('Emitter B - First Measurement')
axes[0].set_xlabel('Wavelength (nm)')
axes[0].set_ylabel('Voltage (V)')
axes[0].set_ylim(vmin_all, vmax_all)  # same vertical scale as right panel

# Right: Emitter A
im2 = axes[1].imshow(
    cz_a, origin='lower', aspect='auto',
    extent=[wz_a.min(), wz_a.max(), vmin_a, vmax_a],
    vmin=cmin, vmax=cmax, cmap='viridis'
)
axes[1].set_title('Emitter A - First Measurement')
axes[1].set_xlabel('Wavelength (nm)')
axes[1].set_ylabel('Voltage (V)')
axes[1].set_ylim(vmin_all, vmax_all)

# Optional: enforce equal data units (1 nm == 1 V physically) inside each axes
if EQUAL_DATA_UNITS:
    # Matplotlib >= 3.3
    try:
        axes[0].set_box_aspect((vmax_all - vmin_all) / xr_b)  # height/width = yspan/xspan
        axes[1].set_box_aspect((vmax_all - vmin_all) / xr_a)
    except AttributeError:
        # Older Matplotlib fallback
        axes[0].set_aspect(xr_b / (vmax_all - vmin_all), adjustable='box')
        axes[1].set_aspect(xr_a / (vmax_all - vmin_all), adjustable='box')

# One colorbar for both
cbar = fig.colorbar(im2, ax=axes.ravel().tolist())
cbar.set_label('Counts')

# Save + show
fig.savefig('Tuning_emitters_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# ----------------------------
# Stats
# ----------------------------
def report_stats(name, wz, volts, cz):
    peak_flat_idx = int(np.nanargmax(cz))
    r, c = np.unravel_index(peak_flat_idx, cz.shape)
    print(f"=== {name} Statistics ===")
    print(f"Zoomed wavelength range: {wz.min():.2f} - {wz.max():.2f} nm")
    print(f"Voltage range: {volts.min():.2f} - {volts.max():.2f} V")
    print(f"Counts range: {np.nanmin(cz):.1f} - {np.nanmax(cz):.1f}")
    print(f"Peak wavelength: {wz[c]:.2f} nm")
    print(f"Peak voltage: {volts[r]:.2f} V")
    print(f"Peak counts: {np.nanmax(cz):.1f}")
    print(f"Number of wavelength points: {len(wz)}\n")
    return wz[c], float(np.nanmax(cz))

pa_wl, pa_ct = report_stats('Emitter A', wz_a, voltage_a, cz_a)
pb_wl, pb_ct = report_stats('Emitter B', wz_b, voltage_b, cz_b)

print("=== Comparison ===")
print(f"Wavelength difference (A_peak - B_peak): {pa_wl - pb_wl:.2f} nm")
print(f"Peak counts ratio (A/B): {pa_ct / pb_ct:.2f}")
