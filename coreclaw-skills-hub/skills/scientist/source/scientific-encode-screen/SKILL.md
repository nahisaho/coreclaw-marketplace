---
name: scientific-encode-screen
description: |
 ENCODE / ChIP-Atlas epigenomeskill。ENCODE REST API
 experimentfilesearch、SCREEN cis 、
 ChIP-Atlas analysis、genome annotationintegration。
 ---

# Scientific ENCODE / SCREEN / ChIP-Atlas

ENCODE REST API / SCREEN / ChIP-Atlas utilizingepigenome
integrated analysispipeline is provided。

## When to Use

- ENCODE experimentdata (ChIP-seq/ATAC-seq/DNase) is searchedand
- SCREEN cCRE (candidate cis-Regulatory Elements) when needed
- ChIP-Atlas factorbindinghistoneanalysiswhen needed
- 's annotationwhen needed
- epigenomedata's chromatinanalysisintegrationwhen needed
- tissue/celltypeepigenomefile is comparedand

---

## Quick Start

## 1. ENCODE experimentsearchfileretrieval

```python
import requests
import pandas as pd
import json

ENCODE_BASE = "https://www.encodeproject.org"
HEADERS = {"Accept": "application/json"}


def encode_search_experiments(assay_title=None, biosample=None,
 target=None, organism="Homo sapiens",
 limit=50):
 """
 ENCODE — experimentdatasearch。

 Parameters:
 assay_title: str — type (example: "ChIP-seq", "ATAC-seq")
 biosample: str — (example: "K562")
 target: str — (example: "CTCF")
 organism: str — organism/species
 limit: int — maximum results
 """
 url = f"{ENCODE_BASE}/search/"
 params = {
 "type": "Experiment",
 "status": "released",
 "replicates.library.biosample.donor.organism.scientific_name": organism,
 "limit": limit,
 "format": "json",
 }
 if assay_title:
 params["assay_title"] = assay_title
 if biosample:
 params["biosample_ontology.term_name"] = biosample
 if target:
 params["target.label"] = target

 resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for exp in data.get("@graph", []):
 results.append({
 "accession": exp.get("accession", ""),
 "assay": exp.get("assay_title", ""),
 "biosample": exp.get("biosample_summary", ""),
 "target": exp.get("target", {}).get("label", ""),
 "status": exp.get("status", ""),
 "lab": exp.get("lab", {}).get("title", ""),
 "date_released": exp.get("date_released", ""),
 "files_count": len(exp.get("files", [])),
 })

 df = pd.DataFrame(results)
 print(f"ENCODE: {len(df)} experiments found")
 return df


def encode_get_files(experiment_accession, file_type="bigWig",
 output_type="signal p-value", assembly="GRCh38"):
 """
 ENCODE — experimentfile URL retrieval。

 Parameters:
 experiment_accession: str — experimentaccession
 file_type: str — file
 output_type: str — output
 assembly: str — assembly
 """
 url = f"{ENCODE_BASE}/search/"
 params = {
 "type": "File",
 "dataset": f"/experiments/{experiment_accession}/",
 "file_format": file_type,
 "output_type": output_type,
 "assembly": assembly,
 "status": "released",
 "format": "json",
 }
 resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
 resp.raise_for_status
 data = resp.json

 files = []
 for f in data.get("@graph", []):
 files.append({
 "accession": f.get("accession", ""),
 "file_format": f.get("file_format", ""),
 "output_type": f.get("output_type", ""),
 "assembly": f.get("assembly", ""),
 "href": ENCODE_BASE + f.get("href", ""),
 "file_size": f.get("file_size", 0),
 "biological_replicate": f.get("biological_replicates", []),
 })

 df = pd.DataFrame(files)
 print(f"ENCODE files ({experiment_accession}): {len(df)} files")
 return df
```

## 2. SCREEN cCRE search

```python
SCREEN_BASE = "https://api.wenglab.org/screen/v2"


def screen_ccre_search(gene=None, region=None, biosample=None,
 assembly="GRCh38"):
 """
 SCREEN — candidate cis-Regulatory Element search。

 Parameters:
 gene: str — gene name (example: "TP53")
 region: str — genome (example: "chr17:7668421-7687490")
 biosample: str — 
 assembly: str — assembly
 """
 url = f"{SCREEN_BASE}/search"
 query = {"assembly": assembly}

 if gene:
 query["gene"] = gene
 if region:
 chrom, pos = region.split(":")
 start, end = pos.split("-")
 query["coordinates"] = {
 "chromosome": chrom,
 "start": int(start),
 "end": int(end),
 }

 resp = requests.post(url, json=query, timeout=30)
 resp.raise_for_status
 data = resp.json

 ccres = []
 for cre in data.get("data", []):
 ccres.append({
 "accession": cre.get("accession", ""),
 "chromosome": cre.get("chrom", ""),
 "start": cre.get("start", 0),
 "end": cre.get("end", 0),
 "ccre_class": cre.get("group", ""),
 "dnase_zscore": cre.get("dnase_zscore", None),
 "h3k4me3_zscore": cre.get("h3k4me3_zscore", None),
 "h3k27ac_zscore": cre.get("h3k27ac_zscore", None),
 "ctcf_zscore": cre.get("ctcf_zscore", None),
 })

 df = pd.DataFrame(ccres)
 print(f"SCREEN cCREs: {len(df)} elements")
 return df
```

## 3. ChIP-Atlas analysis

```python
CHIPATLAS_BASE = "https://chip-atlas.org/api"


def chipatlas_enrichment(gene_list, cell_type=None,
 antigen_class="TFs and others",
 genome="hg38", threshold=5):
 """
 ChIP-Atlas — gene list'sanalysis。

 Parameters:
 gene_list: list[str] — gene list
 cell_type: str — celltype (None = allcelltype)
 antigen_class: str — antigen
 genome: str — genomeassembly
 threshold: int — threshold (kb)
 """
 url = f"{CHIPATLAS_BASE}/enrichment"
 payload = {
 "genome": genome,
 "geneList": gene_list,
 "antigenClass": antigen_class,
 "distanceThreshold": threshold * 1000,
 }
 if cell_type:
 payload["cellType"] = cell_type

 resp = requests.post(url, json=payload, timeout=60)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("results", []):
 results.append({
 "antigen": hit.get("antigen", ""),
 "cell_type": hit.get("cellType", ""),
 "experiment_id": hit.get("experimentId", ""),
 "p_value": hit.get("pValue", 1.0),
 "log_p": hit.get("logPValue", 0),
 "overlap_genes": hit.get("overlapGenes", 0),
 "total_peaks": hit.get("totalPeaks", 0),
 })

 df = pd.DataFrame(results)
 df = df.sort_values("p_value")
 print(f"ChIP-Atlas enrichment: {len(df)} TF/antigen hits")
 return df
```

## 4. ENCODE + SCREEN + ChIP-Atlas integrationpipeline

```python
def encode_epigenome_pipeline(gene_name, biosample="K562",
 output_dir="results"):
 """
 ENCODE/SCREEN/ChIP-Atlas epigenomeintegrationpipeline。

 Parameters:
 gene_name: str — gene name
 biosample: str — 
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) SCREEN cCRE
 ccres = screen_ccre_search(gene=gene_name)
 ccres.to_csv(output_dir / "screen_ccres.csv", index=False)

 # 2) ENCODE experiment
 experiments = encode_search_experiments(
 assay_title="ChIP-seq",
 biosample=biosample,
 target="H3K27ac",
 )
 experiments.to_csv(output_dir / "encode_experiments.csv", index=False)

 # 3) ChIP-Atlas 
 enrichment = chipatlas_enrichment(
 gene_list=[gene_name],
 cell_type=biosample,
 )
 enrichment.to_csv(output_dir / "chipatlas_enrichment.csv", index=False)

 print(f"ENCODE epigenome pipeline: {output_dir}")
 return {
 "ccres": ccres,
 "experiments": experiments,
 "enrichment": enrichment,
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
3. Write `report.md` summarizing methods, results, and interpretation

## Pipeline Integration

```
regulatory-genomics → encode-screen → epigenomics-chromatin
 (RegulomeDB/ReMap) (ENCODE/SCREEN) (ChIP/ATAC bulk)
 │ │ ↓
 variant-interpretation ───┘ scatac-signac
 (ACMG ) │ (scATAC-seq)
 ↓
 gene-regulatory-network
 (GRN )
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/screen_ccres.csv` | cCRE annotation | → variant-interpretation |
| `results/encode_experiments.csv` | ENCODE experimentdata | → epigenomics-chromatin |
| `results/chipatlas_enrichment.csv` | TF | → gene-regulatory-network |
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
