"""Demo — qk Matplotlib/Seaborn style showcase.

Generates a 3x2 panel figure demonstrating the qk palette, typography,
diverging colormap, and context presets.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from qk_style import (
    use,
    QK_COLORS,
    CYCLE,
    qk_cmap,
    heatmap_kws,
    _CONTEXTS,
    _context_overrides,
)

use()

rng = np.random.default_rng(42)

fig, axes = plt.subplots(3, 2, figsize=(12, 14))

# ── 1. Line plot ──
ax = axes[0, 0]
x = np.linspace(0, 4 * np.pi, 200)
for i, label in enumerate(["Series A", "Series B", "Series C", "Series D"]):
    ax.plot(x, np.sin(x + i * 0.8) * (1 - 0.1 * i), label=label)
ax.set_title("Line Plot")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend(loc="lower left")

# ── 2. Bar chart ──
ax = axes[0, 1]
categories = ["Q1", "Q2", "Q3", "Q4"]
values = [rng.integers(40, 100) for _ in categories]
bars = ax.bar(categories, values, color=CYCLE[:4], edgecolor="white", linewidth=0.8)
ax.set_title("Quarterly Revenue")
ax.set_ylabel("Revenue ($M)")

# ── 3. Scatter plot ──
ax = axes[1, 0]
for i, group in enumerate(["Control", "Treatment A", "Treatment B"]):
    n = 50
    xs = rng.normal(i * 2, 1, n)
    ys = 0.8 * xs + rng.normal(0, 0.6, n)
    ax.scatter(xs, ys, s=40, alpha=0.7, label=group, edgecolors="white", linewidth=0.5)
ax.set_title("Scatter Plot")
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.legend(loc="upper left")

# ── 4. Histogram ──
ax = axes[1, 1]
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

# ── 5. Heatmap (qk_diverging colormap) ──
ax = axes[2, 0]
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

# ── 6. Context presets comparison ──
ax = axes[2, 1]
ctx_names = list(_CONTEXTS.keys())
props = [
    "font.size",
    "axes.titlesize",
    "axes.labelsize",
    "xtick.labelsize",
    "legend.fontsize",
]
prop_short = ["Base font", "Title", "Label", "Tick", "Legend"]

x_pos = np.arange(len(props))
width = 0.25

for i, ctx in enumerate(ctx_names):
    overrides = _context_overrides(ctx)
    vals = [overrides[p] for p in props]
    ax.bar(
        x_pos + i * width,
        vals,
        width,
        label=ctx,
        color=CYCLE[i],
        edgecolor="white",
        linewidth=0.5,
    )

ax.set_xticks(x_pos + width)
ax.set_xticklabels(prop_short, rotation=25, ha="right")
ax.set_title("Context Presets — Font Sizes")
ax.set_ylabel("Size (pt)")
ax.legend(loc="upper left")

fig.suptitle("qk Style — Matplotlib Demo (v2.2.0)", color=QK_COLORS["heading"])

fig.savefig("demo.svg")
fig.savefig("demo.png")
print("Saved demo.svg and demo.png")
plt.show()
