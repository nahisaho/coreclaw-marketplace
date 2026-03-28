---
name: scientific-metabolic-flux
description: |
 metabolismanalysisskill。13C/15N 
 datausingmetabolismEMU 
 integrationpipeline。
---

# Scientific Metabolic Flux

13C/15N experimentdatausingmetabolism
EMU (Elementary Metabolite Unit) framework
analysis (FBA) integrationpipeline is provided。

## When to Use

- 13C experimentdataanalysiswhen needed
- EMU/ is builtand
- MID (Mass Isotopomer Distribution) datawhen needed
- 's metabolism amountwhen needed
- FBA and dataintegrationwhen needed

---

## Quick Start

## 1. MID (Mass Isotopomer Distribution) data

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def load_mid_data(mid_file, sep="\t"):
 """
 MID Loading datanormalization。

 Parameters:
 mid_file: str — MID datafile path
 (TSV: metabolite, M+0, M+1, M+2,...)
 sep: str — delimiter
 """
 df = pd.read_csv(mid_file, sep=sep,
 index_col="metabolite")

 mid_cols = [c for c in df.columns
 if c.startswith("M+")]

 for idx in df.index:
 row_sum = df.loc[idx, mid_cols].sum
 if row_sum > 0:
 df.loc[idx, mid_cols] /= row_sum

 print(f"MID data: {len(df)} metabolites, "
 f"{len(mid_cols)} isotopomers")
 return df[mid_cols]


def natural_abundance_correction(mid_df, n_carbons):
 """
 amountcorrection。

 Parameters:
 mid_df: DataFrame — normalization MID data
 n_carbons: dict — metabolite→number/countmapping
 """
 C13_NAT = 0.011 # 13C 

 corrected = mid_df.copy
 for met in corrected.index:
 n_c = n_carbons.get(met, 6)
 n_iso = min(corrected.shape[1], n_c + 1)
 raw = corrected.loc[met].values[:n_iso]

 # correction 
 corr_matrix = np.zeros((n_iso, n_iso))
 for i in range(n_iso):
 for j in range(i, n_iso):
 from math import comb
 k = j - i
 remain = n_c - i
 if k <= remain:
 corr_matrix[i, j] = (
 comb(remain, k)
 * C13_NAT ** k
 * (1 - C13_NAT) ** (remain - k)
 )

 try:
 corrected_vals = np.linalg.solve(
 corr_matrix[:n_iso, :n_iso], raw)
 corrected_vals = np.maximum(corrected_vals, 0)
 corrected_vals /= corrected_vals.sum
 corrected.loc[met, corrected.columns[:n_iso]] = (
 corrected_vals)
 except np.linalg.LinAlgError:
 pass

 print(f"NA correction: {len(corrected)} metabolites")
 return corrected
```

## 2. EMU 

```python
def build_emu_model(reactions, atom_transitions):
 """
 EMU (Elementary Metabolite Unit) construction。

 Parameters:
 reactions: list[dict] — reactiondefinition
 [{id, substrates, products, reversible}]
 atom_transitions: dict — mapping
 {reaction_id: [(from_met, from_atoms,
 to_met, to_atoms)]}
 """
 emu_network = {}

 for rxn in reactions:
 rxn_id = rxn["id"]
 transitions = atom_transitions.get(rxn_id, [])

 for from_met, f_atoms, to_met, t_atoms in (
 transitions
 ):
 emu_size = len(t_atoms)
 emu_key = (to_met, tuple(sorted(t_atoms)))

 if emu_key not in emu_network:
 emu_network[emu_key] = []

 emu_network[emu_key].append({
 "reaction": rxn_id,
 "precursor": from_met,
 "precursor_atoms": f_atoms,
 "reversible": rxn.get(
 "reversible", False),
 })

 print(f"EMU model: {len(emu_network)} EMUs, "
 f"{len(reactions)} reactions")
 return emu_network


def simulate_mid(fluxes, emu_model, substrate_labeling,
 metabolite):
 """
 from's MID simulation。

 Parameters:
 fluxes: dict — {reaction_id: flux_value}
 emu_model: dict — EMU network
 substrate_labeling: dict — 
 {metabolite: [M+0 fraction, M+1,...]}
 metabolite: str — simulationmetabolite
 """
 relevant_emus = {
 k: v for k, v in emu_model.items
 if k[0] == metabolite
 }

 if not relevant_emus:
 return np.array([1.0])

 max_size = max(len(k[1]) for k in relevant_emus)
 mid = np.zeros(max_size + 1)
 mid[0] = 1.0 # : 

 for emu_key, precursors in relevant_emus.items:
 emu_size = len(emu_key[1])
 for prec in precursors:
 rxn_flux = fluxes.get(prec["reaction"], 0)
 prec_label = substrate_labeling.get(
 prec["precursor"],
 [1.0] + [0.0] * emu_size)

 for i, frac in enumerate(
 prec_label[:emu_size + 1]
 ):
 if i <= max_size:
 mid[i] += rxn_flux * frac

 mid_sum = mid.sum
 if mid_sum > 0:
 mid /= mid_sum

 return mid
```

## 3. 

```python
def estimate_fluxes(observed_mids, emu_model,
 substrate_labeling,
 initial_fluxes,
 metabolites):
 """
 methodby/via。

 Parameters:
 observed_mids: dict — {metabolite: np.array}
 MID data
 emu_model: dict — EMU network
 substrate_labeling: dict — 
 initial_fluxes: dict — initialvalue
 metabolites: list — metabolite
 """
 flux_names = list(initial_fluxes.keys)
 x0 = [initial_fluxes[f] for f in flux_names]

 def objective(x):
 fluxes = dict(zip(flux_names, x))
 residual = 0.0
 for met in metabolites:
 if met not in observed_mids:
 continue
 obs = observed_mids[met]
 sim = simulate_mid(
 fluxes, emu_model,
 substrate_labeling, met)
 n = min(len(obs), len(sim))
 residual += np.sum(
 (obs[:n] - sim[:n]) ** 2)
 return residual

 bounds = [(0, None) for _ in flux_names]
 result = minimize(objective, x0, method="L-BFGS-B",
 bounds=bounds)

 estimated = dict(zip(flux_names, result.x))
 print(f"Flux estimation: SSR={result.fun:.6f}, "
 f"converged={result.success}")
 return estimated, result
```

## 4. metabolismintegrationpipeline

```python
def metabolic_flux_pipeline(mid_file, reactions,
 atom_transitions,
 substrate_labeling,
 n_carbons,
 output_dir="results"):
 """
 metabolismintegrationpipeline。

 Parameters:
 mid_file: str — MID datafile
 reactions: list — reactiondefinition
 atom_transitions: dict — mapping
 substrate_labeling: dict — 
 n_carbons: dict — metabolite→number/count
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) MID loadcorrection
 mid_raw = load_mid_data(mid_file)
 mid_corr = natural_abundance_correction(
 mid_raw, n_carbons)
 mid_corr.to_csv(output_dir / "mid_corrected.csv")

 # 2) EMU construction
 emu_model = build_emu_model(
 reactions, atom_transitions)

 # 3) 
 observed = {met: mid_corr.loc[met].values
 for met in mid_corr.index}
 init_fluxes = {r["id"]: 1.0 for r in reactions}
 fluxes, opt_result = estimate_fluxes(
 observed, emu_model, substrate_labeling,
 init_fluxes, list(observed.keys))

 flux_df = pd.DataFrame([
 {"reaction": k, "flux": v}
 for k, v in fluxes.items
 ])
 flux_df.to_csv(output_dir / "fluxes.csv",
 index=False)

 print(f"Metabolic flux pipeline → {output_dir}")
 return {"fluxes": fluxes, "mid_corrected": mid_corr}
```

---

## Pipeline Integration

```
metabolic-modeling → metabolic-flux → systems-biology
 (FBA/COBRA) (13C MFA) (integrated analysis)
 │ │ ↓
flux-balance-analysis ───┘ pathway-enrichment
  (pathway)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/mid_corrected.csv` | correction MID | → metabolic-modeling |
| `results/fluxes.csv` | | → systems-biology |

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

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
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
