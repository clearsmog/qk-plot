"""Demo — qk plotnine (ggplot2) style showcase.

Generates 4 demo plots demonstrating the qk plotnine theme.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    facet_wrap,
    geom_bar,
    geom_histogram,
    geom_line,
    geom_point,
    ggplot,
    labs,
)

from qk_plotnine import scale_color_qk, scale_fill_qk, theme_qk

rng = np.random.default_rng(42)

# ── 1. Scatter with color groups ──
n = 150
df_scatter = pd.DataFrame(
    {
        "x": rng.normal(0, 1, n),
        "y": rng.normal(0, 1, n),
        "group": rng.choice(["Control", "Treatment A", "Treatment B"], n),
    }
)
df_scatter["y"] += df_scatter["group"].map(
    {"Control": 0, "Treatment A": 1, "Treatment B": 2}
)

p1 = (
    ggplot(df_scatter, aes("x", "y", color="group"))
    + geom_point(alpha=0.7, size=2)
    + theme_qk()
    + scale_color_qk()
    + labs(title="Scatter Plot", x="Feature 1", y="Feature 2")
)
p1.save("demo_plotnine_scatter.svg", width=8, height=5, dpi=150)

# ── 2. Bar chart ──
df_bar = pd.DataFrame(
    {
        "quarter": ["Q1", "Q2", "Q3", "Q4"],
        "revenue": [85, 92, 78, 105],
    }
)

p2 = (
    ggplot(df_bar, aes("quarter", "revenue", fill="quarter"))
    + geom_bar(stat="identity")
    + theme_qk()
    + scale_fill_qk()
    + labs(title="Quarterly Revenue", y="Revenue ($M)")
)
p2.save("demo_plotnine_bar.svg", width=8, height=5, dpi=150)

# ── 3. Line with facets ──
months = np.arange(1, 13)
df_line = pd.DataFrame(
    {
        "month": np.tile(months, 3),
        "value": np.concatenate(
            [
                np.cumsum(rng.normal(2, 1, 12)),
                np.cumsum(rng.normal(1.5, 1.2, 12)),
                np.cumsum(rng.normal(1, 0.8, 12)),
            ]
        ),
        "region": np.repeat(["North", "South", "West"], 12),
    }
)

p3 = (
    ggplot(df_line, aes("month", "value", color="region"))
    + geom_line(size=1.5)
    + facet_wrap("region")
    + theme_qk()
    + scale_color_qk()
    + labs(title="Monthly Trend by Region", x="Month", y="Cumulative Value")
)
p3.save("demo_plotnine_facet.svg", width=10, height=5, dpi=150)

# ── 4. Histogram / density ──
df_hist = pd.DataFrame(
    {
        "value": np.concatenate(
            [
                rng.normal(0, 1, 300),
                rng.normal(3, 1.2, 300),
                rng.normal(6, 0.8, 300),
            ]
        ),
        "group": np.repeat(["A", "B", "C"], 300),
    }
)

p4 = (
    ggplot(df_hist, aes("value", fill="group"))
    + geom_histogram(alpha=0.5, bins=30, position="identity")
    + theme_qk()
    + scale_fill_qk()
    + labs(title="Distribution Comparison", x="Value", y="Count")
)
p4.save("demo_plotnine_hist.svg", width=8, height=5, dpi=150)

print("Saved 4 demo SVGs: scatter, bar, facet, hist")
