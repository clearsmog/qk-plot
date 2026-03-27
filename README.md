# qk Plotting Stack (v3.0.0)

Unified plotting theme across matplotlib, seaborn, plotnine, cetz-plot, and Lilaq — all sharing the Tailwind CSS 600-series palette.

## Quick Start

### matplotlib + seaborn
```python
from qk_style import use, QK_COLORS, CYCLE, CYCLE_CB, CYCLE_LIGHT, CYCLE_BAR
from qk_style import heatmap_kws, line_labels, lighten

use()              # paper context (default)
use("talk")        # slides / presentations
use("poster")      # A0/A1 posters
use(colorblind=True)  # Okabe-Ito colorblind-safe cycle

# Composable overlays (no function call needed)
import matplotlib.pyplot as plt
plt.style.use(["qk", "qk-talk"])

import seaborn as sns
sns.heatmap(data, **heatmap_kws(annot=True))

# Replace legend with inline end-of-line labels
line_labels()
```

### seaborn
```python
from qk_style import use, violin_kws, strip_kws, boxplot_kws, barplot_kws
from qk_style import pairplot_kws, jointplot_kws, catplot_kws, CYCLE_BAR
import seaborn as sns

use()
sns.violinplot(data=df, x="group", y="value", **violin_kws())
sns.stripplot(data=df, x="group", y="value", **strip_kws(alpha=0.5))

sns.boxplot(data=df, x="group", y="value", **boxplot_kws())
sns.barplot(data=df, x="cat", y="val", hue="cat", legend=False,
            **barplot_kws(palette=CYCLE_BAR[:4]))
sns.pairplot(df, hue="species", **pairplot_kws())
```

### plotnine (grammar of graphics)
```python
from qk_plotnine import theme_qk, scale_color_qk, scale_fill_qk
from plotnine import ggplot, aes, geom_point

(ggplot(df, aes("x", "y", color="group"))
 + geom_point() + theme_qk() + scale_color_qk())

# Colorblind-safe variant
(ggplot(df, aes("x", "y", color="group"))
 + geom_point() + theme_qk() + scale_color_qk(colorblind=True))
```

### cetz-plot (Typst native)
```typst
#import "@preview/cetz:0.4.2"
#import "@preview/cetz-plot:0.1.3": plot, chart
#import "qk-plot.typ": *

// Style helpers for series and bars
plot.plot(plot-style: qk-plot-style, ...)
chart.columnchart(bar-style: qk-bar-style, ...)
```

### Lilaq (Typst native, preferred)
```typst
#import "@preview/lilaq:0.6.0" as lq
#import "qk-plot.typ": *

#show: qk-lilaq-theme()                   // standard palette
#show: qk-lilaq-theme(colorblind: true)   // Okabe-Ito palette

lq.diagram(
  xlabel: [X], ylabel: [Y],
  lq.plot(xs, ys, label: [Series A]),
)
```

## Seaborn Helpers

All helpers return `dict` -- pass as `**kwargs`. Override any default: `heatmap_kws(linewidths=1.0)`.

| Helper | Key defaults | Usage |
|--------|-------------|-------|
| `heatmap_kws()` | qk_diverging cmap, white gridlines | `sns.heatmap(corr, **heatmap_kws(annot=True))` |
| `violin_kws()` | inner="quart", linewidth=0.8 | `sns.violinplot(df, **violin_kws())` |
| `strip_kws()` | jitter=0.3, white edges | `sns.stripplot(df, **strip_kws())` |
| `boxplot_kws()` | dark linecolor, linewidth=0.8 | `sns.boxplot(df, **boxplot_kws())` |
| `barplot_kws()` | error caps, dark edges | `sns.barplot(df, **barplot_kws())` |
| `catplot_kws()` | height=5, aspect=1.6, margin_titles | `sns.catplot(df, kind="box", **catplot_kws())` |
| `pairplot_kws()` | corner=True, kde diagonal | `sns.pairplot(df, hue="g", **pairplot_kws())` |
| `jointplot_kws()` | height=6, white scatter edges | `sns.jointplot(data=df, x="a", y="b", **jointplot_kws())` |

## Decision Framework

| Scenario | Tool | Why |
|----------|------|-----|
| Most native Typst charts | **Lilaq** | Rich API, qk theme support |
| Distribution comparison | **seaborn** | violin + strip overlay |
| Correlation / heatmap | **seaborn** | heatmap_kws with annotations |
| Pairwise exploration | **seaborn** | pairplot with KDE diagonal |
| Faceted / layered grammar | **plotnine** | ggplot2-style composition |
| Line plot (1-4 series) | **matplotlib** | line_labels or legend |
| Complex (4+ series, annotations) | **matplotlib** | Full API control |
| Simple Typst chart | **cetz-plot** | Lightweight, Typst-native |

## Color Palette

All tools share the same 8-color cycle (Tailwind CSS 600-series):

| Name | Hex | Use |
|------|-----|-----|
| accent | `#2563eb` | Primary / first series |
| danger | `#dc2626` | Alert / second series |
| success | `#059669` | Positive / third series |
| warning | `#d97706` | Caution / fourth series |
| purple | `#7c3aed` | Fifth series |
| teal | `#0d9488` | Sixth series |
| orange | `#ea580c` | Seventh series |
| rose | `#e11d48` | Eighth series |

Semantic colors: heading (`#1e3a8a`), text (`#0f172a`), muted (`#64748b`), surface (`#f8fafc`), border (`#e2e8f0`).

Pre-computed light variants: `CYCLE_LIGHT` / `qk-cycle-light` (75% lightened, area fills), `CYCLE_BAR` / `qk-cycle-bar` (30% lightened, bar fills).

## Colorblind Palette

Okabe-Ito 8-color cycle (`CYCLE_CB` / `qk-cycle-cb`), safe for all color vision deficiencies:

| Name | Hex |
|------|-----|
| blue | `#0072B2` |
| vermillion | `#D55E00` |
| bluish green | `#009E73` |
| yellow | `#F0E442` |
| reddish purple | `#CC79A7` |
| sky blue | `#56B4E9` |
| orange | `#E69F00` |
| black | `#000000` |

## Colormaps

Three registered colormaps available after `use()`:

| Name | Type | Description |
|------|------|-------------|
| `qk_diverging` | LinearSegmented | Blue to white to red |
| `qk_sequential` | LinearSegmented | White to light blue to accent to navy |
| `qk_qualitative` | Listed | 8-color cycle as categorical map |

## Context Presets

| Preset | Base font | Figure size | Line width | Use case |
|--------|-----------|-------------|------------|----------|
| `"paper"` | 11pt | 8x5 | 2.0 | Journal figures, Typst docs |
| `"talk"` | 14pt | 12x7.5 | 2.5 | Slides, presentations |
| `"poster"` | 18pt | 16x10 | 3.0 | A0/A1 poster panels |

Presets are composable overlays: `plt.style.use(["qk", "qk-talk"])` applies the base style then overrides sizing for talks.

## Files

| File | Purpose |
|------|---------|
| `qk.mplstyle` | Matplotlib style sheet (also installed to `~/.matplotlib/stylelib/`) |
| `qk_style.py` | Python module: `use()`, colors, colormaps, `line_labels`, `lighten`, seaborn helpers |
| `qk_plotnine.py` | plotnine theme: `theme_qk`, `scale_color_qk`, `scale_fill_qk` |
| `qk-plot.typ` | Typst style library: colors, `qk-plot-style`, `qk-bar-style`, `qk-lilaq-theme` |
| `demo.py` | matplotlib/seaborn demo (8-panel showcase) |
| `demo_seaborn.py` | seaborn helpers demo (4 SVGs: violin, box, bar, pair) |
| `demo_plotnine.py` | plotnine demo (4 SVG plots) |
| `qk-plot-examples.typ` | cetz-plot + Lilaq demo (6 charts) |
