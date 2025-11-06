# 🧬 Optical Tweezers Unwinding Analysis Scripts and pymol sessions

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Lumicks pylake](https://img.shields.io/badge/dependency-pylake-orange)](https://lumicks-pylake.readthedocs.io/en/latest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A collection of Python scripts for analyzing **optical tweezers** measurements of DNA unwinding activity.  
These scripts are designed for use with the **Lumicks C-Trap** data format and require prior installation of the [`pylake`](https://lumicks-pylake.readthedocs.io/en/latest/) package.

---

## ⚙️ Features

The workflow is organized into Spyder-style code blocks (each separated by `#%%`):

1. **Data Range Selection**  
   Interactively select a region of interest from plotted distance–time data.

2. **Linear Fit Analysis**  
   Perform linear regression on the selected data points to extract slope and intercept values (e.g., unwinding rate).

3. **Pause Detection**  
   Apply a **Savitzky–Golay filter** to smooth the distance trace, convert the filtered data to **base pairs unwound**, and identify **pause states** during the unwinding process.

---

## 📦 Requirements

- Python ≥ 3.8  
- [`lumicks.pylake`](https://lumicks-pylake.readthedocs.io/en/latest/)  
- NumPy  
- Matplotlib  
- SciPy  
- (optional) JupyterLab or Spyder for interactive code-block execution

Install dependencies:
```bash
pip install lumicks.pylake numpy matplotlib scipy
