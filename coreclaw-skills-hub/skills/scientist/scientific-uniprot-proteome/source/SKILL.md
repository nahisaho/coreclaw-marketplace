---
name: scientific-uniprot-proteome
description: |
 UniProt proteome skill. UniProt protein sequence/annotation retrieval, proteome-wide queries, functional annotation extraction, and protein feature analysis.
---

# Scientific UniProt Proteome

UniProt REST API utilizingprotein searchID mapping
annotationretrievalproteomeanalysispipeline is provided。

## When to Use

- protein's amino acidsequenceinformation is searchedand
- UniProt ID anddatabase ID phasetransformationwhen needed
- protein'sGO annotationdisease is investigatedand
- proteome's proteinanalysis is performedand
- UniRef UniParc cross-cuttingsearchwhen needed
- organism/speciesand 'sproteome is retrievedand

---

## Quick Start

## 1. protein searchentryretrieval

```python
import requests
import pandas as pd

UNIPROT_BASE = "https://rest.uniprot.org"


def uniprot_search(query, organism=None, reviewed=True,
 limit=50, fields=None):
 """
 UniProt — protein search。

 Parameters:
 query: str — search query (example: "BRCA1", "kinase")
 organism: str — organism/species (example: "9606" for Human)
 reviewed: bool — Swiss-Prot 's (True) / TrEMBL includes (False)
 limit: int — maximum results
 fields: list[str] — field
 """
 url = f"{UNIPROT_BASE}/uniprotkb/search"
 default_fields = [
 "accession", "id", "protein_name", "gene_names",
 "organism_name", "length", "reviewed",
 "go_p", "go_f", "go_c",
 ]
 params = {
 "query": query,
 "size": min(limit, 500),
 "fields": ",".join(fields or default_fields),
 "format": "json",
 }
 if organism:
 params["query"] += f" AND organism_id:{organism}"
 if reviewed:
 params["query"] += " AND reviewed:true"

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for entry in data.get("results", []):
 protein_name = ""
 if entry.get("proteinDescription"):
 rec = entry["proteinDescription"].get(
 "recommendedName")
 if rec:
 protein_name = rec.get("fullName", {}).get(
 "value", "")

 genes = [g.get("geneName", {}).get("value", "")
 for g in entry.get("genes", [])]

 results.append({
 "accession": entry.get("primaryAccession", ""),
 "entry_name": entry.get("uniProtkbId", ""),
 "protein_name": protein_name,
 "gene_names": "; ".join(genes),
 "organism": entry.get("organism", {}).get(
 "scientificName", ""),
 "length": entry.get("sequence", {}).get(
 "length", 0),
 "reviewed": entry.get("entryType", "") == "UniProtKB reviewed (Swiss-Prot)",
 })

 df = pd.DataFrame(results)
 print(f"UniProt search: {len(df)} entries "
 f"(query='{query}')")
 return df


def uniprot_get_entry(accession, format="json"):
 """
 UniProt — entrydetailsretrieval。

 Parameters:
 accession: str — UniProt ID (example: "P38398")
 format: str — "json" or "fasta"
 """
 url = f"{UNIPROT_BASE}/uniprotkb/{accession}"
 resp = requests.get(url, params={"format": format},
 timeout=30)
 resp.raise_for_status
 if format == "fasta":
 return resp.text
 return resp.json
```

## 2. ID mapping

```python
import time


def uniprot_id_mapping(from_db, to_db, ids):
 """
 UniProt — ID mapping (job)。

 Parameters:
 from_db: str — transformation DB (example: "UniProtKB_AC-ID")
 to_db: str — transformation DB (example: "Gene_Name", "PDB",
 "Ensembl", "RefSeq_Protein")
 ids: list[str] — ID 
 """
 # job
 url = f"{UNIPROT_BASE}/idmapping/run"
 resp = requests.post(url, data={
 "from": from_db, "to": to_db,
 "ids": ",".join(ids),
 }, timeout=30)
 resp.raise_for_status
 job_id = resp.json["jobId"]

 # 
 status_url = f"{UNIPROT_BASE}/idmapping/status/{job_id}"
 for _ in range(30):
 s = requests.get(status_url, timeout=30).json
 if "results" in s or "redirectURL" in s:
 break
 time.sleep(2)

 # resultsretrieval
 result_url = (f"{UNIPROT_BASE}/idmapping/results/"
 f"{job_id}")
 r = requests.get(result_url, timeout=30)
 r.raise_for_status
 data = r.json

 results = []
 for item in data.get("results", []):
 results.append({
 "from_id": item.get("from", ""),
 "to_id": item.get("to", ""),
 })

 df = pd.DataFrame(results)
 print(f"UniProt ID mapping: {len(df)} mappings "
 f"({from_db} → {to_db})")
 return df
```

## 3. annotationretrieval

```python
def uniprot_get_features(accession):
 """
 UniProt — proteinretrieval。

 Parameters:
 accession: str — UniProt ID
 """
 entry = uniprot_get_entry(accession)

 features = []
 for f in entry.get("features", []):
 loc = f.get("location", {})
 start = loc.get("start", {}).get("value")
 end = loc.get("end", {}).get("value")
 features.append({
 "type": f.get("type", ""),
 "description": f.get("description", ""),
 "start": start,
 "end": end,
 "evidence": len(f.get("evidences", [])),
 })

 df = pd.DataFrame(features)
 print(f"UniProt features: {accession} → "
 f"{len(df)} features")
 return df
```

## 4. UniProt integrationpipeline

```python
def uniprot_pipeline(gene_names, organism="9606",
 output_dir="results"):
 """
 UniProt integrationpipeline。

 Parameters:
 gene_names: list[str] — gene symbol list
 organism: str — organism/species Taxonomy ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 all_entries = []
 for gene in gene_names:
 try:
 df = uniprot_search(gene, organism=organism)
 all_entries.append(df)
 except Exception as e:
 print(f" Warning: {gene} — {e}")

 if all_entries:
 combined = pd.concat(all_entries, ignore_index=True)
 combined.to_csv(output_dir / "uniprot_entries.csv",
 index=False)

 # entry's
 if not combined.empty:
 top_acc = combined.iloc[0]["accession"]
 features = uniprot_get_features(top_acc)
 features.to_csv(
 output_dir / "protein_features.csv",
 index=False)

 print(f"UniProt pipeline: {output_dir}")
 return {"entries": combined if all_entries else pd.DataFrame}
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
3. Write `report.md` summarizing methods, results, and interpretation

## Pipeline Integration

```
protein-structure-analysis → uniprot-proteome → protein-design
 (PDB/AlphaFold structure) (UniProt REST API) (de novo design)
 │ │ ↓
 alphafold-structures ──────────┘ drug-target-profiling
 (AlphaFold DB) │ 
 ↓
 protein-domain-family
 (InterPro/Pfam)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/uniprot_entries.csv` | protein searchresults | → protein-structure-analysis |
| `results/protein_features.csv` | | → protein-domain-family |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
