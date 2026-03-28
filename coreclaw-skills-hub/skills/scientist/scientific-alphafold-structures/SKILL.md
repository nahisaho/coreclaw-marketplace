---
name: scientific-alphafold-structures
description: |
 AlphaFold structure prediction skill. Protein structure retrieval from AlphaFold DB, pLDDT confidence scoring, structural alignment, and downstream structural analysis.
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

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
