// qk-plot — Palette constants for cetz-plot charts (v2.3.0)
// Mirrors the 8-color Tailwind 600-series cycle from qk_style.py
// Usage: #import "qk-plot.typ": *

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
#let qk-border = rgb("#e2e8f0")

// 8-color cycle for series assignment: cycle.at(i)
#let qk-cycle = (qk-accent, qk-danger, qk-success, qk-warning, qk-purple, qk-teal, qk-orange, qk-rose)

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
