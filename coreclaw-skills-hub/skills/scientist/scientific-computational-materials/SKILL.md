---
name: scientific-computational-materials
description: |
 Computational materials science skill. DFT calculations, molecular dynamics for materials, crystal structure prediction, band structure analysis, and materials property prediction.
---

# Scientific Computational Materials

crystal、crystal structurepropertiesdatabase
first-principlescalculationoutputphaseanalysisstructurevisualization is provided
calculationpipeline。

## When to Use

- crystal structure's generationtransformationanalysis is performedand
- Materials Project API propertiesdatawhen needed
- phase diagram  by/viaanalysiswhen needed
- DFT calculation (VASP/QE) 's inputfilegenerationoutputanalysiswhen needed
- band structuredensity of states (DOS) visualizationwhen needed
- loop is performedand

---

## Quick Start

## 1. crystal structure

```python
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def create_crystal_structure(lattice_params, species, coords,
 output_file="results/structure.cif"):
 """
 pymatgen by/viacrystal structure's generation andanalysis。

 Parameters:
 - lattice_params: (a, b, c, alpha, beta, gamma) or 3×3 matrix
 - species: ["Si", "O",...]
 - coords: minratecoordinates [[x,y,z],...]
 """
 lattice = Lattice.from_parameters(*lattice_params)
 structure = Structure(lattice, species, coords)

 sga = SpacegroupAnalyzer(structure, symprec=0.1)

 print(f" Crystal structure:")
 print(f" Formula: {structure.composition.reduced_formula}")
 print(f" Space group: {sga.get_space_group_symbol} ({sga.get_space_group_number})")
 print(f" Crystal system: {sga.get_crystal_system}")
 print(f" Lattice: a={lattice.a:.3f}, b={lattice.b:.3f}, c={lattice.c:.3f}")
 print(f" Volume: {structure.volume:.3f} Å³")
 print(f" Density: {structure.density:.3f} g/cm³")

 # forcelltransformation
 conventional = sga.get_conventional_standard_structure
 primitive = sga.get_primitive_standard_structure

 print(f" Conventional cell: {len(conventional)} atoms")
 print(f" Primitive cell: {len(primitive)} atoms")

 # CIF output
 import os
 os.makedirs(os.path.dirname(output_file), exist_ok=True)
 structure.to(filename=output_file)

 return structure, sga


def analyze_structure_symmetry(structure, symprec=0.01):
 """
 crystal'sdetailsanalysis。

 - grouppointgroup
 - Wyckoff 
 - 
 """
 sga = SpacegroupAnalyzer(structure, symprec=symprec)

 symmetry_info = {
 "space_group_symbol": sga.get_space_group_symbol,
 "space_group_number": sga.get_space_group_number,
 "crystal_system": sga.get_crystal_system,
 "point_group": sga.get_point_group_symbol,
 "hall_symbol": sga.get_hall,
 "symmetry_operations": len(sga.get_symmetry_operations),
 }

 # Wyckoff 
 sym_struct = sga.get_symmetrized_structure
 wyckoff_sites = sym_struct.wyckoff_symbols

 print(f" Symmetry analysis:")
 for k, v in symmetry_info.items:
 print(f" {k}: {v}")
 print(f" Wyckoff sites: {wyckoff_sites}")

 return symmetry_info
```

## 2. Materials Project API 

```python
from mp_api.client import MPRester
import pandas as pd


def query_materials_project(formula=None, elements=None,
 band_gap_range=None,
 e_above_hull_max=0.025):
 """
 Materials Project API by/viadatabase。

 searchcondition:
 - formula (formula) — exact or reduced
 - configuration (elements) — includes/
 - band gaprange (band_gap_range) — eV
 - energy (e_above_hull) — 
 """
 import os
 api_key = os.environ.get("MP_API_KEY")
 if not api_key:
 raise EnvironmentError("Materials Project API key not found. Set MP_API_KEY environment variable.")

 with MPRester(api_key) as mpr:
 criteria = {}
 if formula:
 criteria["formula"] = formula
 if elements:
 criteria["elements"] = elements

 docs = mpr.materials.summary.search(
 **criteria,
 energy_above_hull=(0, e_above_hull_max) if e_above_hull_max else None,
 band_gap=band_gap_range,
 fields=[
 "material_id", "formula_pretty", "volume",
 "density", "band_gap", "energy_above_hull",
 "formation_energy_per_atom", "is_stable",
 "symmetry", "nsites",
 ],
 )

 results = []
 for doc in docs:
 results.append({
 "mp_id": doc.material_id,
 "formula": doc.formula_pretty,
 "space_group": doc.symmetry.symbol if doc.symmetry else None,
 "band_gap_eV": doc.band_gap,
 "e_above_hull_eV": doc.energy_above_hull,
 "formation_energy_eV": doc.formation_energy_per_atom,
 "density_g_cm3": doc.density,
 "nsites": doc.nsites,
 "is_stable": doc.is_stable,
 })

 df = pd.DataFrame(results)
 print(f" Materials Project query:")
 print(f" Found: {len(df)} materials")
 if len(df) > 0:
 print(f" Stable: {df['is_stable'].sum}")
 print(f" Band gap range: {df['band_gap_eV'].min:.2f}–{df['band_gap_eV'].max:.2f} eV")

 return df
```

## 3. phase diagramanalysis

```python
import numpy as np
import pandas as pd


def compute_phase_diagram(system_elements, output_file="figures/phase_diagram.png"):
 """
 phase diagram  calculation。

 (Convex Hull):
 - phase: 's point (e_above_hull = 0)
 - phase: 's point (e_above_hull > 0)
 - degradationreaction: 's phase to 'sdegradation
 """
 from mp_api.client import MPRester
 from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

 with MPRester as mpr:
 entries = mpr.get_entries_in_chemsys(system_elements)

 pd_obj = PhaseDiagram(entries)

 print(f" Phase diagram: {'-'.join(system_elements)}")
 print(f" Total entries: {len(entries)}")
 print(f" Stable phases: {len(pd_obj.stable_entries)}")

 for entry in pd_obj.stable_entries:
 formula = entry.composition.reduced_formula
 e_form = pd_obj.get_form_energy_per_atom(entry)
 print(f" {formula}: ΔHf = {e_form:.4f} eV/atom")

 # visualization
 plotter = PDPlotter(pd_obj)
 plotter.get_plot.savefig(output_file, dpi=300, bbox_inches="tight")

 return pd_obj
```

## 4. band structureDOS

```python
import numpy as np


def plot_band_structure(material_id, output_file="figures/band_structure.png"):
 """
 band structure's retrieval andvisualization。

 - k-path (Setyawan-Curtarolo )
 - band gap (/)
 - criteria
 """
 from mp_api.client import MPRester
 from pymatgen.electronic_structure.plotter import BSPlotter

 with MPRester as mpr:
 bs = mpr.get_bandstructure_by_material_id(material_id)

 if bs is None:
 print(f" No band structure available for {material_id}")
 return None

 gap = bs.get_band_gap
 print(f" Band structure: {material_id}")
 print(f" Band gap: {gap['energy']:.3f} eV")
 print(f" Direct: {gap['direct']}")
 print(f" Transition: {gap['transition']}")

 plotter = BSPlotter(bs)
 plotter.get_plot.savefig(output_file, dpi=300, bbox_inches="tight")

 return bs


def plot_density_of_states(material_id, output_file="figures/dos.png"):
 """
 density of states (DOS) 's retrieval andvisualization。

 - Total DOS + projected DOS (degradation)
 - 
 """
 from mp_api.client import MPRester
 from pymatgen.electronic_structure.plotter import DosPlotter

 with MPRester as mpr:
 dos = mpr.get_dos_by_material_id(material_id)

 if dos is None:
 print(f" No DOS available for {material_id}")
 return None

 print(f" DOS: {material_id}")
 print(f" Efermi: {dos.efermi:.3f} eV")

 plotter = DosPlotter
 plotter.add_dos("Total", dos)
 plotter.get_plot.savefig(output_file, dpi=300, bbox_inches="tight")

 return dos
```

## 5. VASP/Quantum ESPRESSO output

```python
from pymatgen.core import Structure


def generate_vasp_inputs(structure, output_dir="vasp_inputs",
 calculation_type="relaxation"):
 """
 VASP inputfilegeneration。

 calculation:
 - relaxation: structure (ISIF=3)
 - static: calculation (NSW=0)
 - band: band structure (ICHARG=11)
 - dos: density of states (LORBIT=11)
 """
 from pymatgen.io.vasp.sets import (
 MPRelaxSet, MPStaticSet,
 )
 import os
 os.makedirs(output_dir, exist_ok=True)

 if calculation_type == "relaxation":
 vis = MPRelaxSet(structure)
 elif calculation_type == "static":
 vis = MPStaticSet(structure)
 elif calculation_type == "band":
 vis = MPStaticSet(structure)
 vis.incar.update({"ICHARG": 11, "LORBIT": 11, "LWAVE": False})
 elif calculation_type == "dos":
 vis = MPStaticSet(structure)
 vis.incar.update({"LORBIT": 11, "NEDOS": 2001, "ISMEAR": -5})
 else:
 vis = MPRelaxSet(structure)

 vis.write_input(output_dir)

 print(f" VASP inputs generated: {output_dir}")
 print(f" Calculation: {calculation_type}")
 print(f" Files: INCAR, POSCAR, POTCAR, KPOINTS")

 return output_dir


def parse_vasp_output(vasprun_file="vasprun.xml"):
 """
 VASP output (vasprun.xml) 's analysis。
 """
 from pymatgen.io.vasp.outputs import Vasprun

 vr = Vasprun(vasprun_file, parse_dos=True, parse_eigen=True)

 print(f" VASP output: {vasprun_file}")
 print(f" Final energy: {vr.final_energy:.6f} eV")
 print(f" Converged: {vr.converged}")
 print(f" Band gap: {vr.get_band_structure.get_band_gap['energy']:.3f} eV")

 return vr
```

## References

### Output Files

| File | Format |
|---|---|
| `results/structure.cif` | CIF |
| `results/materials_query.csv` | CSV |
| `figures/phase_diagram.png` | PNG |
| `figures/band_structure.png` | PNG |
| `figures/dos.png` | PNG |
| `vasp_inputs/` | VASP input set |

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

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-quantum-computing` | amountcalculationVQEquantum chemistry |
| `scientific-cheminformatics` | molecular descriptors and structural analysis |
| `scientific-publication-figures` | structurephase diagramvisualization |
| `scientific-materials-characterization` | XRDSEMexperiment |

### Dependencies

`pymatgen`, `mp-api`, `pandas`, `numpy`, `matplotlib`
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
