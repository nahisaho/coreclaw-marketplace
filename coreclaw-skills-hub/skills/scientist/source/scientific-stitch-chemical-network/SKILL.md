---
name: scientific-stitch-chemical-network
description: |
 STITCH -proteininteractionnetworkskill。STITCH
 REST API using-proteinsearch
 degreenetworkanalysis。
 ---

# Scientific STITCH Chemical Network

STITCH (Search Tool for Interactions of Chemicals) REST API
utilizing-proteininteractionsearchdegree
networkanalysispipeline is provided。

## When to Use

- and protein's interaction is searchedand
- drug'sproteinnetwork is builtand
- (for) analysiswhen needed
- 'snetwork is builtand
- network (Network Pharmacology) is performedand

---

## Quick Start

## 1. -proteininteractionsearch

```python
import requests
import pandas as pd

STITCH_API = "http://stitch.embl.de/api"


def stitch_interactions(chemical, species=9606,
 required_score=400, limit=50):
 """
 STITCH — -proteininteractionsearch。

 Parameters:
 chemical: str — chemical nameor CID
 (example: "aspirin", "CIDm00002244")
 species: int — NCBI Taxonomy ID
 (9606=)
 required_score: int — degree
 (0-1000, 400=medium)
 limit: int — maximum results
 """
 url = f"{STITCH_API}/tsv/interactionsList"
 params = {
 "identifiers": chemical,
 "species": species,
 "required_score": required_score,
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 if "score" in df.columns:
 df["score"] = pd.to_numeric(
 df["score"], errors="coerce")

 print(f"STITCH: {chemical} → {len(df)} interactions")
 return df


def stitch_resolve(identifiers, species=9606):
 """
 STITCH — /protein ID 。

 Parameters:
 identifiers: list[str] — /protein
 species: int — NCBI Taxonomy ID
 """
 url = f"{STITCH_API}/tsv/resolveList"
 params = {
 "identifiers": "\r".join(identifiers),
 "species": species,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 print(f"STITCH resolve: {len(identifiers)} queries → "
 f"{len(df)} results")
 return df
```

## 2. network

```python
def stitch_network(chemicals, species=9606,
 required_score=400):
 """
 STITCH — networkconstruction。

 Parameters:
 chemicals: list[str] — chemical name
 species: int — NCBI Taxonomy ID
 required_score: int — degree
 """
 url = f"{STITCH_API}/tsv/network"
 params = {
 "identifiers": "\r".join(chemicals),
 "species": species,
 "required_score": required_score,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 nodes = set
 if "stringId_A" in df.columns:
 nodes.update(df["stringId_A"].unique)
 if "stringId_B" in df.columns:
 nodes.update(df["stringId_B"].unique)

 print(f"STITCH network: {len(nodes)} nodes, "
 f"{len(df)} edges")
 return df


def polypharmacology_analysis(drug_list, species=9606,
 required_score=700):
 """
 analysis。

 Parameters:
 drug_list: list[str] — drug
 species: int — NCBI Taxonomy ID
 required_score: int — degreethreshold
 """
 all_targets = {}
 for drug in drug_list:
 interactions = stitch_interactions(
 drug, species, required_score)
 if interactions.empty:
 continue

 targets = set
 for col in ["stringId_A", "stringId_B"]:
 if col in interactions.columns:
 targets.update(
 interactions[col].unique)
 # 
 targets = {t for t in targets
 if not t.startswith("CID")}
 all_targets[drug] = targets

 # calculation
 if len(all_targets) < 2:
 return pd.DataFrame

 pairs = []
 drugs = list(all_targets.keys)
 for i in range(len(drugs)):
 for j in range(i + 1, len(drugs)):
 shared = (all_targets[drugs[i]]
 & all_targets[drugs[j]])
 union = (all_targets[drugs[i]]
 | all_targets[drugs[j]])
 jaccard = (len(shared) / len(union)
 if union else 0)
 pairs.append({
 "drug_a": drugs[i],
 "drug_b": drugs[j],
 "shared_targets": len(shared),
 "jaccard_index": jaccard,
 "shared_list": "; ".join(
 sorted(shared)),
 })

 df = pd.DataFrame(pairs)
 df.sort_values("jaccard_index", ascending=False,
 inplace=True)
 print(f"Polypharmacology: {len(drugs)} drugs, "
 f"{len(df)} pairs")
 return df
```

## 3. analysis

```python
def stitch_enrichment(identifiers, species=9606):
 """
 STITCH — analysis。

 Parameters:
 identifiers: list[str] — protein/
 species: int — NCBI Taxonomy ID
 """
 url = f"{STITCH_API}/tsv/enrichment"
 params = {
 "identifiers": "\r".join(identifiers),
 "species": species,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status

 lines = resp.text.strip.split("\n")
 if len(lines) < 2:
 return pd.DataFrame

 header = lines[0].split("\t")
 rows = [line.split("\t") for line in lines[1:]]
 df = pd.DataFrame(rows, columns=header)

 if "p_value" in df.columns:
 df["p_value"] = pd.to_numeric(
 df["p_value"], errors="coerce")
 df.sort_values("p_value", inplace=True)

 print(f"STITCH enrichment: {len(df)} terms")
 return df
```

## 4. STITCH integrationpipeline

```python
def stitch_pipeline(chemicals, species=9606,
 output_dir="results"):
 """
 STITCH integrationpipeline。

 Parameters:
 chemicals: list[str] — chemical name
 species: int — NCBI Taxonomy ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) unitsinteraction
 all_interactions = []
 for chem in chemicals:
 ixns = stitch_interactions(chem, species)
 ixns["query_chemical"] = chem
 all_interactions.append(ixns)
 ixn_df = pd.concat(all_interactions, ignore_index=True)
 ixn_df.to_csv(
 output_dir / "stitch_interactions.csv",
 index=False)

 # 2) network
 network = stitch_network(chemicals, species)
 network.to_csv(
 output_dir / "stitch_network.csv",
 index=False)

 # 3) 
 polypharm = polypharmacology_analysis(
 chemicals, species)
 polypharm.to_csv(
 output_dir / "polypharmacology.csv",
 index=False)

 print(f"STITCH pipeline → {output_dir}")
 return {
 "interactions": ixn_df,
 "network": network,
 "polypharmacology": polypharm,
 }
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
cheminformatics → stitch-chemical-network → drug-target-profiling
 (compound) (STITCH interaction) (DGIdb )
 │ │ ↓
string-network-api ────────┘ pharmacology-targets
 (STRING PPI) (BindingDB/GtoPdb)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/stitch_interactions.csv` | - | → drug-target-profiling |
| `results/stitch_network.csv` | network | → string-network-api |
| `results/polypharmacology.csv` | analysis | → pharmacology-targets |
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
