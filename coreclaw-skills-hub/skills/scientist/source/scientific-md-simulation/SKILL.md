---
name: scientific-md-simulation
description: |
 molecular dynamicssimulationanalysisskill。MDAnalysis by/viatrajectoryanalysis
 RMSD/RMSF/Rg time seriesbindinganalysisstructure
 OpenFF Toolkitforce fieldparametersenergypipeline。
tu_tools:
 - key: pdb
 name: PDB
 description: moleculestructuredatabasereference
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `pdb` | PDB | moleculestructuredatabasereference |
