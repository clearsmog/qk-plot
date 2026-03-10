# qk Plotting Stack (v2.2.0)

Unified plotting theme across matplotlib, seaborn, plotnine, and cetz-plot — all sharing the Tailwind CSS 600-series palette.

## Quick Start

### matplotlib + seaborn
```python
from qk_style import use, QK_COLORS, CYCLE, heatmap_kws
use()              # paper context (default)
use("talk")        # slides / presentations
use("poster")      # A0/A1 posters

import seaborn as sns
sns.heatmap(data, **heatmap_kws(annot=True))
```

### plotnine (grammar of graphics)
```python
from qk_plotnine import theme_qk, scale_color_qk, scale_fill_qk
from plotnine import ggplot, aes, geom_point

(ggplot(df, aes("x", "y", color="group"))
 + geom_point() + theme_qk() + scale_color_qk())
```

### cetz-plot (Typst native)
```typst
#import "@preview/cetz:0.4.2"
#import "qk-plot.typ": *

// Use qk-cycle.at(0), qk-cycle.at(1), etc. for series colors
```

## Decision Framework

| Scenario | Tool | Why |
|----------|------|-----|
| < 3 series, < 20 pts, no computation | **cetz-plot** | Typst-native, font-matched |
| Faceted / layered grammar | **plotnine** | ggplot2-style composition |
| Statistical (violin, kde, heatmap) | **matplotlib + seaborn** | Full statistical toolkit |
| Complex (4+ series, annotations) | **matplotlib** | Full API control |

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

## Context Presets

| Preset | Base font | Figure size | Line width | Use case |
|--------|-----------|-------------|------------|----------|
| `"paper"` | 10.5pt | 8x5 | 2.0 | Journal figures, Typst docs |
| `"talk"` | 14pt | 12x7.5 | 2.5 | Slides, presentations |
| `"poster"` | 18pt | 16x10 | 3.0 | A0/A1 poster panels |

## Files

| File | Purpose |
|------|---------|
| `qk.mplstyle` | Matplotlib style sheet (also installed to `~/.matplotlib/stylelib/`) |
| `qk_style.py` | Python module: `use()`, `QK_COLORS`, `CYCLE`, seaborn helpers |
| `qk_plotnine.py` | plotnine theme: `theme_qk`, `scale_color_qk`, `scale_fill_qk` |
| `qk-plot.typ` | Typst palette constants for cetz-plot |
| `demo.py` | matplotlib/seaborn demo (6-panel showcase) |
| `demo_plotnine.py` | plotnine demo (4 SVG plots) |
| `qk-plot-examples.typ` | cetz-plot demo (3 native Typst charts) |
