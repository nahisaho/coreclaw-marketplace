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
