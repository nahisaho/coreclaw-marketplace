---
name: scientific-semantic-scholar
description: |
 Semantic Scholar skill. Academic paper search via Semantic Scholar API, citation graph exploration, author profiling, and research impact metrics retrieval.
tu_tools:
 - key: semantic_scholar
 name: Semantic Scholar
 description: papersearchcitationanalysisauthorfile
---

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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `semantic_scholar` | Semantic Scholar | papersearchcitationanalysisauthorTLDR |

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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
