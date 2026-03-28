---
name: scientific-paleobiology
description: |
 paleontologydatabaseskill。Paleobiology Database (PBDB) REST
 API by/viaclassificationgroupsearch、
 curvelineanalysis。ToolUniverse integration: paleobiology。
tu_tools:
 - key: paleobiology
 name: Paleobiology Database
 description: PBDB classificationgroupsearch
---

# Scientific Paleobiology

Paleobiology Database (PBDB) REST API utilizingpaleontology
analysispipeline is provided。

## When to Use

- (occurrence) is searchedand
- classificationgroup (taxa) 'sdistribution is investigatedand
- /information is searchedand
- curveline is createdand
- amount's minwhen needed
- distributionanalysiswhen needed

---

## Quick Start

## 1. PBDB search

```python
import requests
import pandas as pd
import numpy as np

PBDB_BASE = "https://paleobiodb.org/data1.2"


def pbdb_search_occurrences(taxon=None, interval=None,
 lngmin=None, lngmax=None,
 latmin=None, latmax=None, limit=1000):
 """
 PBDB — search。

 Parameters:
 taxon: str — classificationgroup (example: "Dinosauria", "Trilobita")
 interval: str — (example: "Cretaceous", "Permian")
 lngmin: float — longitudevalue
 lngmax: float — longitudevalue
 latmin: float — latitudevalue
 latmax: float — latitudevalue
 limit: int — maximum results
 """
 url = f"{PBDB_BASE}/occs/list.json"
 params = {
 "show": "coords,phylo,time",
 "limit": limit,
 }
 if taxon:
 params["base_name"] = taxon
 if interval:
 params["interval"] = interval
 if all(v is not None for v in [lngmin, lngmax, latmin, latmax]):
 params.update({
 "lngmin": lngmin, "lngmax": lngmax,
 "latmin": latmin, "latmax": latmax,
 })

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 records = resp.json.get("records", [])

 results = []
 for r in records:
 results.append({
 "occurrence_no": r.get("oid", ""),
 "taxon_name": r.get("tna", ""),
 "taxon_rank": r.get("rnk", ""),
 "phylum": r.get("phl", ""),
 "class": r.get("cll", ""),
 "order": r.get("odl", ""),
 "family": r.get("fml", ""),
 "early_interval": r.get("oei", ""),
 "late_interval": r.get("oli", ""),
 "max_ma": r.get("eag", None),
 "min_ma": r.get("lag", None),
 "lng": r.get("lng", None),
 "lat": r.get("lat", None),
 "collection_no": r.get("cid", ""),
 "reference_no": r.get("rid", ""),
 })

 df = pd.DataFrame(results)
 print(f"PBDB occurrences: {len(df)} records "
 f"(taxon={taxon}, interval={interval})")
 return df
```

## 2. PBDB classificationgroupinformationsearch

```python
def pbdb_search_taxa(name=None, rank=None, interval=None, limit=500):
 """
 PBDB — classificationgroupsearch。

 Parameters:
 name: str — classificationgroup (example: "Dinosauria")
 rank: str — (example: "genus", "family", "order")
 interval: str — 
 limit: int — maximum results
 """
 url = f"{PBDB_BASE}/taxa/list.json"
 params = {
 "show": "attr,app,size",
 "limit": limit,
 }
 if name:
 params["base_name"] = name
 if rank:
 params["rank"] = rank
 if interval:
 params["interval"] = interval

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 records = resp.json.get("records", [])

 results = []
 for r in records:
 results.append({
 "taxon_no": r.get("oid", ""),
 "taxon_name": r.get("nam", ""),
 "rank": r.get("rnk", ""),
 "parent_name": r.get("prl", ""),
 "n_occs": r.get("noc", 0),
 "first_appearance": r.get("fea", ""),
 "last_appearance": r.get("lla", ""),
 "extant": r.get("ext", ""),
 })

 df = pd.DataFrame(results)
 print(f"PBDB taxa: {len(df)} records (name={name})")
 return df
```

## 3. curveline

```python
def pbdb_diversity_curve(taxon, time_resolution="stage",
 rank="genus"):
 """
 PBDB — curvelinegeneration。

 Parameters:
 taxon: str — classificationgroup
 time_resolution: str — "stage" or "epoch" or "period"
 rank: str — ("genus", "family")
 """
 url = f"{PBDB_BASE}/occs/diversity.json"
 params = {
 "base_name": taxon,
 "count": rank,
 "time_reso": time_resolution,
 }
 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 records = resp.json.get("records", [])

 results = []
 for r in records:
 results.append({
 "interval_name": r.get("idn", ""),
 "max_ma": r.get("eag", None),
 "min_ma": r.get("lag", None),
 "mid_ma": (float(r.get("eag", 0)) +
 float(r.get("lag", 0))) / 2,
 "sampled_in_bin": r.get("dsb", 0),
 "n_originations": r.get("dor", 0),
 "n_extinctions": r.get("dex", 0),
 "range_through": r.get("drt", 0),
 })

 df = pd.DataFrame(results)
 print(f"PBDB diversity: {len(df)} intervals, "
 f"max diversity={df['sampled_in_bin'].max} {rank}")
 return df
```

## 4. paleontologyintegrationpipeline

```python
def paleobiology_pipeline(taxon, interval=None,
 output_dir="results"):
 """
 paleontologyintegrationpipeline。

 Parameters:
 taxon: str — classificationgroup (example: "Dinosauria")
 interval: str — (option)
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) 
 occ = pbdb_search_occurrences(taxon=taxon, interval=interval)
 occ.to_csv(output_dir / "occurrences.csv", index=False)

 # 2) classificationgroupinformation
 taxa = pbdb_search_taxa(name=taxon)
 taxa.to_csv(output_dir / "taxa.csv", index=False)

 # 3) curveline
 diversity = pbdb_diversity_curve(taxon)
 diversity.to_csv(output_dir / "diversity.csv", index=False)

 # 4) 
 if "lat" in occ.columns and "lng" in occ.columns:
 geo_summary = occ.groupby("early_interval").agg(
 n_records=("occurrence_no", "count"),
 mean_lat=("lat", "mean"),
 mean_lng=("lng", "mean"),
 ).reset_index
 geo_summary.to_csv(output_dir / "geo_summary.csv", index=False)

 print(f"Paleobiology pipeline: {output_dir}")
 return {
 "occurrences": occ,
 "taxa": taxa,
 "diversity": diversity,
 }
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `paleobiology` | Paleobiology Database | classificationgroupsearch |

## Pipeline Integration

```
phylogenetics → paleobiology → environmental-ecology
 (phylogenyanalysis)  (GBIF/)
 │ │ ↓
 taxonomy ─────────┘ environmental-geodata
 (classificationsystem) │ (environment)
 ↓
 macroevolution
 (evolution)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/occurrences.csv` | | → environmental-ecology |
| `results/taxa.csv` | classificationgroupinformation | → phylogenetics |
| `results/diversity.csv` | curveline | → macroevolution |
| `results/geo_summary.csv` | | → environmental-geodata |
