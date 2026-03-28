---
name: scientific-arrayexpress-expression
description: |
 ArrayExpress expressionskill。BioStudies/ArrayExpress
 REST API by/viaRNA-seq expressionexperimentsearch
 Data Retrievaldataanalysis。ToolUniverse integration: arrayexpress。
tu_tools:
 - key: arrayexpress
 name: ArrayExpress
 description: ArrayExpress expressionexperimentsearchdatafileretrieval
---

# Scientific ArrayExpress Expression

EBI ArrayExpress / BioStudies REST API utilizingexpressiondata
searchanalysispipeline is provided。

## When to Use

- ArrayExpress/BioStudies 's expressionexperiment is searchedand
- /RNA-seq expressiondata'sdata is retrievedand
- SDRF informationtableanalysiswhen needed
- E-MTAB/E-GEOD accessionfromdataanalysiswhen needed
- expressiondatacross-cuttingsearchwhen needed
- GEO and ArrayExpress 's data and

---

## Quick Start

## 1. BioStudies expressionexperimentsearch

```python
import requests
import pandas as pd

BIOSTUDIES_BASE = "https://www.ebi.ac.uk/biostudies/api/v1"
AE_BASE = "https://www.ebi.ac.uk/arrayexpress/json/v3"


def arrayexpress_search_experiments(query, organism=None,
 experiment_type=None,
 limit=50):
 """
 ArrayExpress — expressionexperimentsearch (BioStudies API)。

 Parameters:
 query: str — search query (example: "breast cancer RNA-seq")
 organism: str — organism/species (example: "Homo sapiens")
 experiment_type: str — experiment (example: "RNA-seq of coding RNA")
 limit: int — maximum results
 """
 url = f"{BIOSTUDIES_BASE}/search"
 params = {
 "query": query,
 "type": "study",
 "pageSize": limit,
 }
 if organism:
 params["organism"] = organism
 if experiment_type:
 params["experimenttype"] = experiment_type

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 hits = data.get("hits", [])
 results = []
 for h in hits:
 attrs = {a.get("name", ""): a.get("value", "")
 for a in h.get("attributes", [])}
 results.append({
 "accession": h.get("accession", ""),
 "title": attrs.get("Title", h.get("title", "")),
 "organism": attrs.get("Organism", ""),
 "experiment_type": attrs.get("Experiment type", ""),
 "release_date": h.get("releaseDate", ""),
 "files_count": h.get("filesCount", 0),
 "links_count": h.get("linksCount", 0),
 })

 df = pd.DataFrame(results)
 print(f"ArrayExpress search: {len(df)} experiments "
 f"(query={query})")
 return df
```

## 2. experimentdataSDRF retrieval

```python
def arrayexpress_get_experiment(accession):
 """
 ArrayExpress — experimentdata & SDRF retrieval。

 Parameters:
 accession: str — accession (example: "E-MTAB-12345")
 """
 url = f"{BIOSTUDIES_BASE}/studies/{accession}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 # data
 attrs = {a.get("name", ""): a.get("value", "")
 for a in data.get("attributes", [])}
 metadata = {
 "accession": accession,
 "title": attrs.get("Title", ""),
 "description": attrs.get("Description", "")[:500],
 "organism": attrs.get("Organism", ""),
 "experiment_type": attrs.get("Experiment type", ""),
 "release_date": data.get("releaseDate", ""),
 }

 # filelist
 files = []
 for section in data.get("section", {}).get("files", []):
 if isinstance(section, list):
 for f in section:
 files.append({
 "filename": f.get("path", ""),
 "type": f.get("type", ""),
 "size": f.get("size", 0),
 })
 elif isinstance(section, dict):
 files.append({
 "filename": section.get("path", ""),
 "type": section.get("type", ""),
 "size": section.get("size", 0),
 })

 files_df = pd.DataFrame(files)

 # SDRF retrieval
 sdrf_url = (f"https://www.ebi.ac.uk/biostudies/files/"
 f"{accession}/{accession}.sdrf.txt")
 sdrf_df = pd.DataFrame
 try:
 sdrf_resp = requests.get(sdrf_url, timeout=30)
 if sdrf_resp.status_code == 200:
 from io import StringIO
 sdrf_df = pd.read_csv(StringIO(sdrf_resp.text), sep="\t")
 except Exception:
 pass

 print(f"ArrayExpress {accession}: {len(files_df)} files, "
 f"{len(sdrf_df)} SDRF rows")
 return metadata, files_df, sdrf_df
```

## 3. expressiondata

```python
def arrayexpress_download_matrix(accession, output_dir="results"):
 """
 ArrayExpress — expression。

 Parameters:
 accession: str — accession
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 metadata, files_df, sdrf_df = arrayexpress_get_experiment(accession)

 # expressionfilesearch
 expr_files = files_df[
 files_df["filename"].str.contains(
 r"processed|normalized|expression|counts",
 case=False, na=False)
 ]

 downloaded = []
 for _, frow in expr_files.iterrows:
 fname = frow["filename"]
 url = (f"https://www.ebi.ac.uk/biostudies/files/"
 f"{accession}/{fname}")
 try:
 resp = requests.get(url, timeout=120)
 if resp.status_code == 200:
 fpath = output_dir / fname.split("/")[-1]
 fpath.write_bytes(resp.content)
 downloaded.append(str(fpath))
 except Exception:
 continue

 # SDRF save
 if not sdrf_df.empty:
 sdrf_df.to_csv(output_dir / "sdrf.csv", index=False)

 print(f"ArrayExpress download: {len(downloaded)} files → "
 f"{output_dir}")
 return {
 "metadata": metadata,
 "files": downloaded,
 "sdrf": sdrf_df,
 }
```

## 4. ArrayExpress integrationpipeline

```python
def arrayexpress_pipeline(query, organism="Homo sapiens",
 output_dir="results"):
 """
 ArrayExpress integrationpipeline。

 Parameters:
 query: str — search query
 organism: str — organism/species
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) experimentsearch
 experiments = arrayexpress_search_experiments(
 query, organism=organism)
 experiments.to_csv(output_dir / "experiments.csv", index=False)

 # 2) experiment'sdetails
 if not experiments.empty:
 top_acc = experiments.iloc[0]["accession"]
 metadata, files, sdrf = arrayexpress_get_experiment(top_acc)
 files.to_csv(output_dir / "experiment_files.csv", index=False)
 if not sdrf.empty:
 sdrf.to_csv(output_dir / "sdrf.csv", index=False)

 print(f"ArrayExpress pipeline: {output_dir}")
 return {"experiments": experiments}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `arrayexpress` | ArrayExpress | expressionexperimentsearchdatafileretrieval |

## Pipeline Integration

```
ebi-databases → arrayexpress-expression → gene-expression-transcriptomics
 (EBI Search) (ArrayExpress/BioStudies) (DESeq2/GSEA)
 │ │ ↓
 geo-expression ─────────┘ pathway-enrichment
 (GEO data) │ (KEGG/Reactome)
 ↓
 multi-omics
 (integrated analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/experiments.csv` | experimentlist | → geo-expression |
| `results/sdrf.csv` | information | → gene-expression-transcriptomics |
| `results/experiment_files.csv` | file | → data-preprocessing |
