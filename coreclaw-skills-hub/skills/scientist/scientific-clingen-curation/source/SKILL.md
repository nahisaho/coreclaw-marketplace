---
name: scientific-clingen-curation
description: |
 ClinGen curation skill. Gene-disease validity classification, variant pathogenicity assessment, dosage sensitivity, and clinical actionability curation using ClinGen resources.
tu_tools:
 - key: clingen
 name: ClinGen
 description: ClinGen genome data
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `clingen` | ClinGen | ClinGen genome data |

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
