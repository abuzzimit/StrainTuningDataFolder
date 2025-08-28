import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Path to your file ---
path = "Y0ORK987_YD_04 Type 2 sample (C).xlsx"

# --- Read sheet with no header so we can detect it ourselves ---
df = pd.read_excel(path, sheet_name="Processed data", header=None)

# Find the row that contains the word 'Depth' (this marks the header line)
header_row = df.apply(lambda r: r.astype(str).str.contains(r"\bDepth\b", case=False, regex=True)).any(axis=1).idxmax()

species_headers = df.iloc[header_row-1].fillna("")
units_row     = df.iloc[header_row+1].fillna("")

# Blocks are arranged as [Depth, CONC, spacer] repeated across columns
blocks = []
for i in range(0, df.shape[1], 3):
    if i + 1 >= df.shape[1]:
        break
    name = str(species_headers[i]).strip()
    if not name or name.lower().startswith("unnamed"):
        continue
    blocks.append({
        "name": name,            # e.g., '12C', 'O–>', 'Si–>'
        "depth_col": i,
        "conc_col":  i + 1,
        "depth_unit": str(units_row[i]).strip(),        # '(nm)'
        "conc_unit":  str(units_row[i+1]).strip()       # '(atoms/cc)' or '(arb. units)'
    })

# Data rows start a couple lines after the units row
start = header_row + 3

def extract(block):
    depth = pd.to_numeric(df.iloc[start:, block["depth_col"]], errors="coerce").to_numpy()
    conc  = pd.to_numeric(df.iloc[start:, block["conc_col"]],  errors="coerce").to_numpy()
    m = np.isfinite(depth) & np.isfinite(conc)
    return {
        "name": block["name"],
        "depth": depth[m],
        "conc":  conc[m],
        "depth_unit": block["depth_unit"],
        "conc_unit":  block["conc_unit"]
    }

series = [extract(b) for b in blocks]
C  = next(s for s in series if "12C" in s["name"])
O  = next((s for s in series if s["name"].startswith("O")), None)
Si = next((s for s in series if s["name"].startswith("Si")), None)

# Make the figure: single axes + twin y-axis (no subplots)
fig, ax = plt.subplots(figsize=(8, 5))

# Carbon on log scale (left axis) - Dark blue color
line_c, = ax.plot(C["depth"], C["conc"], color='#1f77b4', linewidth=2, label="Carbon")
ax.set_yscale("log")
ax.set_xlabel("Depth (nm)")
ax.set_ylabel("Carbon Concentration (atoms/cc)")

# O and Si on right axis (linear) - Orange and Green colors
lines = [line_c]; labels = ["Carbon"]
ax2 = ax.twinx()
if O:
    line_o, = ax2.plot(O["depth"], O["conc"], color='#ff7f0e', linewidth=2, linestyle="-", label="Oxygen")
    lines.append(line_o); labels.append("Oxygen")
if Si:
    line_si, = ax2.plot(Si["depth"], Si["conc"], color='#2ca02c', linewidth=2, linestyle="-", label="Silicon")
    lines.append(line_si); labels.append("Silicon")
ax2.set_ylabel("Silicon and Oxygen Intensity (arbitrary units)")

# Set title
plt.title("Concentration vs Depth for Carbon, Oxygen, and Silicon", fontsize=14, fontweight='bold', pad=20)

# Limits and grid
xmin = min(np.min(C["depth"]), np.min(O["depth"]) if O else np.inf, np.min(Si["depth"]) if Si else np.inf)
xmax = max(np.max(C["depth"]), np.max(O["depth"]) if O else -np.inf, np.max(Si["depth"]) if Si else -np.inf)
ax.set_xlim(xmin, xmax)

# Adjust y-axis limits for better fit
if O and Si:
    # For Carbon (log scale) - set reasonable min/max
    c_min = np.min(C["conc"][C["conc"] > 0])  # Smallest positive value
    c_max = np.max(C["conc"])
    ax.set_ylim(c_min * 0.5, c_max * 3)  # Log scale limits
    
    # For Oxygen and Silicon (linear scale)
    y2_max = max(np.max(O["conc"]), np.max(Si["conc"]))
    ax2.set_ylim(-5, y2_max*1.2)  # Add 20% padding

ax.grid(True, which="both", alpha=0.3)

# Legend inside the plot (horizontal, upper center)
ax.legend(lines, labels, loc="upper center", frameon=True, fontsize=11, 
          fancybox=True, shadow=True, ncol=3)

plt.tight_layout()
plt.show()
