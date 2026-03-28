---
name: scientific-interactive-dashboard
description: |
 Interactive dashboard skill. Streamlit/Plotly Dash scientific dashboard creation, real-time data visualization, parameter exploration interfaces, and research result presentation.
tu_tools:
 - key: biotools
 name: bio.tools
 description: visualizationtoolsearch
---

# Scientific Interactive Dashboard

data's dashboard construction、
parameterssearch/explorationresultsanalysis.

## When to Use

- Streamlit datasearch/explorationdashboard is builtand
- Dash 's highanalysis UI is createdand
- Panel / Voilà Jupyter dashboardwhen needed
- parameters + 's UI implementationwhen needed
- multiple analysisresultswhen needed
- loganalysistool is providedand

---

## Quick Start

## 1. Streamlit datadashboard

```python
def generate_streamlit_dashboard(output_path="dashboard_app.py"):
 """
 Streamlit dashboardtemplategeneration。

 Parameters:
 output_path: str — output Python file
 """
 code = '''
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title="Scientific Data Dashboard",
 layout="wide", page_icon="🔬")

st.title("🔬 Scientific Data Dashboard")

# --- : data & parameters ---
st.sidebar.header("Settings")

uploaded_file = st.sidebar.file_uploader(
 "Upload CSV / Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
 if uploaded_file.name.endswith(".csv"):
 df = pd.read_csv(uploaded_file)
 else:
 df = pd.read_excel(uploaded_file)
else:
 # data
 np.random.seed(42)
 n = 500
 df = pd.DataFrame({
 "x": np.random.randn(n),
 "y": np.random.randn(n),
 "z": np.random.randn(n),
 "category": np.random.choice(["A", "B", "C"], n),
 "value": np.random.exponential(2, n)
 })
 st.sidebar.info("Demo data loaded (upload your own CSV)")

# --- dataoverview ---
col1, col2, col3 = st.columns(3)
col1.metric("Rows", len(df))
col2.metric("Columns", len(df.columns))
col3.metric("Missing", int(df.isnull.sum.sum))

# --- ---
tab1, tab2, tab3, tab4 = st.tabs(
 ["📊 Explorer", "📈 Distribution", "🔗 Correlation", "📋 Data"])

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist
cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist

with tab1:
 st.subheader("Interactive Explorer")
 c1, c2 = st.columns(2)
 x_col = c1.selectbox("X axis", numeric_cols, index=0)
 y_col = c2.selectbox("Y axis", numeric_cols,
 index=min(1, len(numeric_cols)-1))
 color_col = st.selectbox("Color", [None] + cat_cols + numeric_cols)

 fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
 opacity=0.7, title=f"{x_col} vs {y_col}")
 st.plotly_chart(fig, use_container_width=True)

with tab2:
 st.subheader("Distribution Analysis")
 dist_col = st.selectbox("Column", numeric_cols, key="dist")
 n_bins = st.slider("Bins", 10, 100, 30)
 fig2 = px.histogram(df, x=dist_col, nbins=n_bins,
 marginal="box", title=f"Distribution: {dist_col}")
 st.plotly_chart(fig2, use_container_width=True)

with tab3:
 st.subheader("Correlation Matrix")
 corr = df[numeric_cols].corr
 fig3 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
 title="Correlation Heatmap")
 st.plotly_chart(fig3, use_container_width=True)

with tab4:
 st.subheader("Raw Data")
 st.dataframe(df, use_container_width=True)
 csv = df.to_csv(index=False)
 st.download_button("Download CSV", csv, "data.csv", "text/csv")
'''

 with open(output_path, "w") as f:
 f.write(code)

 print(f"Streamlit dashboard → {output_path}")
 print(f" Run: streamlit run {output_path}")
 return output_path
```

## 2. Dash dashboard

```python
def generate_dash_dashboard(output_path="dash_app.py"):
 """
 Dash dashboardtemplategeneration。

 Parameters:
 output_path: str — output Python file
 """
 code = '''
from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import numpy as np
import plotly.express as px

app = Dash(__name__)

# data
np.random.seed(42)
n = 500
df = pd.DataFrame({
 "x": np.random.randn(n),
 "y": np.random.randn(n),
 "z": np.random.randn(n),
 "group": np.random.choice(["Control", "Treatment A", "Treatment B"], n),
 "response": np.random.exponential(2, n)
})

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist

app.layout = html.Div([
 html.H1("Scientific Data Dashboard", style={"textAlign": "center"}),

 html.Div([
 html.Div([
 html.Label("X Axis"),
 dcc.Dropdown(id="x-col", options=numeric_cols,
 value=numeric_cols[0])
 ], style={"width": "30%", "display": "inline-block"}),
 html.Div([
 html.Label("Y Axis"),
 dcc.Dropdown(id="y-col", options=numeric_cols,
 value=numeric_cols[1])
 ], style={"width": "30%", "display": "inline-block"}),
 html.Div([
 html.Label("Color"),
 dcc.Dropdown(id="color-col",
 options=df.columns.tolist,
 value="group")
 ], style={"width": "30%", "display": "inline-block"}),
 ], style={"padding": "20px"}),

 html.Div([
 html.Div([dcc.Graph(id="scatter-plot")],
 style={"width": "50%", "display": "inline-block"}),
 html.Div([dcc.Graph(id="histogram")],
 style={"width": "50%", "display": "inline-block"}),
 ]),

 html.Div([
 html.H3("Summary Statistics"),
 dash_table.DataTable(
 id="summary-table",
 columns=[{"name": c, "id": c}
 for c in ["stat"] + numeric_cols],
 style_table={"overflowX": "auto"})
 ], style={"padding": "20px"})
])

@app.callback(
 [Output("scatter-plot", "figure"),
 Output("histogram", "figure"),
 Output("summary-table", "data")],
 [Input("x-col", "value"),
 Input("y-col", "value"),
 Input("color-col", "value")]
)
def update_plots(x_col, y_col, color_col):
 fig1 = px.scatter(df, x=x_col, y=y_col, color=color_col,
 opacity=0.7, title=f"{x_col} vs {y_col}")
 fig2 = px.histogram(df, x=x_col, color=color_col,
 marginal="box", barmode="overlay", opacity=0.7)
 stats = df[numeric_cols].describe.reset_index
 stats.columns = ["stat"] + numeric_cols
 return fig1, fig2, stats.to_dict("records")

if __name__ == "__main__":
 app.run(debug=True, port=8050)
'''

 with open(output_path, "w") as f:
 f.write(code)

 print(f"Dash dashboard → {output_path}")
 print(f" Run: python {output_path}")
 return output_path
```

## 3. Panel dashboard

```python
def generate_panel_dashboard(output_path="panel_app.py"):
 """
 Panel dashboardtemplategeneration。

 Parameters:
 output_path: str — output Python file
 """
 code = '''
import panel as pn
import pandas as pd
import numpy as np
import plotly.express as px

pn.extension("plotly")

# data
np.random.seed(42)
n = 500
df = pd.DataFrame({
 "x": np.random.randn(n),
 "y": np.random.randn(n),
 "z": np.random.randn(n),
 "group": np.random.choice(["A", "B", "C"], n),
 "value": np.random.exponential(2, n)
})

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist

# 
x_select = pn.widgets.Select(name="X Axis", options=numeric_cols, value="x")
y_select = pn.widgets.Select(name="Y Axis", options=numeric_cols, value="y")
n_bins = pn.widgets.IntSlider(name="Histogram Bins", start=10, end=100, value=30)


@pn.depends(x_select, y_select)
def scatter_plot(x_col, y_col):
 fig = px.scatter(df, x=x_col, y=y_col, color="group",
 opacity=0.7, title=f"{x_col} vs {y_col}")
 return fig


@pn.depends(x_select, n_bins)
def hist_plot(x_col, bins):
 fig = px.histogram(df, x=x_col, nbins=bins, color="group",
 barmode="overlay", opacity=0.7)
 return fig


dashboard = pn.template.FastListTemplate(
 title="Scientific Data Dashboard",
 sidebar=[x_select, y_select, n_bins],
 main=[
 pn.Row(pn.pane.Plotly(scatter_plot, sizing_mode="stretch_width"),
 pn.pane.Plotly(hist_plot, sizing_mode="stretch_width")),
 pn.pane.DataFrame(df.describe.T, sizing_mode="stretch_width")
 ]
)

dashboard.servable
'''

 with open(output_path, "w") as f:
 f.write(code)

 print(f"Panel dashboard → {output_path}")
 print(f" Run: panel serve {output_path}")
 return output_path
```

## 4. dashboardcomparison

```python
def compare_dashboard_frameworks:
 """
 Streamlit / Dash / Panel / Voilà comparisontable output。
 """
 comparison = pd.DataFrame({
 "Framework": ["Streamlit", "Dash", "Panel", "Voilà"],
 "Ease_of_Use": ["★★★★★", "★★★☆☆", "★★★★☆", "★★★★★"],
 "Customization": ["★★★☆☆", "★★★★★", "★★★★☆", "★★☆☆☆"],
 "Interactivity": ["★★★★☆", "★★★★★", "★★★★★", "★★★☆☆"],
 "Performance": ["★★★☆☆", "★★★★★", "★★★★☆", "★★★☆☆"],
 "Deployment": ["Streamlit Cloud", "Heroku/AWS", "Any ASGI", "Binder/Hub"],
 "Best_For": [
 "Rapid prototyping, data exploration",
 "Production apps, complex callbacks",
 "Jupyter integration, scientific viz",
 "Notebook → dashboard conversion"
 ]
 })

 print("=== Dashboard Framework Comparison ===")
 print(comparison.to_string(index=False))
 return comparison
```

---

## Pipeline Integration

```
advanced-visualization → interactive-dashboard → presentation-design
 (advancedvisualization) (dashboard) 
 │ │ ↓
 missing-data-analysis ────────┘ scientific-schematics
 (valueanalysis) (figureformula)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `dashboard_app.py` | Streamlit dashboard | → deployment |
| `dash_app.py` | Dash dashboard | → deployment |
| `panel_app.py` | Panel dashboard | → deployment |
| `framework_comparison.csv` | frameworkcomparison | → selection |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | visualizationtoolsearch |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Visualization)

Before execution, define:
- [ ] **Target audience**: journal / conference / dashboard / internal
- [ ] **Figure dimensions**: width x height, DPI requirement
- [ ] **Color scheme**: colorblind-safe palette confirmed
- [ ] **Data-ink ratio**: minimize non-data elements

#### Pass Criteria
- All figures saved to disk (never plt.show())
- Figures embedded in report.md with captions
- Text is English-only, font size >= 8pt
- Accessibility: contrast ratio >= 4.5:1
- Vector format (SVG/PDF) provided when requested
### Verification Loop

```
Phase 1: PLAN
  |-- Define eval criteria (above checklist)
  |-- Confirm input data availability and format
  |-- Select analysis methods with justification
  +-- Estimate resource requirements (time, memory, API calls)

Phase 2: EXECUTE
  |-- Run analysis pipeline step-by-step
  |-- Save intermediate results after each major step
  |-- Log execution time per step
  +-- Capture warnings/errors without stopping

Phase 3: VERIFY
  |-- Check all Pass Criteria (above)
  |-- Validate output file existence and non-empty
  |-- Cross-check numeric results for sanity (ranges, signs, units)
  |-- Verify figures are readable and correctly labeled
  +-- Run regression check: did existing outputs break?

Phase 4: RECOVER (on failure)
  |-- Identify failed phase and root cause
  |-- Isolate minimum reproducer
  |-- Apply fix and re-run only failed phase
  |-- Log fix as reusable pattern
  +-- If unrecoverable: document limitation and partial results

Phase 5: REPORT
  |-- Generate report.md with all sections
  |-- Embed all figures with captions
  |-- Save numeric results as JSON/CSV
  |-- List all generated files
  +-- Record execution metadata (duration, versions, seed)
```

### Quality Gates

| Gate | Check | Required |
|------|-------|----------|
| G1 | All figures saved to `figures/` (not `plt.show()`) | MUST |
| G2 | All figures embedded in `report.md` | MUST |
| G3 | Numeric results saved as JSON/CSV in `results/` | MUST |
| G4 | Report includes methods, results, discussion | MUST |
| G5 | All figure/table text is English-only | MUST |
| G6 | No hardcoded paths (use `Path` / config) | MUST |
| G7 | Random seed set and documented | MUST |
| G8 | Execution time logged | RECOMMENDED |
| G9 | Input validation performed | RECOMMENDED |
| G10 | Error messages are actionable | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | Data formatting, file I/O, unit conversion |
| Implementation | `standard` (sonnet-class) | Analysis code, pipeline execution, plotting |
| Reasoning | `premium` (opus-class) | Hypothesis generation, result interpretation, review |

### Sub-Agent Orchestration

When the task is complex, split into parallel sub-agents:

```
Orchestrator (this skill)
|-- Agent 1: Data preparation and validation
|-- Agent 2: Core analysis / computation
|-- Agent 3: Visualization and figure generation
+-- Agent 4: Report writing and quality check
```

Each sub-agent receives:
- Specific scope (what to do)
- Input specification (what data to use)
- Output specification (what files to produce)
- Quality gate subset (which gates to check)

### Token Optimization

- Load only the sub-skill needed for the current task
- Compact context after each major phase (discard intermediate logs)
- Use structured output (JSON) over prose for intermediate results
- Prefer code templates over natural language descriptions
- Cache expensive computations (API calls, model training)

### Error Recovery Protocol

```python
def execute_with_recovery(pipeline_steps, max_retries=2):
    results = {}
    for step in pipeline_steps:
        for attempt in range(max_retries + 1):
            try:
                results[step.name] = step.execute()
                break
            except Exception as e:
                if attempt < max_retries:
                    log(f"Step '{step.name}' failed (attempt {attempt+1}): {e}")
                    step.adjust_params()  # reduce batch size, increase timeout
                else:
                    log(f"Step '{step.name}' unrecoverable: {e}")
                    results[step.name] = {"status": "failed", "error": str(e)}
    return results
```
