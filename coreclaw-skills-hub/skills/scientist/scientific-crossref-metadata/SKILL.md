---
name: scientific-crossref-metadata
description: |
 Crossref metadata skill. Scholarly publication metadata retrieval, citation count tracking, DOI resolution, funder information extraction, and bibliometric analysis via Crossref API.
tu_tools:
 - key: crossref
 name: CrossRef
 description: DOI paperdatacitationnumber/countinformation
---

# Scientific CrossRef Metadata

CrossRef REST API utilizingliterature DOI datasearch
citationmininformationregistrysearchpipeline
is provided.

## When to Use

- DOI frompaperdata is retrievedand
- literature titleauthorsearchwhen needed
- 's ISSN and information is investigatedand
- paper's citationnumber/countcitationnumber/count is verifiedand
- research's information is searchedand
- referenceliterature's Data Retrievalwhen needed
- publication and 's publication minwhen needed

---

## Quick Start

## 1. DOI paperdata

```python
import requests
import pandas as pd

CR_BASE = "https://api.crossref.org"
CR_HEADERS = {
 "User-Agent": "SATORI/0.18.0 (mailto:your@email.com)",
}


def crossref_resolve_doi(doi):
 """
 CrossRef — DOI fromData Retrieval。

 Parameters:
 doi: str — DOI (example: "10.1038/s41586-020-2649-2")
 """
 url = f"{CR_BASE}/works/{doi}"
 resp = requests.get(url, headers=CR_HEADERS, timeout=30)
 resp.raise_for_status
 item = resp.json.get("message", {})

 authors = []
 for a in item.get("author", []):
 name = f"{a.get('given', '')} {a.get('family', '')}"
 authors.append(name.strip)

 result = {
 "doi": item.get("DOI", ""),
 "title": " ".join(item.get("title", [])),
 "authors": "; ".join(authors[:10]),
 "journal": " ".join(
 item.get("container-title", [])),
 "publisher": item.get("publisher", ""),
 "type": item.get("type", ""),
 "published_date": _cr_date(
 item.get("published-print") or
 item.get("published-online")),
 "citation_count": item.get(
 "is-referenced-by-count", 0),
 "reference_count": item.get("reference-count", 0),
 "issn": ", ".join(item.get("ISSN", [])),
 "url": item.get("URL", ""),
 "abstract": (item.get("abstract") or "")[:500],
 "funder": "; ".join(
 f.get("name", "")
 for f in item.get("funder", [])),
 "license": _cr_license(item),
 }

 print(f"CrossRef DOI: {doi}")
 print(f" {result['title'][:80]}")
 print(f" Citations: {result['citation_count']}")
 return result


def _cr_date(date_obj):
 if not date_obj:
 return ""
 parts = date_obj.get("date-parts", [[]])[0]
 return "-".join(str(p) for p in parts)


def _cr_license(item):
 licenses = item.get("license", [])
 if licenses:
 return licenses[0].get("content-version", "")
 return ""
```

## 2. papersearch

```python
def crossref_search_works(query, limit=50,
 sort="relevance",
 filter_type=None,
 from_date=None):
 """
 CrossRef — papersearch。

 Parameters:
 query: str — search query
 limit: int — maximum results
 sort: str — ("relevance", "published",
 "is-referenced-by-count")
 filter_type: str — literaturefilter
 (example: "journal-article")
 from_date: str — start (example: "2020-01-01")
 """
 url = f"{CR_BASE}/works"
 params = {
 "query": query,
 "rows": min(limit, 1000),
 "sort": sort,
 }

 filters = []
 if filter_type:
 filters.append(f"type:{filter_type}")
 if from_date:
 filters.append(f"from-pub-date:{from_date}")
 if filters:
 params["filter"] = ",".join(filters)

 resp = requests.get(url, params=params,
 headers=CR_HEADERS, timeout=30)
 resp.raise_for_status
 data = resp.json.get("message", {})

 results = []
 for item in data.get("items", []):
 authors = []
 for a in item.get("author", []):
 name = f"{a.get('given', '')} {a.get('family', '')}"
 authors.append(name.strip)
 results.append({
 "doi": item.get("DOI", ""),
 "title": " ".join(item.get("title", [])),
 "authors": "; ".join(authors[:5]),
 "journal": " ".join(
 item.get("container-title", [])),
 "year": _cr_date(
 item.get("published-print") or
 item.get("published-online")),
 "citations": item.get(
 "is-referenced-by-count", 0),
 "type": item.get("type", ""),
 })

 df = pd.DataFrame(results)
 total = data.get("total-results", 0)
 print(f"CrossRef search: {len(df)}/{total} works "
 f"(query='{query}')")
 return df
```

## 3. informationsearch

```python
def crossref_journal_info(issn):
 """
 CrossRef — informationretrieval。

 Parameters:
 issn: str — ISSN (example: "0028-0836")
 """
 url = f"{CR_BASE}/journals/{issn}"
 resp = requests.get(url, headers=CR_HEADERS, timeout=30)
 resp.raise_for_status
 data = resp.json.get("message", {})

 counts = data.get("counts", {})
 result = {
 "issn": issn,
 "title": data.get("title", ""),
 "publisher": data.get("publisher", ""),
 "subjects": "; ".join(
 s.get("name", "")
 for s in data.get("subjects", [])),
 "total_dois": counts.get("total-dois", 0),
 "current_dois": counts.get("current-dois", 0),
 "backfile_dois": counts.get("backfile-dois", 0),
 }

 print(f"CrossRef journal: {result['title']} "
 f"({result['total_dois']} DOIs)")
 return result


def crossref_search_funders(query, limit=20):
 """
 CrossRef — search。

 Parameters:
 query: str — (example: "NIH", "JSPS")
 limit: int — maximum results
 """
 url = f"{CR_BASE}/funders"
 params = {"query": query, "rows": limit}
 resp = requests.get(url, params=params,
 headers=CR_HEADERS, timeout=30)
 resp.raise_for_status
 data = resp.json.get("message", {})

 results = []
 for item in data.get("items", []):
 results.append({
 "funder_id": item.get("id", ""),
 "name": item.get("name", ""),
 "location": item.get("location", ""),
 "alt_names": "; ".join(
 item.get("alt-names", [])[:3]),
 "work_count": item.get("work-count", 0),
 })

 df = pd.DataFrame(results)
 print(f"CrossRef funders: {len(df)} (query='{query}')")
 return df
```

## 4. CrossRef integrationpipeline

```python
def crossref_pipeline(query, dois=None,
 output_dir="results"):
 """
 CrossRef integrationpipeline。

 Parameters:
 query: str — search query
 dois: list[str] — DOI 
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) papersearch
 works = crossref_search_works(query)
 works.to_csv(output_dir / "works.csv", index=False)

 # 2) DOI 
 if dois:
 resolved = []
 for doi in dois:
 try:
 meta = crossref_resolve_doi(doi)
 resolved.append(meta)
 except Exception as e:
 print(f" Warning: {doi} — {e}")
 continue
 resolved_df = pd.DataFrame(resolved)
 resolved_df.to_csv(output_dir / "doi_resolved.csv",
 index=False)

 # 3) citationmin
 if not works.empty:
 stats = {
 "total_works": len(works),
 "total_citations": works["citations"].sum,
 "mean_citations": works["citations"].mean,
 "median_citations": works["citations"].median,
 "max_citations": works["citations"].max,
 }
 pd.DataFrame([stats]).to_csv(
 output_dir / "citation_stats.csv", index=False)

 print(f"CrossRef pipeline: {output_dir}")
 return {"works": works}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `crossref` | CrossRef | DOI datacitationinformation |

## Pipeline Integration

```
literature-search → crossref-metadata → citation-checker
 (PubMed/NCBI) (CrossRef REST API) (citationverification)
 │ │ ↓
 semantic-scholar ──────┘ deep-research
 (S2 Academic Graph) │ (integration)
 ↓
 bibliometrics
 (amountmin)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/works.csv` | papersearchresults | → semantic-scholar |
| `results/doi_resolved.csv` | DOI data | → citation-checker |
| `results/citation_stats.csv` | citation | → bibliometrics |
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
