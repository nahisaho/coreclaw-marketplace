---
name: scientific-metabolomics-databases
description: |
 Metabolomics databases skill. HMDB/METLIN/MassBank database queries, metabolite annotation, spectral library matching, and cross-database metabolite identification.
---

# Scientific Metabolomics Databases

HMDB / MetaCyc / Metabolomics Workbench 's 3 database integration
metabolitepathway mappingbiomarkerpipeline is provided。

## When to Use

- amount (m/z) frommetabolitewhen needed
- HMDB metabolite's is investigatedand
- MetaCyc metabolismpathway'sdetails is verifiedand
- Metabolomics Workbench 'sdataset is searchedand
- multiple DB cross-cuttingmetaboliteannotationwhen needed

---

## Quick Start

## 1. HMDB metabolite search

```python
import requests
import pandas as pd
import xml.etree.ElementTree as ET


def hmdb_search(query, search_type="name", max_results=50):
 """
 HMDB (Human Metabolome Database) search。

 Parameters:
 query: str — search query (metabolite, HMDB ID, formula)
 search_type: "name", "hmdb_id", "formula", "mass"
 """

 base_url = "https://hmdb.ca/metabolites"

 if search_type == "hmdb_id":
 url = f"{base_url}/{query}.xml"
 resp = requests.get(url, timeout=30)
 if resp.status_code == 200:
 root = ET.fromstring(resp.text)
 ns = {"hmdb": "http://www.hmdb.ca"}
 result = {
 "hmdb_id": root.findtext("hmdb:accession", "", ns),
 "name": root.findtext("hmdb:name", "", ns),
 "chemical_formula": root.findtext("hmdb:chemical_formula", "", ns),
 "monoisotopic_mass": float(root.findtext(
 "hmdb:monisotopic_molecular_weight", "0", ns) or 0),
 "description": (root.findtext("hmdb:description", "", ns) or "")[:300],
 "status": root.findtext("hmdb:status", "", ns),
 "biological_role": root.findtext(
 "hmdb:ontology/hmdb:root/hmdb:term", "", ns),
 }
 return pd.DataFrame([result])

 # namesearch
 results = []
 params = {"query": query, "search_type": search_type}
 print(f"HMDB search: '{query}' (type={search_type})")
 return pd.DataFrame(results)
```

## 2. MetaCyc metabolismpathwaysearch

```python
def metacyc_pathway_search(query, organism="Homo sapiens"):
 """
 MetaCyc metabolismpathwaysearch。

 Parameters:
 query: str — pathway/metabolite/enzyme
 organism: str — organism/speciesfilter
 """
 # MetaCyc_search_pathways, MetaCyc_get_pathway
 # MetaCyc_get_compound, MetaCyc_get_reaction

 results = {
 "query": query,
 "organism": organism,
 "database": "MetaCyc",
 "tools": [
 "MetaCyc_search_pathways — pathwaysearch",
 "MetaCyc_get_pathway — pathwaydetails (reactionenzymemetabolite)",
 "MetaCyc_get_compound — compounddetails (structure)",
 "MetaCyc_get_reaction — reactiondetails (generationenzyme)",
 ],
 }

 print(f"MetaCyc: querying '{query}' for {organism}")
 return results
```

## 3. Metabolomics Workbench Data Retrieval

```python
def metabolomics_workbench_search(query, search_type="compound_name",
 exact_mass=None, mz_tolerance=0.01):
 """
 NIH Metabolomics Workbench REST API search。

 Parameters:
 query: str — search query
 search_type: "compound_name", "refmet", "study", "exact_mass", "mz"
 exact_mass: float — amount (search_type="exact_mass" )
 mz_tolerance: float — m/z (Da)
 """
 base_url = "https://www.metabolomicsworkbench.org/rest"

 # MetabolomicsWorkbench_search_compound_by_name
 # MetabolomicsWorkbench_get_refmet_info
 # MetabolomicsWorkbench_get_study
 # MetabolomicsWorkbench_search_by_exact_mass
 # MetabolomicsWorkbench_search_by_mz
 # MetabolomicsWorkbench_get_compound_by_pubchem_cid

 if search_type == "compound_name":
 url = f"{base_url}/compound/name/{query}/all/"
 elif search_type == "refmet":
 url = f"{base_url}/refmet/name/{query}/all/"
 elif search_type == "study":
 url = f"{base_url}/study/study_id/{query}/summary/"
 elif search_type == "exact_mass":
 url = f"{base_url}/compound/exact_mass/{exact_mass}/tolerance/{mz_tolerance}/"
 elif search_type == "mz":
 url = f"{base_url}/compound/mz_value/{query}/tolerance/{mz_tolerance}/"
 else:
 raise ValueError(f"Unknown search_type: {search_type}")

 resp = requests.get(url, timeout=30)
 if resp.status_code == 200:
 try:
 data = resp.json
 if isinstance(data, list):
 df = pd.DataFrame(data)
 elif isinstance(data, dict):
 df = pd.DataFrame([data])
 else:
 df = pd.DataFrame
 except Exception:
 df = pd.DataFrame
 else:
 df = pd.DataFrame

 print(f"Metabolomics Workbench ({search_type}): {len(df)} results")
 return df
```

## 4. m/z metabolite ( DB)

```python
def identify_metabolites_by_mass(mz_values, adducts=None,
 tolerance_ppm=10,
 databases=None):
 """
 m/z valuefrommultiple DB cross-cuttingmetabolite。

 Parameters:
 mz_values: list[float] — m/z value
 adducts: list — (e.g., ["[M+H]+", "[M+Na]+", "[M-H]-"])
 tolerance_ppm: float — amount (ppm)
 databases: list — search DB ("hmdb", "metacyc", "mwb")
 """
 import numpy as np

 if adducts is None:
 adducts = [
 {"name": "[M+H]+", "mass_diff": 1.007276, "mode": "positive"},
 {"name": "[M+Na]+", "mass_diff": 22.989218, "mode": "positive"},
 {"name": "[M-H]-", "mass_diff": -1.007276, "mode": "negative"},
 {"name": "[M+NH4]+", "mass_diff": 18.034164, "mode": "positive"},
 ]

 if databases is None:
 databases = ["hmdb", "mwb"]

 all_results = []

 for mz in mz_values:
 for adduct in adducts:
 neutral_mass = mz - adduct["mass_diff"]
 tolerance_da = neutral_mass * tolerance_ppm / 1e6

 result = {
 "query_mz": mz,
 "adduct": adduct["name"],
 "neutral_mass": round(neutral_mass, 6),
 "tolerance_da": round(tolerance_da, 6),
 "databases_queried": databases,
 }
 all_results.append(result)

 df = pd.DataFrame(all_results)
 print(f"Mass-based ID: {len(mz_values)} m/z values × "
 f"{len(adducts)} adducts = {len(df)} queries "
 f"across {databases}")
 return df
```

## 5. RefMet standardization

```python
def refmet_standardize(metabolite_names):
 """
 RefMet (Reference Metabolomics) standardization。

 Parameters:
 metabolite_names: list — metabolite (standardization)
 """
 results = []

 for name in metabolite_names:
 result = {
 "input_name": name,
 "refmet_name": None,
 "super_class": None,
 "main_class": None,
 "sub_class": None,
 "formula": None,
 "exact_mass": None,
 }
 results.append(result)

 df = pd.DataFrame(results)
 print(f"RefMet standardization: {len(df)} metabolites queried")
 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/hmdb_metabolites.csv` | CSV |
| `results/metacyc_pathways.json` | JSON |
| `results/mwb_compounds.csv` | CSV |
| `results/mass_id_results.csv` | CSV |
| `results/refmet_standardized.csv` | CSV |
| `figures/metabolite_class_distribution.png` | PNG |

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
| `scientific-metabolomics` | PLS-DA/VIP analysis |
| `scientific-pathway-enrichment` | metabolite → pathway |
| `scientific-cheminformatics` | molecular descriptors and structural analysis |
| `scientific-systems-biology` | FBA metabolism |
| `scientific-multi-omics` | ↔ omicsintegration |

### Dependencies

`requests`, `pandas`, `numpy`, `xml.etree.ElementTree` (stdlib)
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
