---
name: scientific-environmental-geodata
description: |
 environmentdataskill。SoilGrids REST API by/via
 retrieval、WorldClim/CHELSA data、-environment
 integration。 REST API integration (TU )。
tu_tools: []
---

# Scientific Environmental Geodata

SoilGridsWorldClim 's/environmentdata API utilizing
ecologyenvironmentpipeline is provided。

## When to Use

- (pH, SOC, amount) is retrievedand
- bioclimatic variables (BIO1-BIO19) is retrievedand
- typedistribution (SDM) 's environmentnumber/countwhen needed
- 's is evaluatedand
- environment is performedand
- --'s interactionanalysiswhen needed

---

## Quick Start

## 1. SoilGrids retrieval

```python
import requests
import pandas as pd
import numpy as np

SOILGRIDS_BASE = "https://rest.isric.org/soilgrids/v2.0"


def soilgrids_get_properties(lat, lon, properties=None,
 depths=None, values=None):
 """
 SoilGrids — point'sretrieval。

 Parameters:
 lat: float — latitude
 lon: float — longitude
 properties: list[str] — (example: ["phh2o", "soc", "clay"])
 depths: list[str] — degree (example: ["0-5cm", "5-15cm"])
 values: list[str] — value's type (example: ["mean", "Q0.05", "Q0.95"])
 """
 if properties is None:
 properties = ["phh2o", "soc", "clay", "sand", "nitrogen",
 "bdod", "cec", "ocd"]
 if depths is None:
 depths = ["0-5cm", "5-15cm", "15-30cm", "30-60cm"]
 if values is None:
 values = ["mean", "Q0.05", "Q0.95"]

 url = f"{SOILGRIDS_BASE}/properties/query"
 params = {
 "lat": lat,
 "lon": lon,
 "property": properties,
 "depth": depths,
 "value": values,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for layer in data.get("properties", {}).get("layers", []):
 prop_name = layer.get("name", "")
 unit = layer.get("unit_measure", {})
 conversion = unit.get("mapped_units", "")
 for depth_info in layer.get("depths", []):
 row = {
 "property": prop_name,
 "depth": depth_info.get("label", ""),
 "unit": conversion,
 }
 for val_key, val_val in depth_info.get("values", {}).items:
 row[val_key] = val_val
 results.append(row)

 df = pd.DataFrame(results)
 print(f"SoilGrids ({lat}, {lon}): {len(df)} records, "
 f"{len(properties)} properties")
 return df
```

## 2. WorldClim bioclimatic variables

```python
import rasterio
from rasterio.sample import sample_gen


def worldclim_get_bioclim(lat, lon, resolution="2.5m",
 data_dir="worldclim"):
 """
 WorldClim — bioclimatic variablesretrieval。

 Parameters:
 lat: float — latitude
 lon: float — longitude
 resolution: str — degree ("30s", "2.5m", "5m", "10m")
 data_dir: str — WorldClim datadirectory
 """
 from pathlib import Path
 bio_dir = Path(data_dir) / f"wc2.1_{resolution}_bio"

 bioclim_names = {
 1: "Annual Mean Temperature",
 2: "Mean Diurnal Range",
 3: "Isothermality",
 4: "Temperature Seasonality",
 5: "Max Temperature Warmest Month",
 6: "Min Temperature Coldest Month",
 7: "Temperature Annual Range",
 8: "Mean Temperature Wettest Quarter",
 9: "Mean Temperature Driest Quarter",
 10: "Mean Temperature Warmest Quarter",
 11: "Mean Temperature Coldest Quarter",
 12: "Annual Precipitation",
 13: "Precipitation Wettest Month",
 14: "Precipitation Driest Month",
 15: "Precipitation Seasonality",
 16: "Precipitation Wettest Quarter",
 17: "Precipitation Driest Quarter",
 18: "Precipitation Warmest Quarter",
 19: "Precipitation Coldest Quarter",
 }

 results = []
 for bio_num, bio_name in bioclim_names.items:
 tif_path = bio_dir / f"wc2.1_{resolution}_bio_{bio_num}.tif"
 if not tif_path.exists:
 continue
 with rasterio.open(tif_path) as src:
 vals = list(sample_gen(src, [(lon, lat)]))
 value = vals[0][0] if vals else None
 results.append({
 "variable": f"BIO{bio_num}",
 "name": bio_name,
 "value": value,
 })

 df = pd.DataFrame(results)
 print(f"WorldClim ({lat}, {lon}): {len(df)} bioclim variables")
 return df
```

## 3. typedistributionenvironmentnumber/countintegration

```python
def sdm_environmental_stack(occurrences_df, lat_col="latitude",
 lon_col="longitude", buffer_deg=0.5):
 """
 SDM — type'sfor/againstenvironmentnumber/countgeneration。

 Parameters:
 occurrences_df: pd.DataFrame — type
 lat_col: str — latitudecolumn
 lon_col: str — longitudecolumn
 buffer_deg: float — (degree)
 """
 results = []
 for _, row in occurrences_df.iterrows:
 lat, lon = row[lat_col], row[lon_col]

 # SoilGrids
 soil = soilgrids_get_properties(lat, lon,
 properties=["phh2o", "soc", "clay"])
 soil_mean = {}
 for _, s in soil.iterrows:
 if s.get("depth") == "0-5cm":
 soil_mean[f"soil_{s['property']}"] = s.get("mean", None)

 # WorldClim (if available)
 bioclim = {}
 try:
 bio_df = worldclim_get_bioclim(lat, lon)
 bioclim = {r["variable"]: r["value"]
 for _, r in bio_df.iterrows}
 except Exception:
 pass

 combined = {
 lat_col: lat,
 lon_col: lon,
 **soil_mean,
 **bioclim,
 }
 results.append(combined)

 df = pd.DataFrame(results)
 print(f"SDM env stack: {len(df)} points, {len(df.columns)} variables")
 return df
```

## 4. environmentintegrationpipeline

```python
def environmental_geodata_pipeline(occurrences_csv, output_dir="results"):
 """
 environmentintegrationpipeline。

 Parameters:
 occurrences_csv: str — type CSV 
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 occ = pd.read_csv(occurrences_csv)
 print(f"Occurrences: {len(occ)} records")

 # environmentnumber/count
 env_df = sdm_environmental_stack(occ)
 env_df.to_csv(output_dir / "env_stack.csv", index=False)

 # environment
 summary = env_df.describe.T
 summary.to_csv(output_dir / "env_summary.csv")

 print(f"Environmental pipeline: {output_dir}")
 return {"occurrences": occ, "env_stack": env_df, "summary": summary}
```

---

## ToolUniverse Integration

 REST API for (SoilGrids, WorldClim ToolUniverse )。

## Pipeline Integration

```
environmental-ecology → environmental-geodata → marine-ecology
 (GBIF/iNaturalist) (SoilGrids/WorldClim) (OBIS/WoRMS)
 │ │ ↓
 phylogenetics ───────────────┘ biodiversity-indices
 (phylogenyinformation) │ 
 ↓
 species-distribution-model
 (SDM integration)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/env_stack.csv` | environmentnumber/count | → species-distribution-model |
| `results/env_summary.csv` | environment | → environmental-ecology |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
