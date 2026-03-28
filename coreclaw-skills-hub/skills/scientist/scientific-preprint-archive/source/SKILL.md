---
name: scientific-preprint-archive
description: |
 Preprint archive skill. bioRxiv/medRxiv/arXiv search, preprint tracking, citation monitoring, and preprint-to-publication linking.
---

# Scientific Preprint Archive

bioRxiv / medRxiv / arXiv / PMC / DOAJ / Unpaywall / CORE / HAL /
Zenodo / OpenAIRE / OSF Preprints / Fatcat / DBLP integration
literaturesearchpipeline is provided。

## When to Use

- latest's bioRxiv / medRxiv fromsearchwhen needed
- arXiv 's machine learningcalculationpaper is retrievedand
- PMC XML retrievalwhen needed
- OA 's Unpaywall items and
- CORE / Zenodo / OpenAIRE etc.multiplecross-cuttingsearchwhen needed
- systematic review's literature comprehensivesearchwhen needed
- DBLP fromcalculationliteraturedata is retrievedand

---

## Quick Start

## 1. bioRxiv / medRxiv search

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

BIORXIV_API = "https://api.biorxiv.org"


def search_biorxiv(query, server="biorxiv", days=30, cursor=0):
 """
 bioRxiv/medRxiv search。

 Parameters:
 query: str — search query
 server: str — "biorxiv" or "medrxiv"
 days: int — min is searched
 cursor: int — offset

 ToolUniverse:
 bioRxiv_search_preprints(query=query, server=server)
 bioRxiv_get_preprint_details(doi=doi)
 medRxiv_search_preprints(query=query)
 """
 end_date = datetime.now.strftime("%Y-%m-%d")
 start_date = (datetime.now - timedelta(days=days)).strftime("%Y-%m-%d")

 url = f"{BIORXIV_API}/details/{server}/{start_date}/{end_date}/{cursor}"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 results = []
 for paper in data.get("collection", []):
 title = paper.get("title", "").lower
 abstract = paper.get("abstract", "").lower
 if query.lower in title or query.lower in abstract:
 results.append({
 "doi": paper.get("doi", ""),
 "title": paper.get("title", ""),
 "authors": paper.get("authors", ""),
 "date": paper.get("date", ""),
 "category": paper.get("category", ""),
 "server": server,
 "abstract": paper.get("abstract", "")[:300],
 })

 df = pd.DataFrame(results)
 print(f"{server} search '{query}': {len(df)} preprints (last {days} days)")
 return df
```

## 2. arXiv papersearch

```python
import urllib.parse
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"


def search_arxiv(query, category=None, max_results=50, sort_by="submittedDate"):
 """
 arXiv papersearch。

 Parameters:
 query: str — search query
 category: str — arXiv (e.g., "q-bio.GN", "cs.LG", "stat.ML")
 max_results: int — maximum retrieval count
 sort_by: str — "submittedDate", "lastUpdatedDate", "relevance"

 ToolUniverse:
 arXiv_search_papers(query=query, category=category)
 arXiv_get_paper(arxiv_id=arxiv_id)
 """
 search_query = f"all:{query}"
 if category:
 search_query += f"+AND+cat:{category}"

 params = {
 "search_query": search_query,
 "start": 0,
 "max_results": max_results,
 "sortBy": sort_by,
 "sortOrder": "descending",
 }
 resp = requests.get(ARXIV_API, params=params)
 resp.raise_for_status

 ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
 root = ET.fromstring(resp.text)

 results = []
 for entry in root.findall("atom:entry", ns):
 categories = [c.get("term") for c in entry.findall("atom:category", ns)]
 results.append({
 "arxiv_id": entry.find("atom:id", ns).text.split("/abs/")[-1],
 "title": entry.find("atom:title", ns).text.strip.replace("\n", " "),
 "authors": ", ".join(
 a.find("atom:name", ns).text
 for a in entry.findall("atom:author", ns)
 ),
 "published": entry.find("atom:published", ns).text[:10],
 "categories": categories,
 "abstract": entry.find("atom:summary", ns).text.strip[:300],
 "pdf_url": next(
 (l.get("href") for l in entry.findall("atom:link", ns)
 if l.get("title") == "pdf"), ""
 ),
 })

 df = pd.DataFrame(results)
 cat_str = f" [{category}]" if category else ""
 print(f"arXiv search '{query}'{cat_str}: {len(df)} papers")
 return df
```

## 3. PMC 

```python
PMC_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def get_pmc_fulltext(pmcid, email="user@example.com"):
 """
 PMC XML retrieval。

 Parameters:
 pmcid: str — PMC ID (e.g., "PMC1234567")
 email: str — NCBI API for

 ToolUniverse:
 PMC_get_fulltext(pmcid=pmcid)
 """
 params = {
 "db": "pmc",
 "id": pmcid.replace("PMC", ""),
 "rettype": "xml",
 "email": email,
 }
 resp = requests.get(f"{PMC_API}/efetch.fcgi", params=params)
 resp.raise_for_status

 root = ET.fromstring(resp.text)
 article = root.find(".//article")

 sections = {}
 for sec in article.findall(".//sec") if article is not None else []:
 title = sec.find("title")
 if title is not None and title.text:
 paragraphs = [p.text for p in sec.findall("p") if p.text]
 sections[title.text] = " ".join(paragraphs)

 print(f"PMC {pmcid}: {len(sections)} sections retrieved")
 return sections
```

## 4. Unpaywall OA search

```python
UNPAYWALL_API = "https://api.unpaywall.org/v2"


def find_oa_version(doi, email="user@example.com"):
 """
 Unpaywall paper's OA search。

 Parameters:
 doi: str — DOI
 email: str — API use

 ToolUniverse:
 Unpaywall_get_oa_status(doi=doi)
 """
 resp = requests.get(f"{UNPAYWALL_API}/{doi}", params={"email": email})
 resp.raise_for_status
 data = resp.json

 oa_locations = data.get("oa_locations", [])
 result = {
 "doi": doi,
 "is_oa": data.get("is_oa", False),
 "oa_status": data.get("oa_status", ""),
 "best_oa_url": data.get("best_oa_location", {}).get("url_for_pdf", ""),
 "journal": data.get("journal_name", ""),
 "publisher": data.get("publisher", ""),
 "n_oa_locations": len(oa_locations),
 "locations": [
 {
 "url": loc.get("url_for_pdf") or loc.get("url"),
 "host_type": loc.get("host_type"),
 "version": loc.get("version"),
 }
 for loc in oa_locations
 ],
 }
 print(f"Unpaywall {doi}: OA={result['is_oa']}, status={result['oa_status']}")
 return result
```

## 5. CORE integrationsearch

```python
CORE_API = "https://api.core.ac.uk/v3"


def search_core(query, api_key, limit=25):
 """
 CORE cross-cuttingsearch (1.4 + paper)。

 Parameters:
 query: str — search query
 api_key: str — CORE API 
 limit: int — maximum retrieval count

 ToolUniverse:
 CORE_search_works(query=query)
 CORE_get_work(core_id=core_id)
 """
 headers = {"Authorization": f"Bearer {api_key}"}
 params = {"q": query, "limit": limit}
 resp = requests.get(f"{CORE_API}/search/works", headers=headers, params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for work in data.get("results", []):
 results.append({
 "core_id": work.get("id", ""),
 "title": work.get("title", ""),
 "authors": ", ".join(
 a.get("name", "") for a in work.get("authors", [])
 ),
 "year": work.get("yearPublished", ""),
 "doi": work.get("doi", ""),
 "download_url": work.get("downloadUrl", ""),
 "abstract": (work.get("abstract") or "")[:300],
 })

 df = pd.DataFrame(results)
 print(f"CORE search '{query}': {len(df)} works")
 return df
```

## 6. Zenodo recordsearch

```python
ZENODO_API = "https://zenodo.org/api"


def search_zenodo(query, resource_type=None, size=25):
 """
 Zenodo recordsearch (datasetpaper)。

 Parameters:
 query: str — search query
 resource_type: str — "publication", "dataset", "software", "poster"
 size: int — maximum retrieval count

 ToolUniverse:
 Zenodo_search_records(query=query, type=resource_type)
 """
 params = {"q": query, "size": size}
 if resource_type:
 params["type"] = resource_type
 resp = requests.get(f"{ZENODO_API}/records", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", {}).get("hits", []):
 meta = hit.get("metadata", {})
 results.append({
 "zenodo_id": hit.get("id", ""),
 "doi": meta.get("doi", ""),
 "title": meta.get("title", ""),
 "creators": ", ".join(
 c.get("name", "") for c in meta.get("creators", [])
 ),
 "resource_type": meta.get("resource_type", {}).get("type", ""),
 "publication_date": meta.get("publication_date", ""),
 "access_right": meta.get("access_right", ""),
 })

 df = pd.DataFrame(results)
 print(f"Zenodo search '{query}': {len(df)} records")
 return df
```

## 7. DOAJ OA search

```python
DOAJ_API = "https://doaj.org/api"


def search_doaj_articles(query, page=1, page_size=25):
 """
 DOAJ OA search。

 ToolUniverse:
 DOAJ_search_articles(query=query)
 """
 params = {"q": query, "page": page, "pageSize": page_size}
 resp = requests.get(f"{DOAJ_API}/search/articles/{query}")
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("results", []):
 bib = item.get("bibjson", {})
 results.append({
 "doi": bib.get("identifier", [{}])[0].get("id", ""),
 "title": bib.get("title", ""),
 "journal": bib.get("journal", {}).get("title", ""),
 "year": bib.get("year", ""),
 "authors": ", ".join(
 a.get("name", "") for a in bib.get("author", [])
 ),
 "keywords": bib.get("keywords", []),
 })

 df = pd.DataFrame(results)
 print(f"DOAJ search '{query}': {len(df)} OA articles")
 return df
```

## 8. OpenAIRE researchsearch

```python
OPENAIRE_API = "https://api.openaire.eu/search"


def search_openaire(query, result_type="publication", size=25):
 """
 OpenAIRE researchsearch (EU research)。

 ToolUniverse:
 OpenAIRE_search_publications(query=query)
 """
 params = {
 "keywords": query,
 "size": size,
 "format": "json",
 }
 resp = requests.get(f"{OPENAIRE_API}/{result_type}s", params=params)
 resp.raise_for_status
 data = resp.json

 results_list = (
 data.get("response", {}).get("results", {}).get("result", [])
 )
 results = []
 for item in results_list:
 meta = item.get("metadata", {}).get("oaf:entity", {}).get("oaf:result", {})
 results.append({
 "title": meta.get("title", {}).get("$", ""),
 "date": meta.get("dateofacceptance", {}).get("$", ""),
 "publisher": meta.get("publisher", {}).get("$", ""),
 })

 df = pd.DataFrame(results)
 print(f"OpenAIRE search '{query}': {len(df)} results")
 return df
```

## 9. integrationsearchpipeline

```python
def multi_archive_search(query, archives=None, **kwargs):
 """
 multiple/OA cross-cuttingsearch。

 Parameters:
 query: str — search query
 archives: list — ["biorxiv", "medrxiv", "arxiv", "core", "zenodo", "doaj", "openaire"]
 """
 if archives is None:
 archives = ["biorxiv", "arxiv", "core"]

 all_results = {}
 search_funcs = {
 "biorxiv": lambda q: search_biorxiv(q, server="biorxiv"),
 "medrxiv": lambda q: search_biorxiv(q, server="medrxiv"),
 "arxiv": lambda q: search_arxiv(q),
 "core": lambda q: search_core(q, api_key=kwargs.get("core_api_key", "")),
 "zenodo": lambda q: search_zenodo(q),
 "doaj": lambda q: search_doaj_articles(q),
 "openaire": lambda q: search_openaire(q),
 }

 for archive in archives:
 if archive in search_funcs:
 try:
 df = search_funcs[archive](query)
 all_results[archive] = df
 print(f" ✓ {archive}: {len(df)} results")
 except Exception as e:
 print(f" ✗ {archive}: {e}")
 all_results[archive] = pd.DataFrame

 total = sum(len(df) for df in all_results.values)
 print(f"\nTotal: {total} results across {len(archives)} archives")
 return all_results
```

---

## Available Tools

below/following's tool ToolUniverse SMCP usepossible:

| ToolUniverse Category | Key Tools |
|---|---|
| `biorxiv` | `bioRxiv_search_preprints`, `bioRxiv_get_preprint_details` |
| `medrxiv` | `medRxiv_search_preprints` |
| `arxiv` | `arXiv_search_papers`, `arXiv_get_paper` |
| `pmc` | `PMC_get_fulltext` |
| `doaj` | `DOAJ_search_articles` |
| `unpaywall` | `Unpaywall_get_oa_status` |
| `hal` | `HAL_search` |
| `core` | `CORE_search_works`, `CORE_get_work` |
| `zenodo` | `Zenodo_search_records` |
| `openaire` | `OpenAIRE_search_publications` |
| `osf_preprints` | `OSF_search_preprints` |
| `fatcat` | `Fatcat_search_releases` |
| `dblp` | `DBLP_search_publications` |

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/preprint_search.csv` | cross-cuttingsearchresults | → literature-search, systematic-review |
| `results/oa_availability.json` | OA | → deep-research |
| `results/fulltext_corpus/` | | → text-mining-nlp, biomedical-pubtator |
| `results/arxiv_papers.csv` | arXiv paperdata | → deep-learning, graph-neural-networks |

## Pipeline Integration

```
literature-search ──→ preprint-archive ──→ systematic-review
 (PubMed/OpenAlex) (bioRxiv/arXiv/CORE) (PRISMA 2020)
 │
 ├──→ text-mining-nlp (NER/KG)
 ├──→ biomedical-pubtator (PubTator NER)
 └──→ deep-research (integration)
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
