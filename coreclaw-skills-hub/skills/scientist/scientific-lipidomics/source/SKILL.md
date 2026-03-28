---
name: scientific-lipidomics
description: |
 Lipidomics skill. Lipid species identification, quantification, lipid class profiling, lipidome-wide association, and lipidomics pathway analysis.
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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
