---
name: scientific-geospatial-analysis
description: |
 Geospatial analysis skill. Spatial data processing with GeoPandas, coordinate transformations, spatial statistics, map visualization, and geospatial machine learning.
---

# Scientific Geospatial Analysis

data's preprocessingfigurevisualization
pipeline.

## When to Use

- GeoPandas data (Shapefile/GeoJSON) is processedand
- data (GeoTIFF) loadanalysiswhen needed
- correlation (Moran's I / LISA) testingwhen needed
- (Kriging) when needed
- Folium/Kepler.gl figure is createdand
- CRS (coordinatesreferencesystem) transformationbindingwhen needed

> **Note**: environment GIS (SoilGrids/WorldClim) `scientific-environmental-geodata` reference。

---

## Quick Start

## 1. GeoPandas data

```python
import numpy as np
import pandas as pd


def load_and_process_geodata(filepath, target_crs="EPSG:4326"):
 """
 GeoPandas /Loading dataCRS transformation。

 Parameters:
 filepath: str — Shapefile / GeoJSON / GPKG 
 target_crs: str — transformationcoordinatessystem
 """
 import geopandas as gpd

 gdf = gpd.read_file(filepath)
 original_crs = gdf.crs

 if gdf.crs != target_crs:
 gdf = gdf.to_crs(target_crs)

 # basic
 bounds = gdf.total_bounds # [minx, miny, maxx, maxy]
 geom_types = gdf.geometry.geom_type.value_counts.to_dict

 print(f"GeoData: {len(gdf)} features, CRS: {original_crs} → {target_crs}")
 print(f" Bounds: [{bounds[0]:.4f}, {bounds[1]:.4f}] "
 f"to [{bounds[2]:.4f}, {bounds[3]:.4f}]")
 print(f" Geometry types: {geom_types}")
 return gdf


def spatial_join(gdf_left, gdf_right, how="inner", predicate="intersects"):
 """
 binding (Spatial Join)。

 Parameters:
 gdf_left: GeoDataFrame — table
 gdf_right: GeoDataFrame — table
 how: str — "inner" / "left" / "right"
 predicate: str — "intersects" / "within" / "contains"
 """
 import geopandas as gpd

 if gdf_left.crs != gdf_right.crs:
 gdf_right = gdf_right.to_crs(gdf_left.crs)

 joined = gpd.sjoin(gdf_left, gdf_right, how=how, predicate=predicate)

 print(f"Spatial Join ({predicate}, {how}): "
 f"{len(gdf_left)} × {len(gdf_right)} → {len(joined)}")
 return joined
```

## 2. correlation (Moran's I / LISA)

```python
def spatial_autocorrelation(gdf, value_col, weight_type="queen"):
 """
 correlationtesting — Global Moran's I + LISA。

 Parameters:
 gdf: GeoDataFrame — + data
 value_col: str — analysiscolumn
 weight_type: str — "queen" / "rook" / "knn"
 """
 from libpysal.weights import Queen, Rook, KNN
 from esda.moran import Moran, Moran_Local
 import matplotlib.pyplot as plt

 # 
 if weight_type == "queen":
 w = Queen.from_dataframe(gdf)
 elif weight_type == "rook":
 w = Rook.from_dataframe(gdf)
 elif weight_type == "knn":
 w = KNN.from_dataframe(gdf, k=5)

 w.transform = "r"
 y = gdf[value_col].values

 # Global Moran's I
 moran_global = Moran(y, w)

 # LISA (Local Indicators of Spatial Association)
 moran_local = Moran_Local(y, w)

 gdf = gdf.copy
 gdf["lisa_cluster"] = moran_local.q # 1=HH, 2=LH, 3=LL, 4=HL
 gdf["lisa_significant"] = moran_local.p_sim < 0.05
 gdf["local_moran_i"] = moran_local.Is

 # visualization
 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

 gdf.plot(column=value_col, ax=ax1, legend=True,
 cmap="RdYlBu_r", edgecolor="gray", linewidth=0.3)
 ax1.set_title(f"{value_col} (Moran's I={moran_global.I:.4f}, "
 f"p={moran_global.p_sim:.4f})")

 cluster_labels = {1: "High-High", 2: "Low-High",
 3: "Low-Low", 4: "High-Low", 0: "Not Significant"}
 sig_gdf = gdf[gdf["lisa_significant"]]
 if len(sig_gdf) > 0:
 sig_gdf.plot(column="lisa_cluster", ax=ax2,
 categorical=True, legend=True,
 edgecolor="gray", linewidth=0.3)
 ax2.set_title("LISA Clusters (p < 0.05)")

 plt.tight_layout
 path = "spatial_autocorrelation.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 print(f"Moran's I = {moran_global.I:.4f}, p = {moran_global.p_sim:.4f}")
 print(f"LISA: {gdf['lisa_significant'].sum} significant clusters")
 return {"moran_i": moran_global.I, "p_value": moran_global.p_sim,
 "gdf": gdf, "fig": path}
```

## 3. 

```python
def kriging_interpolation(points_df, x_col, y_col, value_col,
 grid_resolution=100,
 variogram_model="spherical"):
 """
 Ordinary Kriging 。

 Parameters:
 points_df: pd.DataFrame — pointdata
 x_col, y_col: str — coordinatescolumn
 value_col: str — column
 grid_resolution: int — griddegree
 variogram_model: str — "spherical" / "exponential" / "gaussian"
 """
 from pykrige.ok import OrdinaryKriging
 import matplotlib.pyplot as plt

 x = points_df[x_col].values
 y = points_df[y_col].values
 z = points_df[value_col].values

 ok = OrdinaryKriging(
 x, y, z,
 variogram_model=variogram_model,
 verbose=False, enable_plotting=False)

 grid_x = np.linspace(x.min, x.max, grid_resolution)
 grid_y = np.linspace(y.min, y.max, grid_resolution)
 z_pred, ss_pred = ok.execute("grid", grid_x, grid_y)

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

 im1 = ax1.imshow(z_pred, origin="lower",
 extent=[x.min, x.max, y.min, y.max],
 cmap="viridis")
 ax1.scatter(x, y, c="red", s=10, edgecolors="black", linewidths=0.5)
 ax1.set_title(f"Kriging Prediction ({variogram_model})")
 plt.colorbar(im1, ax=ax1)

 im2 = ax2.imshow(ss_pred, origin="lower",
 extent=[x.min, x.max, y.min, y.max],
 cmap="Reds")
 ax2.set_title("Kriging Variance (Uncertainty)")
 plt.colorbar(im2, ax=ax2)

 plt.tight_layout
 path = "kriging_result.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 print(f"Kriging ({variogram_model}): {grid_resolution}×{grid_resolution} grid, "
 f"{len(x)} observation points")
 return {"z_pred": z_pred, "variance": ss_pred,
 "grid_x": grid_x, "grid_y": grid_y, "fig": path}
```

## 4. Folium figure

```python
def interactive_map(gdf, value_col=None, popup_cols=None,
 tiles="CartoDB positron",
 output="interactive_map.html"):
 """
 Folium figure。

 Parameters:
 gdf: GeoDataFrame — data
 value_col: str | None — Choropleth column
 popup_cols: list[str] | None — tablecolumn
 tiles: str — 
 output: str — output HTML
 """
 import folium

 center = [gdf.geometry.centroid.y.mean,
 gdf.geometry.centroid.x.mean]
 m = folium.Map(location=center, zoom_start=8, tiles=tiles)

 if value_col and gdf.geometry.geom_type.iloc[0] in ["Polygon", "MultiPolygon"]:
 folium.Choropleth(
 geo_data=gdf.__geo_interface__,
 data=gdf, columns=[gdf.index.name or "index", value_col],
 key_on="feature.id",
 fill_color="YlOrRd",
 legend_name=value_col
 ).add_to(m)
 else:
 for _, row in gdf.iterrows:
 popup_text = ""
 if popup_cols:
 popup_text = "<br>".join(
 [f"<b>{c}</b>: {row[c]}" for c in popup_cols])
 folium.CircleMarker(
 location=[row.geometry.centroid.y, row.geometry.centroid.x],
 radius=5, popup=popup_text,
 color="blue", fill=True
 ).add_to(m)

 m.save(output)
 print(f"Interactive map → {output} ({len(gdf)} features)")
 return output
```

---

## Pipeline Integration

```
environmental-geodata → geospatial-analysis → advanced-visualization
 (environmentData Retrieval) (analysis) (advancedvisualization)
 │ │ ↓
 epidemiology ───────────────┘ interactive-dashboard
  (dashboard)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `spatial_autocorrelation.png` | Moran's I + LISA | → reporting |
| `kriging_result.png` | | → visualization |
| `interactive_map.html` | Folium figure | → dashboard |

## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    """Generic REST API data retrieval with error handling."""
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
