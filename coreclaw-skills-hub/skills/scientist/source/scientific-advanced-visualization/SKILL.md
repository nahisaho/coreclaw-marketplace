---
name: scientific-advanced-visualization
description: |
 dataadvancedvisualizationskill。Plotly 3D 
 Altair visualizationSeaborn plot
 Parallel Coordinatespublicationfigure。
tu_tools:
 - key: biotools
 name: bio.tools
 description: advancedvisualizationtoolsearch
---

# Scientific Advanced Visualization

data's visualization3D 
publicationfigure is provided。

## When to Use

- 3D scatter plotplot and
- Plotly / Altair visualization is createdand
- amountdata Parallel Coordinates / Radar visualizationwhen needed
- paperfor's publication (Nature/Science style) figure is createdand
- time seriessimulationresults's is createdand
- multiple'sfigure is createdand

---

## Quick Start

## 1. Plotly 3D

```python
import numpy as np
import pandas as pd


def plotly_3d_scatter(df, x, y, z, color=None, size=None,
 title="3D Scatter Plot"):
 """
 Plotly 3D scatter plot。

 Parameters:
 df: pd.DataFrame — data
 x, y, z: str — axiscolumn
 color: str | None — mincolumn
 size: str | None — column
 title: str — title
 """
 import plotly.express as px

 fig = px.scatter_3d(df, x=x, y=y, z=z, color=color, size=size,
 title=title, opacity=0.7)
 fig.update_layout(
 scene=dict(
 xaxis_title=x, yaxis_title=y, zaxis_title=z),
 width=900, height=700)

 path = "3d_scatter.html"
 fig.write_html(path)
 print(f"3D Scatter: {len(df)} points → {path}")
 return fig


def plotly_surface(X_grid, Y_grid, Z_grid, title="Surface Plot"):
 """
 Plotly 3D plot。

 Parameters:
 X_grid, Y_grid, Z_grid: np.ndarray — grid
 title: str — title
 """
 import plotly.graph_objects as go

 fig = go.Figure(data=[go.Surface(x=X_grid, y=Y_grid, z=Z_grid,
 colorscale="Viridis")])
 fig.update_layout(
 title=title,
 scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
 width=900, height=700)

 path = "surface_plot.html"
 fig.write_html(path)
 print(f"Surface: {Z_grid.shape} grid → {path}")
 return fig
```

## 2. Altair visualization

```python
def altair_faceted_chart(df, x, y, color, facet_col=None,
 chart_type="scatter"):
 """
 Altair chart。

 Parameters:
 df: pd.DataFrame — data
 x, y: str — axiscolumn
 color: str — mincolumn
 facet_col: str | None — column
 chart_type: str — "scatter" / "line" / "bar" / "box"
 """
 import altair as alt

 base = alt.Chart(df).encode(
 x=alt.X(x, scale=alt.Scale(zero=False)),
 y=alt.Y(y, scale=alt.Scale(zero=False)),
 color=color)

 if chart_type == "scatter":
 chart = base.mark_circle(size=60, opacity=0.7)
 elif chart_type == "line":
 chart = base.mark_line
 elif chart_type == "bar":
 chart = base.mark_bar
 elif chart_type == "box":
 chart = base.mark_boxplot
 else:
 chart = base.mark_circle

 if facet_col:
 chart = chart.facet(facet_col, columns=3)

 chart = chart.properties(width=300, height=250).interactive

 path = "altair_chart.html"
 chart.save(path)
 print(f"Altair {chart_type}: {len(df)} rows → {path}")
 return chart
```

## 3. amountvisualization

```python
def parallel_coordinates_plot(df, class_col, features=None,
 title="Parallel Coordinates"):
 """
 Parallel Coordinates plot。

 Parameters:
 df: pd.DataFrame — data
 class_col: str — classificationcolumn
 features: list[str] | None — tablefeatures (None allnumber/countvalue)
 title: str — title
 """
 import plotly.express as px

 if features is None:
 features = df.select_dtypes(include=[np.number]).columns.tolist
 if class_col in features:
 features.remove(class_col)

 fig = px.parallel_coordinates(
 df, color=class_col, dimensions=features,
 title=title, color_continuous_scale=px.colors.diverging.Tealrose)

 fig.update_layout(width=1000, height=500)

 path = "parallel_coordinates.html"
 fig.write_html(path)
 print(f"Parallel Coordinates: {len(features)} dims → {path}")
 return fig


def radar_chart(categories, values_dict, title="Radar Chart"):
 """
 Radar (Spider) chart — multipleloopcomparison。

 Parameters:
 categories: list[str] — axislabel
 values_dict: dict[str, list[float]] — {loop: value}
 title: str — title
 """
 import plotly.graph_objects as go

 fig = go.Figure

 for name, vals in values_dict.items:
 fig.add_trace(go.Scatterpolar(
 r=vals + [vals[0]],
 theta=categories + [categories[0]],
 fill="toself", name=name, opacity=0.6))

 fig.update_layout(
 polar=dict(radialaxis=dict(visible=True)),
 title=title, width=600, height=500)

 path = "radar_chart.html"
 fig.write_html(path)
 print(f"Radar: {len(values_dict)} groups × {len(categories)} axes → {path}")
 return fig
```

## 4. publicationfigure (Nature/Science style)

```python
def publication_figure(plot_func, figsize=(3.5, 2.8),
 dpi=300, style="nature",
 output="publication_fig.pdf"):
 """
 publication (Nature/Science style) figuregeneration。

 Parameters:
 plot_func: callable — matplotlib drawing/plottingnumber/count (ax argument)
 figsize: tuple — figure (, Nature 1 col = 3.5in)
 dpi: int — degree
 style: str — "nature" / "science" / "acs"
 output: str — output path (.pdf /.svg /.png)
 """
 import matplotlib.pyplot as plt
 import matplotlib as mpl

 # Nature/Science settings
 style_params = {
 "nature": {
 "font.family": "Arial",
 "font.size": 7,
 "axes.linewidth": 0.5,
 "xtick.major.width": 0.5,
 "ytick.major.width": 0.5,
 "lines.linewidth": 1.0,
 "lines.markersize": 3,
 },
 "science": {
 "font.family": "Helvetica",
 "font.size": 8,
 "axes.linewidth": 0.6,
 "xtick.major.width": 0.6,
 "ytick.major.width": 0.6,
 "lines.linewidth": 1.2,
 "lines.markersize": 4,
 },
 "acs": {
 "font.family": "Arial",
 "font.size": 9,
 "axes.linewidth": 0.5,
 "xtick.major.width": 0.5,
 "ytick.major.width": 0.5,
 "lines.linewidth": 1.0,
 "lines.markersize": 4,
 }
 }

 with mpl.rc_context(style_params.get(style, style_params["nature"])):
 fig, ax = plt.subplots(figsize=figsize)
 plot_func(ax)
 ax.spines["top"].set_visible(False)
 ax.spines["right"].set_visible(False)
 plt.tight_layout
 fig.savefig(output, dpi=dpi, bbox_inches="tight")
 plt.close

 print(f"Publication figure ({style}): {figsize} @ {dpi}dpi → {output}")
 return output
```

## 5. 

```python
def create_animation(data_frames, x_col, y_col, time_col,
 title="Animation", fps=10):
 """
 Plotly 。

 Parameters:
 data_frames: pd.DataFrame — timeincludingdata
 x_col, y_col: str — axiscolumn
 time_col: str — time / column
 title: str — title
 fps: int — 
 """
 import plotly.express as px

 fig = px.scatter(data_frames, x=x_col, y=y_col,
 animation_frame=time_col,
 title=title, opacity=0.7,
 range_x=[data_frames[x_col].min * 0.9,
 data_frames[x_col].max * 1.1],
 range_y=[data_frames[y_col].min * 0.9,
 data_frames[y_col].max * 1.1])

 fig.update_layout(
 width=800, height=600,
 updatemenus=[dict(type="buttons",
 buttons=[dict(label="▶ Play",
 method="animate",
 args=[None, {"frame": {"duration": 1000 // fps}}])])])

 path = "animation.html"
 fig.write_html(path)
 print(f"Animation: {data_frames[time_col].nunique} frames @ {fps}fps → {path}")
 return fig
```

---

## Pipeline Integration

```
eda-correlation → advanced-visualization → presentation-design
 (search/explorationanalysis) (advancedvisualization) (presentation)
 │ │ ↓
 pca-tsne ───────────────┘ interactive-dashboard
 (dimensionality reduction) (dashboard)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `3d_scatter.html` | 3D scatter plot | → dashboard |
| `publication_fig.pdf` | publicationfigure | → presentation |
| `parallel_coordinates.html` | amountvisualization | → reporting |
| `animation.html` | | → presentation |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | advancedvisualizationtoolsearch |
