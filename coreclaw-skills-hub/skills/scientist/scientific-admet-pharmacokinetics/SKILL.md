---
name: scientific-admet-pharmacokinetics
description: |
 ADMET and pharmacokinetics prediction skill. Absorption, Distribution, Metabolism, Excretion, Toxicity modeling with RDKit, DeepChem, and PK/PD simulation pipelines.
tu_tools:
 - key: pubchem
 name: PubChem
 description: compoundactivitydatabase
---

# Scientific ADMET & Pharmacokinetics

ADMET predictionand drug'sskill。initialincompound's
drugevaluationsupports。

## When to Use

- compound's ADMET integrationpredictionwhen needed
- compound's optimizationwhen needed
- PK/PD parameterswhen needed
- compoundlibrary's filter is performedand
- toxicity（hERG、Ames、toxicity） predictionwhen needed

## Quick Start

### 1. ADMET predictionpipelineoverview

```
Input: SMILES / SDF
 ↓
Step 1: Absorption
 - Caco-2 
 - HIA (Human Intestinal Absorption)
 - 
 - Pgp 
 ↓
Step 2: Distribution
 - bindingrate (PPB)
 - brain (BBB) 
 - distribution (VDss)
 ↓
Step 3: Metabolism
 - CYP inhibition/prediction (1A2, 2C9, 2C19, 2D6, 3A4)
 - metabolism (Half-life)
 - prediction
 ↓
Step 4: Excretion
 - 
 - 
 - prediction
 ↓
Step 5: Toxicity
 - hERG inhibition (toxicity)
 - Ames prediction (variant/mutation)
 - DILI 
 - LD50 toxicity
 ↓
Output: ADMET Profile Card
```

---

## Phase 1: Absorption prediction

### Caco-2 & HIA

```python
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

def predict_absorption_properties(smiles):
 """
 parameters's calculationprediction。
 """
 mol = Chem.MolFromSmiles(smiles)
 if mol is None:
 raise ValueError(f"Invalid SMILES: {smiles}")

 # parameters（）
 properties = {
 "MW": Descriptors.MolWt(mol),
 "LogP": Descriptors.MolLogP(mol),
 "TPSA": Descriptors.TPSA(mol),
 "HBA": Descriptors.NumHAcceptors(mol),
 "HBD": Descriptors.NumHDonors(mol),
 "RotBonds": Descriptors.NumRotatableBonds(mol),
 }

 # Rule-based absorption prediction
 properties["Lipinski_Violations"] = sum([
 properties["MW"] > 500,
 properties["LogP"] > 5,
 properties["HBA"] > 10,
 properties["HBD"] > 5,
 ])

 # TPSA-based intestinal absorption estimate
 # Ertl et al., J. Med. Chem. 2000
 if properties["TPSA"] < 140:
 properties["HIA_prediction"] = "High"
 else:
 properties["HIA_prediction"] = "Low"

 # BBB penetration estimate (TPSA < 90 Å²)
 properties["BBB_prediction"] = "Permeable" if properties["TPSA"] < 90 else "Non-permeable"

 return properties
```

---

## Phase 2: evaluation

### filterevaluation

```python
def evaluate_druglikeness(smiles):
 """
 multiplefilterby/viaevaluation。
 """
 mol = Chem.MolFromSmiles(smiles)
 results = {}

 # Lipinski Rule of 5
 results["Lipinski"] = {
 "MW": Descriptors.MolWt(mol) <= 500,
 "LogP": Descriptors.MolLogP(mol) <= 5,
 "HBA": Descriptors.NumHAcceptors(mol) <= 10,
 "HBD": Descriptors.NumHDonors(mol) <= 5,
 "pass": None, # True if ≤1 violation
 }
 violations = sum(1 for v in list(results["Lipinski"].values)[:4] if not v)
 results["Lipinski"]["pass"] = violations <= 1

 # Veber Rules (oral bioavailability)
 results["Veber"] = {
 "RotBonds": Descriptors.NumRotatableBonds(mol) <= 10,
 "TPSA": Descriptors.TPSA(mol) <= 140,
 "pass": None,
 }
 results["Veber"]["pass"] = all(
 v for k, v in results["Veber"].items if k != "pass"
 )

 # QED (Quantitative Estimate of Drug-likeness)
 from rdkit.Chem import QED
 results["QED"] = QED.qed(mol)

 # Ghose Filter
 mw = Descriptors.MolWt(mol)
 logp = Descriptors.MolLogP(mol)
 mr = Descriptors.MolMR(mol)
 n_atoms = mol.GetNumAtoms
 results["Ghose"] = {
 "pass": (160 <= mw <= 480 and -0.4 <= logp <= 5.6
 and 40 <= mr <= 130 and 20 <= n_atoms <= 70)
 }

 return results
```

---

## Phase 3: toxicityprediction

### structurealert & toxicityendpoint

```python
# PAINS (Pan-Assay Interference Compounds) filter
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

def check_structural_alerts(smiles):
 """
 structurealert (PAINS, Brenk) 's 。
 """
 mol = Chem.MolFromSmiles(smiles)
 alerts = []

 # PAINS filter
 params = FilterCatalogParams
 params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
 catalog = FilterCatalog(params)
 if catalog.HasMatch(mol):
 entry = catalog.GetFirstMatch(mol)
 alerts.append({
 "type": "PAINS",
 "description": entry.GetDescription,
 "severity": "Warning",
 })

 # Brenk filter（toxicitystructure）
 params_brenk = FilterCatalogParams
 params_brenk.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
 catalog_brenk = FilterCatalog(params_brenk)
 if catalog_brenk.HasMatch(mol):
 entry = catalog_brenk.GetFirstMatch(mol)
 alerts.append({
 "type": "Brenk",
 "description": entry.GetDescription,
 "severity": "Warning",
 })

 return alerts
```

### toxicity

```markdown
## Toxicity Risk Assessment

| Endpoint | Prediction | Confidence | Risk Level |
|----------------|------------|------------|------------|
| hERG IC50 | | | Low/Med/High |
| Ames | | | Low/Med/High |
| DILI | | | Low/Med/High |
| LD50 (rat) | | | Low/Med/High |
| Skin Sensitiz. | | | Low/Med/High |
| Carcinogenicity| | | Low/Med/High |

### Structural Alerts
| Alert Type | Description | Severity |
|------------|-------------|----------|
```

---

## Phase 4: PK/PD 

### 

```python
import numpy as np
from scipy.integrate import odeint

def one_compartment_pk(dose, ka, ke, vd, time_points):
 """
 1- PK （）。
 dose: amount (mg)
 ka: degreenumber/count (h⁻¹)
 ke: degreenumber/count (h⁻¹)
 vd: distribution (L)
 """
 def pk_ode(y, t, ka, ke):
 dAg_dt = -ka * y[0] # 
 dCp_dt = (ka * y[0] - ke * y[1] * vd) / vd # 
 return [dAg_dt, dCp_dt]

 y0 = [dose, 0]
 solution = odeint(pk_ode, y0, time_points, args=(ka, ke))

 return {
 "time": time_points,
 "concentration": solution[:, 1],
 "Cmax": np.max(solution[:, 1]),
 "Tmax": time_points[np.argmax(solution[:, 1])],
 "AUC": np.trapz(solution[:, 1], time_points),
 "half_life": np.log(2) / ke,
 }
```

---

## ADMET Profile Card template

```markdown
# ADMET Profile: [COMPOUND NAME]

**SMILES**: [canonical SMILES]
**Molecular Formula**: [formula]
**Date**: [date]

## 1. Physicochemical Properties
| Property | Value | Optimal Range | Status |
|----------|-------|---------------|--------|
| MW | | 150-500 | ✓/✗ |
| LogP | | -0.4 to 5.6 | ✓/✗ |
| TPSA | | 20-140 Å² | ✓/✗ |
| HBA | | ≤10 | ✓/✗ |
| HBD | | ≤5 | ✓/✗ |
| QED | | >0.5 | ✓/✗ |

## 2. Absorption
| Parameter | Value | Interpretation |
|-----------|-------|----------------|

## 3. Distribution
| Parameter | Value | Interpretation |
|-----------|-------|----------------|

## 4. Metabolism
| CYP Enzyme | Substrate? | Inhibitor? |
|------------|------------|------------|
| 1A2 | | |
| 2C9 | | |
| 2C19 | | |
| 2D6 | | |
| 3A4 | | |

## 5. Excretion
| Parameter | Value | Interpretation |
|-----------|-------|----------------|

## 6. Toxicity
| Endpoint | Prediction | Risk |
|----------|------------|------|

## 7. Druglikeness Summary
| Filter | Pass? | Violations |
|-----------|-------|------------|
| Lipinski | | |
| Veber | | |
| Ghose | | |
| PAINS | | |
| Brenk | | |

## 8. Recommendations
- [ ] Lead optimization priorities
- [ ] Key liabilities to address
- [ ] Suggested structural modifications
```

---

## Completeness Checklist

- [ ] : MW, LogP, TPSA, HBA, HBD, QED
- [ ] : Caco-2, HIA, Pgp 
- [ ] distribution: PPB, BBB, VDss
- [ ] metabolism: CYP 5 isoform (1A2/2C9/2C19/2D6/3A4)
- [ ] :, Half-life
- [ ] toxicity: hERG, Ames, DILI ≥ 3 endpoint
- [ ] structurealert: PAINS + Brenk 
- [ ] : Lipinski + Veber + QED

## Best Practices

1. **predictionvalue degree**: 's applicability domain verification
2. **multipletool Cross-validate**: ADMET-AI, DeepChem, SwissADME 's resultscomparison
3. **knowncompound Benchmark**: 's and comparison
4. **structurealertreferenceinformation**: PAINS also 's possible
5. **PK parameters in vivo correction**: allometric scaling type

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/admet_profile.json` | ADMET file（JSON） | all 5 evaluationcompletion |
| `results/admet_report.md` | ADMET evaluationreport（Markdown） | allanalysiscompletion |
| `results/pk_model.json` | PK parameters（JSON） | PK completion |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| ADMET-AI | `ADMETAI_predict_BBB_penetrance` | BBB prediction |
| ADMET-AI | `ADMETAI_predict_CYP_interactions` | CYP interactionprediction |
| ADMET-AI | `ADMETAI_predict_toxicity` | toxicityprediction |
| ADMET-AI | `ADMETAI_predict_bioavailability` | prediction |
| PubChem | `PubChem_get_compound_properties_by_CID` | compound property retrieval |
| ChEMBL | `ChEMBL_get_molecule` | molecule information retrieval |
| ChEMBL | `ChEMBL_get_activity` | bioassay data |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-drug-target-profiling` | ← bindingcompound's ADMET evaluation |
| `scientific-cheminformatics` | ← moleculestructureinformation'sproviding |
| `scientific-drug-repurposing` | → ADMET compound'sevaluation |
| `scientific-clinical-decision-support` | → PK parameters's application |
| `scientific-academic-writing` | → publishing research results |
| `scientific-regulatory-science` | → FDA |

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
