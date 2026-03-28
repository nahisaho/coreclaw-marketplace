---
name: scientific-structural-proteomics
description: |
 Structural proteomics skill. Cross-linking mass spectrometry analysis, HDX-MS data processing, native MS, and structural biology data integration.
---

# Scientific Structural Proteomics

6 items's structuredatabase integration
proteinstructurepipeline is provided。

## When to Use

- PDB entry's detailsstructureinformation (resolution, experimentmethod, structure) is retrievedand
- EM information EMDB fromretrievalwhen needed
- UniProt protein'svariant/mutationgenomemapping is investigatedand
- protein's configuration Complex Portal and
- DeepGO sequence's GO prediction is performedand
- EVE missense variant/mutation's is retrievedand

---

## Quick Start

## 1. PDBe structureData Retrieval

```python
import requests
import pandas as pd

PDBE_API = "https://www.ebi.ac.uk/pdbe/api"


def get_pdbe_entry(pdb_id):
 """
 PDBe entry's summarystructureretrieval。

 Parameters:
 pdb_id: str — PDB ID (e.g., "1cbs")

 """
 pdb = pdb_id.lower

 # Summary
 resp_s = requests.get(f"{PDBE_API}/pdb/entry/summary/{pdb}")
 resp_s.raise_for_status
 summary = resp_s.json.get(pdb, [{}])[0]

 # Quality
 resp_q = requests.get(f"{PDBE_API}/pdb/entry/quality/{pdb}")
 quality = (
 resp_q.json.get(pdb, [{}])[0] if resp_q.status_code == 200 else {}
 )

 # Experiment
 resp_e = requests.get(f"{PDBE_API}/pdb/entry/experiment/{pdb}")
 experiment = (
 resp_e.json.get(pdb, [{}])[0] if resp_e.status_code == 200 else {}
 )

 entry = {
 "pdb_id": pdb,
 "title": summary.get("title", ""),
 "method": experiment.get("experimental_method", ""),
 "resolution": experiment.get("resolution", ""),
 "release_date": summary.get("release_date", ""),
 "r_factor": quality.get("r_factor", ""),
 "r_free": quality.get("r_free", ""),
 }

 print(f"PDBe {pdb}: {entry['method']} @ {entry['resolution']}Å")
 return entry, summary, quality
```

## 2. EMDB EM structure

```python
EMDB_API = "https://www.ebi.ac.uk/emdb/api"


def get_emdb_structure(emdb_id):
 """
 EMDB entry's 3D EM informationretrieval。

 Parameters:
 emdb_id: str — EMDB ID (e.g., "EMD-1234")

 """
 url = f"{EMDB_API}/entry/{emdb_id}"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 admin = data.get("admin", {})
 map_info = data.get("map", {})

 entry = {
 "emdb_id": emdb_id,
 "title": admin.get("title", ""),
 "resolution": map_info.get("resolution", {}).get("value", ""),
 "contour_level": map_info.get("contour_level", {}).get("value", ""),
 "deposition_date": admin.get("deposition_date", ""),
 }

 print(f"EMDB {emdb_id}: {entry['resolution']}Å resolution")
 return entry, data
```

## 3. Proteins API (UniProt) variant/mutation

```python
PROTEINS_API = "https://www.ebi.ac.uk/proteins/api"


def get_protein_features(uniprot_id):
 """
 Proteins API fromprotein'svariant/mutationinformationretrieval。

 Parameters:
 uniprot_id: str — UniProt accession (e.g., "P04637")

 """
 headers = {"Accept": "application/json"}

 # Protein info
 resp_p = requests.get(
 f"{PROTEINS_API}/proteins/{uniprot_id}", headers=headers
 )
 resp_p.raise_for_status
 protein = resp_p.json

 # Features
 resp_f = requests.get(
 f"{PROTEINS_API}/features/{uniprot_id}", headers=headers
 )
 features = resp_f.json if resp_f.status_code == 200 else {}

 feature_list = features.get("features", [])
 domains = [f for f in feature_list if f.get("type") == "DOMAIN"]
 variants = [f for f in feature_list if f.get("type") == "VARIANT"]

 print(f"Proteins API {uniprot_id}: "
 f"{len(domains)} domains, {len(variants)} variants")
 return protein, feature_list
```

## 4. Complex Portal 

```python
def get_complex_portal(complex_id):
 """
 Complex Portal fromprotein's detailsretrieval。

 Parameters:
 complex_id: str — Complex Portal ID (e.g., "CPX-1")

 """
 url = (
 f"https://www.ebi.ac.uk/intact/complex-ws/complex/{complex_id}"
 )
 resp = requests.get(url, headers={"Accept": "application/json"})
 resp.raise_for_status
 data = resp.json

 participants = data.get("participants", [])
 subunits = []
 for p in participants:
 interactor = p.get("interactor", {})
 subunits.append({
 "identifier": interactor.get("identifier", ""),
 "name": interactor.get("name", ""),
 "stoichiometry": p.get("stoichiometry", ""),
 })

 print(f"Complex Portal {complex_id}: "
 f"{data.get('name', '?')}, {len(subunits)} subunits")
 return data, subunits
```

## 5. DeepGO prediction & EVE variant/mutationevaluation

```python
def predict_deepgo_function(sequence):
 """
 DeepGO proteinsequencefrom GO prediction。

 """
 url = "https://deepgo.cbrc.kaust.edu.sa/deepgo/api/create"
 resp = requests.post(url, json={"data_format": "fasta", "data": sequence})
 resp.raise_for_status
 data = resp.json

 predictions = data.get("predictions", [])
 print(f"DeepGO: {len(predictions)} GO term predictions")
 return predictions


def get_eve_variant_score(gene_name, variant=None):
 """
 EVE (Evolutionary model of Variant Effect) by/via
 missense variant/mutation'sretrieval。

 """
 url = f"https://evemodel.org/api/proteins/{gene_name}"

 if variant:
 url += f"/variants/{variant}"

 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 if variant:
 score = data.get("eve_score", None)
 classification = data.get("eve_class", "")
 print(f"EVE {gene_name} {variant}: score={score}, class={classification}")
 else:
 print(f"EVE {gene_name}: found")

 return data
```

## References

### Output Files

| File | Format |
|---|---|
| `results/pdbe_entry.json` | JSON |
| `results/emdb_structure.json` | JSON |
| `results/protein_features.json` | JSON |
| `results/complex_portal.json` | JSON |
| `results/deepgo_predictions.json` | JSON |
| `results/eve_scores.json` | JSON |

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
| `scientific-protein-structure-analysis` | proteinstructure |
| `scientific-proteomics-mass-spectrometry` | proteomics |
| `scientific-protein-interaction-network` | PPI |
| `scientific-molecular-docking` | |
| `scientific-variant-interpretation` | variant/mutation |

### Dependencies

`requests`, `pandas`
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
