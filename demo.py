"""Demo — qk Matplotlib/Seaborn style showcase (v3.0.0).

Generates a 4x2 panel figure demonstrating the qk palette, typography,
colormaps, line_labels, colorblind palette, and context presets.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from qk_style import (
    use,
    QK_COLORS,
    CYCLE,
    CYCLE_CB,
    qk_cmap,
    heatmap_kws,
    line_labels,
)

use()

rng = np.random.default_rng(42)

fig, axes = plt.subplots(4, 2, figsize=(12, 18))

# ── 1. Line plot ──
ax = axes[0, 0]
x = np.linspace(0, 4 * np.pi, 200)
for i, label in enumerate(["Series A", "Series B", "Series C", "Series D"]):
    ax.plot(x, np.sin(x + i * 0.8) * (1 - 0.1 * i), label=label)
ax.set_title("Line Plot")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend(loc="lower left")

# ── 2. Line plot + line_labels() ──
ax = axes[0, 1]
for i, label in enumerate(["Series A", "Series B", "Series C", "Series D"]):
    ax.plot(x, np.sin(x + i * 0.8) * (1 - 0.1 * i), label=label)
ax.set_title("Line Plot + line_labels()")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()  # will be removed by line_labels
line_labels(ax)

# ── 3. Bar chart ──
ax = axes[1, 0]
categories = ["Q1", "Q2", "Q3", "Q4"]
values = [rng.integers(40, 100) for _ in categories]
bars = ax.bar(categories, values, color=CYCLE[:4], edgecolor="white", linewidth=0.8)
ax.set_title("Quarterly Revenue")
ax.set_ylabel("Revenue ($M)")

# ── 4. Scatter plot ──
ax = axes[1, 1]
for i, group in enumerate(["Control", "Treatment A", "Treatment B"]):
    n = 50
    xs = rng.normal(i * 2, 1, n)
    ys = 0.8 * xs + rng.normal(0, 0.6, n)
    ax.scatter(xs, ys, s=40, alpha=0.7, label=group, linewidth=0.5)
ax.set_title("Scatter Plot (default white edges)")
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.legend(loc="upper left")

# ── 5. Histogram ──
ax = axes[2, 0]
for i, (label, mu) in enumerate([("Group A", 0), ("Group B", 2), ("Group C", 4)]):
    data = rng.normal(mu, 1, 300)
    ax.hist(
        data,
        bins=25,
        histtype="stepfilled",
        alpha=0.45,
        label=label,
        edgecolor=CYCLE[i],
        linewidth=0.8,
    )
ax.set_title("Distribution Comparison")
ax.set_xlabel("Value")
ax.set_ylabel("Count")
ax.legend(loc="upper right")

# ── 6. Heatmap (qk_diverging colormap) ──
ax = axes[2, 1]
corr_data = rng.standard_normal((6, 6))
corr_data = (corr_data + corr_data.T) / 2  # make symmetric
np.fill_diagonal(corr_data, 1.0)
corr_data = np.clip(corr_data, -1, 1)
labels = [f"Var {i + 1}" for i in range(6)]
kws = heatmap_kws(annot=True, fmt=".2f", vmin=-1, vmax=1)
sns.heatmap(
    corr_data,
    ax=ax,
    xticklabels=labels,
    yticklabels=labels,
    **kws,
)
ax.set_title("Correlation Heatmap (qk_diverging)")

# ── 7. Sequential colormap ──
ax = axes[3, 0]
xg = np.linspace(-3, 3, 100)
yg = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(xg, yg)
Z = np.exp(-(X**2 + Y**2) / 2)
ax.contourf(X, Y, Z, levels=12, cmap=qk_cmap("qk_sequential"))
ax.set_title("Filled Contour (qk_sequential)")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")

# ── 8. Colorblind palette ──
ax = axes[3, 1]
cb_labels = [
    "Blue",
    "Vermillion",
    "Green",
    "Yellow",
    "Purple",
    "Sky",
    "Orange",
    "Black",
]
bars = ax.bar(
    range(len(cb_labels)),
    range(8, 0, -1),
    color=CYCLE_CB,
    edgecolor="white",
    linewidth=0.8,
)
ax.set_title("Colorblind-Safe Palette (Okabe-Ito)")
ax.set_ylabel("Value")
ax.set_xticks(range(len(cb_labels)), cb_labels, rotation=35, ha="right")

fig.suptitle("qk Style — Matplotlib Demo (v3.0.0)", color=QK_COLORS["heading"])

fig.savefig("demo.svg")
fig.savefig("demo.png")
print("Saved demo.svg and demo.png")
plt.show()
