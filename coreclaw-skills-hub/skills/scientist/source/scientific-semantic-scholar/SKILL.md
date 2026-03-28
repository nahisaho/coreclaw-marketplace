---
name: scientific-semantic-scholar
description: |
 Semantic Scholar graphskill。Semantic Scholar Academic
 Graph API by/viapapersearchauthorfilecitationgraph
 TLDR 。---

# Scientific Semantic Scholar

Semantic Scholar Academic Graph API utilizingpapersearch
citationnetworkanalysisauthorfilepaperpipeline
is provided.

## When to Use

- paperhigh-accuracy searchwhen needed
- citationcitationnetworkanalysiswhen needed
- author's h-indexpapernumber/countresearch is investigatedand
- paper's and
- TLDR (automated) is retrievedand
- min's citation minwhen needed
- PubMed/OpenAlex 's search and

---

## Quick Start

## 1. papersearch

```python
import requests
import pandas as pd

S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_HEADERS = {} # API key: {"x-api-key": "YOUR_KEY"}


def semantic_scholar_search(query, limit=50,
 year_range=None,
 fields_of_study=None):
 """
 Semantic Scholar — papersearch。

 Parameters:
 query: str — search query
 limit: int — maximum results
 year_range: str — range (example: "2020-2024")
 fields_of_study: list[str] — minfilter
 """
 url = f"{S2_BASE}/paper/search"
 params = {
 "query": query,
 "limit": min(limit, 100),
 "fields": ("paperId,title,year,citationCount,"
 "influentialCitationCount,authors,"
 "journal,tldr,openAccessPdf,fieldsOfStudy"),
 }
 if year_range:
 params["year"] = year_range
 if fields_of_study:
 params["fieldsOfStudy"] = ",".join(fields_of_study)

 resp = requests.get(url, params=params,
 headers=S2_HEADERS, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for p in data.get("data", []):
 authors = [a.get("name", "") for a in p.get("authors", [])]
 tldr_text = ""
 if p.get("tldr"):
 tldr_text = p["tldr"].get("text", "")
 results.append({
 "paper_id": p.get("paperId", ""),
 "title": p.get("title", ""),
 "year": p.get("year"),
 "citation_count": p.get("citationCount", 0),
 "influential_citations": p.get(
 "influentialCitationCount", 0),
 "authors": "; ".join(authors[:5]),
 "journal": (p.get("journal") or {}).get("name", ""),
 "fields": ", ".join(p.get("fieldsOfStudy") or []),
 "tldr": tldr_text[:300],
 "pdf_url": (p.get("openAccessPdf") or {}).get("url", ""),
 })

 df = pd.DataFrame(results)
 print(f"Semantic Scholar: {len(df)} papers "
 f"(query='{query}')")
 return df


def semantic_scholar_get_paper(paper_id):
 """
 Semantic Scholar — paperdetailsretrieval。

 Parameters:
 paper_id: str — S2 Paper ID / DOI / ArXiv ID
 """
 url = f"{S2_BASE}/paper/{paper_id}"
 params = {
 "fields": ("paperId,title,year,abstract,citationCount,"
 "influentialCitationCount,authors,references,"
 "citations,journal,tldr,openAccessPdf,"
 "fieldsOfStudy,publicationDate,venue"),
 }
 resp = requests.get(url, params=params,
 headers=S2_HEADERS, timeout=30)
 resp.raise_for_status
 return resp.json
```

## 2. authorfilecitationanalysis

```python
def semantic_scholar_author(author_id, paper_limit=100):
 """
 Semantic Scholar — authorfileretrieval。

 Parameters:
 author_id: str — S2 Author ID
 paper_limit: int — retrievalpapernumber/count
 """
 url = f"{S2_BASE}/author/{author_id}"
 params = {
 "fields": ("authorId,name,affiliations,homepage,"
 "paperCount,citationCount,hIndex"),
 }
 resp = requests.get(url, params=params,
 headers=S2_HEADERS, timeout=30)
 resp.raise_for_status
 profile = resp.json

 # paperlist
 papers_url = f"{S2_BASE}/author/{author_id}/papers"
 p_params = {
 "fields": "paperId,title,year,citationCount,venue",
 "limit": min(paper_limit, 1000),
 }
 p_resp = requests.get(papers_url, params=p_params,
 headers=S2_HEADERS, timeout=30)
 p_resp.raise_for_status

 papers = []
 for p in p_resp.json.get("data", []):
 papers.append({
 "paper_id": p.get("paperId", ""),
 "title": p.get("title", ""),
 "year": p.get("year"),
 "citations": p.get("citationCount", 0),
 "venue": p.get("venue", ""),
 })

 papers_df = pd.DataFrame(papers)

 print(f"Author {profile.get('name', '')}: "
 f"h-index={profile.get('hIndex', 0)}, "
 f"{profile.get('paperCount', 0)} papers, "
 f"{profile.get('citationCount', 0)} citations")
 return profile, papers_df
```

## 3. citationnetworkdegreemin

```python
def semantic_scholar_citation_graph(paper_id,
 direction="both",
 limit=100):
 """
 Semantic Scholar — citationgraphretrieval。

 Parameters:
 paper_id: str — S2 Paper ID
 direction: str — "citations", "references", "both"
 limit: int — eachdirection's
 """
 graphs = {}
 fields = "paperId,title,year,citationCount,authors"

 if direction in ("citations", "both"):
 url = f"{S2_BASE}/paper/{paper_id}/citations"
 resp = requests.get(url, params={"fields": fields,
 "limit": limit},
 headers=S2_HEADERS, timeout=30)
 resp.raise_for_status
 cites = []
 for c in resp.json.get("data", []):
 cp = c.get("citingPaper", {})
 cites.append({
 "paper_id": cp.get("paperId", ""),
 "title": cp.get("title", ""),
 "year": cp.get("year"),
 "citations": cp.get("citationCount", 0),
 })
 graphs["citations"] = pd.DataFrame(cites)

 if direction in ("references", "both"):
 url = f"{S2_BASE}/paper/{paper_id}/references"
 resp = requests.get(url, params={"fields": fields,
 "limit": limit},
 headers=S2_HEADERS, timeout=30)
 resp.raise_for_status
 refs = []
 for r in resp.json.get("data", []):
 rp = r.get("citedPaper", {})
 refs.append({
 "paper_id": rp.get("paperId", ""),
 "title": rp.get("title", ""),
 "year": rp.get("year"),
 "citations": rp.get("citationCount", 0),
 })
 graphs["references"] = pd.DataFrame(refs)

 for k, v in graphs.items:
 print(f" {k}: {len(v)} papers")
 return graphs
```

## 4. literatureintegrationpipeline

```python
def semantic_scholar_pipeline(query, year_range=None,
 output_dir="results"):
 """
 Semantic Scholar integrationpipeline。

 Parameters:
 query: str — search query
 year_range: str — range
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) papersearch
 papers = semantic_scholar_search(query,
 year_range=year_range)
 papers.to_csv(output_dir / "papers.csv", index=False)

 # 2) citationpaper'scitationgraph
 if not papers.empty:
 top = papers.sort_values("citation_count",
 ascending=False).iloc[0]
 pid = top["paper_id"]
 graphs = semantic_scholar_citation_graph(pid)
 for k, df in graphs.items:
 df.to_csv(output_dir / f"{k}.csv", index=False)

 # 3) citation
 if not papers.empty and "year" in papers.columns:
 yearly = papers.groupby("year").agg(
 papers_count=("paper_id", "count"),
 total_citations=("citation_count", "sum"),
 avg_citations=("citation_count", "mean"),
 ).reset_index
 yearly.to_csv(output_dir / "yearly_trend.csv",
 index=False)

 print(f"Semantic Scholar pipeline: {output_dir}")
 return {"papers": papers}
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
literature-search → semantic-scholar → deep-research
 (PubMed/NCBI) (Academic Graph API) (knowledge synthesis)
 │ │ ↓
 crossref-metadata ─────┘ citation-checker
 (DOI/metadata) │ (citationverification)
 ↓
 gene-expression-transcriptomics
 (papercitationdatafrom's analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/papers.csv` | papersearchresults | → deep-research |
| `results/citations.csv` | citationpaper | → citation-checker |
| `results/references.csv` | citationpaper | → meta-analysis |
| `results/yearly_trend.csv` | citation | → bibliometrics |
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
