import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

# Using a seed so the results stay the same every time we run the script
np.random.seed(1234)
n_sim = 100000

# Setting up our geological guesses using different distributions
area = np.random.normal(500, 40, n_sim)
thickness = np.random.triangular(20, 50, 120, n_sim)
porosity = np.random.uniform(0.12, 0.28, n_sim)
saturation = np.random.beta(2, 5, n_sim)
recovery = np.random.lognormal(0.3, 0.05, n_sim)

# Step 1: Calculate the "Big Picture" - what happens when all variables vary at once?
total_recoverable_volume = area * thickness * porosity * (1 - saturation) * recovery

# Step 2: Sensitivity Analysis - figuring out which variable has the most impact
results = np.zeros((6, n_sim))
variables = [area, thickness, porosity, (1 - saturation), recovery]
numeric_results = np.zeros((5, 3))
tornado = np.zeros((5, 3))

for idx, curr_var in enumerate(variables):
    others = variables[:idx] + variables[idx+1:]
    other_prod = np.prod([np.median(o) for o in others])
    
    # Calculate the "swing" for the Tornado plot (P10 to P90)
    trv_down, trv_med, trv_up = np.percentile(curr_var, [10, 50, 90]) * other_prod
    trv = curr_var * other_prod

    tornado[idx, :] = trv_down, trv_med, trv_up
    results[idx, :] = trv
    numeric_results[idx, :] = np.percentile(trv, [10, 50, 90])

# Store the full simulation results in the last slot for side-by-side comparison
results[5, :] = total_recoverable_volume

# The Tornado Plot 
names = ['Area', 'Thickness', 'Porosity', 'Saturation Impact', 'Recovery Factor', 'Comparison']
labels = names[:5]
widths = tornado[:, 2] - tornado[:, 0]
lows = tornado[:, 0]

plt.figure(figsize=(10, 6))
# 'left=lows' makes the bars float between the P10 and P90 values
plt.barh(labels, widths, left=lows, color='lightseagreen', edgecolor='black')

# Draw a line down the middle to show our "Most Likely" outcome
base_case = np.median(total_recoverable_volume)
plt.axvline(base_case, color='red', linestyle='--', label=f'Base Case: {base_case:.0f}')

plt.title('Sensitivity Analysis: Which variables drive the most risk?')
plt.xlabel('Volume')
plt.legend()

#  The S-Curve (Cumulative Distribution Function)
plt.figure(figsize=(10, 6))
# Sorting the data creates the 'S' shape of the cumulative probability
sorted_vols = np.sort(total_recoverable_volume)
y_values = np.linspace(0, 1, n_sim)

plt.plot(sorted_vols, y_values, color='navy', linewidth=2, label='Cumulative Probability')

# Mark the key thresholds (P10, P50, P90)
p_markers = np.percentile(total_recoverable_volume, [10, 50, 90])
colors = ['orange', 'green', 'red']
labels_p = ['P10 (Low)', 'P50 (Mid)', 'P90 (High)']

for val, col, lab in zip(p_markers, colors, labels_p):
    plt.axvline(val, color=col, linestyle=':', label=f'{lab}: {val:.0f}')

plt.title('S-Curve: Probability of Exceeding Volume Targets')
plt.ylabel('Probability')
plt.xlabel('Total Recoverable Volume')
plt.legend()
plt.grid(alpha=0.3)

# Individual Impact Histograms
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for i in range(6):
    sns.histplot(results[i, :], ax=axes[i], kde=True, color='skyblue')
    axes[i].set_title(f'Effect of {names[i]}')
    axes[i].set_xlabel('Volume')

plt.tight_layout()
plt.show()