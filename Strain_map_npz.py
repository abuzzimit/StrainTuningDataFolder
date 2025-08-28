import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.path import Path


def main():
    d = np.load('Strain_larger_35V_241124.npz')
    y, z, strain_yy = d['y'], d['z'], d['strain_yy']
    mask = (y > -1) & (z > -1)
    y_filt, z_filt, strain_filt = y[mask], z[mask], strain_yy[mask]

    def pareto_front(y, z, minimize_y=True, minimize_z=True):
        yy = y if minimize_y else -y
        zz = z if minimize_z else -z
        order = np.lexsort((zz, yy))
        yy_s, zz_s = yy[order], zz[order]

        pareto_mask = np.ones(len(yy_s), dtype=bool)
        best_zz = np.inf
        for i, val in enumerate(zz_s):
            if val < best_zz:
                best_zz = val
            else:
                pareto_mask[i] = False
        return order[pareto_mask]

    idx_upper = pareto_front(y_filt, z_filt, minimize_y=False, minimize_z=False)
    yu, zu = y_filt[idx_upper], z_filt[idx_upper]
    u_order = np.argsort(yu)
    yu, zu = yu[u_order], zu[u_order]

    idx_lower = pareto_front(y_filt, z_filt, minimize_y=True, minimize_z=True)
    yl, zl = y_filt[idx_lower], z_filt[idx_lower]
    l_order = np.argsort(yl)
    yl, zl = yl[l_order], zl[l_order]

    ymin_val = np.min(y_filt); ymax_val = np.max(y_filt)
    ymin_pts = np.column_stack((y_filt[np.isclose(y_filt, ymin_val)], z_filt[np.isclose(y_filt, ymin_val)]))
    ymax_pts = np.column_stack((y_filt[np.isclose(y_filt, ymax_val)], z_filt[np.isclose(y_filt, ymax_val)]))
    ymin_bottom = ymin_pts[np.argmin(ymin_pts[:, 1])]
    ymin_top    = ymin_pts[np.argmax(ymin_pts[:, 1])]
    ymax_bottom = ymax_pts[np.argmin(ymax_pts[:, 1])]
    ymax_top    = ymax_pts[np.argmax(ymax_pts[:, 1])]

    boundary_y = []
    boundary_z = []
    boundary_y.append(ymin_bottom[0]); boundary_z.append(ymin_bottom[1])
    boundary_y.extend(yl); boundary_z.extend(zl)
    boundary_y.append(ymax_bottom[0]); boundary_z.append(ymax_bottom[1])
    boundary_y.append(ymax_top[0]); boundary_z.append(ymax_top[1])
    boundary_y.extend(yu[::-1]); boundary_z.extend(zu[::-1])
    boundary_y.append(ymin_top[0]); boundary_z.append(ymin_top[1])

    polygon = np.column_stack((boundary_y, boundary_z))
    poly_path = Path(polygon)

    Ny, Nz = 1000, 200
    yg = np.linspace(np.min(boundary_y), np.max(boundary_y), Ny)
    zg = np.linspace(np.min(boundary_z), np.max(boundary_z), Nz)
    Yg, Zg = np.meshgrid(yg, zg)

    points = np.column_stack((y_filt, z_filt))
    values = strain_filt

    strain_grid = griddata(points, values, (Yg, Zg), method='linear')

    mask_inside = poly_path.contains_points(np.column_stack((Yg.ravel(), Zg.ravel())))
    mask_inside = mask_inside.reshape(Yg.shape)
    strain_grid[~mask_inside] = np.nan

    plt.figure(figsize=(8, 6))
    strain_grid_ueps = strain_grid * 1e6
    plt.pcolormesh(Yg, Zg, strain_grid_ueps, shading='auto', cmap='viridis')
    plt.colorbar(label='Strain (μeps)')
    plt.plot(boundary_y, boundary_z, 'k-', lw=2, label='Boundary')
    plt.xlabel("$y$")
    plt.ylabel("$z$")
    plt.title("Interpolated strain inside boundary")
    plt.legend()
    plt.xlim(-0.9, 20)
    plt.ylim(np.min(boundary_z) - 0.1, np.max(boundary_z) + 0.1)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

