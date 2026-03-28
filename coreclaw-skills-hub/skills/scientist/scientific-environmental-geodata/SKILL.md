---
name: scientific-environmental-geodata
description: |
 Environmental geodata skill. Satellite imagery analysis, remote sensing data processing, climate data integration, land use classification, and environmental monitoring.
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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
