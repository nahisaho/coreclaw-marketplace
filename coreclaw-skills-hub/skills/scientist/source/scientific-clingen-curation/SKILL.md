---
name: scientific-clingen-curation
description: |
 ClinGen genomeskill。ClinGen API 
 gene-disease、、
 amount、evaluationpipeline。
 ---

# Scientific ClinGen Curation

ClinGen (Clinical Genome Resource) API utilizing
gene-diseaseclassification
amountevaluation
pipeline.

## When to Use

- gene-disease's is evaluatedand
- (possible) when needed
- all/ is evaluatedand
- ClinGen classification is retrievedand
- ACMG -based is performedand

---

## Quick Start

## 1. gene-disease

```python
import requests
import pandas as pd

CLINGEN_BASE = "https://search.clinicalgenome.org/kb"


def clingen_gene_validity(gene_symbol):
 """
 ClinGen — gene-diseaseclassificationretrieval。

 Parameters:
 gene_symbol: str — gene symbol (example: "BRCA1")
 """
 url = (f"{CLINGEN_BASE}/gene-validity/"
 f"?search={gene_symbol}&format=json")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = data if isinstance(data, list) else \
 data.get("results", [])

 rows = []
 for item in results:
 rows.append({
 "gene": item.get("gene", {}).get(
 "symbol", gene_symbol),
 "disease": item.get("disease", {}).get(
 "label", ""),
 "classification": item.get(
 "classification", ""),
 "moi": item.get("moi", ""),
 "sop": item.get("sopVersion", ""),
 })

 df = pd.DataFrame(rows)
 print(f"ClinGen validity: {gene_symbol} → "
 f"{len(df)} gene-disease pairs")
 return df


def clingen_gene_validity_batch(gene_symbols):
 """
 ClinGen — multiplegenebatchretrieval。

 Parameters:
 gene_symbols: list[str] — gene symbol list
 """
 all_results = []
 for sym in gene_symbols:
 df = clingen_gene_validity(sym)
 if not df.empty:
 all_results.append(df)
 if all_results:
 combined = pd.concat(all_results,
 ignore_index=True)
 cls_dist = combined["classification"].value_counts
 print(f"Validity distribution: "
 f"{cls_dist.to_dict}")
 return combined
 return pd.DataFrame
```

## 2. amount

```python
def clingen_dosage_sensitivity(gene_symbol):
 """
 ClinGen — amount (haplo/triplo) evaluationretrieval。

 Parameters:
 gene_symbol: str — gene symbol
 """
 url = (f"{CLINGEN_BASE}/gene-dosage/"
 f"?search={gene_symbol}&format=json")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = data if isinstance(data, list) else \
 data.get("results", [])

 rows = []
 for item in results:
 rows.append({
 "gene": item.get("gene", {}).get(
 "symbol", gene_symbol),
 "haplo_score": item.get(
 "haploinsufficiency", {}).get(
 "score", ""),
 "haplo_label": item.get(
 "haploinsufficiency", {}).get(
 "label", ""),
 "triplo_score": item.get(
 "triplosensitivity", {}).get(
 "score", ""),
 "triplo_label": item.get(
 "triplosensitivity", {}).get(
 "label", ""),
 })

 df = pd.DataFrame(rows)
 print(f"ClinGen dosage: {gene_symbol} → "
 f"{len(df)} entries")
 return df
```

## 3. 

```python
def clingen_actionability(gene_symbol):
 """
 ClinGen — retrieval。

 Parameters:
 gene_symbol: str — gene symbol
 """
 url = (f"{CLINGEN_BASE}/actionability/"
 f"?search={gene_symbol}&format=json")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = data if isinstance(data, list) else \
 data.get("results", [])

 rows = []
 for item in results:
 rows.append({
 "gene": item.get("gene", {}).get(
 "symbol", gene_symbol),
 "disease": item.get("disease", {}).get(
 "label", ""),
 "classification": item.get(
 "classification", ""),
 "date": item.get("date", ""),
 })

 df = pd.DataFrame(rows)
 print(f"ClinGen actionability: {gene_symbol} → "
 f"{len(df)} entries")
 return df
```

## 4. ClinGen integrationpipeline

```python
def clingen_pipeline(gene_symbols,
 output_dir="results"):
 """
 ClinGen integrationpipeline。

 Parameters:
 gene_symbols: list[str] — gene symbol list
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) Gene-disease validity
 validity_df = clingen_gene_validity_batch(
 gene_symbols)
 if not validity_df.empty:
 validity_df.to_csv(
 output_dir / "clingen_validity.csv",
 index=False)

 # 2) Dosage sensitivity
 dosage_results = []
 for sym in gene_symbols:
 dos = clingen_dosage_sensitivity(sym)
 if not dos.empty:
 dosage_results.append(dos)
 if dosage_results:
 dosage_df = pd.concat(dosage_results,
 ignore_index=True)
 dosage_df.to_csv(
 output_dir / "clingen_dosage.csv",
 index=False)

 # 3) Actionability
 action_results = []
 for sym in gene_symbols:
 act = clingen_actionability(sym)
 if not act.empty:
 action_results.append(act)
 if action_results:
 action_df = pd.concat(action_results,
 ignore_index=True)
 action_df.to_csv(
 output_dir / "clingen_actionability.csv",
 index=False)

 print(f"ClinGen pipeline → {output_dir}")
 return {"validity": validity_df}
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
variant-interpretation → clingen-curation → clinical-decision-support
 (ClinVar/ACMG) (GDV/DOS/ACT) (support)
 │ │ ↓
 variant-effect-prediction ─┘ pharmacogenomics
 (SpliceAI/CADD) (PGx )
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/clingen_validity.csv` | gene-disease | → genetic-counseling |
| `results/clingen_dosage.csv` | amount | → cnv-analysis |
| `results/clingen_actionability.csv` | possible | → precision-medicine |
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
