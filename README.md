# RATE Framework Simulation Engine

This repository contains the source code and simulation scripts for the paper:
**"Risk-Anchored Temporal Equilibrium: A Physics-Based Diagnostic for Valuation Anomalies in Low-Interest Environments"**

The **RATE (Risk-Anchored Temporal Equilibrium)** framework introduces a dual-anchor mechanism to analyze the mismatch between market psychological expectations (Psychological Anchor, $n$) and asset physical growth constraints (Physical Anchor, $E[T]$).

## 📂 Repository Structure

- `rate_simulation.py`: The core simulation engine that calculates $n$, $E[T]$, and the Time Paradox Index (TPI). It also generates the visualization charts (Figure 3-1, Figure 3-2) used in the paper.
- `requirements.txt`: List of Python dependencies required to run the simulation.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed. You can check your version by running:
```bash
python --version
Installation
1. Clone the repository:
2. Install dependencies:
📊 Usage
To run the simulation and generate the diagnostic charts:
python rate_simulation.py
The script will output the TPI calculation results in the console and display the "Psychological vs. Physical Time" comparison chart.
📝 Citation
If you use this code in your research, please cite our paper:
[LIU DIANPENG]. (2026). Risk-Anchored Temporal Equilibrium: The Physicist’s Critique of Growth in Low-Rate Environments.
📄 License
This project is licensed under the Apache License 2.0.


**# RATE Framework – Robustness Check (Appendix B)

This repository contains the **official Python implementation** for the robustness check presented in **Appendix B** of the paper:

> **Risk‑Anchored Temporal Equilibrium: The Physicist‘s Critique of Growth in Low‑Rate Environments**  
> RATE Research Group, 2026

The script reproduces **Figure B‑1** and **Table B‑1** in full, validating the conservative nature of the linear approximation used in the main text.

---

## 📌 Overview

The main text of the paper employs a **linear approximation** for the risk premium in the ZZ‑CAPM framework:  
`c(σ) = λσ` with `λ = 0.2`. This yields an equilibrium volatility `σ* ≈ 48.4%` under the baseline scenario (`r = 1.8%`, `g = 20%`).

However, the **original ZZ‑CAPM** defines the risk premium as a **non‑linear implicit function** of both volatility `σ` and the investor’s required payback period `n`:

\[
c(\sigma,n) = -\frac{1}{n}\ln\left[2\left(1-N\left(\frac{\sigma\sqrt{n}}{4}\right)\right)\right], \qquad 
n = \frac{1}{r + c(\sigma,n)}.
\]

This script solves the above **self‑consistent equation** via robust bisection and compares the exact `n(σ)` with the linear approximations for `λ = 0.20, 0.25, 0.30`.

**Key finding:** The linear approximation **systematically underestimates** the investor’s patience `n`, hence **overestimates risk tolerance**. The exact `σ*` is **57.4%** – far higher than any linear estimate. Therefore, the linear model used in the paper is a **conservative, downward‑biased estimator**; it never overlooks true risks.

---

## 🔧 Requirements

- Python **3.8 or higher**
- Required packages: `numpy`, `scipy`, `matplotlib`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the main script:

```bash
python RATE_ZZ_robustness.py
```

No additional arguments are required – all parameters are hard‑coded to match the paper’s baseline.

---

## 📊 Output

### 1. **Console Output – Table B‑1**
The script prints a formatted table showing equilibrium volatilities `σ*` for each tested `λ`:

```
============================================================
表 B-1  不同线性近似系数下的均衡波动率与偏差
============================================================
λ        线性 σ*     非线性 σ*     偏差 Δσ*
------------------------------------------------------------
0.20       48.4%        57.4%        -9.0%
0.25       46.3%        57.4%       -11.1%
0.30       44.3%        57.4%       -13.1%
============================================================
```

### 2. **Figure B‑1 – Linear vs. Non‑linear Psychological Anchor**
A publication‑ready vector graphic **`RATE_ZZ_robustness.pdf`** is saved in the current directory. It contains:
- Physical anchor `E[T]` (red solid line)
- Non‑linear exact `n(σ)` (green solid line)
- Linear approximations for `λ = 0.20, 0.25, 0.30` (coloured dashed lines)
- Physical meltdown line `σ_max = √(2g) = 63.2%`
- Equilibrium points and annotations

This figure can be directly included in LaTeX documents.

---

## ⚙️ Customization

You can easily modify the **macro parameters** at the top of `RATE_ZZ_robustness.py`:

```python
R = 0.018      # risk‑free rate (default: 1.8%)
G = 0.20       # nominal growth rate (default: 20%)
M = 2.0        # target multiple (default: 2, i.e. doubling)
LAMBDA_LIST = [0.20, 0.25, 0.30]   # linear coefficients to test
```

After changing any parameter, re‑run the script to obtain updated results.

---

## 📄 License

This code is released under the **MIT License**. You are free to use, modify, and distribute it, provided that proper citation to the original paper is maintained.

---

## 📬 Citation

If you use this code in your research, please cite:

> RATE Research Group (2026). *Risk‑Anchored Temporal Equilibrium: The Physicist's Critique of Growth in Low‑Rate Environments*. [Manuscript in preparation].

For the underlying theoretical models, please refer to:

- Zhang, Z. (2008, 2021). *ZZ Growth Model & ZZ‑CAPM*.  
- Karatzas, I., & Shreve, S. E. (1991). *Brownian Motion and Stochastic Calculus*.

---

## 🙋 Support

For questions or issues, please open an issue on GitHub or contact the corresponding author.

**Repository:** [https://github.com/fidopapa/RATE-Framework](https://github.com/fidopapa/RATE-Framework)
