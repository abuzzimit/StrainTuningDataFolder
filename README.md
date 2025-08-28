# Strain Tuning Data Analysis

This repository contains Python scripts for analyzing strain tuning data for quantum emitters. The project is located in the `StrainTuningDataFolder` directory.

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
- **openpyxl** - Excel file reading (for Concentration.py)
- **seaborn** - Statistical data visualization
- **jupyter** - Interactive notebooks (optional)

## Scripts

### Core Analysis Scripts
- `g2.py` - g²(τ) correlation analysis with blinking model fitting
- `PL_scan.py` - Photoluminescence scan data processing and visualization
- `Strain_map.py` - Strain mapping and interpolation
- `Lifetime.py` - Lifetime fitting with mono-exponential model
- `Saturation_curve.py` - Power saturation curve analysis
- `Tuning_emitters.py` - Emitter tuning analysis and comparison
- `Beta_factor.py` - Beta factor colormap visualization
- `Concentration.py` - Concentration vs depth analysis from Excel data

### Data Files
- `solo_rider_first_g2.mat` - g² correlation data
- `PL_scan.npz` - Photoluminescence scan data
- `Strain_larger_35V_241124.txt` - Strain measurement data
- `lifetime_sL20_us_.txt` - Lifetime measurement data
- `Saturation_spectrometer_B.npz` - Saturation curve data
- `Tuning_emitter_A.npz` / `Tuning_emitter_B.npz` - Emitter tuning data
- `betaTE0.npz` - Beta factor data
- `Y0ORK987_YD_04 Type 2 sample (C).xlsx` - Concentration depth profile data

## Usage

### Method 1: Using convenience scripts (Recommended)
Use the provided batch or PowerShell scripts to automatically activate the virtual environment and run analysis scripts:

**Windows Batch:**
```bash
run_analysis.bat script_name.py
```

**PowerShell:**
```powershell
.\run_analysis.ps1 script_name.py
```

**Examples:**
```bash
run_analysis.bat g2.py
run_analysis.bat Concentration.py
run_analysis.bat Strain_map.py
```

### Method 2: Manual activation
Activate the virtual environment first, then run scripts:

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run scripts
python script_name.py
```

**Examples:**
```bash
python g2.py
python Concentration.py
python Strain_map.py
```

## Output

Scripts generate plots and save them as PNG/PDF files. Some scripts also print fitting parameters and analysis results to the console.

## Project Structure

```
StrainTuningDataFolder/
├── venv/                          # Virtual environment
├── *.py                           # Python analysis scripts
├── *.mat, *.txt, *.npz, *.xlsx   # Data files
├── *.png, *.pdf                  # Generated plots
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
├── run_analysis.bat              # Windows batch script for easy execution
└── run_analysis.ps1              # PowerShell script for easy execution
```

## Notes

- Make sure the virtual environment is activated before running scripts
- All data files should be in the same directory as the scripts
- The `.gitignore` file excludes the virtual environment and generated plots from version control
- Scripts use relative paths, so they should work regardless of the absolute location of the project folder
