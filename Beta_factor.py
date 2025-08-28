import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib import colors

def plot_betaTE0_colormap():
    """
    Load betaTE0.npz and plot interpolated 2D colormaps for βz, βx, βy over the full
    symmetric plane by mirroring the provided top-right quadrant.
    """
    data = np.load('betaTE0.npz')

    # Arrays: original quadrant (Δx >= 0, Δz >= 0)
    beta_z = data['beta_z_TE0']  # shape (Nx, Nz) e.g., (7,5)
    beta_x = data['beta_x_TE0']  # shape (Nx, Nz)
    beta_y = data['beta_y_TE0']  # shape (Nx, Nz)
    delta_x = data['delta_x']    # shape (Nx,)
    delta_z = data['delta_z']    # shape (Nz,)

    # Mesh for the original quadrant: shapes (Nz, Nx)
    Xq, Zq = np.meshgrid(delta_x, delta_z)    # (Nz, Nx)

    # Points from the original quadrant (flattened)
    pts_q = np.column_stack((Xq.ravel(), Zq.ravel()))

    # Values must match (Nz, Nx) layout — transpose from (Nx, Nz) to (Nz, Nx)
    vz_q = beta_z.T.ravel()
    vx_q = beta_x.T.ravel()
    vy_q = beta_y.T.ravel()

    # Mirror into all four quadrants (even symmetry)
    pts_all = np.vstack([
        pts_q,
        np.column_stack((-Xq.ravel(),  Zq.ravel())),
        np.column_stack(( Xq.ravel(), -Zq.ravel())),
        np.column_stack((-Xq.ravel(), -Zq.ravel())),
    ])
    vz_all = np.concatenate([vz_q, vz_q, vz_q, vz_q])
    vx_all = np.concatenate([vx_q, vx_q, vx_q, vx_q])
    vy_all = np.concatenate([vy_q, vy_q, vy_q, vy_q])

    # Symmetric fine grid
    x_max = float(np.max(delta_x))
    z_max = float(np.max(delta_z))
    x_fine = np.linspace(-x_max, x_max, 201)
    z_fine = np.linspace(-z_max, z_max, 201)
    Xf, Zf = np.meshgrid(x_fine, z_fine)

    # Interpolate (linear is stable on sparse grids)
    beta_z_interp = griddata(pts_all, vz_all, (Xf, Zf), method='linear')
    beta_x_interp = griddata(pts_all, vx_all, (Xf, Zf), method='linear')
    beta_y_interp = griddata(pts_all, vy_all, (Xf, Zf), method='linear')

    # Shared normalization across all plots
    norm = colors.Normalize(vmin=0, vmax=1)
    extent = [-x_max, x_max, -z_max, z_max]

    # Figure with 3 subplots and a single colorbar outside
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    fig.suptitle('Dipole waveguide coupling for different dipole orientations', fontsize=16, y=0.98)

    im1 = axes[0].imshow(beta_x_interp, origin='lower', extent=extent,
                         cmap='viridis', norm=norm, aspect='equal')
    axes[0].set_title('[110]')
    axes[0].set_xlabel('Δx')
    axes[0].set_ylabel('Δz')

    im2 = axes[1].imshow(beta_y_interp, origin='lower', extent=extent,
                         cmap='viridis', norm=norm, aspect='equal')
    axes[1].set_title(r'[$\bar{1}$10]')
    axes[1].set_xlabel('Δx')
    axes[1].set_ylabel('Δz')

    im3 = axes[2].imshow(beta_z_interp, origin='lower', extent=extent,
                         cmap='viridis', norm=norm, aspect='equal')
    axes[2].set_title('[011]')
    axes[2].set_xlabel('Δx')
    axes[2].set_ylabel('Δz')

    # One shared colorbar outside (right)
    cbar = fig.colorbar(im3, ax=axes, location='right', pad=0.02, shrink=0.5, aspect=10)
    cbar.set_label('β')

    plt.show()
    return fig, axes

if __name__ == "__main__":
    plot_betaTE0_colormap()
