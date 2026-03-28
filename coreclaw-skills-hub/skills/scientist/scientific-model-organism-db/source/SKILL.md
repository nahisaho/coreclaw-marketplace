---
name: scientific-model-organism-db
description: |
 Model organism database skill. FlyBase/WormBase/SGD/ZFIN/MGI queries, ortholog mapping, phenotype data retrieval, and cross-species gene function comparison.
---

# Scientific Model Organism Database

key 5 database (FlyBase / WormBase / ZFIN / RGD / MGI) 
integrationgenetabletypediseasecross-cuttingsearchpipeline is provided。

## When to Use

- gene'slog is searchedand
- 's tabletypedata diseaseresearchutilizingwhen needed
- gene's tabletypeinformation is retrievedand
- multiple's save is comparedand
- IMPC (existingskill) ///linedatawhen needed

---

## Quick Start

## 1. MGI (Mouse Genome Informatics) genesearch

```python
import requests
import pandas as pd

MGI_API = "http://www.informatics.jax.org/api"


def search_mgi_gene(query, limit=20):
 """
 MGI genesearch。

 Parameters:
 query: str — gene nameor
 limit: int — maximum retrieval count
 """
 url = f"{MGI_API}/gene/search"
 params = {"query": query, "limit": limit}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 rows = []
 for gene in data.get("results", []):
 rows.append({
 "mgi_id": gene.get("mgiId"),
 "symbol": gene.get("symbol"),
 "name": gene.get("name"),
 "chromosome": gene.get("chromosome"),
 "feature_type": gene.get("featureType"),
 "organism": "Mus musculus",
 })

 df = pd.DataFrame(rows[:limit])
 print(f"MGI search '{query}': {len(df)} genes")
 return df
```

## 2. RGD (Rat Genome Database) genesearch

```python
RGD_API = "https://rest.rgd.mcw.edu/rgdws"


def search_rgd_gene(query, species="rat"):
 """
 RGD genesearch。

 Parameters:
 query: str — gene symbol
 species: str — "rat", "mouse", "human"
 """
 species_map = {"rat": 3, "mouse": 2, "human": 1}
 species_key = species_map.get(species, 3)

 url = f"{RGD_API}/genes/{query}/{species_key}"
 resp = requests.get(url, headers={"Accept": "application/json"})
 resp.raise_for_status
 data = resp.json

 if isinstance(data, dict):
 data = [data]

 rows = []
 for gene in data:
 rows.append({
 "rgd_id": gene.get("rgdId"),
 "symbol": gene.get("symbol"),
 "name": gene.get("name"),
 "chromosome": gene.get("chromosome"),
 "type": gene.get("type"),
 "organism": species,
 })

 df = pd.DataFrame(rows)
 print(f"RGD search '{query}': {len(df)} genes ({species})")
 return df
```

## 3. ZFIN (Zebrafish Information Network)

```python
ZFIN_API = "https://zfin.org/action/api"


def search_zfin_gene(query, limit=20):
 """
 ZFIN genesearch。

 Parameters:
 query: str — gene nameor
 limit: int — maximum retrieval count
 """
 url = f"{ZFIN_API}/marker/search"
 params = {"name": query, "limit": limit, "type": "gene"}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 rows = []
 for gene in data.get("results", []):
 rows.append({
 "zfin_id": gene.get("zdbID"),
 "symbol": gene.get("abbreviation"),
 "name": gene.get("name"),
 "type": gene.get("markerType"),
 "organism": "Danio rerio",
 })

 df = pd.DataFrame(rows[:limit])
 print(f"ZFIN search '{query}': {len(df)} genes")
 return df
```

## 4. FlyBase (Drosophila)

```python
FLYBASE_API = "https://api.flybase.org/api/v1.0"


def search_flybase_gene(query, limit=20):
 """
 FlyBase genesearch。

 Parameters:
 query: str — gene nameor
 limit: int — maximum retrieval count
 """
 url = f"{FLYBASE_API}/gene/search/{query}"
 params = {"limit": limit}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 genes = data.get("resultset", {}).get("result", [])
 rows = []
 for gene in genes:
 rows.append({
 "flybase_id": gene.get("id"),
 "symbol": gene.get("symbol"),
 "name": gene.get("name"),
 "chromosome": gene.get("location", {}).get("chromosome"),
 "organism": "Drosophila melanogaster",
 })

 df = pd.DataFrame(rows[:limit])
 print(f"FlyBase search '{query}': {len(df)} genes")
 return df
```

## 5. WormBase (C. elegans)

```python
WORMBASE_API = "https://wormbase.org/rest"


def search_wormbase_gene(query, limit=20):
 """
 WormBase linegenesearch。

 Parameters:
 query: str — gene nameor
 limit: int — maximum retrieval count
 """
 url = f"{WORMBASE_API}/field/gene/{query}/overview"
 resp = requests.get(url, headers={"Accept": "application/json"})
 resp.raise_for_status
 data = resp.json

 overview = data.get("overview", {})
 info = {
 "wormbase_id": overview.get("name", {}).get("data", {}).get("id"),
 "symbol": overview.get("name", {}).get("data", {}).get("label"),
 "concise_description": overview.get("concise_description", {}).get(
 "data", ""
 ),
 "organism": "Caenorhabditis elegans",
 }

 print(f"WormBase: {info['symbol']} ({info['wormbase_id']})")
 return info
```

## 6. cross-cuttinglogsearch

```python
def cross_species_ortholog_search(human_gene):
 """
 gene's 5 logcross-cuttingsearch。

 Parameters:
 human_gene: str — gene symbol (example: "TP53")

 Pipeline:
 MGI → RGD → ZFIN → FlyBase → WormBase
 """
 results = []

 # Mouse (MGI)
 try:
 mgi = search_mgi_gene(human_gene, limit=3)
 if not mgi.empty:
 results.append({"organism": "Mouse", "db": "MGI",
 "symbol": mgi.iloc[0]["symbol"],
 "id": mgi.iloc[0]["mgi_id"]})
 except Exception as e:
 print(f"MGI error: {e}")

 # Rat (RGD)
 try:
 rgd = search_rgd_gene(human_gene, "rat")
 if not rgd.empty:
 results.append({"organism": "Rat", "db": "RGD",
 "symbol": rgd.iloc[0]["symbol"],
 "id": str(rgd.iloc[0]["rgd_id"])})
 except Exception as e:
 print(f"RGD error: {e}")

 # Zebrafish (ZFIN)
 try:
 zfin = search_zfin_gene(human_gene.lower, limit=3)
 if not zfin.empty:
 results.append({"organism": "Zebrafish", "db": "ZFIN",
 "symbol": zfin.iloc[0]["symbol"],
 "id": zfin.iloc[0]["zfin_id"]})
 except Exception as e:
 print(f"ZFIN error: {e}")

 # Drosophila (FlyBase)
 try:
 fly = search_flybase_gene(human_gene, limit=3)
 if not fly.empty:
 results.append({"organism": "Drosophila", "db": "FlyBase",
 "symbol": fly.iloc[0]["symbol"],
 "id": fly.iloc[0]["flybase_id"]})
 except Exception as e:
 print(f"FlyBase error: {e}")

 # C. elegans (WormBase)
 try:
 worm = search_wormbase_gene(human_gene.lower)
 if worm.get("wormbase_id"):
 results.append({"organism": "C. elegans", "db": "WormBase",
 "symbol": worm["symbol"],
 "id": worm["wormbase_id"]})
 except Exception as e:
 print(f"WormBase error: {e}")

 df = pd.DataFrame(results)
 print(f"\nOrthologs of {human_gene}: {len(df)} model organisms")
 return df
```

## 7. tabletypedataintegration

```python
def get_mgi_phenotypes(mgi_id):
 """
 MGI gene's tabletypeannotationretrieval。

 Parameters:
 mgi_id: str — MGI ID (example: "MGI:98834")
 """
 url = f"{MGI_API}/gene/{mgi_id}/phenotypes"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 rows = []
 for pheno in data.get("phenotypes", []):
 rows.append({
 "mp_id": pheno.get("mpId"),
 "mp_term": pheno.get("mpTerm"),
 "allele_symbol": pheno.get("alleleSymbol"),
 "genetic_background": pheno.get("geneticBackground"),
 })

 df = pd.DataFrame(rows)
 print(f"Phenotypes for {mgi_id}: {len(df)} MP annotations")
 return df
```

---

## Pipeline Integration

```
ensembl-genomics ──→ model-organism-db ──→ disease-research
 (log ID) (tabletypedata) (disease)
 │ │ ↓
biothings-idmapping ──┘ ↓ rare-disease-genetics
 (ID mapping) phylogenetics (OMIM/Orphanet)
 (typephylogenyanalysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/model_orthologs.csv` | log | → ensembl-genomics |
| `results/mgi_phenotypes.csv` | tabletype | → disease-research |
| `results/cross_species.json` | cross-cuttingcomparisonresults | → phylogenetics |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
