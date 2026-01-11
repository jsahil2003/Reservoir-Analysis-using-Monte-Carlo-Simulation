# Reservoir Uncertainty Analysis using Monte Carlo Simulation

### Project Purpose
This project is a high-performance **Monte Carlo Simulation** built to quantify geological uncertainty in oil and gas reservoir appraisals. Instead of relying on a single "best guess," this tool runs 100,000 iterations to determine the full range of potential outcomes for **Total Recoverable Volume**.

### Core Methodology
The tool models subsurface uncertainty by assigning unique probability distributions to key geological parameters. This ensures that the final volume estimate accounts for the "tails" of risk (Low Case vs. High Case).

* **Area:** Normal Distribution (Bell curve)
* **Thickness:** Triangular Distribution (Skewed geological estimates)
* **Porosity:** Uniform Distribution (Range-bound uncertainty)
* **Saturation:** Beta Distribution (Non-linear fluid distribution)
* **Recovery Factor:** Lognormal Distribution (Standard for efficiency factors)



### Analytical Suite
The project generates three industry-standard outputs to assist in decision-making:

1.  **Sensitivity Analysis (Tornado Plot):** Uses a "One-at-a-Time" (OAT) approach to isolate which variable (e.g., Thickness vs. Porosity) is the primary driver of project risk.
2.  **Cumulative Risk Profile (S-Curve):** Generates an industry-standard CDF (Cumulative Distribution Function) to provide the **P10 (Low)**, **P50 (Mid)**, and **P90 (High)** confidence levels.
3.  **Impact Distributions:** A multi-plot grid of histograms that visualizes how each individual parameter's uncertainty propagates through the volumetric equation.




### Engineering Optimizations
The calculation engine is optimized for speed and mathematical accuracy:

* **Vectorized Processing:** Leverages NumPy broadcasting to perform millions of operations in milliseconds, bypassing slow Python loops.
* **Efficient List Slicing:** Implemented **$O(1)$ slicing** (`variables[:idx] + variables[idx+1:]`) for the sensitivity logic. This allows the tool to isolate specific variables without the computational cost of searching the entire dataset.
* **Broadcasting:** Efficiently applies scalar products to massive arrays to calculate sensitivity swings instantly.

---

*This project was developed as part of a technical portfolio to demonstrate proficiency in probabilistic modeling, NumPy optimization, and subsurface risk analysis.*
