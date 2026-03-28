---
name: scientific-gdc-portal
description: |
 GDC Portal skill. Genomic Data Commons cancer data retrieval, mutation frequency analysis, clinical-genomic correlation, and multi-project data integration.
tu_tools:
 - key: gdc
 name: GDC
 description: NCI Genomic Data Commons REST API
---

# Scientific GDC Portal

NCI Genomic Data Commons (GDC) REST API utilizing
cancergenomecross-cuttingsearchData Retrieval
cellvariant/mutation (SSM)gene expressionpipeline is provided。

## When to Use

- TCGA/TARGET 's cancergenomedatacross-cuttingsearchwhen needed
- cancertype'sdata is retrievedand
- gene'scellvariant/mutation (SSM) frequency is investigatedand
- cancer'ssummary is retrievedand
- GDC filedata search URL is retrievedand

---

## Quick Start

## 1. search

```python
import requests
import pandas as pd

GDC_API = "https://api.gdc.cancer.gov"


def gdc_projects(disease_type=None, limit=50):
 """
 GDC — search。

 Parameters:
 disease_type: str — diseasefilter
 (example: "Breast Invasive Carcinoma")
 limit: int — maximum results
 """
 url = f"{GDC_API}/projects"
 params = {
 "size": limit,
 "fields": ("project_id,name,primary_site,"
 "disease_type,summary.case_count,"
 "summary.file_count"),
 }

 if disease_type:
 params["filters"] = (
 '{"op":"=","content":{"field":'
 f'"disease_type","value":"{disease_type}"}}}}'
 )

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for hit in data.get("data", {}).get("hits", []):
 summary = hit.get("summary", {})
 rows.append({
 "project_id": hit.get("project_id", ""),
 "name": hit.get("name", ""),
 "primary_site": "; ".join(
 hit.get("primary_site", [])),
 "disease_type": "; ".join(
 hit.get("disease_type", [])),
 "case_count": summary.get(
 "case_count", 0),
 "file_count": summary.get(
 "file_count", 0),
 })

 df = pd.DataFrame(rows)
 print(f"GDC projects: {len(df)}")
 return df
```

## 2. data

```python
def gdc_cases(project_id, limit=100):
 """
 GDC — Data Retrieval。

 Parameters:
 project_id: str — project ID
 (example: "TCGA-BRCA")
 limit: int — maximum results
 """
 url = f"{GDC_API}/cases"
 filters = {
 "op": "=",
 "content": {
 "field": "project.project_id",
 "value": project_id,
 },
 }
 params = {
 "filters": str(filters).replace("'", '"'),
 "fields": ("case_id,submitter_id,"
 "demographic.gender,"
 "demographic.race,"
 "demographic.vital_status,"
 "diagnoses.primary_diagnosis,"
 "diagnoses.tumor_stage,"
 "diagnoses.age_at_diagnosis"),
 "size": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for hit in data.get("data", {}).get("hits", []):
 demo = hit.get("demographic", {}) or {}
 diag = (hit.get("diagnoses", [{}]) or [{}])[0]
 rows.append({
 "case_id": hit.get("case_id", ""),
 "submitter_id": hit.get("submitter_id", ""),
 "gender": demo.get("gender", ""),
 "race": demo.get("race", ""),
 "vital_status": demo.get(
 "vital_status", ""),
 "diagnosis": diag.get(
 "primary_diagnosis", ""),
 "stage": diag.get("tumor_stage", ""),
 "age_at_diagnosis": diag.get(
 "age_at_diagnosis", ""),
 })

 df = pd.DataFrame(rows)
 print(f"GDC cases: {project_id} → {len(df)}")
 return df
```

## 3. cellvariant/mutation (SSM) search

```python
def gdc_ssm_by_gene(gene_symbol, project_id=None,
 limit=100):
 """
 GDC — genecellvariant/mutationsearch。

 Parameters:
 gene_symbol: str — gene symbol (example: "TP53")
 project_id: str — project ID filter
 limit: int — maximum results
 """
 url = f"{GDC_API}/ssms"
 filters = {
 "op": "and",
 "content": [
 {
 "op": "=",
 "content": {
 "field":
 "consequence.transcript."
 "gene.symbol",
 "value": gene_symbol,
 },
 }
 ],
 }

 if project_id:
 filters["content"].append({
 "op": "=",
 "content": {
 "field": "cases.project.project_id",
 "value": project_id,
 },
 })

 params = {
 "filters": str(filters).replace("'", '"'),
 "fields": ("ssm_id,genomic_dna_change,"
 "consequence.transcript.aa_change,"
 "consequence.transcript."
 "consequence_type,"
 "consequence.transcript."
 "gene.symbol"),
 "size": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for hit in data.get("data", {}).get("hits", []):
 for csq in hit.get("consequence", []):
 tx = csq.get("transcript", {})
 rows.append({
 "ssm_id": hit.get("ssm_id", ""),
 "genomic_change": hit.get(
 "genomic_dna_change", ""),
 "gene": tx.get("gene", {}).get(
 "symbol", ""),
 "aa_change": tx.get("aa_change", ""),
 "consequence_type": tx.get(
 "consequence_type", ""),
 })

 df = pd.DataFrame(rows)
 print(f"GDC SSM: {gene_symbol} → {len(df)} variants")
 return df
```

## 4. GDC integrationpipeline

```python
def gdc_pipeline(project_id, gene_symbol=None,
 output_dir="results"):
 """
 GDC integrationpipeline。

 Parameters:
 project_id: str — project ID
 gene_symbol: str — genefilter
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) information
 projects = gdc_projects
 projects.to_csv(output_dir / "gdc_projects.csv",
 index=False)

 # 2) data
 cases = gdc_cases(project_id)
 cases.to_csv(output_dir / "gdc_cases.csv",
 index=False)

 # 3) cellvariant/mutation
 if gene_symbol:
 ssm = gdc_ssm_by_gene(gene_symbol, project_id)
 ssm.to_csv(output_dir / "gdc_ssm.csv",
 index=False)

 print(f"GDC pipeline: {project_id} → {output_dir}")
 return {"cases": cases}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `gdc` | GDC | NCI Genomic Data Commons REST API |

## Pipeline Integration

```
cancer-genomics → gdc-portal → precision-oncology
 (COSMIC/DepMap) (GDC API) (MTB report)
 │ │ ↓
icgc-cancer-data ───────┘ variant-interpretation
 (ICGC DCC) (ClinVar/ACMG)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gdc_projects.csv` | list | → cancer-genomics |
| `results/gdc_cases.csv` | data | → precision-oncology |
| `results/gdc_ssm.csv` | cellvariant/mutation | → variant-interpretation |
---

## Harness Optimization (v0.4.0)

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
