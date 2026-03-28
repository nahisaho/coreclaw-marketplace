---
name: scientific-stitch-chemical-network
description: |
 STITCH chemical network skill. STITCH chemical-protein interaction queries, chemical similarity networks, and drug-target network construction.
tu_tools:
 - key: stitch
 name: STITCH
 description: -proteininteractionnetwork (EMBL)
---

# Scientific STITCH Chemical Network

STITCH (Search Tool for Interactions of Chemicals) REST API
utilizing-proteininteractionsearchdegree
networkanalysispipeline is provided。

## When to Use

- and protein's interaction is searchedand
- drug'sproteinnetwork is builtand
- (for) analysiswhen needed
- 'snetwork is builtand
- network (Network Pharmacology) is performedand

---

## Quick Start

## 1. -proteininteractionsearch

```python
import requests
import pandas as pd

STITCH_API = "http://stitch.embl.de/api"


def stitch_interactions(chemical, species=9606,
 required_score=400, limit=50):
 """
 STITCH — -proteininteractionsearch。

 Parameters:
 chemical: str — chemical nameor CID
 (example: "aspirin", "CIDm00002244")
 species: int — NCBI Taxonomy ID
 (9606=)
 required_score: int — degree
 (0-1000, 400=medium)
 limit: int — maximum results
 """
 url = f"{STITCH_API}/tsv/interactionsList"
 params = {
 "identifiers": chemical,
 "species": species,
 "required_score": required_score,
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 if "score" in df.columns:
 df["score"] = pd.to_numeric(
 df["score"], errors="coerce")

 print(f"STITCH: {chemical} → {len(df)} interactions")
 return df


def stitch_resolve(identifiers, species=9606):
 """
 STITCH — /protein ID 。

 Parameters:
 identifiers: list[str] — /protein
 species: int — NCBI Taxonomy ID
 """
 url = f"{STITCH_API}/tsv/resolveList"
 params = {
 "identifiers": "\r".join(identifiers),
 "species": species,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 print(f"STITCH resolve: {len(identifiers)} queries → "
 f"{len(df)} results")
 return df
```

## 2. network

```python
def stitch_network(chemicals, species=9606,
 required_score=400):
 """
 STITCH — networkconstruction。

 Parameters:
 chemicals: list[str] — chemical name
 species: int — NCBI Taxonomy ID
 required_score: int — degree
 """
 url = f"{STITCH_API}/tsv/network"
 params = {
 "identifiers": "\r".join(chemicals),
 "species": species,
 "required_score": required_score,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 nodes = set
 if "stringId_A" in df.columns:
 nodes.update(df["stringId_A"].unique)
 if "stringId_B" in df.columns:
 nodes.update(df["stringId_B"].unique)

 print(f"STITCH network: {len(nodes)} nodes, "
 f"{len(df)} edges")
 return df


def polypharmacology_analysis(drug_list, species=9606,
 required_score=700):
 """
 analysis。

 Parameters:
 drug_list: list[str] — drug
 species: int — NCBI Taxonomy ID
 required_score: int — degreethreshold
 """
 all_targets = {}
 for drug in drug_list:
 interactions = stitch_interactions(
 drug, species, required_score)
 if interactions.empty:
 continue

 targets = set
 for col in ["stringId_A", "stringId_B"]:
 if col in interactions.columns:
 targets.update(
 interactions[col].unique)
 # 
 targets = {t for t in targets
 if not t.startswith("CID")}
 all_targets[drug] = targets

 # calculation
 if len(all_targets) < 2:
 return pd.DataFrame

 pairs = []
 drugs = list(all_targets.keys)
 for i in range(len(drugs)):
 for j in range(i + 1, len(drugs)):
 shared = (all_targets[drugs[i]]
 & all_targets[drugs[j]])
 union = (all_targets[drugs[i]]
 | all_targets[drugs[j]])
 jaccard = (len(shared) / len(union)
 if union else 0)
 pairs.append({
 "drug_a": drugs[i],
 "drug_b": drugs[j],
 "shared_targets": len(shared),
 "jaccard_index": jaccard,
 "shared_list": "; ".join(
 sorted(shared)),
 })

 df = pd.DataFrame(pairs)
 df.sort_values("jaccard_index", ascending=False,
 inplace=True)
 print(f"Polypharmacology: {len(drugs)} drugs, "
 f"{len(df)} pairs")
 return df
```

## 3. analysis

```python
def stitch_enrichment(identifiers, species=9606):
 """
 STITCH — analysis。

 Parameters:
 identifiers: list[str] — protein/
 species: int — NCBI Taxonomy ID
 """
 url = f"{STITCH_API}/tsv/enrichment"
 params = {
 "identifiers": "\r".join(identifiers),
 "species": species,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 if "p_value" in df.columns:
 df["p_value"] = pd.to_numeric(
 df["p_value"], errors="coerce")
 df.sort_values("p_value", inplace=True)

 print(f"STITCH enrichment: {len(df)} terms")
 return df
```

## 4. STITCH integrationpipeline

```python
def stitch_pipeline(chemicals, species=9606,
 output_dir="results"):
 """
 STITCH integrationpipeline。

 Parameters:
 chemicals: list[str] — chemical name
 species: int — NCBI Taxonomy ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) unitsinteraction
 all_interactions = []
 for chem in chemicals:
 ixns = stitch_interactions(chem, species)
 ixns["query_chemical"] = chem
 all_interactions.append(ixns)
 ixn_df = pd.concat(all_interactions, ignore_index=True)
 ixn_df.to_csv(
 output_dir / "stitch_interactions.csv",
 index=False)

 # 2) network
 network = stitch_network(chemicals, species)
 network.to_csv(
 output_dir / "stitch_network.csv",
 index=False)

 # 3) 
 polypharm = polypharmacology_analysis(
 chemicals, species)
 polypharm.to_csv(
 output_dir / "polypharmacology.csv",
 index=False)

 print(f"STITCH pipeline → {output_dir}")
 return {
 "interactions": ixn_df,
 "network": network,
 "polypharmacology": polypharm,
 }
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `stitch` | STITCH | -proteininteraction (EMBL) |

## Pipeline Integration

```
cheminformatics → stitch-chemical-network → drug-target-profiling
 (compound) (STITCH interaction) (DGIdb )
 │ │ ↓
string-network-api ────────┘ pharmacology-targets
 (STRING PPI) (BindingDB/GtoPdb)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/stitch_interactions.csv` | - | → drug-target-profiling |
| `results/stitch_network.csv` | network | → string-network-api |
| `results/polypharmacology.csv` | analysis | → pharmacology-targets |

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
