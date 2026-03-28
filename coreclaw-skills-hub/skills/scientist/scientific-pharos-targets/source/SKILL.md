---
name: scientific-pharos-targets
description: |
 Pharos targets skill. Target Development Level (TDL) classification, understudied protein identification, Illuminating the Druggable Genome (IDG) resource queries.
tu_tools:
 - key: pharos
 name: Pharos
 description: IDG Pharos/TCRD target knowledge base
---

# Scientific Pharos Targets

IDG (Illuminating the Druggable Genome) Pharos GraphQL API
utilizing TDL classificationdisease-
ligandsearchexistingpipeline is provided。

## When to Use

- protein's (Tclin/Tchem/Tbio/Tdark) is verifiedand
- IDG 'sinvestigationwhen needed
- diseaseligandPPI is searchedand
- Tchem/Tbio from is exploredand
- 'sdruggabilitycomparison is performedand

---

## Quick Start

## 1. TDL classificationsearch

```python
import requests
import pandas as pd

PHAROS_API = "https://pharos-api.ncats.io/graphql"


def pharos_target(gene_symbol):
 """
 Pharos — detailsinformationretrieval。

 Parameters:
 gene_symbol: str — gene symbol (example: "ACE2")
 """
 query = """
 query targetDetails($sym: String!) {
 target(q: {sym: $sym}) {
 name
 sym
 tdl
 fam
 novelty
 description
 uniprotId: accession
 diseaseCount
 ligandCount
 ppiCount
 }
 }
 """
 resp = requests.post(
 PHAROS_API,
 json={"query": query,
 "variables": {"sym": gene_symbol}},
 timeout=30)
 resp.raise_for_status
 data = resp.json.get("data", {}).get("target", {})

 if not data:
 print(f"Pharos: {gene_symbol} not found")
 return {}

 print(f"Pharos: {gene_symbol} → TDL={data['tdl']}, "
 f"fam={data.get('fam', 'N/A')}, "
 f"diseases={data.get('diseaseCount', 0)}, "
 f"ligands={data.get('ligandCount', 0)}")
 return data


def pharos_target_list(gene_symbols):
 """
 Pharos — multiple TDL batchretrieval。

 Parameters:
 gene_symbols: list[str] — gene symbol list
 """
 results = []
 for sym in gene_symbols:
 data = pharos_target(sym)
 if data:
 results.append(data)

 df = pd.DataFrame(results)
 if not df.empty:
 tdl_counts = df["tdl"].value_counts
 print(f"TDL distribution: "
 f"{tdl_counts.to_dict}")
 return df
```

## 2. disease-

```python
def pharos_target_diseases(gene_symbol, top_n=20):
 """
 Pharos — 'sdiseaseretrieval。

 Parameters:
 gene_symbol: str — gene symbol
 top_n: int — top count
 """
 query = """
 query targetDiseases($sym: String!, $top: Int!) {
 target(q: {sym: $sym}) {
 sym
 diseases(top: $top) {
 name
 associationCount
 datasource_count
 }
 }
 }
 """
 resp = requests.post(
 PHAROS_API,
 json={"query": query,
 "variables": {"sym": gene_symbol,
 "top": top_n}},
 timeout=30)
 resp.raise_for_status
 target = resp.json.get("data", {}).get(
 "target", {})
 diseases = target.get("diseases", [])

 df = pd.DataFrame(diseases)
 print(f"Pharos diseases: {gene_symbol} → "
 f"{len(df)} associations")
 return df
```

## 3. ligandsearch

```python
def pharos_target_ligands(gene_symbol, top_n=20):
 """
 Pharos — 'sligand/activationretrieval。

 Parameters:
 gene_symbol: str — gene symbol
 top_n: int — top count
 """
 query = """
 query targetLigands($sym: String!, $top: Int!) {
 target(q: {sym: $sym}) {
 sym
 ligands(top: $top) {
 name
 smiles
 isdrug
 actcnt
 activities {
 type
 value
 moa
 }
 }
 }
 }
 """
 resp = requests.post(
 PHAROS_API,
 json={"query": query,
 "variables": {"sym": gene_symbol,
 "top": top_n}},
 timeout=30)
 resp.raise_for_status
 target = resp.json.get("data", {}).get(
 "target", {})
 ligands = target.get("ligands", [])

 rows = []
 for lig in ligands:
 rows.append({
 "name": lig.get("name", ""),
 "smiles": lig.get("smiles", ""),
 "is_drug": lig.get("isdrug", False),
 "activity_count": lig.get("actcnt", 0),
 })

 df = pd.DataFrame(rows)
 n_drugs = df["is_drug"].sum if not df.empty else 0
 print(f"Pharos ligands: {gene_symbol} → "
 f"{len(df)} compounds ({n_drugs} drugs)")
 return df
```

## 4. Pharos integrationpipeline

```python
def pharos_pipeline(gene_symbols,
 output_dir="results"):
 """
 Pharos integrationpipeline。

 Parameters:
 gene_symbols: list[str] — gene symbol list
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) TDL classification
 targets = pharos_target_list(gene_symbols)
 targets.to_csv(output_dir / "pharos_targets.csv",
 index=False)

 # 2) disease (top)
 all_diseases = []
 for sym in gene_symbols[:10]:
 diseases = pharos_target_diseases(sym)
 diseases["target"] = sym
 all_diseases.append(diseases)
 if all_diseases:
 disease_df = pd.concat(all_diseases,
 ignore_index=True)
 disease_df.to_csv(
 output_dir / "pharos_diseases.csv",
 index=False)

 # 3) ligand
 all_ligands = []
 for sym in gene_symbols[:10]:
 ligands = pharos_target_ligands(sym)
 ligands["target"] = sym
 all_ligands.append(ligands)
 if all_ligands:
 ligand_df = pd.concat(all_ligands,
 ignore_index=True)
 ligand_df.to_csv(
 output_dir / "pharos_ligands.csv",
 index=False)

 print(f"Pharos pipeline → {output_dir}")
 return {"targets": targets}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `pharos` | Pharos | IDG Pharos/TCRD target knowledge base |

## Pipeline Integration

```
drug-target-profiling → pharos-targets → drug-repurposing
 (DGIdb/) (TDL/IDG) 
 │ │ ↓
 pharmacology-targets ─────┘ compound-screening
 (BindingDB/GtoPdb) (ZINC library)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/pharos_targets.csv` | TDL classificationresults | → drug-target-profiling |
| `results/pharos_diseases.csv` | disease | → disease-research |
| `results/pharos_ligands.csv` | ligand/ | → drug-repurposing |

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
