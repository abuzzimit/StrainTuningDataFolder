import os
import numpy as np


def convert_g2(mat_path="solo_rider_first_g2.mat", out_path="solo_rider_first_g2.npz"):
    try:
        import scipy.io
    except ImportError as e:
        print(f"[g2] SciPy not available: {e}")
        return False
    if not os.path.exists(mat_path):
        print(f"[g2] Source file not found: {mat_path}")
        return False
    try:
        data = scipy.io.loadmat(mat_path)["Data"]
        corr_delay = data["time"][0][0][0]
        np.savez(out_path, corr_delay=corr_delay)
        print(f"[g2] Wrote {out_path}")
        return True
    except Exception as e:
        print(f"[g2] Failed to convert: {e}")
        return False


def convert_lifetime(txt_path="lifetime_sL20_us_.txt", out_path="lifetime_sL20_us_.npz"):
    if not os.path.exists(txt_path):
        print(f"[lifetime] Source file not found: {txt_path}")
        return False
    try:
        data = np.loadtxt(txt_path, delimiter=",")
        time = data[:, 0].astype(float)
        counts = data[:, 1].astype(float)
        np.savez(out_path, time=time, counts=counts)
        return True
    except Exception as e:
        print(f"[lifetime] Failed to convert: {e}")
        return False


def convert_strain(txt_path="Strain_larger_35V_241124.txt", out_path="Strain_larger_35V_241124.npz"):
    if not os.path.exists(txt_path):
        print(f"[strain] Source file not found: {txt_path}")
        return False
    try:
        data = np.loadtxt(txt_path, skiprows=9)
        # columns: [?, y, z, strain_yy, ...] based on current script
        y = data[:, 1]
        z = data[:, 2]
        strain_yy = data[:, 3]
        np.savez(out_path, y=y, z=z, strain_yy=strain_yy)
        print(f"[strain] Wrote {out_path}")
        return True
    except Exception as e:
        print(f"[strain] Failed to convert: {e}")
        return False


def convert_concentration(xlsx_path="Y0ORK987_YD_04 Type 2 sample (C).xlsx", out_path="Concentration_processed.npz"):
    try:
        import pandas as pd
    except ImportError as e:
        print(f"[concentration] pandas not available: {e}")
        return False
    if not os.path.exists(xlsx_path):
        print(f"[concentration] Source file not found: {xlsx_path}")
        return False
    try:
        df = pd.read_excel(xlsx_path, sheet_name="Processed data", header=None)

        # Find header row containing 'Depth'
        header_row = df.apply(lambda r: r.astype(str).str.contains(r"\bDepth\b", case=False, regex=True)).any(axis=1).idxmax()

        species_headers = df.iloc[header_row - 1].fillna("")
        units_row = df.iloc[header_row + 1].fillna("")

        # Identify 3-column blocks: [Depth, CONC, spacer]
        blocks = []
        for i in range(0, df.shape[1], 3):
            if i + 1 >= df.shape[1]:
                break
            name = str(species_headers[i]).strip()
            if not name or name.lower().startswith("unnamed"):
                continue
            blocks.append({
                "name": name,
                "depth_col": i,
                "conc_col": i + 1,
                "depth_unit": str(units_row[i]).strip(),
                "conc_unit": str(units_row[i + 1]).strip(),
            })

        start = header_row + 3

        def extract(block):
            depth = pd.to_numeric(df.iloc[start:, block["depth_col"]], errors="coerce").to_numpy()
            conc = pd.to_numeric(df.iloc[start:, block["conc_col"]], errors="coerce").to_numpy()
            m = np.isfinite(depth) & np.isfinite(conc)
            return {
                "name": block["name"],
                "depth": depth[m],
                "conc": conc[m],
                "depth_unit": block["depth_unit"],
                "conc_unit": block["conc_unit"],
            }

        series = [extract(b) for b in blocks]

        def find_series(prefix):
            for s in series:
                if s["name"].startswith(prefix):
                    return s
            return None

        C = find_series("12C")
        O = find_series("O")
        Si = find_series("Si")

        np.savez(
            out_path,
            depth_C=(C["depth"] if C else np.array([], float)),
            conc_C=(C["conc"] if C else np.array([], float)),
            depth_O=(O["depth"] if O else np.array([], float)),
            conc_O=(O["conc"] if O else np.array([], float)),
            depth_Si=(Si["depth"] if Si else np.array([], float)),
            conc_Si=(Si["conc"] if Si else np.array([], float)),
            depth_unit=(C["depth_unit"] if C else units_row[0]),
            conc_unit_C=(C["conc_unit"] if C else ""),
            conc_unit_O=(O["conc_unit"] if O else ""),
            conc_unit_Si=(Si["conc_unit"] if Si else ""),
        )
        print(f"[concentration] Wrote {out_path}")
        return True
    except Exception as e:
        print(f"[concentration] Failed to convert: {e}")
        return False


def main():
    ok = True
    ok &= convert_g2()
    ok &= convert_lifetime()
    ok &= convert_strain()
    ok &= convert_concentration()
    if ok:
        print("All conversions completed.")
    else:
        print("Some conversions failed. See messages above.")


if __name__ == "__main__":
    main()
