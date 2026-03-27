# qk-plot (v3.0.0)

Unified plotting theme: matplotlib, seaborn, plotnine, cetz-plot, Lilaq.

## File Relationships

```
qk.mplstyle          <-- source of truth for rcParams
    |
qk_style.py          <-- Python API wrapping mplstyle + seaborn + colormaps
    |
qk_plotnine.py       <-- plotnine theme mirroring qk_style
    |
qk-plot.typ          <-- Typst colors + cetz-plot helpers + Lilaq theme
```

## Color Sync Protocol

Changes to colors MUST propagate to ALL 4 files:
1. `qk.mplstyle` — `axes.prop_cycle`
2. `qk_style.py` — `QK_COLORS`, `CYCLE`, `CYCLE_LIGHT`, `CYCLE_BAR`
3. `qk_plotnine.py` — `CYCLE`
4. `qk-plot.typ` — `qk-cycle`, individual `qk-*` color lets, `qk-cycle-light`, `qk-cycle-bar`

## Version Management

Version string appears in header comments of all 4 code files, `demo.py` suptitle, and `README.md` title. Bump all simultaneously.

## Key Constraints

- `svg.fonttype: path` MUST remain set (Typst SVG rendering)
- `savefig.pad_inches >= 0.3` (prevent edge clipping)
- Inter font is primary; fallback chain: Inter, Helvetica Neue, Arial, DejaVu Sans
- Minimum 8pt for any text element in any context
- Okabe-Ito colorblind palette (`CYCLE_CB`) is frozen — do not modify

## Verification

After any change:
1. `python demo.py` — check demo.svg/demo.png render correctly
2. `python demo_seaborn.py` — check 4 SVGs render correctly
3. `python demo_plotnine.py` — check 4 SVGs render correctly
4. `typst compile qk-plot-examples.typ` — check cetz-plot + Lilaq charts
5. `grep -r "vX.Y.Z"` — verify version strings are consistent

## Seaborn Helpers (8 total)

`heatmap_kws`, `violin_kws`, `strip_kws`, `boxplot_kws`, `barplot_kws`, `catplot_kws`, `pairplot_kws`, `jointplot_kws` — all return `dict`, pass as `**kwargs`.

For per-bar colors: `sns.barplot(df, hue="col", legend=False, **barplot_kws(palette=CYCLE_BAR[:n]))`.

## Typst Integration

- **Lilaq** (preferred): `#show: qk-lilaq-theme()` applies full qk styling
- **cetz-plot**: use `qk-plot-style` and `qk-bar-style` helpers
- SVGs from matplotlib/plotnine embed via `#image("chart.svg", width: 100%)`
- Typography constants: `qk-font-family`, `qk-font-sizes` dict
- Stroke constants: `qk-grid-stroke`, `qk-spine-stroke`, `qk-line-width`
