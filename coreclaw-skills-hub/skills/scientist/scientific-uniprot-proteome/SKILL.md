---
name: scientific-uniprot-proteome
description: |
 UniProt proteome skill. UniProt protein sequence/annotation retrieval, proteome-wide queries, functional annotation extraction, and protein feature analysis.
tu_tools:
 - key: uniprot
 name: UniProt
 description: proteinsequenceannotationID mapping
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `uniprot` | UniProt | protein searchID mappingsequenceannotation |

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
