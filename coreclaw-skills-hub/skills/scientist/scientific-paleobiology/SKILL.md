---
name: scientific-paleobiology
description: |
 Paleobiology skill. Fossil record analysis, paleobiodiversity estimation, extinction rate calculation, stratigraphic data processing, and macroevolutionary pattern analysis.
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
