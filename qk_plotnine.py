"""qk_plotnine — plotnine (ggplot2) theme for the qk palette (v2.3.0).

Usage:
    from qk_plotnine import theme_qk, scale_color_qk, scale_fill_qk
    ggplot(df, aes("x", "y", color="group")) + geom_point() + theme_qk() + scale_color_qk()
"""

from __future__ import annotations

import matplotlib

from plotnine import (
    element_blank,
    element_line,
    element_rect,
    element_text,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_bw,
)

# Mirror palettes from qk_style.py
CYCLE = [
    "#2563eb",  # accent (blue)
    "#dc2626",  # danger (red)
    "#059669",  # success (green)
    "#d97706",  # warning (amber)
    "#7c3aed",  # purple
    "#0d9488",  # teal
    "#ea580c",  # orange
    "#e11d48",  # rose
]

# Okabe-Ito colorblind-safe palette
CYCLE_CB = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#CC79A7",  # reddish purple
    "#56B4E9",  # sky blue
    "#E69F00",  # orange
    "#000000",  # black
]


class theme_qk(theme_bw):
    """qk theme for plotnine — matches the matplotlib qk style."""

    def __init__(self, base_size: float = 10.5, base_family: str = "Inter"):
        super().__init__(base_size=base_size, base_family=base_family)
        self += theme(
            plot_title=element_text(
                color="#1e3a8a", weight="bold", size=base_size * 1.33
            ),
            axis_title=element_text(
                weight="bold", color="#0f172a", size=base_size * 1.05
            ),
            axis_text=element_text(color="#0f172a", size=base_size * 0.95),
            axis_ticks=element_line(color="#64748b"),
            panel_background=element_rect(fill="white"),
            panel_grid_major_y=element_line(color="#e2e8f0", alpha=0.5, size=0.6),
            panel_grid_major_x=element_blank(),
            panel_grid_minor=element_blank(),
            legend_background=element_rect(fill="white", color="none"),
            legend_key=element_rect(fill="white", color="none"),
            strip_background=element_rect(fill="#f8fafc", color="#e2e8f0"),
        )
        # Set svg.fonttype for Typst SVG embedding
        matplotlib.rcParams["svg.fonttype"] = "path"


def scale_color_qk(*, colorblind: bool = False):
    """Discrete color scale. Use colorblind=True for Okabe-Ito palette."""
    colors = CYCLE_CB if colorblind else CYCLE
    return scale_color_manual(values=colors)


def scale_fill_qk(*, colorblind: bool = False):
    """Discrete fill scale. Use colorblind=True for Okabe-Ito palette."""
    colors = CYCLE_CB if colorblind else CYCLE
    return scale_fill_manual(values=colors)
