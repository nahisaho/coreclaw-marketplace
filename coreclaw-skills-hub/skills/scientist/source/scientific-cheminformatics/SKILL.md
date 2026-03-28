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

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
