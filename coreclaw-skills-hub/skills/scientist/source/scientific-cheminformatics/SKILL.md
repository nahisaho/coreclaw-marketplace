---
name: scientific-cheminformatics
description: |
 analysis'sskill。RDKit usingmoleculecalculation、Morgan 、
 Tanimoto degree、structurealert、Lipinski Rule of 5 evaluation is performedfor。
 Scientific Skills Exp-02, 05 。
---

# Scientific Cheminformatics Analysis

RDKit usingmoleculeanalysispipelineskill。SMILES → molecule → SAR analysis →
toxicitypredictionto/until'sworkflow is provided。

## When to Use

- compound'swhen needed
- SMILES frommoleculecalculationwhen needed
- compound's structuredegreeevaluationwhen needed
- structureactivitycorrelation（SAR） analysiswhen needed
- structurealert（）when needed
- Lipinski Rule of 5 / evaluationwhen needed

## Quick Start

## Standard Pipeline

### 1. SMILES → moleculetransformation

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, QED, Lipinski
from rdkit.Chem.Scaffolds import MurckoScaffold
import pandas as pd
import numpy as np

def smiles_to_mol(smiles):
 """SMILES from RDKit molecule is generated。"""
 mol = Chem.MolFromSmiles(smiles)
 if mol is None:
 raise ValueError(f"Invalid SMILES: {smiles}")
 return mol
```

### 2. molecule'scalculation

```python
def calculate_descriptors(smiles_list, names=None):
 """
 SMILES fromkeymoleculecalculation.
 value: DataFrame
 """
 records = []
 for i, smi in enumerate(smiles_list):
 mol = Chem.MolFromSmiles(smi)
 if mol is None:
 continue

 record = {
 "Name": names[i] if names else f"Mol_{i}",
 "SMILES": smi,
 "MW": Descriptors.MolWt(mol),
 "LogP": Descriptors.MolLogP(mol),
 "TPSA": Descriptors.TPSA(mol),
 "HBA": Descriptors.NumHAcceptors(mol),
 "HBD": Descriptors.NumHDonors(mol),
 "RotBonds": Descriptors.NumRotatableBonds(mol),
 "AromaticRings": Descriptors.NumAromaticRings(mol),
 "HeavyAtoms": mol.GetNumHeavyAtoms,
 "QED": QED.qed(mol),
 "Fraction_CSP3": Descriptors.FractionCSP3(mol),
 }
 records.append(record)

 return pd.DataFrame(records)
```

### 3. Morgan & Tanimoto degree

```python
from rdkit import DataStructs

def compute_fingerprints(smiles_list, radius=2, nBits=2048):
 """Morgan is generated。"""
 fps = []
 for smi in smiles_list:
 mol = Chem.MolFromSmiles(smi)
 if mol:
 fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
 fps.append(fp)
 return fps

def tanimoto_similarity_matrix(fps, names=None):
 """Tanimoto degree is computed。"""
 n = len(fps)
 sim_matrix = np.zeros((n, n))
 for i in range(n):
 for j in range(n):
 sim_matrix[i, j] = DataStructs.TanimotoSimilarity(fps[i], fps[j])

 if names is None:
 names = [f"Mol_{i}" for i in range(n)]

 sim_df = pd.DataFrame(sim_matrix, index=names, columns=names)
 sim_df.to_csv("results/tanimoto_similarity.csv")
 return sim_df
```

### 4. Lipinski Rule of 5 evaluation

```python
def lipinski_evaluation(desc_df):
 """Lipinski Rule of 5 's 。"""
 desc_df = desc_df.copy
 desc_df["Lipinski_MW"] = desc_df["MW"] <= 500
 desc_df["Lipinski_LogP"] = desc_df["LogP"] <= 5
 desc_df["Lipinski_HBA"] = desc_df["HBA"] <= 10
 desc_df["Lipinski_HBD"] = desc_df["HBD"] <= 5
 desc_df["Lipinski_Violations"] = 4 - (
 desc_df["Lipinski_MW"].astype(int) +
 desc_df["Lipinski_LogP"].astype(int) +
 desc_df["Lipinski_HBA"].astype(int) +
 desc_df["Lipinski_HBD"].astype(int)
 )
 desc_df["Lipinski_Pass"] = desc_df["Lipinski_Violations"] <= 1
 return desc_df
```

### 5. structurealert（）（Exp-05）

```python
STRUCTURAL_ALERTS = {
 "Nitro": "[N+](=O)[O-]",
 "Epoxide": "C1OC1",
 "Aldehyde": "[CH]=O",
 "Michael_Acceptor": "C=CC(=O)",
 "Acyl_Halide": "C(=O)[F,Cl,Br,I]",
 "Aniline": "c1ccccc1N",
 "Hydrazine": "NN",
 "Sulfonate": "S(=O)(=O)[O-]",
}

def detect_structural_alerts(smiles_list, names=None, alerts=None):
 """SMARTS by/viastructurealert's 。"""
 if alerts is None:
 alerts = STRUCTURAL_ALERTS

 results = []
 for i, smi in enumerate(smiles_list):
 mol = Chem.MolFromSmiles(smi)
 if mol is None:
 continue

 name = names[i] if names else f"Mol_{i}"
 for alert_name, smarts in alerts.items:
 pattern = Chem.MolFromSmarts(smarts)
 if mol.HasSubstructMatch(pattern):
 results.append({"Name": name, "SMILES": smi,
 "Alert": alert_name, "SMARTS": smarts})

 return pd.DataFrame(results)
```

### 6. Murcko analysis

```python
def scaffold_analysis(smiles_list, names=None):
 """Murcko 's extraction andclassification。"""
 scaffolds = []
 for i, smi in enumerate(smiles_list):
 mol = Chem.MolFromSmiles(smi)
 if mol:
 core = MurckoScaffold.GetScaffoldForMol(mol)
 scaffolds.append({
 "Name": names[i] if names else f"Mol_{i}",
 "SMILES": smi,
 "Scaffold": Chem.MolToSmiles(core),
 })
 return pd.DataFrame(scaffolds)
```

## References

### Output Files

| File | Format |
|---|---|
| `results/molecular_properties.csv` | CSV |
| `results/tanimoto_similarity.csv` | CSV |
| `results/structural_alerts.csv` | CSV |
| `figures/chemical_space_pca.png` | PNG |
| `figures/similarity_heatmap.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| PubChem | `PubChem_get_CID_by_compound_name` | compound→CID transformation |
| PubChem | `PubChem_get_compound_properties_by_CID` | compound property retrieval |
| PubChem | `PubChem_search_compounds_by_similarity` | compoundsearch |
| ChEMBL | `ChEMBL_search_molecules` | moleculesearch |
| ChEMBL | `ChEMBL_get_molecule` | molecule information retrieval |
| ZINC | `ZINC_search_by_smiles` | SMILES search |

#### Reference Experiments

- **Exp-02**: EGFR inhibition SAR analysis（、Tanimoto、MCS、Scaffold）
- **Exp-05**: toxicityprediction（structurealert、Morgan FP classification）
