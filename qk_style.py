"""qk_style — Apply the qk Matplotlib/Seaborn theme (v2.2.0).

Usage:
    from qk_style import use
    use()              # paper context (default)
    use("talk")        # larger fonts/lines for slides
    use("poster")      # even larger for A0/A1 posters
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

# ── qk palette (Tailwind CSS 600-series) ──
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

_STYLE_FILE = Path(__file__).with_name("qk.mplstyle")

# ── Context presets (scaling overrides) ──
_PAPER_BASE = 10.5

_CONTEXTS: dict[str, dict] = {
    "paper": {
        "font.size": 10.5,
        "figure.figsize": (8, 5),
        "lines.linewidth": 2.0,
    },
    "talk": {
        "font.size": 14,
        "figure.figsize": (12, 7.5),
        "lines.linewidth": 2.5,
    },
    "poster": {
        "font.size": 18,
        "figure.figsize": (16, 10),
        "lines.linewidth": 3.0,
    },
}

# Paper-baseline sizes (must match qk.mplstyle)
_PAPER_TITLE = 14
_PAPER_LABEL = 11
_PAPER_TICK = 10
_PAPER_LEGEND = 9


def _context_overrides(name: str) -> dict:
    """Build full rcParams overrides for the given context preset."""
    ctx = _CONTEXTS[name]
    scale = ctx["font.size"] / _PAPER_BASE
    return {
        "font.size": ctx["font.size"],
        "axes.titlesize": round(_PAPER_TITLE * scale, 1),
        "axes.labelsize": round(_PAPER_LABEL * scale, 1),
        "xtick.labelsize": round(_PAPER_TICK * scale, 1),
        "ytick.labelsize": round(_PAPER_TICK * scale, 1),
        "legend.fontsize": round(_PAPER_LEGEND * scale, 1),
        "figure.figsize": list(ctx["figure.figsize"]),
        "lines.linewidth": ctx["lines.linewidth"],
    }


def use(context: str = "paper") -> None:
    """Apply the qk style globally (Matplotlib + Seaborn if available).

    Parameters
    ----------
    context : str
        Scaling preset — ``"paper"`` (default), ``"talk"``, or ``"poster"``.
    """
    if context not in _CONTEXTS:
        raise ValueError(
            f"Unknown context {context!r}. Choose from: {', '.join(_CONTEXTS)}"
        )

    plt.style.use(str(_STYLE_FILE))
    plt.rcParams.update(_context_overrides(context))

    # Register the qk diverging colormap
    qk_cmap()

    try:
        set_seaborn_theme()
    except ImportError:
        pass


def qk_cmap():
    """Register and return a blue-white-red diverging colormap."""
    from matplotlib.colors import LinearSegmentedColormap

    import matplotlib as mpl

    cmap = LinearSegmentedColormap.from_list(
        "qk_diverging",
        [QK_COLORS["accent"], "#ffffff", QK_COLORS["danger"]],
    )
    mpl.colormaps.register(cmap, force=True)
    return cmap


def heatmap_kws(**overrides) -> dict:
    """Return default seaborn heatmap kwargs with qk styling."""
    defaults = {
        "cmap": "qk_diverging",
        "linewidths": 0.5,
        "linecolor": "white",
        "annot_kws": {"size": 9},
    }
    defaults.update(overrides)
    return defaults


def violin_kws(**overrides) -> dict:
    """Return default seaborn violin plot kwargs with qk styling."""
    defaults = {"inner": "quart", "linewidth": 0.8, "saturation": 0.85}
    defaults.update(overrides)
    return defaults


def strip_kws(**overrides) -> dict:
    """Return default seaborn strip plot kwargs with qk styling."""
    defaults = {"jitter": 0.3, "edgecolor": "white", "linewidth": 0.5}
    defaults.update(overrides)
    return defaults


def qk_palette(n: int | None = None):
    """Return the qk color cycle as a Seaborn palette.

    Parameters
    ----------
    n : int, optional
        Number of colors. Defaults to the full 8-color cycle.
    """
    import seaborn as sns

    colors = CYCLE[:n] if n else CYCLE
    return sns.color_palette(colors)


def set_seaborn_theme() -> None:
    """Configure Seaborn to use qk aesthetics."""
    import seaborn as sns

    sns.set_palette(qk_palette())
    sns.set_style(
        "white",
        {
            "axes.facecolor": "white",
            "axes.edgecolor": QK_COLORS["border"],
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": QK_COLORS["border"],
            "grid.alpha": 0.5,
            "grid.linewidth": 0.6,
        },
    )


def despine(ax=None, **kwargs) -> None:
    """Remove top/right spines (convenience wrapper).

    Delegates to seaborn.despine if available, otherwise manual removal.
    """
    try:
        import seaborn as sns

        sns.despine(ax=ax, **kwargs)
    except ImportError:
        ax = ax or plt.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
