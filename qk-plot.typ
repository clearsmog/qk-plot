// qk-plot — Style library for cetz-plot and Lilaq charts (v3.0.0)
// Mirrors the Tailwind CSS 600-series palette from qk_style.py
// Usage: #import "qk-plot.typ": *

// ── Color palette ──

#let qk-accent = rgb("#2563eb")
#let qk-danger = rgb("#dc2626")
#let qk-success = rgb("#059669")
#let qk-warning = rgb("#d97706")
#let qk-purple = rgb("#7c3aed")
#let qk-teal = rgb("#0d9488")
#let qk-orange = rgb("#ea580c")
#let qk-rose = rgb("#e11d48")

// Semantic aliases
#let qk-heading = rgb("#1e3a8a")
#let qk-text = rgb("#0f172a")
#let qk-muted = rgb("#64748b")
#let qk-surface = rgb("#f8fafc")
#let qk-border = rgb("#e2e8f0")

// 8-color cycle for series assignment: qk-cycle.at(i)
#let qk-cycle = (qk-accent, qk-danger, qk-success, qk-warning, qk-purple, qk-teal, qk-orange, qk-rose)

// Pre-computed light variants
#let qk-cycle-light = qk-cycle.map(c => c.lighten(75%))  // area/fill backgrounds
#let qk-cycle-bar = qk-cycle.map(c => c.lighten(30%))    // bar fills

// Okabe-Ito colorblind-safe 8-color cycle (mirrors CYCLE_CB from qk_style.py)
#let qk-cycle-cb = (
  rgb("#0072B2"),  // blue
  rgb("#D55E00"),  // vermillion
  rgb("#009E73"),  // bluish green
  rgb("#F0E442"),  // yellow
  rgb("#CC79A7"),  // reddish purple
  rgb("#56B4E9"),  // sky blue
  rgb("#E69F00"),  // orange
  rgb("#000000"),  // black
)

// ── Typography constants (matching qk.mplstyle) ──

#let qk-font-family = ("Inter", "Helvetica Neue", "Arial")
#let qk-font-sizes = (
  base: 11pt,
  title: 14pt,
  label: 11.5pt,
  tick: 10.5pt,
  legend: 9.5pt,
  suptitle: 18pt,
)

// ── Stroke constants (matching qk.mplstyle) ──

#let qk-grid-stroke = 0.6pt + qk-border.transparentize(50%)
#let qk-spine-stroke = 0.8pt + qk-border
#let qk-line-width = 2pt

// ── cetz-plot style helpers ──

#let qk-plot-style(i) = {
  let c = qk-cycle.at(calc.rem(i, qk-cycle.len()))
  (stroke: c + qk-line-width, fill: qk-cycle-light.at(calc.rem(i, qk-cycle.len())))
}

#let qk-bar-style(i) = {
  let c = qk-cycle.at(calc.rem(i, qk-cycle.len()))
  (stroke: c + 0.75pt, fill: qk-cycle-bar.at(calc.rem(i, qk-cycle.len())))
}

// ── Lilaq theme ──
// Usage: #show: qk-lilaq-theme()
// Colorblind variant: #show: qk-lilaq-theme(colorblind: true)

#let qk-lilaq-theme(colorblind: false) = {
  import "@preview/lilaq:0.6.0" as lq
  let colors = if colorblind { qk-cycle-cb } else { qk-cycle }
  it => {
    show: lq.set-diagram(
      cycle: colors,
      xaxis: (subticks: none, mirror: false),
      yaxis: (subticks: none, mirror: false),
    )
    show: lq.set-spine(stroke: qk-spine-stroke)
    show: lq.set-grid(stroke: qk-grid-stroke)
    show: lq.set-tick(stroke: 0.7pt, inset: 0pt, outset: 2.5pt)
    show: lq.set-legend(pad: 0.4em, stroke: none, fill: white)
    // Typography via show rules on Lilaq element selectors
    show lq.selector(lq.tick-label): set text(size: qk-font-sizes.tick)
    show lq.selector(lq.label): set text(size: qk-font-sizes.label)
    show lq.selector(lq.title): set text(size: qk-font-sizes.title, weight: "bold", fill: qk-heading)
    it
  }
}
