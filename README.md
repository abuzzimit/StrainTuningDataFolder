# Strain Tuning Data Analysis

This repository contains a Jupyter notebook for analyzing strain tuning data for quantum emitters. The project is located in the `StrainTuningDataFolder` directory.

## Setup

### Virtual Environment
The project uses a Python virtual environment to manage dependencies.

**To activate the virtual environment:**
```bash
.\venv\Scripts\Activate.ps1
```

**To deactivate:**
```bash
deactivate
```

### Dependencies
All required packages are listed in `requirements.txt`. The main packages include:

- **numpy** - Numerical computations and array operations
- **matplotlib** - Plotting and visualization
- **scipy** - Scientific computing (interpolation, optimization)
- **lmfit** - Curve fitting and modeling
- **pandas** - Data manipulation and analysis
- **jupyter** - Interactive notebooks

## Analysis

### Main Analysis Notebook
- `analysis.ipynb` - Complete analysis notebook containing all strain tuning data analysis

The notebook includes the following analyses:
- Beta factor coupling maps for different dipole orientations
- Depth profile and impurity concentrations from SIMS measurements
- Second-order correlation g(τ) analysis with blinking model fitting
- Time-resolved lifetime fitting with mono-exponential decay
- Photoluminescence scan mapping
- Power saturation curve analysis
- Strain map interpolation and visualization
- Spectral tuning versus voltage for multiple emitters

### Data Files
- `beta_factors.npz` - Beta factor data for dipole-waveguide coupling
- `depth_profile.npz` - Depth profile data from SIMS measurements
- `g2_data.npz` - g² correlation data
- `lifetime_data.npz` - Lifetime measurement data
- `pl_scan.npz` - Photoluminescence scan data
- `saturation_data.npz` - Saturation curve data
- `strain_map.npz` - Strain mapping data
- `tuning_A.npz` / `tuning_B.npz` - Emitter tuning data

## Usage

### Running the Analysis
1. Activate the virtual environment:
```bash
.\venv\Scripts\Activate.ps1
```

2. Launch Jupyter Lab or Jupyter Notebook:
```bash
jupyter lab
# or
jupyter notebook
```

3. Open `analysis.ipynb` and run the cells to perform the analysis.

## Output

The notebook generates plots and displays them inline. All analysis results are shown directly in the notebook cells.

## Project Structure

```
StrainTuningDataFolder/
├── venv/                          # Virtual environment
├── analysis.ipynb                 # Main analysis notebook
├── *.npz                          # Data files
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

## Notes

- Make sure the virtual environment is activated before running the notebook
- All data files should be in the same directory as the notebook
- The `.gitignore` file excludes the virtual environment and generated plots from version control
- The notebook uses relative paths, so it should work regardless of the absolute location of the project folder
