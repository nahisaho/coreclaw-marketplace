---
name: scientific-reactome-pathways
description: |
 Reactome pathwayskill。Reactome Content Service
 REST API by/viapathwaysearchretrievalUniProt mapping
 pathwayfigureData Retrieval。ToolUniverse integration: reactome。
tu_tools:
 - key: reactome
 name: Reactome
 description: pathwaydatabase REST API
---

# Scientific Reactome Pathways

Reactome Content Service REST API utilizingpathwaysearch
structureretrievalUniProt accession→pathway mapping
pathwayfigureData Retrievalpipeline is provided。

## When to Use

- pathway name and keywordsearchwhen needed
- pathway is retrievedand
- UniProt accessionfrompathway mappingwhen needed
- pathway's (protein/compound) when needed
- pathwayfigure's layoutdata is retrievedand

---

## Quick Start

## 1. pathwaysearchdetailsretrieval

```python
import requests
import pandas as pd

REACTOME = "https://reactome.org/ContentService"


def reactome_search(query, species="Homo sapiens",
 limit=25):
 """
 Reactome — pathwaysearch。

 Parameters:
 query: str — search query (example: "apoptosis", "MAPK")
 species: str — species name (example: "Homo sapiens")
 limit: int — maximum results
 """
 url = f"{REACTOME}/search/query"
 params = {
 "query": query,
 "species": species,
 "types": "Pathway",
 "cluster": "true",
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for group in data.get("results", []):
 for entry in group.get("entries", [])[:limit]:
 rows.append({
 "stId": entry.get("stId", ""),
 "name": entry.get("name", ""),
 "species": entry.get("species", ""),
 "exact_type": entry.get(
 "exactType", ""),
 "compartments": "; ".join(
 entry.get("compartmentNames", [])),
 })

 df = pd.DataFrame(rows[:limit])
 print(f"Reactome search: '{query}' → {len(df)} "
 f"pathways")
 return df


def reactome_pathway_detail(pathway_id):
 """
 Reactome — pathwaydetailsretrieval。

 Parameters:
 pathway_id: str — Reactome Stable ID
 (example: "R-HSA-109581")
 """
 url = f"{REACTOME}/data/pathway/{pathway_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 result = {
 "stId": data.get("stId", ""),
 "name": data.get("displayName", ""),
 "species": data.get("speciesName", ""),
 "is_inferred": data.get("isInferred", False),
 "has_diagram": data.get("hasDiagram", False),
 "n_sub_events": len(
 data.get("hasEvent", [])),
 "n_compartments": len(
 data.get("compartment", [])),
 "release_date": data.get("releaseDate", ""),
 }
 return result
```

## 2. UniProt→pathway mapping

```python
def reactome_uniprot_pathways(uniprot_id,
 species="Homo sapiens"):
 """
 Reactome — UniProt → pathway mapping。

 Parameters:
 uniprot_id: str — UniProt accession
 (example: "P38398" = BRCA1)
 species: str — species name
 """
 url = f"{REACTOME}/data/pathways/low/entity/{uniprot_id}"
 params = {"species": species}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for pw in data:
 rows.append({
 "pathway_id": pw.get("stId", ""),
 "pathway_name": pw.get("displayName", ""),
 "species": pw.get("speciesName", ""),
 "has_diagram": pw.get("hasDiagram", False),
 })

 df = pd.DataFrame(rows)
 print(f"Reactome UniProt→pathway: {uniprot_id} "
 f"→ {len(df)} pathways")
 return df
```

## 3. pathwayretrieval

```python
def reactome_participants(pathway_id):
 """
 Reactome — pathwaylist。

 Parameters:
 pathway_id: str — Reactome Stable ID
 """
 url = (f"{REACTOME}/data/participants/"
 f"{pathway_id}")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data:
 pe_name = item.get("displayName", "")
 for ref in item.get("refEntities", []):
 rows.append({
 "pathway_id": pathway_id,
 "participant": pe_name,
 "db_name": ref.get("databaseName", ""),
 "identifier": ref.get("identifier", ""),
 "name": ref.get("displayName", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Reactome participants: {pathway_id} "
 f"→ {len(df)} entities")
 return df
```

## 4. Reactome integrationpipeline

```python
def reactome_pipeline(query_or_uniprot,
 output_dir="results"):
 """
 Reactome integrationpipeline。

 Parameters:
 query_or_uniprot: str — search query or UniProt ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 is_uniprot = (len(query_or_uniprot) == 6
 and query_or_uniprot[0].isalpha)

 if is_uniprot:
 # UniProt → pathway
 pathways = reactome_uniprot_pathways(
 query_or_uniprot)
 else:
 # search
 pathways = reactome_search(query_or_uniprot)

 pathways.to_csv(output_dir / "reactome_pathways.csv",
 index=False)

 # pathway's
 if not pathways.empty:
 top_id = (pathways.iloc[0].get("pathway_id")
 or pathways.iloc[0].get("stId"))
 parts = reactome_participants(top_id)
 parts.to_csv(
 output_dir / "reactome_participants.csv",
 index=False)

 print(f"Reactome pipeline: {output_dir}")
 return {"pathways": pathways}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `reactome` | Reactome | pathwaydatabase REST API |

## Pipeline Integration

```
pathway-enrichment → reactome-pathways → systems-biology
 (GO/pathway) (Reactome API) (networkanalysis)
 │ │ ↓
uniprot-proteome ──────────┘ metabolomics-databases
 (UniProt ID) (MetaCyc metabolism)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/reactome_pathways.csv` | pathwaylist | → pathway-enrichment |
| `results/reactome_participants.csv` | | → protein-interaction-network |
---

## Harness Optimization (v0.4.0)

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
