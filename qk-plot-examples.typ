// qk-plot-examples — Three cetz-plot charts using the qk palette
#import "@preview/cetz:0.4.2"
#import "@preview/cetz-plot:0.1.3": plot, chart

#import "qk-plot.typ": *

#set text(font: "Inter", size: 10.5pt)
#set page(margin: 2cm)

// Palette function for plot-style: returns stroke + fill per series index
#let qk-plot-style(i) = {
  let c = qk-cycle.at(calc.rem(i, qk-cycle.len()))
  (stroke: c + 2pt, fill: c.lighten(75%))
}

// Palette function for bar-style: returns stroke + fill per bar index
#let qk-bar-style(i) = {
  let c = qk-cycle.at(calc.rem(i, qk-cycle.len()))
  (stroke: c + 0.75pt, fill: c.lighten(30%))
}

= qk-plot Examples

== Line Chart

#figure(
  cetz.canvas({
    import cetz.draw: *

    plot.plot(
      size: (10, 6),
      x-label: [Month],
      y-label: [Revenue (\$M)],
      x-tick-step: 1,
      y-tick-step: 10,
      y-min: 0,
      y-grid: true,
      legend: auto,
      plot-style: qk-plot-style,
      {
        plot.add(
          ((1, 45), (2, 52), (3, 48), (4, 61), (5, 58), (6, 72)),
          label: [Product A],
        )
        plot.add(
          ((1, 30), (2, 35), (3, 42), (4, 38), (5, 45), (6, 51)),
          label: [Product B],
        )
        plot.add(
          ((1, 22), (2, 28), (3, 31), (4, 35), (5, 40), (6, 47)),
          label: [Product C],
        )
      },
    )
  }),
  caption: [Monthly revenue by product line],
)

#pagebreak()

== Column Chart

#figure(
  cetz.canvas({
    import cetz.draw: *

    chart.columnchart(
      size: (10, 6),
      y-label: [Users (thousands)],
      x-label: [Quarter],
      bar-style: qk-bar-style,
      (
        ([Q1], 84),
        ([Q2], 112),
        ([Q3], 97),
        ([Q4], 135),
      ),
    )
  }),
  caption: [Quarterly active users],
)

#pagebreak()

== Area Chart (fill-between)

#figure(
  cetz.canvas({
    import cetz.draw: *

    plot.plot(
      size: (10, 6),
      x-label: [Day],
      y-label: [Requests (k)],
      x-tick-step: 1,
      y-tick-step: 5,
      y-min: 0,
      y-grid: true,
      legend: auto,
      plot-style: qk-plot-style,
      {
        // Area series 1: filled line
        plot.add(
          ((1, 12), (2, 18), (3, 15), (4, 22), (5, 19), (6, 25), (7, 28)),
          fill: true,
          label: [API v2],
        )
        // Area series 2: filled line
        plot.add(
          ((1, 5), (2, 8), (3, 10), (4, 7), (5, 12), (6, 14), (7, 11)),
          fill: true,
          label: [API v1],
        )
      },
    )
  }),
  caption: [Daily API request volume by version],
)
