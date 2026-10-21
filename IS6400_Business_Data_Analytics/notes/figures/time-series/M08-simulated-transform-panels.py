from pathlib import Path
import csv
import math

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent
t = np.arange(1, 25, dtype=float)
season_by_position = np.array([0.18, -0.08, 0.12, -0.22])
season = season_by_position[((t.astype(int) - 1) % 4)]
trend = 2.0 + 0.04 * t
noise = 0.03 * np.sin(0.9 * t)

# Positive, deterministic teaching series. These are declared components,
# not estimates from the lecture's heater-demand figure.
log_y = trend + season + noise
y = np.exp(log_y)
boxcox_lambda0 = np.log(y)
deseasonalized = boxcox_lambda0 - season
detrended = deseasonalized - trend

rows = zip(t.astype(int), y, boxcox_lambda0, season, trend, deseasonalized, detrended)
with (OUT / "M08-simulated-transform-data.csv").open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "t", "simulated_positive_y", "boxcox_lambda0_log_y",
        "given_season_log", "given_trend_log", "deseasonalized_log",
        "detrended_log",
    ])
    writer.writerows(rows)

fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), constrained_layout=True)
panels = [
    (axes[0, 0], y, "(a) Simulated positive series", "simulated units"),
    (axes[0, 1], boxcox_lambda0, "(b) Box-Cox with λ = 0: log(y)", "log units"),
    (axes[1, 0], deseasonalized, "(c) Subtract given seasonal component", "log units"),
    (axes[1, 1], detrended, "(d) Subtract given trend", "log residual units"),
]

for ax, values, title, ylabel in panels:
    ax.plot(t, values, marker="o", markersize=3, linewidth=1.5, color="#1769aa")
    ax.axhline(0, color="#777777", linewidth=0.7, alpha=0.7)
    ax.set_title(title, fontsize=11, weight="bold")
    ax.set_xlabel("time index t")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)

idx = 4  # t = 5
for ax, values, _, _ in panels:
    ax.scatter([t[idx]], [values[idx]], color="#d62728", zorder=5)

fig.suptitle(
    "Notebook supplement — deterministic simulated data, not the lecture's source data",
    fontsize=13,
    weight="bold",
)
fig.text(
    0.5,
    -0.01,
    "Construction: log(y_t) = (2 + 0.04t) + s_position + 0.03 sin(0.9t); "
    "s = [0.18, -0.08, 0.12, -0.22]. Red point: t = 5.",
    ha="center",
    fontsize=9,
)
fig.savefig(OUT / "M08-simulated-transform-panels.svg", format="svg", bbox_inches="tight")
fig.savefig(OUT / "M08-simulated-transform-panels.preview.png", dpi=160, bbox_inches="tight")

assert np.all(y > 0)
assert np.allclose(boxcox_lambda0, log_y)
assert np.allclose(deseasonalized, trend + noise)
assert np.allclose(detrended, noise)

print(f"t5_y={y[idx]:.6f}")
print(f"t5_log={boxcox_lambda0[idx]:.6f}")
print(f"t5_season={season[idx]:.6f}")
print(f"t5_deseasonal={deseasonalized[idx]:.6f}")
print(f"t5_trend={trend[idx]:.6f}")
print(f"t5_detrended={detrended[idx]:.6f}")
