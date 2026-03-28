---
name: scientific-literature-search
description: |
 literaturesearchretrievalskill。PubMed E-utilities、Semantic Scholar、
 OpenAlex、EuropePMC、CrossRef 's 5 database API integration
 literaturesearchpipeline。MeSH structuresearch、citationnetworkmin、
 author/metrics、allretrieval、PICO searchsupport。
 29 ---

# Scientific Literature Search

PubMed / Semantic Scholar / OpenAlex / EuropePMC / CrossRef 's 
5 DB integrationliteraturesearchData Retrievalpipeline is provided。

## When to Use

- PubMed MeSH forusingstructuresearchwhen needed
- Semantic Scholar paperwhen needed
- OpenAlex authormetrics minwhen needed
- paper'scitation/citationnetwork is builtand
- systematic reviewfor DB cross-cuttingsearchwhen needed

---

## Quick Start

## 1. PubMed E-utilities search

```python
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time


def pubmed_search(query, max_results=100, sort="relevance",
 date_from=None, date_to=None, rettype="xml"):
 """
 PubMed E-utilities by/viastructuresearch。

 Parameters:
 query: str — PubMed (MeSH support)
 max_results: int — retrievalitemsnumber/count
 sort: "relevance" or "date"
 date_from/to: "YYYY/MM/DD" 
 """
 base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

 # Step 1: esearch — PMID retrieval
 params = {
 "db": "pubmed",
 "term": query,
 "retmax": max_results,
 "sort": sort,
 "retmode": "json",
 }
 if date_from:
 params["mindate"] = date_from
 params["datetype"] = "pdat"
 if date_to:
 params["maxdate"] = date_to

 resp = requests.get(f"{base}/esearch.fcgi", params=params)
 data = resp.json
 pmids = data["esearchresult"]["idlist"]
 total = int(data["esearchresult"]["count"])
 print(f"PubMed search: {total} total results, fetching {len(pmids)}")

 if not pmids:
 return pd.DataFrame

 # Step 2: efetch — detailsretrieval
 time.sleep(0.4)
 fetch_params = {
 "db": "pubmed",
 "id": ",".join(pmids),
 "rettype": "xml",
 "retmode": "xml",
 }
 resp = requests.get(f"{base}/efetch.fcgi", params=fetch_params)
 root = ET.fromstring(resp.text)

 articles = []
 for article in root.findall(".//PubmedArticle"):
 medline = article.find(".//MedlineCitation")
 pmid = medline.findtext("PMID", "")
 title = medline.findtext(".//ArticleTitle", "")
 abstract = medline.findtext(".//AbstractText", "")
 journal = medline.findtext(".//Journal/Title", "")
 year = medline.findtext(".//PubDate/Year", "")

 authors = []
 for author in medline.findall(".//Author"):
 last = author.findtext("LastName", "")
 fore = author.findtext("ForeName", "")
 if last:
 authors.append(f"{last} {fore}")

 mesh_terms = [m.findtext("DescriptorName", "")
 for m in medline.findall(".//MeshHeading")]

 articles.append({
 "pmid": pmid,
 "title": title,
 "abstract": abstract[:500],
 "journal": journal,
 "year": year,
 "authors": "; ".join(authors[:5]),
 "mesh_terms": "; ".join(mesh_terms[:10]),
 })

 return pd.DataFrame(articles)
```

## 2. Semantic Scholar API search

```python
def semantic_scholar_search(query, max_results=50, year_from=None,
 fields=None):
 """
 Semantic Scholar Academic Graph API search。

 Parameters:
 query: str — search query
 fields: list — retrievalfield
 """
 url = "https://api.semanticscholar.org/graph/v1/paper/search"

 if fields is None:
 fields = ["title", "abstract", "year", "citationCount",
 "influentialCitationCount", "authors", "url",
 "openAccessPdf"]

 params = {
 "query": query,
 "limit": min(max_results, 100),
 "fields": ",".join(fields),
 }
 if year_from:
 params["year"] = f"{year_from}-"

 resp = requests.get(url, params=params)
 data = resp.json
 papers = data.get("data", [])

 results = []
 for p in papers:
 results.append({
 "paper_id": p.get("paperId", ""),
 "title": p.get("title", ""),
 "abstract": (p.get("abstract") or "")[:300],
 "year": p.get("year"),
 "citations": p.get("citationCount", 0),
 "influential_citations": p.get("influentialCitationCount", 0),
 "authors": "; ".join([a.get("name", "")
 for a in (p.get("authors") or [])[:5]]),
 "url": p.get("url", ""),
 "open_access": bool(p.get("openAccessPdf")),
 })

 df = pd.DataFrame(results)
 print(f"Semantic Scholar: {data.get('total', 0)} total, "
 f"{len(df)} fetched")
 return df
```

## 3. OpenAlex authormetrics

```python
def openalex_search(query, entity_type="works", max_results=50,
 filters=None):
 """
 OpenAlex API search (250M+ works, 90M+ authors)。

 Parameters:
 query: str — search query
 entity_type: "works", "authors", "institutions", "concepts"
 filters: dict — OpenAlex filter (e.g., {"from_publication_date": "2020-01-01"})
 """
 base = "https://api.openalex.org"
 url = f"{base}/{entity_type}"

 params = {
 "search": query,
 "per-page": min(max_results, 200),
 "mailto": "research@example.com",
 }
 if filters:
 filter_parts = [f"{k}:{v}" for k, v in filters.items]
 params["filter"] = ",".join(filter_parts)

 resp = requests.get(url, params=params)
 data = resp.json

 results = data.get("results", [])
 total = data.get("meta", {}).get("count", 0)
 print(f"OpenAlex {entity_type}: {total} total, {len(results)} fetched")

 if entity_type == "works":
 return pd.DataFrame([{
 "id": r.get("id", ""),
 "title": r.get("title", ""),
 "year": r.get("publication_year"),
 "citations": r.get("cited_by_count", 0),
 "doi": r.get("doi", ""),
 "type": r.get("type", ""),
 "open_access": r.get("open_access", {}).get("is_oa", False),
 } for r in results])
 elif entity_type == "authors":
 return pd.DataFrame([{
 "id": r.get("id", ""),
 "name": r.get("display_name", ""),
 "works_count": r.get("works_count", 0),
 "citations": r.get("cited_by_count", 0),
 "h_index": r.get("summary_stats", {}).get("h_index", 0),
 "institution": (r.get("last_known_institutions") or [{}])[0].get(
 "display_name", "") if r.get("last_known_institutions") else "",
 } for r in results])

 return results
```

## 4. EuropePMC allsearch

```python
def europepmc_search(query, max_results=50, source="MED",
 open_access_only=False):
 """
 EuropePMC REST API search (39M+ records)。

 Parameters:
 query: str — search query
 source: "MED" (PubMed), "PMC" (PubMed Central), "AGR", "CBA"
 open_access_only: True 's
 """
 url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

 q = query
 if open_access_only:
 q += " AND OPEN_ACCESS:y"

 params = {
 "query": q,
 "resultType": "core",
 "pageSize": min(max_results, 100),
 "format": "json",
 "src": source,
 }

 resp = requests.get(url, params=params)
 data = resp.json
 results = data.get("resultList", {}).get("result", [])
 total = data.get("hitCount", 0)

 articles = []
 for r in results:
 articles.append({
 "pmid": r.get("pmid", ""),
 "pmcid": r.get("pmcid", ""),
 "title": r.get("title", ""),
 "journal": r.get("journalTitle", ""),
 "year": r.get("pubYear", ""),
 "citations": r.get("citedByCount", 0),
 "has_fulltext": r.get("hasTextMinedTerms", "N") == "Y",
 "is_open_access": r.get("isOpenAccess", "N") == "Y",
 })

 df = pd.DataFrame(articles)
 print(f"EuropePMC: {total} total, {len(df)} fetched")
 return df
```

## 5. CrossRef Data Retrieval

```python
def crossref_search(query, max_results=50, filter_type=None,
 from_date=None, sort="relevance"):
 """
 CrossRef REST API search (DOI data)。

 Parameters:
 query: str — search query
 filter_type: str — DOI filter ("journal-article", "book-chapter")
 from_date: str — "YYYY-MM-DD"
 sort: "relevance", "published", "is-referenced-by-count"
 """
 url = "https://api.crossref.org/works"
 params = {
 "query": query,
 "rows": min(max_results, 100),
 "sort": sort,
 "mailto": "research@example.com",
 }

 filters = []
 if filter_type:
 filters.append(f"type:{filter_type}")
 if from_date:
 filters.append(f"from-pub-date:{from_date}")
 if filters:
 params["filter"] = ",".join(filters)

 resp = requests.get(url, params=params)
 data = resp.json
 items = data.get("message", {}).get("items", [])
 total = data.get("message", {}).get("total-results", 0)

 results = []
 for item in items:
 title = item.get("title", [""])[0] if item.get("title") else ""
 results.append({
 "doi": item.get("DOI", ""),
 "title": title,
 "journal": item.get("container-title", [""])[0] if item.get("container-title") else "",
 "year": item.get("published", {}).get("date-parts", [[None]])[0][0],
 "citations": item.get("is-referenced-by-count", 0),
 "type": item.get("type", ""),
 "publisher": item.get("publisher", ""),
 })

 df = pd.DataFrame(results)
 print(f"CrossRef: {total} total, {len(df)} fetched")
 return df
```

## 6. citationnetworkconstruction

```python
def build_citation_network(seed_pmids, depth=1, max_per_level=20):
 """
 PubMed paper's citation/citationnetworkconstruction。

 Parameters:
 seed_pmids: list — point and PMID list
 depth: int — search/explorationdegree (1=citation's)
 max_per_level: int — each's nodenumber/count
 """
 import networkx as nx

 G = nx.DiGraph
 visited = set
 current_level = set(seed_pmids)

 for level in range(depth + 1):
 next_level = set
 for pmid in list(current_level)[:max_per_level]:
 if pmid in visited:
 continue
 visited.add(pmid)
 G.add_node(pmid, level=level, is_seed=(level == 0))

 # elink citationretrieval
 time.sleep(0.4)
 url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
 params = {
 "dbfrom": "pubmed", "db": "pubmed",
 "id": pmid, "linkname": "pubmed_pubmed_citedin",
 "retmode": "json",
 }
 try:
 resp = requests.get(url, params=params)
 data = resp.json
 links = data.get("linksets", [{}])[0].get("linksetdbs", [])
 if links:
 cited_by = [l["id"] for l in links[0].get("links", [])[:max_per_level]]
 for citing in cited_by:
 G.add_edge(citing, pmid)
 next_level.add(citing)
 except Exception:
 continue

 current_level = next_level - visited

 print(f"Citation network: {G.number_of_nodes} nodes, "
 f"{G.number_of_edges} edges, depth={depth}")
 return G
```

## References

### Output Files

| File | Format |
|---|---|
| `results/pubmed_search.csv` | CSV |
| `results/semantic_scholar_results.csv` | CSV |
| `results/openalex_results.csv` | CSV |
| `results/europepmc_results.csv` | CSV |
| `results/crossref_results.csv` | CSV |
| `results/citation_network.graphml` | GraphML |
| `figures/citation_network.png` | PNG |

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

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-deep-research` | literaturesearch → |
| `scientific-citation-checker` | citationverificationintegration |
| `scientific-systematic-review` | phylogenysearch |
| `scientific-meta-analysis` | literature |
| `scientific-academic-writing` | literature's automated |
| `scientific-text-mining-nlp` | extraction's NLP analysis |

### Dependencies

`requests`, `pandas`, `networkx`, `xml.etree.ElementTree` (stdlib)
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
