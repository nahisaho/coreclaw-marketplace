---
name: scientific-ebi-databases
description: |
 EBI databasegroupintegrationskill。EBI Search cross-cuttingsearch、ENA Browser
 、BioStudies researchdata、dbfetch entryretrieval、
 MetaboLights 'sintegrationpipeline。
---

# Scientific EBI Databases

EBI Search / ENA Browser / BioStudies / dbfetch / MetaboLights integration
EBI databasegrouppipeline is provided。

## When to Use

- EBI Search multipledatabasecross-cuttingsearchwhen needed
- ENA (European Nucleotide Archive) sequencedata is searchedand
- BioStudies researchdata and
- dbfetch entryretrievalwhen needed
- MetaboLights experimentdatawhen needed

---

## Quick Start

## 1. EBI Search cross-cuttingsearch

```python
import requests
import pandas as pd

EBI_SEARCH_API = "https://www.ebi.ac.uk/ebisearch/ws/rest"


def search_ebi(query, domain="allebi", size=25, fields=None):
 """
 EBI Search cross-cuttingsearch — multiple EBI databasesearch。

 Parameters:
 query: str — search query
 domain: str — search ("allebi", "uniprot", "pdb", "ena", etc.)
 size: int — maximum retrieval count
 fields: list — field

 ToolUniverse:
 EBI_Search_query(query=query, domain=domain)
 EBI_Search_get_entry(domain=domain, entry_id=entry_id)
 """
 params = {
 "query": query,
 "size": size,
 "format": "json",
 }
 if fields:
 params["fields"] = ",".join(fields)

 resp = requests.get(f"{EBI_SEARCH_API}/{domain}", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for entry in data.get("entries", []):
 row = {"id": entry.get("id", ""), "source": entry.get("source", "")}
 for field in entry.get("fields", {}):
 row[field] = entry["fields"][field][0] if entry["fields"][field] else ""
 results.append(row)

 df = pd.DataFrame(results)
 total = data.get("hitCount", 0)
 print(f"EBI Search [{domain}] '{query}': {total} total hits, {len(df)} returned")
 return df
```

## 2. ENA (European Nucleotide Archive) sequencesearch

```python
ENA_API = "https://www.ebi.ac.uk/ena/browser/api"


def search_ena(query, result_type="sequence", limit=100):
 """
 ENA search。

 Parameters:
 query: str — search query or Taxon ID
 result_type: str — "sequence", "read_run", "analysis", "study"
 limit: int — maximum retrieval count

 ToolUniverse:
 ENA_search(query=query, result=result_type)
 ENA_get_entry(accession=accession)
 """
 params = {
 "query": query,
 "result": result_type,
 "limit": limit,
 "format": "json",
 }
 resp = requests.get(f"{ENA_API}/search", params=params)
 resp.raise_for_status
 data = resp.json

 df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame
 print(f"ENA search '{query}' [{result_type}]: {len(df)} entries")
 return df


def get_ena_entry(accession, display="json"):
 """
 ENA accessionnumberby/viaentryretrieval。

 Parameters:
 accession: str — ENA accession (e.g., "ERS000001", "ERR000001")
 """
 resp = requests.get(
 f"{ENA_API}/entry/{accession}",
 params={"display": display}
 )
 resp.raise_for_status
 print(f"ENA entry {accession}: retrieved")
 return resp.json if display == "json" else resp.text
```

## 3. BioStudies researchdatasearch

```python
BIOSTUDIES_API = "https://www.ebi.ac.uk/biostudies/api/v1"


def search_biostudies(query, page_size=25):
 """
 BioStudies researchdatasearch。

 Parameters:
 query: str — search query
 page_size: int — 

 ToolUniverse:
 BioStudies_search(query=query)
 BioStudies_get_study(accession=accession)
 """
 params = {"query": query, "pageSize": page_size}
 resp = requests.get(f"{BIOSTUDIES_API}/search", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 results.append({
 "accession": hit.get("accno", ""),
 "title": hit.get("title", ""),
 "author": hit.get("author", ""),
 "release_date": hit.get("rtime", ""),
 "type": hit.get("type", ""),
 "files": hit.get("files", 0),
 "links": hit.get("links", 0),
 })

 df = pd.DataFrame(results)
 total = data.get("totalHits", 0)
 print(f"BioStudies search '{query}': {total} total, {len(df)} returned")
 return df
```

## 4. dbfetch entryretrieval

```python
DBFETCH_API = "https://www.ebi.ac.uk/Tools/dbfetch/dbfetch"


def dbfetch(db, ids, format_type="json", style="raw"):
 """
 dbfetch — EBI databaseentryretrieval。

 Parameters:
 db: str — database (e.g., "uniprotkb", "embl", "pdb")
 ids: list — ID 
 format_type: str — outputshapeformula ("json", "fasta", "xml")
 style: str — ("raw", "html")

 ToolUniverse:
 dbfetch_get_entries(db=db, ids=ids, format=format_type)
 """
 ids_str = ",".join(ids) if isinstance(ids, list) else ids
 params = {
 "db": db,
 "id": ids_str,
 "format": format_type,
 "style": style,
 }
 resp = requests.get(DBFETCH_API, params=params)
 resp.raise_for_status

 print(f"dbfetch [{db}]: {len(ids) if isinstance(ids, list) else 1} entries, "
 f"format={format_type}")
 if format_type == "json":
 return resp.json
 return resp.text
```

## 5. MetaboLights 

```python
METABOLIGHTS_API = "https://www.ebi.ac.uk/metabolights/ws"


def search_metabolights(query):
 """
 MetaboLights experimentdatasearch。

 Parameters:
 query: str — search query (compound、disease、organism/species)

 ToolUniverse:
 MetaboLights_search_studies(query=query)
 MetaboLights_get_study(study_id=study_id)
 """
 resp = requests.get(
 f"{METABOLIGHTS_API}/studies/search",
 params={"query": query}
 )
 resp.raise_for_status
 data = resp.json

 results = []
 for study in data.get("content", []):
 results.append({
 "study_id": study.get("studyIdentifier", ""),
 "title": study.get("title", ""),
 "organism": study.get("organism", ""),
 "description": (study.get("description") or "")[:200],
 "submission_date": study.get("submissionDate", ""),
 "status": study.get("studyStatus", ""),
 })

 df = pd.DataFrame(results)
 print(f"MetaboLights search '{query}': {len(df)} studies")
 return df


def get_metabolights_study(study_id):
 """MetaboLights unitsresearchretrieval。"""
 resp = requests.get(f"{METABOLIGHTS_API}/studies/{study_id}")
 resp.raise_for_status
 data = resp.json
 print(f"MetaboLights {study_id}: {data.get('title', '')[:80]}")
 return data
```

---

## Available Tools

| ToolUniverse Category | Key Tools |
|---|---|
| `ebi_search` | `EBI_Search_query`, `EBI_Search_get_entry` |
| `ena_browser` | `ENA_search`, `ENA_get_entry` |
| `biostudies` | `BioStudies_search`, `BioStudies_get_study` |
| `dbfetch` | `dbfetch_get_entries` |
| `metabolights` | `MetaboLights_search_studies`, `MetaboLights_get_study` |

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/ebi_search.csv` | EBI cross-cuttingsearchresults | → bioinformatics, literature-search |
| `results/ena_sequences.fasta` | ENA sequencedata | → genome-sequence-tools, sequence-analysis |
| `results/biostudies_metadata.json` | researchinformation | → multi-omics, systematic-review |
| `results/metabolights_study.json` | data | → metabolomics, metabolomics-databases |

## Pipeline Integration

```
genome-sequence-tools ──→ ebi-databases ──→ metabolomics-databases
 (NCBI/BLAST) (ENA/EBI Search) (HMDB/MetaCyc)
 │
 ├──→ bioinformatics (sequencedata)
 ├──→ sequence-analysis (FASTA)
 └──→ structural-proteomics (PDBe cross-ref)
```
---

## Harness Optimization (v0.4.0)

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
