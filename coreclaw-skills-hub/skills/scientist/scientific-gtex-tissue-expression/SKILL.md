---
name: scientific-gtex-tissue-expression
description: |
 GTEx tissue expression skill. Tissue-specific gene expression queries from GTEx portal, eQTL analysis, cross-tissue comparison, and gene expression variation analysis.
---

# Scientific GTEx Tissue Expression

GTEx (Genotype-Tissue Expression) Portal REST API v2 utilizing
tissuegene expressionanalysiseQTL searchtissuecomparisonpipeline
is provided.

## When to Use

- gene's tissueexpression is investigatedand
- tissuein eQTL (expression levelshapegene) is searchedand
- multipletissuegene expression is comparedand
- TPM (Transcripts Per Million) expressiondata is retrievedand
- gene expression is evaluatedand
- tissue's geneexpression minwhen needed

---

## Quick Start

## 1. tissuegene expressionretrieval

```python
import requests
import pandas as pd

GTEX_BASE = "https://gtexportal.org/api/v2"


def gtex_gene_expression(gene_id, tissue=None):
 """
 GTEx — tissuegene expression (median TPM) retrieval。

 Parameters:
 gene_id: str — gene symbol or Ensembl ID
 (example: "BRCA1", "ENSG00000012048")
 tissue: str — tissue ID (None all tissues)
 (example: "Breast_Mammary_Tissue")
 """
 url = f"{GTEX_BASE}/expression/medianGeneExpression"
 params = {
 "gencodeId": gene_id,
 "datasetId": "gtex_v8",
 }
 if tissue:
 params["tissueSiteDetailId"] = tissue

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "gene_symbol": item.get("geneSymbol", ""),
 "gencode_id": item.get("gencodeId", ""),
 "tissue": item.get("tissueSiteDetailId", ""),
 "tissue_name": item.get("tissueSiteDetail", ""),
 "median_tpm": item.get("median", 0),
 "sample_count": item.get("numSamples", 0),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("median_tpm", ascending=False)

 print(f"GTEx expression: {gene_id} → "
 f"{len(df)} tissues")
 return df


def gtex_top_tissues(gene_id, top_n=10):
 """
 GTEx — expression leveltoptissue。

 Parameters:
 gene_id: str — gene symbol or Ensembl ID
 top_n: int — toptissuenumber/count
 """
 df = gtex_gene_expression(gene_id)
 top = df.head(top_n) if not df.empty else df
 print(f"GTEx top {top_n} tissues for {gene_id}:")
 for _, row in top.iterrows:
 print(f" {row['tissue_name']}: "
 f"{row['median_tpm']:.2f} TPM "
 f"(n={row['sample_count']})")
 return top
```

## 2. eQTL search

```python
def gtex_eqtl_lookup(gene_id, tissue, variant_id=None):
 """
 GTEx — eQTL 。

 Parameters:
 gene_id: str — gene symbol or Ensembl ID
 tissue: str — tissue ID
 (example: "Liver", "Whole_Blood")
 variant_id: str — ID (optional)
 (example: "rs12345")
 """
 url = f"{GTEX_BASE}/association/singleTissueEqtl"
 params = {
 "gencodeId": gene_id,
 "tissueSiteDetailId": tissue,
 "datasetId": "gtex_v8",
 }
 if variant_id:
 params["variantId"] = variant_id

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "gene_symbol": item.get("geneSymbol", ""),
 "variant_id": item.get("variantId", ""),
 "tissue": tissue,
 "pvalue": item.get("pValue"),
 "nes": item.get("nes"), # normalized effect size
 "maf": item.get("maf"),
 "ref": item.get("ref", ""),
 "alt": item.get("alt", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("pvalue")

 print(f"GTEx eQTL: {gene_id} in {tissue} → "
 f"{len(df)} associations")
 return df
```

## 3. tissuecomparison

```python
def gtex_multi_gene_comparison(gene_ids, tissues=None):
 """
 GTEx — multiplegenemultipletissue'sexpressioncomparison。

 Parameters:
 gene_ids: list[str] — gene list
 tissues: list[str] — tissue list (None all tissues)
 """
 all_data = []
 for gid in gene_ids:
 try:
 df = gtex_gene_expression(gid)
 if tissues:
 df = df[df["tissue"].isin(tissues)]
 all_data.append(df)
 except Exception as e:
 print(f" Warning: {gid} — {e}")
 continue

 if not all_data:
 return pd.DataFrame

 combined = pd.concat(all_data, ignore_index=True)

 # table: =tissue, =gene, value=TPM
 if not combined.empty:
 pivot = combined.pivot_table(
 index="tissue_name",
 columns="gene_symbol",
 values="median_tpm",
 aggfunc="first",
 )
 print(f"GTEx comparison: {len(gene_ids)} genes × "
 f"{len(pivot)} tissues")
 return pivot

 return combined
```

## 4. GTEx integrationpipeline

```python
def gtex_pipeline(gene_ids, tissues=None,
 output_dir="results"):
 """
 GTEx integrationpipeline。

 Parameters:
 gene_ids: list[str] — gene list
 tissues: list[str] — tissue list (None all tissues)
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) allgene's tissueexpression
 all_expr = []
 for gid in gene_ids:
 try:
 df = gtex_gene_expression(gid)
 df.to_csv(output_dir / f"expression_{gid}.csv",
 index=False)
 all_expr.append(df)
 except Exception:
 continue

 # 2) tissuecomparison
 pivot = gtex_multi_gene_comparison(gene_ids, tissues)
 if isinstance(pivot, pd.DataFrame) and not pivot.empty:
 pivot.to_csv(output_dir / "expression_matrix.csv")

 # 3) eQTL search (toptissue)
 eqtl_results = []
 for gid in gene_ids:
 if all_expr:
 top = all_expr[-1].head(3)
 for _, row in top.iterrows:
 try:
 eqtl = gtex_eqtl_lookup(gid,
 row["tissue"])
 eqtl_results.append(eqtl)
 except Exception:
 continue
 if eqtl_results:
 eqtl_combined = pd.concat(eqtl_results,
 ignore_index=True)
 eqtl_combined.to_csv(output_dir / "eqtl_results.csv",
 index=False)

 print(f"GTEx pipeline: {output_dir}")
 return {"expression": all_expr, "matrix": pivot}
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
gene-expression-transcriptomics → gtex-tissue-expression → variant-interpretation
 (DESeq2/edgeR minexpression) (tissue TPM + eQTL) (variant/mutationevaluation)
 │ │ ↓
 arrayexpress-expression ──────────┘ gwas-catalog
 (ArrayExpress data) │ (GWAS analysis)
 ↓
 disease-research
 (diseasegene)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/expression_*.csv` | genetissueexpression | → disease-research |
| `results/expression_matrix.csv` | genecomparison | → pathway-enrichment |
| `results/eqtl_results.csv` | eQTL | → variant-interpretation |
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
