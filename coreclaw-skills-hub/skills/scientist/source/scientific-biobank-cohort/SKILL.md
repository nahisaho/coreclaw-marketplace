---
name: scientific-biobank-cohort
description: |
 large-scaledataanalysisskill。UK Biobank /
 BBJ / All of Us 'slarge-scaledatafor/against
 searchGWAS summaryPheWAS pipeline。
---

# Scientific Biobank Cohort

UK Biobank (BBJ)All of Us 'slarge-scale
data utilizingsearchGWAS summary
PheWAS analysispipeline is provided。

## When to Use

- 's is searchedand
- GWAS summarydatavisualizationwhen needed
- PheWAS (Phenome-Wide Association Study) is performedand
- 's basicwhen needed
- -comprehensivesearchwhen needed

---

## Quick Start

## 1. search

```python
import pandas as pd
import numpy as np


def phenotype_dictionary(pheno_file, category=None,
 keyword=None):
 """
 — search。

 Parameters:
 pheno_file: str — CSV 
 (UK Biobank Data-Field listing )
 category: str — filter
 keyword: str — keywordfilter
 """
 df = pd.read_csv(pheno_file)

 if category:
 df = df[df["Category"].str.contains(
 category, case=False, na=False)]
 if keyword:
 mask = (
 df["Field"].str.contains(
 keyword, case=False, na=False)
 | df["Description"].str.contains(
 keyword, case=False, na=False)
 )
 df = df[mask]

 print(f"Phenotype dict: {len(df)} fields matched")
 return df


def cohort_demographics(pheno_df, age_col="age",
 sex_col="sex"):
 """
 — summary。

 Parameters:
 pheno_df: DataFrame — data
 age_col: str — 
 sex_col: str — 
 """
 summary = {
 "n_participants": len(pheno_df),
 "age_mean": pheno_df[age_col].mean,
 "age_std": pheno_df[age_col].std,
 "sex_distribution": (
 pheno_df[sex_col]
.value_counts(normalize=True)
.to_dict
 ),
 }
 print(f"Cohort: n={summary['n_participants']}, "
 f"age={summary['age_mean']:.1f}±"
 f"{summary['age_std']:.1f}")
 return summary
```

## 2. GWAS summary

```python
def load_gwas_summary(sumstat_file, p_threshold=5e-8,
 sep="\t"):
 """
 GWAS summaryfileloadfilter。

 Parameters:
 sumstat_file: str — summaryfile path
 (TSV: CHR, POS, SNP, A1, A2, BETA, SE, P)
 p_threshold: float — P valuethreshold
 sep: str — delimiter
 """
 df = pd.read_csv(sumstat_file, sep=sep)

 # standardcolumnnormalization
 col_map = {
 "chromosome": "CHR", "chr": "CHR",
 "position": "POS", "pos": "POS", "bp": "POS",
 "rsid": "SNP", "snp": "SNP", "variant_id": "SNP",
 "effect_allele": "A1", "a1": "A1",
 "other_allele": "A2", "a2": "A2",
 "beta": "BETA", "effect_size": "BETA",
 "se": "SE", "standard_error": "SE",
 "pval": "P", "p_value": "P", "pvalue": "P",
 }
 df.columns = [col_map.get(c.lower, c)
 for c in df.columns]

 # filter
 sig = df[df["P"] < p_threshold].copy
 sig.sort_values("P", inplace=True)

 print(f"GWAS summary: {len(df)} total, "
 f"{len(sig)} significant (P<{p_threshold})")
 return sig


def manhattan_data(gwas_df, chr_col="CHR",
 pos_col="POS", p_col="P"):
 """
 Manhattan plotfordatatransformation。

 Parameters:
 gwas_df: DataFrame — GWAS summary
 chr_col: str — 
 pos_col: str — 
 p_col: str — P value
 """
 df = gwas_df.copy
 df["-log10P"] = -np.log10(df[p_col])

 # calculation
 chr_lengths = (
 df.groupby(chr_col)[pos_col].max
.sort_index
 )
 chr_offsets = chr_lengths.cumsum.shift(1).fillna(0)
 df["cumpos"] = df.apply(
 lambda r: r[pos_col] + chr_offsets.get(
 r[chr_col], 0),
 axis=1)

 print(f"Manhattan data: {len(df)} variants, "
 f"max -log10P={df['-log10P'].max:.1f}")
 return df
```

## 3. PheWAS (Phenome-Wide Association Study)

```python
def phewas_analysis(genotype_series, pheno_df,
 pheno_cols=None,
 p_threshold=0.05):
 """
 PheWAS — 1for/againsttabletype。

 Parameters:
 genotype_series: Series — genetype
 (0/1/2 )
 pheno_df: DataFrame — data
 pheno_cols: list — testingtabletype
 p_threshold: float — Bonferroni threshold
 """
 from scipy import stats

 if pheno_cols is None:
 pheno_cols = [c for c in pheno_df.columns
 if pheno_df[c].dtype in
 [np.float64, np.int64]]

 results = []
 for col in pheno_cols:
 mask = pheno_df[col].notna
 if mask.sum < 50:
 continue
 geno = genotype_series[mask]
 pheno = pheno_df.loc[mask, col]

 # number/countvalue → lineshaperegression 
 slope, intercept, r, p, se = stats.linregress(
 geno, pheno)
 results.append({
 "phenotype": col,
 "beta": slope,
 "se": se,
 "p_value": p,
 "n": mask.sum,
 })

 df = pd.DataFrame(results)
 n_tests = len(df)
 bonf = p_threshold / n_tests if n_tests > 0 else 0.05
 df["significant"] = df["p_value"] < bonf
 df.sort_values("p_value", inplace=True)

 n_sig = df["significant"].sum
 print(f"PheWAS: {n_tests} phenotypes tested, "
 f"{n_sig} significant (Bonferroni)")
 return df
```

## 4. integrationpipeline

```python
def biobank_pipeline(sumstat_file, pheno_file=None,
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 sumstat_file: str — GWAS summaryfile
 pheno_file: str — file
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) GWAS summaryload
 gwas = load_gwas_summary(sumstat_file)
 gwas.to_csv(output_dir / "gwas_significant.csv",
 index=False)

 # 2) Manhattan plotdata
 manhattan = manhattan_data(gwas)
 manhattan.to_csv(
 output_dir / "manhattan_data.csv", index=False)

 # 3) search (usepossible)
 if pheno_file:
 pheno_dict = phenotype_dictionary(pheno_file)
 pheno_dict.to_csv(
 output_dir / "phenotype_dict.csv",
 index=False)

 print(f"Biobank pipeline → {output_dir}")
 return {"gwas": gwas, "manhattan": manhattan}
```

---

## Pipeline Integration

```
epidemiology-public-health → biobank-cohort → population-genetics
  (GWAS/PheWAS) (analysis)
 │ │ ↓
 mendelian-randomization ───────┘ rare-disease-genetics
 (causal inference) (Mendelian analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gwas_significant.csv` | Genome-wide significant SNP | → population-genetics |
| `results/manhattan_data.csv` | Manhattan plotdata | → GWAS visualization |
| `results/phenotype_dict.csv` | | → PheWAS |

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
