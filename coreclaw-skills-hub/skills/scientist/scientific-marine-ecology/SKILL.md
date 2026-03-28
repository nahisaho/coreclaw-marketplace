---
name: scientific-marine-ecology
description: |
 Marine ecology skill. Ocean biodiversity analysis, marine species distribution modeling, fisheries data analysis, coral reef assessment, and marine environmental monitoring.
---

# Scientific Marine Ecology

OBIS / WoRMS / GBIF / FishBase utilizing
distributionanalysispipeline is provided。

## When to Use

- 'sdistributiondata is retrievedand
- 's classificationinformation (WoRMS) verificationwhen needed
- analysiswhen needed
- 's shapedata (FishBase) is retrievedand
- all'sevaluation is performedand
- environment and typedistribution's minwhen needed

---

## Quick Start

## 1. OBIS distribution

```python
import requests
import pandas as pd
import numpy as np

OBIS_BASE = "https://api.obis.org/v3"


def obis_occurrence_search(taxon_name=None, taxon_id=None,
 geometry=None, year_range=None, limit=1000):
 """
 OBIS — search。

 Parameters:
 taxon_name: str — (example: "Delphinidae")
 taxon_id: int — AphiaID
 geometry: str — WKT (example: "POLYGON((...))")
 year_range: tuple — (start_year, end_year)
 limit: int — retrievalitemsnumber/count
 """
 url = f"{OBIS_BASE}/occurrence"
 params = {"size": min(limit, 5000)}

 if taxon_name:
 params["scientificname"] = taxon_name
 if taxon_id:
 params["taxonid"] = taxon_id
 if geometry:
 params["geometry"] = geometry
 if year_range:
 params["startdate"] = f"{year_range[0]}-01-01"
 params["enddate"] = f"{year_range[1]}-12-31"

 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json

 records = []
 for rec in data.get("results", []):
 records.append({
 "scientific_name": rec.get("scientificName", ""),
 "aphia_id": rec.get("aphiaID", ""),
 "latitude": rec.get("decimalLatitude", None),
 "longitude": rec.get("decimalLongitude", None),
 "depth": rec.get("depth", None),
 "date": rec.get("date_mid", ""),
 "dataset_id": rec.get("dataset_id", ""),
 "basis_of_record": rec.get("basisOfRecord", ""),
 })

 df = pd.DataFrame(records)
 print(f"OBIS: '{taxon_name or taxon_id}' → {len(df)} occurrences")
 return df


def obis_checklist(geometry=None, area_id=None):
 """
 OBIS — type。

 Parameters:
 geometry: str — WKT 
 area_id: int — OBIS ID
 """
 url = f"{OBIS_BASE}/checklist"
 params = {"size": 5000}
 if geometry:
 params["geometry"] = geometry
 if area_id:
 params["areaid"] = area_id

 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json

 species = []
 for sp in data.get("results", []):
 species.append({
 "scientific_name": sp.get("scientificName", ""),
 "aphia_id": sp.get("taxonID", ""),
 "records": sp.get("records", 0),
 "kingdom": sp.get("kingdom", ""),
 "phylum": sp.get("phylum", ""),
 "class": sp.get("class", ""),
 "order": sp.get("order", ""),
 "family": sp.get("family", ""),
 })

 df = pd.DataFrame(species)
 print(f"OBIS checklist: {len(df)} species")
 return df
```

## 2. WoRMS classificationsearch

```python
WORMS_BASE = "https://www.marinespecies.org/rest"


def worms_taxon_search(name, fuzzy=True, marine_only=True):
 """
 WoRMS — classificationsearch。

 Parameters:
 name: str — species name/
 fuzzy: bool — search
 marine_only: bool — type's
 """
 url = f"{WORMS_BASE}/AphiaRecordsByName/{name}"
 params = {
 "like": str(fuzzy).lower,
 "marine_only": str(marine_only).lower,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for taxon in data if isinstance(data, list) else [data]:
 results.append({
 "aphia_id": taxon.get("AphiaID", ""),
 "scientific_name": taxon.get("scientificname", ""),
 "authority": taxon.get("authority", ""),
 "status": taxon.get("status", ""),
 "rank": taxon.get("rank", ""),
 "valid_name": taxon.get("valid_name", ""),
 "kingdom": taxon.get("kingdom", ""),
 "phylum": taxon.get("phylum", ""),
 "class": taxon.get("class", ""),
 "order": taxon.get("order", ""),
 "family": taxon.get("family", ""),
 "genus": taxon.get("genus", ""),
 "is_marine": taxon.get("isMarine", 0),
 "is_brackish": taxon.get("isBrackish", 0),
 "is_freshwater": taxon.get("isFreshwater", 0),
 })

 df = pd.DataFrame(results)
 print(f"WoRMS: '{name}' → {len(df)} taxa")
 return df


def worms_classification(aphia_id):
 """
 WoRMS — allclassificationretrieval。

 Parameters:
 aphia_id: int — AphiaID
 """
 url = f"{WORMS_BASE}/AphiaClassificationByAphiaID/{aphia_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 hierarchy = []
 node = data
 while node:
 hierarchy.append({
 "aphia_id": node.get("AphiaID", ""),
 "name": node.get("scientificname", ""),
 "rank": node.get("rank", ""),
 })
 node = node.get("child")

 df = pd.DataFrame(hierarchy)
 print(f"WoRMS classification: {len(df)} levels")
 return df
```

## 3. GBIF record

```python
GBIF_BASE = "https://api.gbif.org/v1"


def gbif_species_search(name, limit=20):
 """
 GBIF — species namesearchclassification。

 Parameters:
 name: str — species name
 limit: int — results
 """
 url = f"{GBIF_BASE}/species/search"
 params = {"q": name, "limit": limit}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for sp in data.get("results", []):
 results.append({
 "taxon_key": sp.get("key", ""),
 "scientific_name": sp.get("scientificName", ""),
 "canonical_name": sp.get("canonicalName", ""),
 "status": sp.get("taxonomicStatus", ""),
 "rank": sp.get("rank", ""),
 "kingdom": sp.get("kingdom", ""),
 "phylum": sp.get("phylum", ""),
 "class": sp.get("class", ""),
 "order": sp.get("order", ""),
 "family": sp.get("family", ""),
 "num_occurrences": sp.get("numOccurrences", 0),
 })

 df = pd.DataFrame(results)
 print(f"GBIF species: '{name}' → {len(df)} taxa")
 return df


def gbif_occurrence_search(taxon_key=None, country=None,
 year_range=None, limit=300):
 """
 GBIF — search。

 Parameters:
 taxon_key: int — GBIF taxon key
 country: str — ISO (example: "JP")
 year_range: tuple — (start, end)
 limit: int — itemsnumber/count
 """
 url = f"{GBIF_BASE}/occurrence/search"
 params = {"limit": min(limit, 300)}

 if taxon_key:
 params["taxonKey"] = taxon_key
 if country:
 params["country"] = country
 if year_range:
 params["year"] = f"{year_range[0]},{year_range[1]}"

 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json

 records = []
 for rec in data.get("results", []):
 records.append({
 "gbif_id": rec.get("gbifID", ""),
 "scientific_name": rec.get("scientificName", ""),
 "latitude": rec.get("decimalLatitude", None),
 "longitude": rec.get("decimalLongitude", None),
 "country": rec.get("country", ""),
 "year": rec.get("year", ""),
 "basis_of_record": rec.get("basisOfRecord", ""),
 "institution": rec.get("institutionCode", ""),
 })

 df = pd.DataFrame(records)
 print(f"GBIF occurrences: {len(df)} records (total: {data.get('count', 0)})")
 return df
```

## 4. FishBase data

```python
FISHBASE_BASE = "https://fishbase.ropensci.org"


def fishbase_species(genus=None, species=None, family=None):
 """
 FishBase — typeData Retrieval。

 Parameters:
 genus: str — 
 species: str — type
 family: str — 
 """
 url = f"{FISHBASE_BASE}/species"
 params = {"limit": 100}
 if genus:
 params["Genus"] = genus
 if species:
 params["Species"] = species
 if family:
 params["Family"] = family

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 records = []
 for fish in data.get("data", []):
 records.append({
 "spec_code": fish.get("SpecCode", ""),
 "genus": fish.get("Genus", ""),
 "species": fish.get("Species", ""),
 "family": fish.get("Family", ""),
 "body_shape": fish.get("BodyShapeI", ""),
 "max_length": fish.get("Length", None),
 "vulnerability": fish.get("Vulnerability", None),
 "importance": fish.get("Importance", ""),
 "habitat": fish.get("DemersPelag", ""),
 "depth_range": f"{fish.get('DepthRangeShallow', '')}-{fish.get('DepthRangeDeep', '')}",
 })

 df = pd.DataFrame(records)
 print(f"FishBase: {len(df)} species")
 return df
```

## 5. ecologyintegrationpipeline

```python
def marine_ecology_pipeline(taxon_name, region_wkt=None,
 output_dir="results"):
 """
 OBIS + WoRMS + GBIF + FishBase integrationpipeline。

 Parameters:
 taxon_name: str — classificationgroup
 region_wkt: str — investigation WKT
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) WoRMS classificationverification
 taxonomy = worms_taxon_search(taxon_name)
 taxonomy.to_csv(output_dir / "worms_taxonomy.csv", index=False)

 aphia_id = None
 if len(taxonomy) > 0:
 aphia_id = taxonomy.iloc[0]["aphia_id"]
 classification = worms_classification(aphia_id)
 classification.to_csv(output_dir / "classification.csv", index=False)

 # 2) OBIS distribution
 obis_data = obis_occurrence_search(
 taxon_name=taxon_name,
 taxon_id=aphia_id,
 geometry=region_wkt,
 )
 obis_data.to_csv(output_dir / "obis_occurrences.csv", index=False)

 # 3) GBIF 
 gbif_sp = gbif_species_search(taxon_name)
 if len(gbif_sp) > 0:
 taxon_key = gbif_sp.iloc[0]["taxon_key"]
 gbif_occ = gbif_occurrence_search(taxon_key=taxon_key)
 gbif_occ.to_csv(output_dir / "gbif_occurrences.csv", index=False)
 else:
 gbif_occ = pd.DataFrame

 # 4) 
 if len(obis_data) > 0:
 n_species = obis_data["scientific_name"].nunique
 lat_range = (obis_data["latitude"].min, obis_data["latitude"].max)
 depth_range = (obis_data["depth"].min, obis_data["depth"].max)
 print(f"Diversity: {n_species} species, "
 f"lat {lat_range}, depth {depth_range}")

 print(f"Marine ecology pipeline: {output_dir}")
 return {
 "taxonomy": taxonomy,
 "obis_occurrences": obis_data,
 "gbif_occurrences": gbif_occ,
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
environmental-ecology → marine-ecology → phylogenetics
 (ecology) (OBIS/WoRMS/GBIF) (phylogenyanalysis)
 │ │ ↓
 biodiversity-db ───────────┘ species-distribution
 (ENA/BOLD) │ (distribution)
 ↓
 fisheries-management
 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/worms_taxonomy.csv` | WoRMS classificationinformation | → phylogenetics |
| `results/obis_occurrences.csv` | OBIS | → species-distribution |
| `results/gbif_occurrences.csv` | GBIF | → biodiversity-db |
| `results/classification.csv` | classification | → environmental-ecology |
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
