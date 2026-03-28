---
name: scientific-pharmgkb-pgx
description: |
 PharmGKB pharmacogenomics skill. PharmGKB clinical annotation queries, drug-gene interaction lookup, dosing guideline retrieval, and pharmacogenomic pathway analysis.
tu_tools:
 - key: pharmgkb
 name: PharmGKB
 description: annotationdruggenePGx 
---

# Scientific PharmGKB PGx

PharmGKB (Pharmacogenomics Knowledgebase) REST API utilizing
annotationdruggeneinteractionamount
guideline searchpipeline is provided。

## When to Use

- drug and genevariant/mutation's is investigatedand
- annotation  is searchedand
- amount (CPIC/DPWG) is retrievedand
- and tabletype'ssupport is verifiedand
- drug's informationretrievalwhen needed
- 'sdrugselection is supportedand

---

## Quick Start

## 1. druggenesearch

```python
import requests
import pandas as pd

PGKB_BASE = "https://api.pharmgkb.org/v1/data"


def pharmgkb_search_drugs(query, limit=50):
 """
 PharmGKB — drugsearch。

 Parameters:
 query: str — drug (example: "warfarin", "clopidogrel")
 limit: int — maximum results
 """
 url = f"{PGKB_BASE}/chemical"
 params = {"name": query, "view": "max"}

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "pharmgkb_id": item.get("id", ""),
 "name": item.get("name", ""),
 "generic_names": "; ".join(
 item.get("genericNames", [])),
 "trade_names": "; ".join(
 item.get("tradeNames", [])[:5]),
 "type": item.get("type", ""),
 "cross_references": len(
 item.get("crossReferences", [])),
 })

 df = pd.DataFrame(results)
 print(f"PharmGKB drugs: {len(df)} results "
 f"(query='{query}')")
 return df


def pharmgkb_search_genes(query, limit=50):
 """
 PharmGKB — genesearch。

 Parameters:
 query: str — gene symbol (example: "CYP2D6")
 limit: int — maximum results
 """
 url = f"{PGKB_BASE}/gene"
 params = {"symbol": query, "view": "max"}

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "pharmgkb_id": item.get("id", ""),
 "symbol": item.get("symbol", ""),
 "name": item.get("name", ""),
 "chromosome": item.get("chromosomeFormatted", ""),
 "cpic_gene": item.get("cpicGene", False),
 "has_prescribing_info": item.get(
 "hasPrescribingInfo", False),
 })

 df = pd.DataFrame(results)
 print(f"PharmGKB genes: {len(df)} results "
 f"(query='{query}')")
 return df
```

## 2. annotationretrieval

```python
def pharmgkb_clinical_annotations(gene_or_drug,
 search_type="gene"):
 """
 PharmGKB — annotationsearch。

 Parameters:
 gene_or_drug: str — gene symbol or drug
 search_type: str — "gene" or "drug"
 """
 url = f"{PGKB_BASE}/clinicalAnnotation"
 params = {"view": "max"}

 if search_type == "gene":
 # gene search
 gene_url = f"{PGKB_BASE}/gene"
 g_resp = requests.get(gene_url,
 params={"symbol": gene_or_drug},
 timeout=30)
 g_resp.raise_for_status
 genes = g_resp.json.get("data", [])
 if genes:
 params["relatedGenes.id"] = genes[0].get("id", "")
 else:
 # drug search
 drug_url = f"{PGKB_BASE}/chemical"
 d_resp = requests.get(drug_url,
 params={"name": gene_or_drug},
 timeout=30)
 d_resp.raise_for_status
 drugs = d_resp.json.get("data", [])
 if drugs:
 params["relatedChemicals.id"] = drugs[0].get("id", "")

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 genes = [g.get("symbol", "")
 for g in item.get("relatedGenes", [])]
 drugs = [c.get("name", "")
 for c in item.get("relatedChemicals", [])]
 results.append({
 "annotation_id": item.get("id", ""),
 "level": item.get("level", ""),
 "score": item.get("score", ""),
 "genes": "; ".join(genes),
 "drugs": "; ".join(drugs),
 "phenotype_category": item.get(
 "phenotypeCategory", ""),
 "sentences": (item.get("textHtml") or "")[:300],
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("level")

 print(f"PharmGKB annotations: {len(df)} "
 f"({search_type}={gene_or_drug})")
 return df
```

## 3. amountretrieval

```python
def pharmgkb_dosing_guidelines(drug_name=None, gene=None):
 """
 PharmGKB — amount (CPIC/DPWG) search。

 Parameters:
 drug_name: str — drug
 gene: str — gene symbol
 """
 url = f"{PGKB_BASE}/guideline"
 params = {"view": "max"}

 if drug_name:
 params["relatedChemicals.name"] = drug_name
 if gene:
 params["relatedGenes.symbol"] = gene

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 genes = [g.get("symbol", "")
 for g in item.get("relatedGenes", [])]
 drugs = [c.get("name", "")
 for c in item.get("relatedChemicals", [])]
 results.append({
 "guideline_id": item.get("id", ""),
 "name": item.get("name", ""),
 "source": item.get("source", ""),
 "genes": "; ".join(genes),
 "drugs": "; ".join(drugs),
 "recommendation": (item.get("textHtml") or "")[:500],
 })

 df = pd.DataFrame(results)
 print(f"PharmGKB guidelines: {len(df)} "
 f"(drug={drug_name}, gene={gene})")
 return df
```

## 4. PharmGKB integrationpipeline

```python
def pharmgkb_pipeline(drug_name, genes=None,
 output_dir="results"):
 """
 PharmGKB integrationpipeline。

 Parameters:
 drug_name: str — drug
 genes: list[str] — gene list
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) drugsearch
 drugs = pharmgkb_search_drugs(drug_name)
 drugs.to_csv(output_dir / "drugs.csv", index=False)

 # 2) drug'sannotation
 annotations = pharmgkb_clinical_annotations(
 drug_name, search_type="drug")
 annotations.to_csv(output_dir / "annotations.csv",
 index=False)

 # 3) amount
 guidelines = pharmgkb_dosing_guidelines(
 drug_name=drug_name)
 guidelines.to_csv(output_dir / "guidelines.csv",
 index=False)

 # 4) geneanalysis
 if genes:
 gene_results = []
 for g in genes:
 try:
 g_ann = pharmgkb_clinical_annotations(
 g, search_type="gene")
 g_ann["query_gene"] = g
 gene_results.append(g_ann)
 except Exception:
 continue
 if gene_results:
 gene_df = pd.concat(gene_results,
 ignore_index=True)
 gene_df.to_csv(
 output_dir / "gene_annotations.csv",
 index=False)

 print(f"PharmGKB pipeline: {output_dir}")
 return {
 "drugs": drugs,
 "annotations": annotations,
 "guidelines": guidelines,
 }
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `pharmgkb` | PharmGKB | annotationdruggenePGx |

## Pipeline Integration

```
pharmacogenomics → pharmgkb-pgx → clinical-decision-support
 (PGx analysisall) (PharmGKB API) (clinical decision support)
 │ │ ↓
 drug-discovery ──────┘ precision-oncology
 (drug) │ (tumor)
 ↓
 variant-interpretation
 (variant/mutation)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/drugs.csv` | druginformation | → drug-discovery |
| `results/annotations.csv` | annotation | → variant-interpretation |
| `results/guidelines.csv` | amount | → clinical-decision-support |
| `results/gene_annotations.csv` | geneannotation | → pharmacogenomics |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
