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
