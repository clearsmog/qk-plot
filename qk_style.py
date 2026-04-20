"""qk_style — Apply the qk Matplotlib/Seaborn theme (v3.1.0).

Usage:
    from qk_style import use
    use()              # paper context (default)
    use("talk")        # larger fonts/lines for slides
    use("poster")      # even larger for A0/A1 posters

Composable overlays (after importing this module):
    plt.style.use(["qk", "qk-talk"])
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from qk_colors import (
    CYCLE,
    CYCLE_BAR,
    CYCLE_CB,
    CYCLE_LIGHT,
    QK_COLORS,
    lighten,
)

_STYLE_FILE = Path(__file__).with_name("qk.mplstyle")

# Grid alpha used by both the mplstyle and set_seaborn_theme — keep in sync.
_GRID_ALPHA = 0.5

# ── Context presets (scaling overrides) ──
_PAPER_BASE = 11

_CONTEXTS: dict[str, dict] = {
    "paper": {
        "font.size": 11,
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
_PAPER_LABEL = 11.5
_PAPER_TICK = 10.5
_PAPER_LEGEND = 9.5


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


# ── Auto font registration ──


def _ensure_inter() -> None:
    """Register Inter font files if not already available to matplotlib."""
    from matplotlib import font_manager as fm

    # Check if Inter is already available
    available = {f.name.lower() for f in fm.fontManager.ttflist}
    if "inter" in available:
        return

    search_dirs = [
        Path.home() / "Library" / "Fonts",
        Path("/System/Library/Fonts"),
        Path("/System/Library/Fonts/Supplemental"),
        Path("/usr/share/fonts"),
        Path.home() / ".local" / "share" / "fonts",
    ]

    registered = False
    for d in search_dirs:
        if not d.is_dir():
            continue
        for pattern in ("Inter*.ttf", "Inter*.otf"):
            for font_path in d.glob(pattern):
                fm.fontManager.addfont(str(font_path))
                registered = True

    if registered:
        fm._load_fontmanager(try_read_cache=False)


# ── Composable context overlays ──


def _register_context_styles() -> None:
    """Register qk-talk and qk-poster as composable style overlays.

    After this, ``plt.style.use(["qk", "qk-talk"])`` works without
    separate .mplstyle files on disk.
    """
    import matplotlib.style as mstyle

    for name in ("talk", "poster"):
        style_name = f"qk-{name}"
        if style_name not in mstyle.library:
            mstyle.library[style_name] = _context_overrides(name)
            mstyle.available.append(style_name)


try:
    _register_context_styles()
except Exception:
    pass


# ── Public API ──


def use(context: str = "paper", *, colorblind: bool = False) -> None:
    """Apply the qk style globally (Matplotlib + Seaborn if available).

    Parameters
    ----------
    context : str
        Scaling preset — ``"paper"`` (default), ``"talk"``, or ``"poster"``.
    colorblind : bool
        If True, swap the color cycle to the Okabe-Ito colorblind-safe palette.
    """
    if context not in _CONTEXTS:
        raise ValueError(
            f"Unknown context {context!r}. Choose from: {', '.join(_CONTEXTS)}"
        )

    _ensure_inter()
    plt.style.use(str(_STYLE_FILE))
    plt.rcParams.update(_context_overrides(context))

    if colorblind:
        from cycler import cycler

        plt.rcParams["axes.prop_cycle"] = cycler(color=CYCLE_CB)

    # Register all colormaps
    qk_cmap()
    qk_cmap("qk_sequential")
    qk_cmap("qk_qualitative")

    try:
        set_seaborn_theme(colorblind=colorblind)
    except ImportError:
        pass


def qk_cmap(name: str = "qk_diverging"):
    """Register and return a qk colormap.

    Parameters
    ----------
    name : str
        ``"qk_diverging"`` (default) — blue-white-red
        ``"qk_sequential"`` — white to dark blue
        ``"qk_qualitative"`` — 8-color categorical
    """
    import matplotlib as mpl
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap

    if name == "qk_diverging":
        cmap = LinearSegmentedColormap.from_list(
            "qk_diverging",
            [QK_COLORS["accent"], "#ffffff", QK_COLORS["danger"]],
        )
    elif name == "qk_sequential":
        cmap = LinearSegmentedColormap.from_list(
            "qk_sequential",
            ["#ffffff", "#93c5fd", QK_COLORS["accent"], "#1e3a8a"],
        )
    elif name == "qk_qualitative":
        cmap = ListedColormap(CYCLE, name="qk_qualitative")
    else:
        raise ValueError(
            f"Unknown colormap {name!r}. "
            "Choose from: qk_diverging, qk_sequential, qk_qualitative"
        )

    mpl.colormaps.register(cmap, force=True)
    return cmap


def line_labels(ax=None, **text_kwargs) -> None:
    """Place labels at the end of each line, replacing the legend.

    Reads label and color from each Line2D on the axes, places an
    annotation at the last data point, and removes the legend. Font size
    tracks the active ``legend.fontsize`` rcParam so labels scale with
    the paper / talk / poster contexts.
    """
    from matplotlib.lines import Line2D

    if ax is None:
        ax = plt.gca()

    defaults = {
        "fontsize": plt.rcParams["legend.fontsize"],
        "fontweight": 500,
        "va": "center",
    }
    defaults.update(text_kwargs)

    for line in ax.get_lines():
        if not isinstance(line, Line2D):
            continue
        label = line.get_label()
        if label.startswith("_"):
            continue
        xdata, ydata = line.get_xdata(), line.get_ydata()
        if len(xdata) == 0:
            continue
        ax.annotate(
            f"  {label}",
            xy=(xdata[-1], ydata[-1]),
            color=line.get_color(),
            **defaults,
        )

    legend = ax.get_legend()
    if legend is not None:
        legend.remove()


def heatmap_kws(**overrides) -> dict:
    """Return default seaborn heatmap kwargs with qk styling.

    Annotation size tracks the active ``legend.fontsize`` rcParam so
    heatmaps scale with the paper / talk / poster contexts.
    """
    defaults = {
        "cmap": "qk_diverging",
        "linewidths": 0.5,
        "linecolor": "white",
        "annot_kws": {"size": plt.rcParams["legend.fontsize"]},
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


def boxplot_kws(**overrides) -> dict:
    """Return default seaborn boxplot kwargs with qk styling."""
    defaults = {
        "saturation": 0.85,
        "linewidth": 0.8,
        "linecolor": QK_COLORS["text"],
        "fliersize": 4,
    }
    defaults.update(overrides)
    return defaults


def barplot_kws(**overrides) -> dict:
    """Return default seaborn barplot kwargs with qk styling.

    For per-bar colors, pass hue=x_col and palette=CYCLE_BAR:
        sns.barplot(df, x="cat", y="val", hue="cat", legend=False,
                    **barplot_kws(palette=CYCLE_BAR))
    """
    defaults = {
        "saturation": 0.85,
        "edgecolor": QK_COLORS["text"],
        "linewidth": 0.8,
        "capsize": 0.1,
        "err_kws": {"linewidth": 1.2},
    }
    defaults.update(overrides)
    return defaults


def catplot_kws(**overrides) -> dict:
    """Return default seaborn catplot kwargs with qk styling."""
    defaults = {"height": 5, "aspect": 1.6, "margin_titles": True}
    defaults.update(overrides)
    return defaults


def pairplot_kws(**overrides) -> dict:
    """Return default seaborn pairplot kwargs with qk styling."""
    defaults = {
        "corner": True,
        "diag_kind": "kde",
        "height": 2.5,
        "plot_kws": {"alpha": 0.6, "edgecolor": "white", "linewidth": 0.5},
        "diag_kws": {"linewidth": 1.5},
    }
    defaults.update(overrides)
    return defaults


def jointplot_kws(**overrides) -> dict:
    """Return default seaborn jointplot kwargs with qk styling."""
    defaults = {
        "height": 6,
        "marginal_kws": {"linewidth": 1.2},
        "joint_kws": {"alpha": 0.6, "edgecolor": "white", "linewidth": 0.5},
    }
    defaults.update(overrides)
    return defaults


def qk_palette(n: int | None = None, *, colorblind: bool = False):
    """Return the qk color cycle as a Seaborn palette.

    Parameters
    ----------
    n : int, optional
        Number of colors. Defaults to the full 8-color cycle.
    colorblind : bool
        If True, return the Okabe-Ito palette instead.
    """
    import seaborn as sns

    base = CYCLE_CB if colorblind else CYCLE
    colors = base[:n] if n else base
    return sns.color_palette(colors)


def set_seaborn_theme(*, colorblind: bool = False) -> None:
    """Configure Seaborn to use qk aesthetics."""
    import seaborn as sns

    palette = qk_palette(colorblind=colorblind)
    sns.set_palette(palette)
    sns.set_style(
        "white",
        {
            "axes.facecolor": "white",
            "axes.edgecolor": QK_COLORS["border"],
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": QK_COLORS["border"],
            "grid.alpha": _GRID_ALPHA,
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


def sparkline(ax, x, y, *, color: str | None = None, linewidth: float | None = None,
              mark_extrema: bool = True, **plot_kwargs):
    """Render a Tufte-style sparkline — a compact, axis-less line trace.

    Strips spines, ticks, grid, and labels; tightens the y-range to the data.
    Optionally marks the min and max points. Returns the Line2D for further
    styling.

    Parameters
    ----------
    ax : matplotlib Axes
        Target axes; its decorations are removed in place.
    x, y : sequences
        Data coordinates.
    color : str, optional
        Line color; defaults to ``QK_COLORS["text"]``.
    linewidth : float, optional
        Line width; defaults to ``rcParams["lines.linewidth"] * 0.7`` so
        sparklines stay quieter than primary charts.
    mark_extrema : bool
        If True, places small dots at the min and max of ``y``.
    **plot_kwargs
        Forwarded to ``ax.plot``.
    """
    color = color or QK_COLORS["text"]
    linewidth = linewidth if linewidth is not None else plt.rcParams["lines.linewidth"] * 0.7

    (line,) = ax.plot(x, y, color=color, linewidth=linewidth, **plot_kwargs)

    if mark_extrema and len(y):
        y_arr = list(y)
        i_min, i_max = y_arr.index(min(y_arr)), y_arr.index(max(y_arr))
        ax.plot(list(x)[i_min], y_arr[i_min], "o", color=QK_COLORS["accent"],
                markersize=3, zorder=3)
        ax.plot(list(x)[i_max], y_arr[i_max], "o", color=QK_COLORS["danger"],
                markersize=3, zorder=3)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(False)
    ax.margins(x=0.02, y=0.15)
    return line
