"""Demo — qk Seaborn helpers showcase (v3.0.0).

Generates 4 SVG files demonstrating the qk seaborn helpers:
violin + strip overlay, boxplot, barplot (CYCLE_BAR), pairplot.
"""

import numpy as np
import pandas as pd
import seaborn as sns

from qk_style import (
    CYCLE_BAR,
    use,
    barplot_kws,
    boxplot_kws,
    pairplot_kws,
    strip_kws,
    violin_kws,
)

use()
rng = np.random.default_rng(42)

# ── Shared synthetic data ──
n = 200
df = pd.DataFrame(
    {
        "group": rng.choice(["Control", "Treatment A", "Treatment B"], n),
        "value": np.concatenate(
            [
                rng.normal(5, 1.2, n // 3),
                rng.normal(6.5, 1.0, n // 3),
                rng.normal(5.8, 1.5, n - 2 * (n // 3)),
            ]
        ),
        "metric": rng.normal(50, 15, n),
    }
)

# ── 1. Violin + strip overlay ──
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(data=df, x="group", y="value", ax=ax, **violin_kws())
sns.stripplot(data=df, x="group", y="value", ax=ax, **strip_kws(alpha=0.4, size=4))
ax.set_title("Distribution Comparison")
ax.set_ylabel("Response Value")
ax.set_xlabel("")
fig.savefig("demo_seaborn_violin.svg")
plt.close(fig)

# ── 2. Boxplot ──
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x="group", y="metric", ax=ax, **boxplot_kws())
ax.set_title("Metric by Group")
ax.set_ylabel("Metric Score")
ax.set_xlabel("")
fig.savefig("demo_seaborn_box.svg")
plt.close(fig)

# ── 3. Barplot with CYCLE_BAR ──
bar_df = pd.DataFrame(
    {
        "quarter": ["Q1", "Q2", "Q3", "Q4"],
        "revenue": [84, 112, 97, 135],
        "stderr": [5, 8, 6, 10],
    }
)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=bar_df,
    x="quarter",
    y="revenue",
    hue="quarter",
    legend=False,
    ax=ax,
    **barplot_kws(palette=CYCLE_BAR[:4], errorbar=None),
)
ax.set_title("Quarterly Revenue")
ax.set_ylabel("Revenue ($M)")
ax.set_xlabel("")
fig.savefig("demo_seaborn_bar.svg")
plt.close(fig)

# ── 4. Pairplot ──
pair_df = pd.DataFrame(
    {
        "Length": rng.normal(5, 1, 150),
        "Width": rng.normal(3, 0.8, 150),
        "Depth": rng.normal(4, 1.2, 150),
        "Type": rng.choice(["A", "B", "C"], 150),
    }
)
pair_df["Width"] += pair_df["Length"] * 0.3  # add correlation
pair_df["Depth"] += pair_df["Length"] * 0.2

g = sns.pairplot(data=pair_df, hue="Type", **pairplot_kws())
g.savefig("demo_seaborn_pair.svg")
plt.close(g.figure)

print("Saved 4 demo SVGs: violin, box, bar, pair")
