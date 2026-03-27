// qk-plot-examples — cetz-plot and Lilaq charts using the qk style (v3.0.0)
#import "@preview/cetz:0.4.2"
#import "@preview/cetz-plot:0.1.3": plot, chart
#import "@preview/lilaq:0.6.0" as lq

#import "qk-plot.typ": *

#set text(font: qk-font-family, size: qk-font-sizes.base)
#set page(margin: 2cm)

= qk-plot Examples

== cetz-plot: Line Chart

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
      legend: "inner-north-east",
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
  caption: [Monthly revenue by product line (cetz-plot)],
)

#pagebreak()

== cetz-plot: Column Chart

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
  caption: [Quarterly active users (cetz-plot)],
)

#pagebreak()

== cetz-plot: Area Chart

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
      legend: "inner-north-east",
      plot-style: qk-plot-style,
      {
        plot.add(
          ((1, 12), (2, 18), (3, 15), (4, 22), (5, 19), (6, 25), (7, 28)),
          fill: true,
          label: [API v2],
        )
        plot.add(
          ((1, 5), (2, 8), (3, 10), (4, 7), (5, 12), (6, 14), (7, 11)),
          fill: true,
          label: [API v1],
        )
      },
    )
  }),
  caption: [Daily API request volume by version (cetz-plot)],
)

#pagebreak()

== Lilaq: Line Chart

#show: qk-lilaq-theme()

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    title: [Monthly Revenue],
    xlabel: [Month],
    ylabel: [Revenue (\$M)],
    ylim: (0, auto),
    lq.plot((1, 2, 3, 4, 5, 6), (45, 52, 48, 61, 58, 72), label: [Product A]),
    lq.plot((1, 2, 3, 4, 5, 6), (30, 35, 42, 38, 45, 51), label: [Product B]),
    lq.plot((1, 2, 3, 4, 5, 6), (22, 28, 31, 35, 40, 47), label: [Product C]),
  ),
  caption: [Monthly revenue by product line (Lilaq)],
)

#pagebreak()

== Lilaq: Bar Chart

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    title: [Quarterly Users],
    xlabel: [Quarter],
    ylabel: [Users (thousands)],
    ylim: (0, auto),
    lq.bar(
      (0, 1, 2, 3),
      (84, 112, 97, 135),
      label: [Active users],
    ),
  ),
  caption: [Quarterly active users (Lilaq)],
)

#pagebreak()

== Lilaq: Scatter (Colorblind-Safe)

#{
  show: qk-lilaq-theme(colorblind: true)

  import calc: cos, sin

  let n = 40
  let x1 = range(n).map(i => calc.cos(i * 0.3) * 2 + 3)
  let y1 = range(n).map(i => calc.sin(i * 0.3) * 2 + 4)
  let x2 = range(n).map(i => calc.cos(i * 0.3 + 1) * 1.5 + 6)
  let y2 = range(n).map(i => calc.sin(i * 0.3 + 1) * 1.5 + 3)

  figure(
    lq.diagram(
      width: 10cm,
      height: 6cm,
      title: [Feature Space (Okabe-Ito)],
      xlabel: [Feature 1],
      ylabel: [Feature 2],
      lq.scatter(x1, y1, label: [Cluster A]),
      lq.scatter(x2, y2, label: [Cluster B]),
    ),
    caption: [Scatter plot with colorblind-safe palette (Lilaq)],
  )
}
