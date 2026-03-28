---
name: scientific-molecular-docking
description: |
 structuremolecular dockingskill。DiffDock (generative model)、
 AutoDock Vina (number/count)、GNINA (CNN ) integration
 protein-ligandbindingprediction、、
 bindingenergy、integrationpipeline。
---

# Scientific Molecular Docking

DiffDock / AutoDock Vina / GNINA 's 3 by/via
structurebindingpredictionpipeline is provided。

## When to Use

- protein-ligandbindingpredictionwhen needed
- compoundlibrary'swhen needed
- bindingenergy ligandwhen needed
- DiffDock AI 's bindinggeneration is performedand
- multiple's method'sevaluationwhen needed

---

## Quick Start

## 1. ligandreceptor's

```python
import os
import subprocess
import pandas as pd
import numpy as np


def prepare_receptor(pdb_file, output_dir="structures/prepared",
 remove_water=True, add_hydrogens=True):
 """
 forreceptor (protein) 。

 Parameters:
 pdb_file: str — input PDB file
 remove_water: bool — molecule
 add_hydrogens: bool — 
 """
 os.makedirs(output_dir, exist_ok=True)
 base_name = os.path.splitext(os.path.basename(pdb_file))[0]

 # PDB → PDBQT transformation (AutoDock Vina for)
 pdbqt_file = f"{output_dir}/{base_name}_receptor.pdbqt"

 try:
 from openbabel import pybel
 mol = next(pybel.readfile("pdb", pdb_file))
 if remove_water:
 mol.OBMol.DeleteWater
 if add_hydrogens:
 mol.addh
 mol.write("pdbqt", pdbqt_file, overwrite=True)
 print(f"Receptor prepared: {pdbqt_file}")
 except ImportError:
 # Open Babel : MGLTools prepare_receptor4
 cmd = ["prepare_receptor4.py", "-r", pdb_file,
 "-o", pdbqt_file, "-A", "hydrogens"]
 if remove_water:
 cmd.extend(["-U", "waters"])
 subprocess.run(cmd, check=True)
 print(f"Receptor prepared (MGLTools): {pdbqt_file}")

 return pdbqt_file


def prepare_ligands(sdf_file, output_dir="structures/ligands"):
 """
 ligandfile (SDF → PDBQT/MOL2)。
 """
 os.makedirs(output_dir, exist_ok=True)

 try:
 from openbabel import pybel
 ligands = list(pybel.readfile("sdf", sdf_file))
 prepared = []
 for i, mol in enumerate(ligands):
 mol.addh
 mol.make3D
 name = mol.title or f"ligand_{i}"
 out = f"{output_dir}/{name}.pdbqt"
 mol.write("pdbqt", out, overwrite=True)
 prepared.append({"name": name, "file": out, "atoms": len(mol.atoms)})
 print(f"Prepared {len(prepared)} ligands from {sdf_file}")
 return pd.DataFrame(prepared)
 except ImportError:
 print("openbabel not available, using RDKit fallback")
 from rdkit import Chem
 from rdkit.Chem import AllChem
 suppl = Chem.SDMolSupplier(sdf_file)
 prepared = []
 for i, mol in enumerate(suppl):
 if mol is None:
 continue
 mol = Chem.AddHs(mol)
 AllChem.EmbedMolecule(mol, randomSeed=42)
 name = mol.GetProp("_Name") if mol.HasProp("_Name") else f"lig_{i}"
 out = f"{output_dir}/{name}.mol2"
 Chem.MolToMolFile(mol, out)
 prepared.append({"name": name, "file": out})
 return pd.DataFrame(prepared)
```

## 2. AutoDock Vina 

```python
def autodock_vina_dock(receptor_pdbqt, ligand_pdbqt,
 center, box_size,
 exhaustiveness=32, n_poses=9):
 """
 AutoDock Vina by/viamolecular docking。

 Parameters:
 receptor_pdbqt: str — receptor PDBQT
 ligand_pdbqt: str — ligand PDBQT
 center: tuple — (x, y, z) coordinates
 box_size: tuple — (sx, sy, sz) (Å)
 exhaustiveness: int — search/explorationdegree (8-64)
 n_poses: int — outputnumber/count
 """
 try:
 from vina import Vina
 v = Vina(sf_name="vina")
 v.set_receptor(receptor_pdbqt)
 v.set_ligand_from_file(ligand_pdbqt)
 v.compute_vina_maps(center=list(center), box_size=list(box_size))
 v.dock(exhaustiveness=exhaustiveness, n_poses=n_poses)

 energies = v.energies
 results = []
 for i, e in enumerate(energies):
 results.append({
 "pose": i + 1,
 "affinity_kcal": e[0],
 "rmsd_lb": e[1] if len(e) > 1 else None,
 "rmsd_ub": e[2] if len(e) > 2 else None,
 })

 output = ligand_pdbqt.replace(".pdbqt", "_docked.pdbqt")
 v.write_poses(output, n_poses=n_poses, overwrite=True)

 df = pd.DataFrame(results)
 print(f"Vina docking: best affinity = {df['affinity_kcal'].min:.1f} kcal/mol")
 return df, output

 except ImportError:
 # CLI 
 output = ligand_pdbqt.replace(".pdbqt", "_docked.pdbqt")
 cmd = [
 "vina",
 "--receptor", receptor_pdbqt,
 "--ligand", ligand_pdbqt,
 "--center_x", str(center[0]),
 "--center_y", str(center[1]),
 "--center_z", str(center[2]),
 "--size_x", str(box_size[0]),
 "--size_y", str(box_size[1]),
 "--size_z", str(box_size[2]),
 "--exhaustiveness", str(exhaustiveness),
 "--num_modes", str(n_poses),
 "--out", output,
 ]
 subprocess.run(cmd, check=True)
 return pd.DataFrame, output
```

## 3. DiffDock AI 

```python
def diffdock_predict(protein_file, ligand_file, n_poses=10,
 output_dir="results/diffdock"):
 """
 DiffDock (generative model) 。

 Parameters:
 protein_file: str — protein PDB file
 ligand_file: str — ligand SDF/MOL2 file
 n_poses: int — generationnumber/count
 """
 os.makedirs(output_dir, exist_ok=True)

 # DiffDock-L (large model) inference
 cmd = [
 "python", "-m", "diffdock.inference",
 "--protein_path", protein_file,
 "--ligand", ligand_file,
 "--out_dir", output_dir,
 "--samples_per_complex", str(n_poses),
 "--model_dir", "DiffDock-L",
 "--confidence_model_dir", "DiffDock-L",
 ]

 print(f"Running DiffDock ({n_poses} poses)...")
 try:
 subprocess.run(cmd, check=True, capture_output=True)
 except FileNotFoundError:
 print("DiffDock not installed. Install from: "
 "https://github.com/gcorso/DiffDock")
 return pd.DataFrame

 # results
 results = []
 for i in range(n_poses):
 pose_file = f"{output_dir}/rank{i+1}.sdf"
 conf_file = f"{output_dir}/rank{i+1}_confidence.txt"
 confidence = None
 if os.path.exists(conf_file):
 with open(conf_file) as f:
 confidence = float(f.read.strip)
 results.append({
 "pose": i + 1,
 "file": pose_file,
 "confidence": confidence,
 })

 df = pd.DataFrame(results)
 if len(df) > 0 and "confidence" in df.columns:
 print(f"DiffDock: {len(df)} poses, "
 f"best confidence = {df['confidence'].max}")
 return df
```

## 4. 

```python
def virtual_screening(receptor_pdbqt, ligand_library,
 center, box_size,
 method="vina", top_n=20):
 """
 compoundlibrary's 。

 Parameters:
 receptor_pdbqt: str — receptor PDBQT
 ligand_library: list[str] — ligand PDBQT file's
 center/box_size: parameters
 method: "vina" or "diffdock"
 top_n: int — topnumber/count
 """
 all_results = []

 for i, ligand in enumerate(ligand_library):
 lig_name = os.path.splitext(os.path.basename(ligand))[0]
 print(f" [{i+1}/{len(ligand_library)}] Docking {lig_name}...", end=" ")

 if method == "vina":
 df, _ = autodock_vina_dock(
 receptor_pdbqt, ligand, center, box_size,
 exhaustiveness=16, n_poses=3
 )
 if len(df) > 0:
 best = df.iloc[0]
 all_results.append({
 "ligand": lig_name,
 "best_affinity": best["affinity_kcal"],
 "n_poses": len(df),
 })
 print(f"{best['affinity_kcal']:.1f} kcal/mol")

 results_df = pd.DataFrame(all_results)
 results_df = results_df.sort_values("best_affinity").head(top_n)

 print(f"\nVirtual screening: {len(ligand_library)} compounds → "
 f"top {top_n} candidates")
 return results_df
```

## References

### Output Files

| File | Format |
|---|---|
| `structures/prepared/*_receptor.pdbqt` | PDBQT |
| `structures/ligands/*.pdbqt` | PDBQT |
| `results/docking_results.csv` | CSV |
| `results/diffdock/rank*.sdf` | SDF |
| `results/virtual_screening.csv` | CSV |
| `figures/docking_scores.png` | PNG |

### Available Tools

> 's skillmainly K-Dense-AI/claude-scientific-skills 's diffdock skillreference。ToolUniverse SMCP fortool、proteinstructure PDB/AlphaFold toolretrievalpossible。

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-protein-structure-analysis` | receptorstructureretrievalbinding |
| `scientific-drug-target-profiling` | → |
| `scientific-cheminformatics` | ligandfilter |
| `scientific-admet-pharmacokinetics` | → ADMET |
| `scientific-drug-repurposing` | |
| `scientific-protein-interaction-network` | PPI → surface |

### Dependencies

`vina` (AutoDock Vina), `rdkit`, `openbabel` (optional), `numpy`, `pandas`
---

## Harness Optimization (v0.4.0)

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
