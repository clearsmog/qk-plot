"""qk_colors — Shared color primitives for the qk plotting stack (v3.1.0).

Single source of truth for the qk palette. Both qk_style.py (matplotlib /
seaborn) and qk_plotnine.py (plotnine) import from here, so a palette edit
touches exactly one file.

The Typst companion lives in qk-plot.typ and must be kept in sync manually —
see CLAUDE.md "Color Sync Protocol".
"""

from __future__ import annotations

QK_COLORS = {
    "accent": "#2563eb",
    "danger": "#dc2626",
    "success": "#059669",
    "warning": "#d97706",
    "purple": "#7c3aed",
    "teal": "#0d9488",
    "orange": "#ea580c",
    "rose": "#e11d48",
    "heading": "#1e3a8a",
    "text": "#0f172a",
    "muted": "#64748b",
    "surface": "#f8fafc",
    "border": "#e2e8f0",
}

CYCLE = [
    QK_COLORS["accent"],
    QK_COLORS["danger"],
    QK_COLORS["success"],
    QK_COLORS["warning"],
    QK_COLORS["purple"],
    QK_COLORS["teal"],
    QK_COLORS["orange"],
    QK_COLORS["rose"],
]

# Okabe-Ito colorblind-safe palette (frozen — do not modify)
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


def lighten(hex_color: str, amount: float = 0.75) -> str:
    """Lighten a hex color by mixing with white.

    Parameters
    ----------
    hex_color : str
        Hex color string (with or without '#' prefix).
    amount : float
        0.0 = unchanged, 1.0 = white.
    """
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = round(r + (255 - r) * amount)
    g = round(g + (255 - g) * amount)
    b = round(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"


CYCLE_LIGHT = [lighten(c, 0.75) for c in CYCLE]  # area / fill backgrounds
CYCLE_BAR = [lighten(c, 0.30) for c in CYCLE]    # bar fill colors

__all__ = [
    "QK_COLORS",
    "CYCLE",
    "CYCLE_CB",
    "CYCLE_LIGHT",
    "CYCLE_BAR",
    "lighten",
]
