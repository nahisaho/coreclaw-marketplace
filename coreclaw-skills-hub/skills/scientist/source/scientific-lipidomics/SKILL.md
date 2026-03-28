---
name: scientific-lipidomics
description: |
 analysisskill。LipidMAPS / SwissLipids / LION
 lipiddatabaseintegrationsearchlipidclassification
 lipid MS/MS spectrumlipidpathway
 lipidpipeline。
 TU skill ( REST API + Python library)。
tu_tools:
 - key: lipidmaps
 name: LIPID MAPS
 description: lipidstructureclassificationdatabasesearch
---

# Scientific Lipidomics

LipidMAPS / SwissLipids / LION lipiddatabaseintegration
lipidstructuresearchclassificationMS/MS 
lipidpathwayanalysispipeline is provided。

## When to Use

- LC-MS/MS data's lipid is performedand
- LipidMAPS lipidstructure is searchedand
- lipidfile'sanalysis (fold change/p-value) is performedand
- LION lipidanalysis is performedand
- lipidpathway (lipid/lipidmetabolism) visualizationwhen needed

---

## Quick Start

## 1. LipidMAPS structuresearch

```python
import requests
import pandas as pd

LIPIDMAPS_API = "https://www.lipidmaps.org/rest"


def lipidmaps_search(name=None, formula=None,
 mass=None, tolerance=0.01):
 """
 LipidMAPS — lipidstructuresearch。

 Parameters:
 name: str | None — lipid (partial)
 formula: str | None — moleculeformula
 mass: float | None — amount
 tolerance: float — amount (Da)
 """
 if mass is not None:
 url = (f"{LIPIDMAPS_API}/compound/lm_id/"
 f"mass/{mass}/{tolerance}")
 elif name:
 url = (f"{LIPIDMAPS_API}/compound/lm_id/"
 f"name/{name}")
 elif formula:
 url = (f"{LIPIDMAPS_API}/compound/lm_id/"
 f"formula/{formula}")
 else:
 print("LipidMAPS: provide name, formula, "
 "or mass")
 return pd.DataFrame

 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 if isinstance(data, dict):
 data = [data]

 rows = []
 for item in data:
 rows.append({
 "lm_id": item.get("lm_id", ""),
 "name": item.get("name", ""),
 "sys_name": item.get(
 "systematic_name", ""),
 "formula": item.get("formula", ""),
 "mass": item.get("mass", 0),
 "main_class": item.get(
 "main_class", ""),
 "sub_class": item.get("sub_class", ""),
 })

 df = pd.DataFrame(rows)
 print(f"LipidMAPS: {len(df)} lipids found")
 return df


def lipidmaps_classification(lm_id):
 """
 LipidMAPS — lipidclassificationretrieval。

 Parameters:
 lm_id: str — LipidMAPS ID (example: "LMFA01010001")
 """
 url = (f"{LIPIDMAPS_API}/compound/"
 f"lm_id/{lm_id}/all")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 classification = {
 "lm_id": data.get("lm_id", ""),
 "category": data.get("core", ""),
 "main_class": data.get("main_class", ""),
 "sub_class": data.get("sub_class", ""),
 "class_level4": data.get(
 "class_level4", ""),
 "smiles": data.get("smiles", ""),
 "inchi_key": data.get("inchi_key", ""),
 }

 print(f"LipidMAPS: {lm_id} → "
 f"{classification['main_class']} / "
 f"{classification['sub_class']}")
 return classification
```

## 2. lipidanalysis

```python
import numpy as np
from scipy import stats


def lipid_differential_analysis(data, groups,
 fdr_threshold=0.05):
 """
 lipidanalysis (Fold Change + t-test)。

 Parameters:
 data: pd.DataFrame — lipiddegree
 (=, =lipid)
 groups: list[int] — looplabel (0 or 1)
 fdr_threshold: float — FDR threshold
 """
 from statsmodels.stats.multitest import (
 multipletests)

 groups = np.array(groups)
 g0 = data[groups == 0]
 g1 = data[groups == 1]

 results = []
 for lipid in data.columns:
 mean0 = g0[lipid].mean
 mean1 = g1[lipid].mean
 fc = (mean1 / mean0 if mean0 > 0
 else np.inf)
 log2fc = np.log2(fc) if fc > 0 else 0
 _, pval = stats.ttest_ind(
 g0[lipid], g1[lipid])
 results.append({
 "lipid": lipid,
 "mean_ctrl": round(mean0, 4),
 "mean_case": round(mean1, 4),
 "fold_change": round(fc, 4),
 "log2FC": round(log2fc, 4),
 "pvalue": pval,
 })

 df = pd.DataFrame(results)
 _, fdr, _, _ = multipletests(
 df["pvalue"], method="fdr_bh")
 df["fdr"] = fdr
 df["significant"] = df["fdr"] < fdr_threshold

 n_sig = df["significant"].sum
 n_up = ((df["significant"]) &
 (df["log2FC"] > 0)).sum
 n_down = ((df["significant"]) &
 (df["log2FC"] < 0)).sum
 print(f"Lipid DA: {n_sig} significant "
 f"({n_up} up, {n_down} down)")
 return df.sort_values("pvalue")
```

## 3. lipid

```python
def lipid_subclass_enrichment(
 sig_lipids, all_lipids, class_map):
 """
 lipid (Fisher exact)。

 Parameters:
 sig_lipids: list[str] — significantlipid
 all_lipids: list[str] — alllipid
 class_map: dict — {lipid: subclass} mapping
 """
 from scipy.stats import fisher_exact

 sig_set = set(sig_lipids)
 all_set = set(all_lipids)

 # 
 subclasses = set(class_map.values)
 results = []
 for sc in subclasses:
 sc_all = {l for l, c in class_map.items
 if c == sc and l in all_set}
 sc_sig = sc_all & sig_set
 a = len(sc_sig)
 b = len(sig_set) - a
 c = len(sc_all) - a
 d = len(all_set) - a - b - c
 if a == 0:
 continue
 _, pval = fisher_exact(
 [[a, b], [c, d]],
 alternative="greater")
 results.append({
 "subclass": sc,
 "sig_in_class": a,
 "total_in_class": len(sc_all),
 "pvalue": pval,
 "ratio": round(a / len(sc_all), 3),
 })

 df = pd.DataFrame(results).sort_values("pvalue")
 print(f"Subclass enrichment: "
 f"{(df['pvalue'] < 0.05).sum} "
 f"significant subclasses")
 return df
```

## 4. integrationpipeline

```python
def lipidomics_pipeline(data, groups,
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 data: pd.DataFrame — lipiddegree
 groups: list[int] — looplabel
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) analysis
 da = lipid_differential_analysis(data, groups)
 da.to_csv(output_dir / "lipid_da.csv",
 index=False)

 # 2) LipidMAPS annotation
 annotations = []
 for lipid in data.columns[:30]:
 result = lipidmaps_search(name=lipid)
 if not result.empty:
 row = result.iloc[0].to_dict
 row["query"] = lipid
 annotations.append(row)
 if annotations:
 ann_df = pd.DataFrame(annotations)
 ann_df.to_csv(
 output_dir / "lipid_annotations.csv",
 index=False)

 print(f"Lipidomics pipeline → {output_dir}")
 return {"da": da}
```

---

## Pipeline Integration

```
metabolomics → lipidomics → pathway-enrichment
 (LC-MS allmetabolite) (lipid) (lipidmetabolismpathway)
 │ │ ↓
 metabolomics-network ─┘ multi-omics
 (metabolitecorrelation) (omicsintegration)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/lipid_da.csv` | lipid | → biomarker-discovery |
| `results/lipid_annotations.csv` | LipidMAPS note | → pathway-enrichment |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `lipidmaps` | LIPID MAPS | lipidstructureclassificationdatabasesearch |
---

## Harness Optimization (v0.4.0)

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
