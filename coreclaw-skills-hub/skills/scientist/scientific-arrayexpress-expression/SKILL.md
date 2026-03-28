---
name: scientific-arrayexpress-expression
description: |
 ArrayExpress gene expression skill. Microarray and RNA-seq data retrieval from ArrayExpress/BioStudies, normalization, differential expression, and cross-study comparison.
---

# Scientific ArrayExpress Expression

EBI ArrayExpress / BioStudies REST API utilizingexpressiondata
searchanalysispipeline is provided。

## When to Use

- ArrayExpress/BioStudies 's expressionexperiment is searchedand
- /RNA-seq expressiondata'sdata is retrievedand
- SDRF informationtableanalysiswhen needed
- E-MTAB/E-GEOD accessionfromdataanalysiswhen needed
- expressiondatacross-cuttingsearchwhen needed
- GEO and ArrayExpress 's data and

---

## Quick Start

## 1. BioStudies expressionexperimentsearch

```python
import requests
import pandas as pd

BIOSTUDIES_BASE = "https://www.ebi.ac.uk/biostudies/api/v1"
AE_BASE = "https://www.ebi.ac.uk/arrayexpress/json/v3"


def arrayexpress_search_experiments(query, organism=None,
 experiment_type=None,
 limit=50):
 """
 ArrayExpress — expressionexperimentsearch (BioStudies API)。

 Parameters:
 query: str — search query (example: "breast cancer RNA-seq")
 organism: str — organism/species (example: "Homo sapiens")
 experiment_type: str — experiment (example: "RNA-seq of coding RNA")
 limit: int — maximum results
 """
 url = f"{BIOSTUDIES_BASE}/search"
 params = {
 "query": query,
 "type": "study",
 "pageSize": limit,
 }
 if organism:
 params["organism"] = organism
 if experiment_type:
 params["experimenttype"] = experiment_type

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 hits = data.get("hits", [])
 results = []
 for h in hits:
 attrs = {a.get("name", ""): a.get("value", "")
 for a in h.get("attributes", [])}
 results.append({
 "accession": h.get("accession", ""),
 "title": attrs.get("Title", h.get("title", "")),
 "organism": attrs.get("Organism", ""),
 "experiment_type": attrs.get("Experiment type", ""),
 "release_date": h.get("releaseDate", ""),
 "files_count": h.get("filesCount", 0),
 "links_count": h.get("linksCount", 0),
 })

 df = pd.DataFrame(results)
 print(f"ArrayExpress search: {len(df)} experiments "
 f"(query={query})")
 return df
```

## 2. experimentdataSDRF retrieval

```python
def arrayexpress_get_experiment(accession):
 """
 ArrayExpress — experimentdata & SDRF retrieval。

 Parameters:
 accession: str — accession (example: "E-MTAB-12345")
 """
 url = f"{BIOSTUDIES_BASE}/studies/{accession}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 # data
 attrs = {a.get("name", ""): a.get("value", "")
 for a in data.get("attributes", [])}
 metadata = {
 "accession": accession,
 "title": attrs.get("Title", ""),
 "description": attrs.get("Description", "")[:500],
 "organism": attrs.get("Organism", ""),
 "experiment_type": attrs.get("Experiment type", ""),
 "release_date": data.get("releaseDate", ""),
 }

 # filelist
 files = []
 for section in data.get("section", {}).get("files", []):
 if isinstance(section, list):
 for f in section:
 files.append({
 "filename": f.get("path", ""),
 "type": f.get("type", ""),
 "size": f.get("size", 0),
 })
 elif isinstance(section, dict):
 files.append({
 "filename": section.get("path", ""),
 "type": section.get("type", ""),
 "size": section.get("size", 0),
 })

 files_df = pd.DataFrame(files)

 # SDRF retrieval
 sdrf_url = (f"https://www.ebi.ac.uk/biostudies/files/"
 f"{accession}/{accession}.sdrf.txt")
 sdrf_df = pd.DataFrame
 try:
 sdrf_resp = requests.get(sdrf_url, timeout=30)
 if sdrf_resp.status_code == 200:
 from io import StringIO
 sdrf_df = pd.read_csv(StringIO(sdrf_resp.text), sep="\t")
 except Exception:
 pass

 print(f"ArrayExpress {accession}: {len(files_df)} files, "
 f"{len(sdrf_df)} SDRF rows")
 return metadata, files_df, sdrf_df
```

## 3. expressiondata

```python
def arrayexpress_download_matrix(accession, output_dir="results"):
 """
 ArrayExpress — expression。

 Parameters:
 accession: str — accession
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 metadata, files_df, sdrf_df = arrayexpress_get_experiment(accession)

 # expressionfilesearch
 expr_files = files_df[
 files_df["filename"].str.contains(
 r"processed|normalized|expression|counts",
 case=False, na=False)
 ]

 downloaded = []
 for _, frow in expr_files.iterrows:
 fname = frow["filename"]
 url = (f"https://www.ebi.ac.uk/biostudies/files/"
 f"{accession}/{fname}")
 try:
 resp = requests.get(url, timeout=120)
 if resp.status_code == 200:
 fpath = output_dir / fname.split("/")[-1]
 fpath.write_bytes(resp.content)
 downloaded.append(str(fpath))
 except Exception:
 continue

 # SDRF save
 if not sdrf_df.empty:
 sdrf_df.to_csv(output_dir / "sdrf.csv", index=False)

 print(f"ArrayExpress download: {len(downloaded)} files → "
 f"{output_dir}")
 return {
 "metadata": metadata,
 "files": downloaded,
 "sdrf": sdrf_df,
 }
```

## 4. ArrayExpress integrationpipeline

```python
def arrayexpress_pipeline(query, organism="Homo sapiens",
 output_dir="results"):
 """
 ArrayExpress integrationpipeline。

 Parameters:
 query: str — search query
 organism: str — organism/species
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) experimentsearch
 experiments = arrayexpress_search_experiments(
 query, organism=organism)
 experiments.to_csv(output_dir / "experiments.csv", index=False)

 # 2) experiment'sdetails
 if not experiments.empty:
 top_acc = experiments.iloc[0]["accession"]
 metadata, files, sdrf = arrayexpress_get_experiment(top_acc)
 files.to_csv(output_dir / "experiment_files.csv", index=False)
 if not sdrf.empty:
 sdrf.to_csv(output_dir / "sdrf.csv", index=False)

 print(f"ArrayExpress pipeline: {output_dir}")
 return {"experiments": experiments}
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
3. Write `report.md` summarizing methods, results, and interpretation

## Pipeline Integration

```
ebi-databases → arrayexpress-expression → gene-expression-transcriptomics
 (EBI Search) (ArrayExpress/BioStudies) (DESeq2/GSEA)
 │ │ ↓
 geo-expression ─────────┘ pathway-enrichment
 (GEO data) │ (KEGG/Reactome)
 ↓
 multi-omics
 (integrated analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/experiments.csv` | experimentlist | → geo-expression |
| `results/sdrf.csv` | information | → gene-expression-transcriptomics |
| `results/experiment_files.csv` | file | → data-preprocessing |
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
