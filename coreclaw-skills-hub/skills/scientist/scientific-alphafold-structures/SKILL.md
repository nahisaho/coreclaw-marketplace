---
name: scientific-alphafold-structures
description: |
 AlphaFold structure prediction skill. Protein structure retrieval from AlphaFold DB, pLDDT confidence scoring, structural alignment, and downstream structural analysis.
tu_tools:
 - key: alphafold
 name: AlphaFold Database
 description: AlphaFold predictionstructurePAE retrieval
---

# Scientific AlphaFold Structures

AlphaFold Protein Structure Database REST API utilizing
structurepredictionretrievaldegreeanalysispipeline is provided。

## When to Use

- UniProt ID from AlphaFold predictionstructure is retrievedand
- pLDDT structuredegree is evaluatedand
- PAE (Predicted Aligned Error) predictiondegree minwhen needed
- structure (ratio) is verifiedand
- AlphaFold structureexperimentstructure andcomparisonwhen needed
- large-scaleproteomestructuredata batchretrievalwhen needed

---

## Quick Start

## 1. AlphaFold predictionstructureretrieval

```python
import requests
import pandas as pd
import numpy as np
from io import StringIO

AFDB_BASE = "https://alphafold.ebi.ac.uk/api"


def alphafold_get_prediction(uniprot_id, version=4):
 """
 AlphaFold DB — predictionstructureretrieval。

 Parameters:
 uniprot_id: str — UniProt accession (example: "P00533")
 version: int — AlphaFold 
 """
 url = f"{AFDB_BASE}/prediction/{uniprot_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 entries = resp.json

 if not entries:
 print(f"No AlphaFold prediction for {uniprot_id}")
 return None

 entry = entries[0] if isinstance(entries, list) else entries
 result = {
 "uniprot_id": uniprot_id,
 "entry_id": entry.get("entryId", ""),
 "gene": entry.get("gene", ""),
 "organism": entry.get("organismScientificName", ""),
 "tax_id": entry.get("taxId", ""),
 "sequence_length": entry.get("uniprotEnd", 0)
 - entry.get("uniprotStart", 0) + 1,
 "model_url": entry.get("cifUrl", ""),
 "pdb_url": entry.get("pdbUrl", ""),
 "pae_url": entry.get("paeImageUrl", ""),
 "global_plddt": entry.get("globalMetricValue", None),
 "model_version": entry.get("latestVersion", version),
 }

 print(f"AlphaFold {uniprot_id}: pLDDT={result['global_plddt']}, "
 f"length={result['sequence_length']}")
 return result
```

## 2. pLDDT degreefileanalysis

```python
import biotite.structure.io.pdbx as pdbx
import biotite.structure as struc


def alphafold_plddt_profile(uniprot_id, output_dir="results"):
 """
 AlphaFold — pLDDT degreefile。

 Parameters:
 uniprot_id: str — UniProt accession
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # CIF retrieval
 pred = alphafold_get_prediction(uniprot_id)
 if not pred:
 return pd.DataFrame

 cif_url = pred["model_url"]
 resp = requests.get(cif_url, timeout=60)
 resp.raise_for_status

 cif_path = output_dir / f"AF-{uniprot_id}.cif"
 cif_path.write_bytes(resp.content)

 # pLDDT = B-factor in AlphaFold structures
 pdbx_file = pdbx.CIFFile.read(str(cif_path))
 structure = pdbx.get_structure(pdbx_file, model=1)
 ca_mask = structure.atom_name == "CA"
 ca_atoms = structure[ca_mask]

 residues = []
 for i, atom in enumerate(ca_atoms):
 residues.append({
 "residue_index": i + 1,
 "residue_name": atom.res_name,
 "chain": atom.chain_id,
 "plddt": atom.b_factor,
 })

 df = pd.DataFrame(residues)

 # degree
 df["confidence"] = pd.cut(
 df["plddt"],
 bins=[0, 50, 70, 90, 100],
 labels=["Very low", "Low", "Confident", "Very high"],
 )

 n_high = (df["plddt"] >= 70).sum
 print(f"pLDDT profile {uniprot_id}: {len(df)} residues, "
 f"{n_high}/{len(df)} confident (≥70)")
 return df
```

## 3. PAE (Predicted Aligned Error) analysis

```python
def alphafold_pae_analysis(uniprot_id):
 """
 AlphaFold — PAE analysis。

 Parameters:
 uniprot_id: str — UniProt accession
 """
 url = (f"https://alphafold.ebi.ac.uk/files/"
 f"AF-{uniprot_id}-F1-predicted_aligned_error_v4.json")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 pae_data = data[0] if isinstance(data, list) else data
 pae_matrix = np.array(pae_data.get("predicted_aligned_error",
 pae_data.get("pae", [])))

 # ( PAE block)
 n_res = pae_matrix.shape[0]
 mean_pae = pae_matrix.mean
 low_pae_mask = pae_matrix < mean_pae * 0.5

 # and 's PAE 
 domain_scores = []
 for i in range(n_res):
 row = low_pae_mask[i]
 domain_scores.append(row.sum / n_res)

 result = {
 "uniprot_id": uniprot_id,
 "pae_matrix_shape": pae_matrix.shape,
 "mean_pae": float(mean_pae),
 "median_pae": float(np.median(pae_matrix)),
 "min_pae": float(pae_matrix.min),
 "max_pae": float(pae_matrix.max),
 "domain_scores": domain_scores,
 }

 print(f"PAE {uniprot_id}: {n_res}x{n_res} matrix, "
 f"mean={mean_pae:.1f} Å")
 return result, pae_matrix
```

## 4. AlphaFold integrationpipeline

```python
def alphafold_pipeline(uniprot_ids, output_dir="results"):
 """
 AlphaFold structureanalysisintegrationpipeline。

 Parameters:
 uniprot_ids: list[str] — UniProt IDs
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 all_predictions = []
 all_plddt = []

 for uid in uniprot_ids:
 # 1) predictionretrieval
 pred = alphafold_get_prediction(uid)
 if pred:
 all_predictions.append(pred)

 # 2) pLDDT file
 plddt = alphafold_plddt_profile(uid, output_dir=output_dir)
 if not plddt.empty:
 plddt["uniprot_id"] = uid
 all_plddt.append(plddt)

 # 
 pred_df = pd.DataFrame(all_predictions)
 pred_df.to_csv(output_dir / "predictions.csv", index=False)

 if all_plddt:
 plddt_df = pd.concat(all_plddt, ignore_index=True)
 plddt_df.to_csv(output_dir / "plddt_profiles.csv", index=False)

 print(f"AlphaFold pipeline: {len(all_predictions)} structures")
 return {"predictions": pred_df}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `alphafold` | AlphaFold Database | predictionstructurepLDDTPAE retrieval |

## Pipeline Integration

```
protein-structure-analysis → alphafold-structures → protein-design
 (PDB experimentstructure) (AlphaFold prediction) (de novo design)
 │ │ ↓
 structural-proteomics ─────────┘ molecular-docking
 (EMDB/PDBe) │ (bindingprediction)
 ↓
 variant-effect-prediction
 (structurevariant/mutationevaluation)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/predictions.csv` | predictiondata | → protein-structure-analysis |
| `results/plddt_profiles.csv` | pLDDT | → protein-design |
| `results/AF-*.cif` | predictionstructurefile | → molecular-docking |

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
