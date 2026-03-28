---
name: scientific-regulatory-genomics
description: |
 skill。RegulomeDB 、
 ReMap factorbindingmapping、4D Nucleome (4DN) genomestructure
 analysis's integrationpipeline。
---

# Scientific Regulatory Genomics

RegulomeDB / ReMap / 4D Nucleome integration
 (analysis) pipeline is provided。

## When to Use

- 's is evaluatedand
- RegulomeDB SNP 'swhen needed
- ReMap factorbinding'smapping is verifiedand
- 4DN datafromgenomestructure (TAD/loop) analysiswhen needed
- GWAS 'swhen needed

---

## Quick Start

## 1. RegulomeDB 

```python
import requests
import pandas as pd

REGULOMEDB_API = "https://regulomedb.org/regulome-search"


def score_regulome_variants(variants):
 """
 RegulomeDB — 's 。

 Parameters:
 variants: list — (rsID or chr:pos shapeformula)
 e.g., ["rs12345", "chr1:109274570"]

 """
 results = []
 for variant in variants:
 params = {"regions": variant, "genome": "GRCh38", "format": "json"}
 resp = requests.get(REGULOMEDB_API, params=params)
 if resp.status_code != 200:
 results.append({"variant": variant, "score": None, "error": True})
 continue

 data = resp.json
 for hit in data.get("@graph", []):
 results.append({
 "variant": variant,
 "regulome_score": hit.get("regulome_score", {}).get("ranking", ""),
 "probability": hit.get("regulome_score", {}).get("probability", ""),
 "chrom": hit.get("chrom", ""),
 "start": hit.get("start", ""),
 "end": hit.get("end", ""),
 "dnase": hit.get("dnase", ""),
 "proteins_binding": hit.get("proteins_binding", []),
 "motifs": hit.get("motifs", []),
 "eqtls": hit.get("eqtls", []),
 "chromatin_state": hit.get("chromatin_state", {}),
 })

 df = pd.DataFrame(results)
 if not df.empty and "regulome_score" in df.columns:
 high_func = (df["regulome_score"].astype(str).str.match(r"^[12]")).sum
 print(f"RegulomeDB: {len(variants)} variants scored, "
 f"{high_func} with high regulatory function (score 1-2)")
 return df
```

## 2. ReMap factorbindingmapping

```python
REMAP_API = "https://remap.univ-amu.fr/api/v1"


def search_remap_binding(chrom, start, end, genome="hg38"):
 """
 ReMap — genome'sfactor/bindingmapping。

 Parameters:
 chrom: str — (e.g., "chr1")
 start: int — startcoordinates
 end: int — endcoordinates
 genome: str — genomeassembly ("hg38", "hg19", "mm10")

 """
 params = {
 "chrom": chrom,
 "start": start,
 "end": end,
 "genome": genome,
 }
 resp = requests.get(f"{REMAP_API}/peaks/search", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for peak in data.get("peaks", []):
 results.append({
 "tf_name": peak.get("tf_name", ""),
 "biotype": peak.get("biotype", ""),
 "cell_type": peak.get("cell_type", ""),
 "experiment": peak.get("experiment_accession", ""),
 "peak_start": peak.get("start", ""),
 "peak_end": peak.get("end", ""),
 "score": peak.get("score", ""),
 })

 df = pd.DataFrame(results)
 unique_tfs = df["tf_name"].nunique if not df.empty else 0
 print(f"ReMap {chrom}:{start}-{end}: {len(df)} peaks, {unique_tfs} unique TFs")
 return df


def get_remap_tf_targets(tf_name, genome="hg38"):
 """
 ReMap — factor's allbindingretrieval。

 Parameters:
 tf_name: str — factor (e.g., "TP53", "CTCF", "STAT3")
 """
 params = {"tf": tf_name, "genome": genome}
 resp = requests.get(f"{REMAP_API}/peaks/tf", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for peak in data.get("peaks", [])[:1000]: # Limit for large TFs
 results.append({
 "chrom": peak.get("chrom", ""),
 "start": peak.get("start", ""),
 "end": peak.get("end", ""),
 "cell_type": peak.get("cell_type", ""),
 "score": peak.get("score", ""),
 })

 df = pd.DataFrame(results)
 print(f"ReMap TF '{tf_name}': {len(df)} binding sites")
 return df
```

## 3. 4D Nucleome (4DN) genomestructure

```python
FOURDN_API = "https://data.4dnucleome.org"


def search_4dn_experiments(query, experiment_type=None):
 """
 4D Nucleome — genomeexperimentdatasearch。

 Parameters:
 query: str — search query (cell、protein)
 experiment_type: str — experiment ("in situ Hi-C", "SPRITE", "GAM")

 """
 params = {
 "searchTerm": query,
 "type": "ExperimentSetReplicate",
 "format": "json",
 }
 if experiment_type:
 params["experiment_type.display_title"] = experiment_type

 resp = requests.get(f"{FOURDN_API}/search/", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("@graph", []):
 results.append({
 "accession": item.get("accession", ""),
 "title": item.get("display_title", ""),
 "experiment_type": item.get("experiment_type", {}).get("display_title", ""),
 "biosource": item.get("biosource_summary", ""),
 "lab": item.get("lab", {}).get("display_title", ""),
 "status": item.get("status", ""),
 })

 df = pd.DataFrame(results)
 print(f"4DN search '{query}': {len(df)} experiment sets")
 return df
```

## 4. integrated analysispipeline

```python
def regulatory_variant_pipeline(variants, genome="hg38"):
 """
 integrated analysis。

 Parameters:
 variants: list — (rsID or chr:pos)
 """
 print("=" * 60)
 print("Regulatory Variant Analysis Pipeline")
 print("=" * 60)

 # Step 1: RegulomeDB scoring
 print("\n[1/3] RegulomeDB scoring...")
 regulome_df = score_regulome_variants(variants)

 # Step 2: ReMap TF binding for high-scoring variants
 print("\n[2/3] ReMap TF binding analysis...")
 remap_results = {}
 for _, row in regulome_df.iterrows:
 if row.get("chrom") and row.get("start"):
 chrom = row["chrom"]
 start = int(row["start"]) - 500
 end = int(row["end"]) + 500
 try:
 remap_df = search_remap_binding(chrom, start, end, genome)
 remap_results[row["variant"]] = remap_df
 except Exception as e:
 print(f" ReMap error for {row['variant']}: {e}")

 # Step 3: Summary
 print("\n[3/3] Summary")
 summary = {
 "total_variants": len(variants),
 "regulome_scored": len(regulome_df),
 "high_regulatory": (
 regulome_df["regulome_score"].astype(str).str.match(r"^[12]")
 ).sum if "regulome_score" in regulome_df.columns else 0,
 "remap_annotated": len(remap_results),
 }
 print(f" Total: {summary['total_variants']}, "
 f"High regulatory: {summary['high_regulatory']}, "
 f"ReMap annotated: {summary['remap_annotated']}")

 return {"regulome": regulome_df, "remap": remap_results, "summary": summary}
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

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/regulome_scores.csv` | | → variant-interpretation, variant-effect-prediction |
| `results/remap_binding.csv` | TF bindingmapping | → epigenomics-chromatin, disease-research |
| `results/4dn_contacts.json` | 3D genomestructuredata | → single-cell-genomics, epigenomics-chromatin |

## Pipeline Integration

```
variant-interpretation ──→ regulatory-genomics ──→ epigenomics-chromatin
 (ACMG/AMP) (RegulomeDB/ReMap/4DN) (ChIP-seq/ATAC)
 │
 ├──→ disease-research (GWAS enhancer)
 ├──→ gene-expression (eQTL/)
 └──→ noncoding-rna (ncRNA )
```
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
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
