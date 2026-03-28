---
name: scientific-civic-evidence
description: |
 CIViC skill。CIViC (Clinical Interpretation
 of Variants in Cancer) REST API using
 moleculefilesearch。
 ToolUniverse integration: civic。
tu_tools:
 - key: civic
 name: CIViC
 description: cancerdatabase
---

# Scientific CIViC Evidence

CIViC (Clinical Interpretation of Variants in Cancer) REST API
utilizingretrieval
moleculefilepipeline is provided。

## When to Use

- cancer's is searchedand
- (prognosisdiagnosis) is retrievedand
- geneand 'ssummary is verifiedand
- moleculefile (Molecular Profile) is searchedand
- (recommended) is retrievedand

---

## Quick Start

## 1. search

```python
import requests
import pandas as pd

CIVIC_API = "https://civicdb.org/api"


def civic_variant_search(gene_name, variant_name=None,
 limit=50):
 """
 CIViC — search。

 Parameters:
 gene_name: str — gene name (example: "BRAF")
 variant_name: str — 
 (example: "V600E")
 limit: int — maximum results
 """
 url = f"{CIVIC_API}/variants"
 params = {"count": limit}

 # gene name search
 gene_url = f"{CIVIC_API}/genes/{gene_name}"
 try:
 resp = requests.get(gene_url, timeout=30)
 if resp.status_code == 200:
 gene_data = resp.json
 else:
 # search API 
 search_url = f"{CIVIC_API}/genes"
 params_g = {"name": gene_name, "count": 5}
 resp = requests.get(search_url,
 params=params_g,
 timeout=30)
 resp.raise_for_status
 records = resp.json.get("records", [])
 gene_data = records[0] if records else {}
 except Exception as e:
 print(f" CIViC gene lookup: {e}")
 gene_data = {}

 if not gene_data:
 return pd.DataFrame

 variants = gene_data.get("variants", [])
 rows = []
 for v in variants[:limit]:
 name = v.get("name", "")
 if variant_name and variant_name.lower \
 not in name.lower:
 continue
 rows.append({
 "variant_id": v.get("id", ""),
 "gene": gene_name,
 "variant_name": name,
 "description": (v.get("description", "")
 [:200]),
 "evidence_count": len(
 v.get("evidence_items", [])),
 })

 df = pd.DataFrame(rows)
 print(f"CIViC variants: {gene_name} → {len(df)}")
 return df


def civic_gene_summary(gene_name):
 """
 CIViC — genesummaryretrieval。

 Parameters:
 gene_name: str — gene name (example: "EGFR")
 """
 url = f"{CIVIC_API}/genes/{gene_name}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 result = {
 "gene_id": data.get("id", ""),
 "name": data.get("name", ""),
 "description": data.get("description", ""),
 "n_variants": len(data.get("variants", [])),
 "aliases": "; ".join(
 data.get("aliases", [])),
 }
 return result
```

## 2. retrieval

```python
def civic_evidence_items(variant_id, limit=50):
 """
 CIViC — retrieval。

 Parameters:
 variant_id: int — ID
 limit: int — maximum results
 """
 url = f"{CIVIC_API}/variants/{variant_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for ev in data.get("evidence_items", [])[:limit]:
 drugs = [d.get("name", "")
 for d in ev.get("drugs", [])]
 rows.append({
 "evidence_id": ev.get("id", ""),
 "variant_id": variant_id,
 "evidence_type": ev.get(
 "evidence_type", ""),
 "evidence_level": ev.get(
 "evidence_level", ""),
 "evidence_direction": ev.get(
 "evidence_direction", ""),
 "clinical_significance": ev.get(
 "clinical_significance", ""),
 "disease": ev.get("disease", {}).get(
 "name", ""),
 "drugs": "; ".join(drugs),
 "rating": ev.get("rating", ""),
 "status": ev.get("status", ""),
 "source_citation": ev.get(
 "source", {}).get("citation", ""),
 })

 df = pd.DataFrame(rows)
 print(f"CIViC evidence: variant {variant_id} "
 f"→ {len(df)} items")
 return df
```

## 3. retrieval

```python
def civic_assertions(gene_name=None, limit=50):
 """
 CIViC — (recommended) retrieval。

 Parameters:
 gene_name: str — gene namefilter
 limit: int — maximum results
 """
 url = f"{CIVIC_API}/assertions"
 params = {"count": limit}

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for a in data.get("records", []):
 genes = [g.get("name", "")
 for g in a.get("genes", [])]
 if gene_name and gene_name not in genes:
 continue
 drugs = [d.get("name", "")
 for d in a.get("drugs", [])]
 rows.append({
 "assertion_id": a.get("id", ""),
 "genes": "; ".join(genes),
 "variant": a.get("variant", {}).get(
 "name", ""),
 "disease": a.get("disease", {}).get(
 "name", ""),
 "drugs": "; ".join(drugs),
 "assertion_type": a.get(
 "assertion_type", ""),
 "assertion_direction": a.get(
 "assertion_direction", ""),
 "clinical_significance": a.get(
 "clinical_significance", ""),
 "amp_level": a.get("amp_level", ""),
 "status": a.get("status", ""),
 })

 df = pd.DataFrame(rows)
 print(f"CIViC assertions: {len(df)}")
 return df
```

## 4. CIViC integrationpipeline

```python
def civic_pipeline(gene_name, variant_name=None,
 output_dir="results"):
 """
 CIViC integrationpipeline。

 Parameters:
 gene_name: str — gene name (example: "BRAF")
 variant_name: str — (example: "V600E")
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) genesummary
 summary = civic_gene_summary(gene_name)
 pd.DataFrame([summary]).to_csv(
 output_dir / "civic_gene.csv", index=False)

 # 2) search
 variants = civic_variant_search(gene_name,
 variant_name)
 variants.to_csv(output_dir / "civic_variants.csv",
 index=False)

 # 3) 's
 if not variants.empty:
 top_vid = variants.iloc[0]["variant_id"]
 evidence = civic_evidence_items(top_vid)
 evidence.to_csv(
 output_dir / "civic_evidence.csv",
 index=False)

 # 4) 
 assertions = civic_assertions(gene_name)
 assertions.to_csv(
 output_dir / "civic_assertions.csv",
 index=False)

 print(f"CIViC pipeline: {gene_name} → {output_dir}")
 return {"variants": variants}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `civic` | CIViC | cancer (~12 tools) |

## Pipeline Integration

```
variant-interpretation → civic-evidence → precision-oncology
 (ClinVar ) (CIViC REST) (tumor)
 │ │ ↓
 gnomad-variants ────────────┘ drug-target-profiling
 (frequency) │ 
 ↓
 opentargets-genetics
 (OT -disease)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/civic_gene.csv` | genesummary | → cancer-genomics |
| `results/civic_variants.csv` | list | → variant-interpretation |
| `results/civic_evidence.csv` | | → precision-oncology |
| `results/civic_assertions.csv` | | → pharmacogenomics |
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
