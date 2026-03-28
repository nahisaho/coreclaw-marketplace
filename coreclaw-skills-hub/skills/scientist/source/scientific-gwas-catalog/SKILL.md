---
name: scientific-gwas-catalog
description: |
 GWAS logskill。NHGRI-EBI GWAS Catalog REST API by/viagenome
 researchdatashapegenesearch。
 ---

# Scientific GWAS Catalog

NHGRI-EBI GWAS Catalog REST API utilizing GWAS data
analysisgenepipeline is provided。

## When to Use

- GWAS Catalog fromdisease/shape's is searchedand
- 's Pvalue is retrievedand
- gene's LD blockinformationanalysiswhen needed
- shape PheWAS-like analysis is performedand
- GWAS amount analysiswhen needed
- GWAS datafrom PRS is extractedand

---

## Quick Start

## 1. GWAS search

```python
import requests
import pandas as pd
import numpy as np

GWAS_BASE = "https://www.ebi.ac.uk/gwas/rest/api"


def gwas_search_associations(trait=None, gene=None, variant=None,
 p_upper=5e-8, limit=100):
 """
 GWAS Catalog — search。

 Parameters:
 trait: str — shape/disease EFO ID or name (example: "EFO_0001645")
 gene: str — gene name (example: "BRCA1")
 variant: str — rsID (example: "rs1234567")
 p_upper: float — Pvalue
 limit: int — maximum results
 """
 if trait:
 url = f"{GWAS_BASE}/efoTraits/{trait}/associations"
 elif gene:
 url = f"{GWAS_BASE}/associations/search/findByGene"
 elif variant:
 url = f"{GWAS_BASE}/singleNucleotidePolymorphisms/{variant}/associations"
 else:
 url = f"{GWAS_BASE}/associations"

 params = {"size": limit}
 if gene:
 params["geneName"] = gene

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 associations = data.get("_embedded", {}).get("associations", [])
 results = []
 for assoc in associations:
 p_value = assoc.get("pvalue", 1.0)
 if p_value and float(p_value) > p_upper:
 continue

 loci = assoc.get("loci", [{}])
 genes = []
 for locus in loci:
 for gene_info in locus.get("authorReportedGenes", []):
 genes.append(gene_info.get("geneName", ""))

 snps = []
 for snp_info in assoc.get("snps", []):
 snps.append(snp_info.get("rsId", ""))

 results.append({
 "association_id": assoc.get("associationId", ""),
 "p_value": float(p_value) if p_value else None,
 "p_value_mlog": assoc.get("pvalueMantissa", 0),
 "or_beta": assoc.get("orPerCopyNum", None),
 "beta_num": assoc.get("betaNum", None),
 "beta_direction": assoc.get("betaDirection", ""),
 "ci": assoc.get("range", ""),
 "risk_allele_freq": assoc.get("riskFrequency", ""),
 "snps": "; ".join(snps),
 "genes": "; ".join(genes),
 "trait": assoc.get("efoTraits", [{}])[0].get("trait", "")
 if assoc.get("efoTraits") else "",
 "study_accession": assoc.get("study", {}).get(
 "accessionId", ""),
 })

 df = pd.DataFrame(results)
 print(f"GWAS associations: {len(df)} results "
 f"(trait={trait}, gene={gene}, p<{p_upper})")
 return df.sort_values("p_value") if not df.empty else df
```

## 2. GWAS researchdatasearch

```python
def gwas_search_studies(query=None, efo_trait=None, limit=50):
 """
 GWAS Catalog — researchdatasearch。

 Parameters:
 query: str — search
 efo_trait: str — EFO shape ID
 limit: int — maximum results
 """
 if efo_trait:
 url = f"{GWAS_BASE}/efoTraits/{efo_trait}/studies"
 else:
 url = f"{GWAS_BASE}/studies/search/findByDiseaseTrait"

 params = {"size": limit}
 if query:
 params["diseaseTrait"] = query

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 studies = data.get("_embedded", {}).get("studies", [])
 results = []
 for s in studies:
 results.append({
 "accession": s.get("accessionId", ""),
 "title": s.get("title", ""),
 "pubmed_id": s.get("publicationInfo", {}).get(
 "pubmedId", ""),
 "author": s.get("publicationInfo", {}).get(
 "author", {}).get("fullname", ""),
 "journal": s.get("publicationInfo", {}).get(
 "publication", ""),
 "date": s.get("publicationInfo", {}).get(
 "publicationDate", ""),
 "initial_sample_size": s.get("initialSampleSize", ""),
 "replication_sample_size": s.get(
 "replicationSampleSize", ""),
 "ancestry": s.get("ancestries", []),
 })

 df = pd.DataFrame(results)
 print(f"GWAS studies: {len(df)} results")
 return df
```

## 3. GWAS shapesearchPheWAS

```python
def gwas_phewas(variant_rsid, p_threshold=5e-8):
 """
 GWAS Catalog — PheWAS (shapecross-cuttingsearch)。

 Parameters:
 variant_rsid: str — rsID (example: "rs7903146")
 p_threshold: float — Pvaluethreshold
 """
 url = (f"{GWAS_BASE}/singleNucleotidePolymorphisms/"
 f"{variant_rsid}/associations")
 resp = requests.get(url, params={"size": 500}, timeout=30)
 resp.raise_for_status
 data = resp.json

 associations = data.get("_embedded", {}).get("associations", [])
 results = []
 for assoc in associations:
 p_val = assoc.get("pvalue", 1.0)
 if p_val and float(p_val) > p_threshold:
 continue
 for trait in assoc.get("efoTraits", []):
 results.append({
 "variant": variant_rsid,
 "trait": trait.get("trait", ""),
 "efo_uri": trait.get("shortForm", ""),
 "p_value": float(p_val) if p_val else None,
 "or_beta": assoc.get("orPerCopyNum", None),
 "study": assoc.get("study", {}).get(
 "accessionId", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("p_value")
 print(f"PheWAS {variant_rsid}: {len(df)} trait associations")
 return df
```

## 4. GWAS integrationpipeline

```python
def gwas_catalog_pipeline(trait_query, output_dir="results"):
 """
 GWAS Catalog integrationpipeline。

 Parameters:
 trait_query: str — shape/disease
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) researchsearch
 studies = gwas_search_studies(query=trait_query)
 studies.to_csv(output_dir / "gwas_studies.csv", index=False)

 # 2) 
 assocs = gwas_search_associations(gene=None, trait=None)
 assocs.to_csv(output_dir / "gwas_associations.csv", index=False)

 # 3) 's PheWAS
 if not assocs.empty:
 top_snps = assocs["snps"].str.split("; ").explode.unique[:5]
 phewas_all = []
 for rsid in top_snps:
 if rsid.startswith("rs"):
 phewas = gwas_phewas(rsid)
 phewas_all.append(phewas)
 if phewas_all:
 phewas_df = pd.concat(phewas_all, ignore_index=True)
 phewas_df.to_csv(output_dir / "phewas.csv", index=False)

 print(f"GWAS pipeline: {output_dir}")
 return {"studies": studies, "associations": assocs}
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
disease-research → gwas-catalog → variant-interpretation
 (DisGeNET/OMIM) (GWAS Catalog) (ACMG/AMP)
 │ │ ↓
 population-genetics ──┘ variant-effect-prediction
 (Fst/PCA) │ (CADD/SpliceAI)
 ↓
 precision-oncology
 (significance)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gwas_studies.csv` | GWAS researchdata | → literature-search |
| `results/gwas_associations.csv` | | → variant-interpretation |
| `results/phewas.csv` | PheWAS results | → disease-research |
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
