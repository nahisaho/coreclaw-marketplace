---
name: scientific-md-simulation
description: |
 Molecular dynamics simulation skill. GROMACS/OpenMM simulation setup, force field selection, trajectory analysis, free energy calculations, and enhanced sampling methods.
---

# Scientific MD Simulation

MDAnalysis and OpenFF Toolkit utilizingmolecular dynamics (MD) simulation
analysispipeline is provided。trajectoryfromstructurecalculation、
bindinganalysis、force fieldparametersto/untilintegration。

## When to Use

- MD trajectory (DCD/XTC/TRR/GRO) analysiswhen needed
- RMSD/RMSF/Radius of Gyration time series calculationwhen needed
- bindinganalysiswhen needed
- OpenFF molecule'sforce fieldparameters automatedgenerationwhen needed
- protein-ligand's is evaluatedand
- tablesurface (SASA) calculationwhen needed

---

## Quick Start

## 1. trajectory & basicinformation

```python
import MDAnalysis as mda
import numpy as np
import pandas as pd


def load_trajectory(topology, trajectory):
 """
 MD trajectory。

 Parameters:
 topology: str — file (PSF/PDB/GRO/PRMTOP)
 trajectory: str — trajectoryfile (DCD/XTC/TRR)

 K-Dense: mdanalysis
 """
 u = mda.Universe(topology, trajectory)

 info = {
 "n_atoms": u.atoms.n_atoms,
 "n_residues": u.residues.n_residues,
 "n_segments": u.segments.n_segments,
 "n_frames": u.trajectory.n_frames,
 "dt_ps": u.trajectory.dt,
 "total_time_ns": u.trajectory.n_frames * u.trajectory.dt / 1000,
 "topology_format": topology.split(".")[-1],
 "trajectory_format": trajectory.split(".")[-1],
 }

 print(f"Loaded: {info['n_atoms']} atoms, {info['n_frames']} frames, "
 f"{info['total_time_ns']:.1f} ns")
 return u, info
```

## 2. RMSD analysis

```python
from MDAnalysis.analysis.rms import RMSD


def compute_rmsd(universe, selection="backbone", ref_frame=0):
 """
 RMSD (Root Mean Square Deviation) calculation。

 Parameters:
 universe: mda.Universe — MD universe
 selection: str — atom selection
 ref_frame: int — reference
 """
 R = RMSD(universe, universe, select=selection, ref_frame=ref_frame)
 R.run

 df = pd.DataFrame({
 "frame": R.results.rmsd[:, 0].astype(int),
 "time_ps": R.results.rmsd[:, 1],
 "rmsd_A": R.results.rmsd[:, 2],
 })
 df["time_ns"] = df["time_ps"] / 1000

 print(f"RMSD ({selection}): mean={df['rmsd_A'].mean:.2f} Å, "
 f"max={df['rmsd_A'].max:.2f} Å")
 return df
```

## 3. RMSF analysis

```python
from MDAnalysis.analysis.rms import RMSF as RMSFAnalysis


def compute_rmsf(universe, selection="name CA"):
 """
 RMSF (Root Mean Square Fluctuation) per residue。

 Parameters:
 universe: mda.Universe — MD universe
 selection: str — atom selection ( Cα)
 """
 atoms = universe.select_atoms(selection)
 R = RMSFAnalysis(atoms).run

 df = pd.DataFrame({
 "resid": atoms.resids,
 "resname": atoms.resnames,
 "rmsf_A": R.results.rmsf,
 })

 # 's
 threshold = df["rmsf_A"].mean + 2 * df["rmsf_A"].std
 df["flexible"] = df["rmsf_A"] > threshold

 print(f"RMSF: mean={df['rmsf_A'].mean:.2f} Å, "
 f"flexible residues={df['flexible'].sum}")
 return df
```

## 4. Radius of Gyration

```python
def compute_radius_of_gyration(universe, selection="protein"):
 """
 Radius of Gyration (Rg) time seriescalculation。

 Parameters:
 universe: mda.Universe — MD universe
 selection: str — atom selection
 """
 protein = universe.select_atoms(selection)
 rg_data = []

 for ts in universe.trajectory:
 rg = protein.radius_of_gyration
 rg_data.append({
 "frame": ts.frame,
 "time_ns": ts.time / 1000,
 "rg_A": rg,
 })

 df = pd.DataFrame(rg_data)
 print(f"Rg: mean={df['rg_A'].mean:.2f} Å, "
 f"std={df['rg_A'].std:.2f} Å")
 return df
```

## 5. bindinganalysis

```python
from MDAnalysis.analysis.hydrogenbonds import HydrogenBondAnalysis


def hydrogen_bond_analysis(universe, donor_sel="protein", acceptor_sel="protein",
 d_a_cutoff=3.0, angle_cutoff=150):
 """
 bindinganalysis。

 Parameters:
 universe: mda.Universe — MD universe
 donor_sel: str — selection
 acceptor_sel: str — selection
 d_a_cutoff: float — D-A threshold (Å)
 angle_cutoff: float — D-H-A degreethreshold (°)
 """
 hbonds = HydrogenBondAnalysis(
 universe,
 donors_sel=donor_sel,
 acceptors_sel=acceptor_sel,
 d_a_cutoff=d_a_cutoff,
 d_h_a_angle_cutoff=angle_cutoff,
 )
 hbonds.run

 # bindingnumber/count
 counts = hbonds.count_by_time
 df_counts = pd.DataFrame({
 "time_ps": counts[:, 0],
 "n_hbonds": counts[:, 1].astype(int),
 })

 print(f"H-bonds: mean={df_counts['n_hbonds'].mean:.1f}/frame, "
 f"total unique={len(hbonds.results.hbonds)}")
 return hbonds, df_counts
```

## 6. SASA (tablesurface)

```python
from MDAnalysis.analysis.sasa import SASA


def compute_sasa(universe, selection="protein"):
 """
 Solvent Accessible Surface Area (SASA) calculation。

 Parameters:
 universe: mda.Universe
 selection: str — atom selection
 """
 atoms = universe.select_atoms(selection)
 sasa = SASA(atoms)
 sasa.run

 df = pd.DataFrame({
 "frame": range(len(sasa.results.area)),
 "sasa_A2": sasa.results.area,
 })

 print(f"SASA: mean={df['sasa_A2'].mean:.1f} Å², "
 f"std={df['sasa_A2'].std:.1f} Å²")
 return df
```

## 7. OpenFF force fieldparameters

```python
def parameterize_with_openff(smiles, force_field="openff-2.1.0"):
 """
 OpenFF Toolkit ligand'sforce fieldparametersautomatedgeneration。

 Parameters:
 smiles: str — ligand SMILES
 force_field: str — OpenFF force field

 K-Dense: openff
 """
 from openff.toolkit import Molecule, ForceField
 from openff.interchange import Interchange

 mol = Molecule.from_smiles(smiles)
 mol.generate_conformers(n_conformers=1)

 ff = ForceField(f"{force_field}.offxml")
 topology = mol.to_topology
 interchange = Interchange.from_smirnoff(ff, topology)

 result = {
 "smiles": smiles,
 "force_field": force_field,
 "n_atoms": mol.n_atoms,
 "n_bonds": mol.n_bonds,
 "n_conformers": mol.n_conformers,
 "partial_charges": mol.partial_charges,
 }

 print(f"OpenFF parameterized: {smiles} ({mol.n_atoms} atoms, "
 f"FF={force_field})")
 return interchange, result
```

## 8. integration MD analysispipeline

```python
def md_analysis_pipeline(topology, trajectory, selection="protein"):
 """
 MD trajectoryintegrated analysispipeline。

 Pipeline:
 load → RMSD → RMSF → Rg → H-bonds → summary
 """
 u, info = load_trajectory(topology, trajectory)

 rmsd = compute_rmsd(u, "backbone")
 rmsf = compute_rmsf(u, "name CA")
 rg = compute_radius_of_gyration(u, selection)
 hbonds, hb_counts = hydrogen_bond_analysis(u)

 summary = {
 "system": info,
 "rmsd_mean_A": round(rmsd["rmsd_A"].mean, 2),
 "rmsd_std_A": round(rmsd["rmsd_A"].std, 2),
 "rmsf_mean_A": round(rmsf["rmsf_A"].mean, 2),
 "n_flexible_residues": int(rmsf["flexible"].sum),
 "rg_mean_A": round(rg["rg_A"].mean, 2),
 "hbonds_mean_per_frame": round(hb_counts["n_hbonds"].mean, 1),
 }

 print(f"\n=== MD Analysis Summary ===")
 for k, v in summary.items:
 if isinstance(v, dict):
 continue
 print(f" {k}: {v}")

 return summary
```

---

## Pipeline Integration

```
molecular-docking ──→ md-simulation ──→ admet-pharmacokinetics
  (MD evaluation) (PK parameters)
 │ │ ↓
protein-structure ──┘ │ drug-target-profiling
 (PDB/AlphaFold) ↓ (evaluation)
 computational-materials
 (pymatgen/VASP integration)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/rmsd_timeseries.csv` | RMSD time series | → publication-figures |
| `results/rmsf_per_residue.csv` | RMSF | → protein-structure-analysis |
| `results/hbond_analysis.csv` | bindinganalysis | → molecular-docking |
| `results/md_summary.json` | integration | → admet-pharmacokinetics |

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
3. Write `report.md` summarizing methods, results, and interpretation

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
