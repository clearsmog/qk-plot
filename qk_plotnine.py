"""qk_plotnine — plotnine (ggplot2) theme for the qk palette (v3.1.0).

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

from qk_colors import CYCLE, CYCLE_BAR, CYCLE_CB


class theme_qk(theme_bw):
    """qk theme for plotnine — matches the matplotlib qk style."""

    def __init__(self, base_size: float = 11, base_family: str = "Inter"):
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
            panel_grid_major_y=element_line(color="#e2e8f0", alpha=0.5, linewidth=0.6),
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


def scale_fill_qk_bar():
    """Discrete fill scale using the lightened bar palette (CYCLE_BAR).

    Matches the ``CYCLE_BAR`` seaborn pattern — use for bar / column charts
    where the full-saturation CYCLE would overwhelm categorical reading.
    """
    return scale_fill_manual(values=CYCLE_BAR)
