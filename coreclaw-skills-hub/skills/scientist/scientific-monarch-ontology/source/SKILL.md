---
name: scientific-monarch-ontology
description: |
 Monarch ontology skill. Monarch Initiative queries for disease-gene associations, phenotype ontology navigation, cross-species phenotype comparison, and knowledge graph exploration.
tu_tools:
 - key: monarch
 name: Monarch Initiative
 description: disease-tabletype-geneintegration API
---

# Scientific Monarch Initiative Ontology

Monarch Initiative API utilizingdisease-gene-tabletype
retrievalHPO 
searchpipeline is provided。

## When to Use

- disease's genetabletype (HPO) is searchedand
- genefromdiseasetabletypewhen needed
- HPO forwhen needed
- for's degreecalculationwhen needed
- disease-tabletype-gene'sintegrationwhen needed

---

## Quick Start

## 1. disease-gene-tabletype

```python
import requests
import pandas as pd

MONARCH_API = "https://api.monarchinitiative.org/v3/api"


def monarch_disease_genes(disease_id, limit=50):
 """
 Monarch — disease→generetrieval。

 Parameters:
 disease_id: str — disease ID
 (example: "MONDO:0007254" = breast cancer)
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/association"
 params = {
 "subject": disease_id,
 "category": "biolink:GeneToDiseaseAssociation",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 obj = item.get("object", {})
 rows.append({
 "disease_id": disease_id,
 "gene_id": obj.get("id", ""),
 "gene_label": obj.get("label", ""),
 "relation": item.get("predicate", ""),
 "source": "; ".join(
 item.get("provided_by", [])),
 })

 df = pd.DataFrame(rows)
 print(f"Monarch disease→genes: {disease_id} "
 f"→ {len(df)} genes")
 return df


def monarch_disease_phenotypes(disease_id, limit=100):
 """
 Monarch — disease→tabletype (HPO) retrieval。

 Parameters:
 disease_id: str — disease ID
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/association"
 params = {
 "subject": disease_id,
 "category":
 "biolink:DiseaseToPhenotypicFeatureAssociation",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 obj = item.get("object", {})
 rows.append({
 "disease_id": disease_id,
 "phenotype_id": obj.get("id", ""),
 "phenotype_label": obj.get("label", ""),
 "frequency": item.get("frequency_qualifier",
 ""),
 "onset": item.get("onset_qualifier", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Monarch disease→phenotypes: {disease_id} "
 f"→ {len(df)} HPO terms")
 return df
```

## 2. gene→disease

```python
def monarch_gene_diseases(gene_id, limit=50):
 """
 Monarch — gene→diseaseretrieval。

 Parameters:
 gene_id: str — gene ID
 (example: "HGNC:1100" = BRCA1)
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/association"
 params = {
 "subject": gene_id,
 "category": "biolink:GeneToDiseaseAssociation",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 obj = item.get("object", {})
 rows.append({
 "gene_id": gene_id,
 "disease_id": obj.get("id", ""),
 "disease_label": obj.get("label", ""),
 "relation": item.get("predicate", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Monarch gene→diseases: {gene_id} "
 f"→ {len(df)} diseases")
 return df
```

## 3. searchfor

```python
def monarch_search(query, category=None, limit=25):
 """
 Monarch — search。

 Parameters:
 query: str — search query
 category: str — filter
 (example: "biolink:Disease", "biolink:Gene",
 "biolink:PhenotypicFeature")
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/search"
 params = {"q": query, "limit": limit}
 if category:
 params["category"] = category

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 rows.append({
 "id": item.get("id", ""),
 "label": item.get("name", ""),
 "category": item.get("category", ""),
 "description": (item.get("description", "")
 or "")[:200],
 })

 df = pd.DataFrame(rows)
 print(f"Monarch search: '{query}' → {len(df)}")
 return df
```

## 4. Monarch integrationpipeline

```python
def monarch_pipeline(disease_query,
 output_dir="results"):
 """
 Monarch integrationpipeline。

 Parameters:
 disease_query: str — disease or ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) diseasesearch
 diseases = monarch_search(disease_query,
 category="biolink:Disease")
 diseases.to_csv(output_dir / "monarch_diseases.csv",
 index=False)

 if diseases.empty:
 print(f"Monarch: '{disease_query}' not found")
 return {"diseases": diseases}

 disease_id = diseases.iloc[0]["id"]

 # 2) gene
 genes = monarch_disease_genes(disease_id)
 genes.to_csv(output_dir / "monarch_genes.csv",
 index=False)

 # 3) tabletype (HPO)
 phenotypes = monarch_disease_phenotypes(disease_id)
 phenotypes.to_csv(
 output_dir / "monarch_phenotypes.csv",
 index=False)

 print(f"Monarch pipeline: {disease_query} "
 f"→ {output_dir}")
 return {"genes": genes, "phenotypes": phenotypes}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `monarch` | Monarch Initiative | disease-tabletype-geneintegration |

## Pipeline Integration

```
disease-research → monarch-ontology → rare-disease-genetics
 (GWAS/DisGeNET) (Monarch API) (OMIM/Orphanet)
 │ │ ↓
variant-interpretation ───┘ ontology-enrichment
 (ClinVar/ACMG) (EFO/OLS/Enrichr)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/monarch_diseases.csv` | diseasesearchresults | → disease-research |
| `results/monarch_genes.csv` | gene | → variant-interpretation |
| `results/monarch_phenotypes.csv` | HPO tabletype | → rare-disease-genetics |
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
