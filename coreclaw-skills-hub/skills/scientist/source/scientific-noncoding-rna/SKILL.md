---
name: scientific-noncoding-rna
description: |
 RNA (ncRNA) analysisskill。Rfam RNA search、
 RNAcentral integration ncRNA database、variance、structuremapping、
 phylogenyanalysispipeline。
---

# Scientific Noncoding RNA

Rfam and RNAcentral utilizing ncRNA search、
sequenceannotation、structurepredictionpipeline is provided。

## When to Use

- RNA (miRNA, lncRNA, rRNA, tRNA ) classificationwhen needed
- Rfam variance RNA sequence is searchedand
- RNAcentral ncRNA 's is retrievedand
- RNA structurestructuremappinginformation is retrievedand
- RNA 's phylogenyinformation is investigatedand

---

## Quick Start

## 1. Rfam search

```python
import requests
import pandas as pd

RFAM_API = "https://rfam.org/family"


def get_rfam_family(rfam_acc):
 """
 Rfam RNA 's detailsinformationretrieval。

 Parameters:
 rfam_acc: str — Rfam accession (e.g., "RF00001") or ID

 ToolUniverse:
 Rfam_get_family(rfam_acc=rfam_acc)
 Rfam_id_to_accession(rfam_id=rfam_id)
 """
 url = f"https://rfam.org/family/{rfam_acc}?content-type=application/json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 info = data.get("rfam", {}).get("acc", {})
 desc = data.get("rfam", {}).get("description", "")

 print(f"Rfam {rfam_acc}: {data.get('rfam', {}).get('id', '?')}")
 return data
```

## 2. Rfam sequencesearch (Infernal cmscan)

```python
import time


def rfam_sequence_search(sequence, email=None):
 """
 Rfam RNA sequence Infernal cmscan 
 RNA 。

 Parameters:
 sequence: str — RNA sequence

 ToolUniverse:
 Rfam_search_sequence(sequence=sequence)
 """
 url = "https://rfam.org/search/sequence"

 payload = {
 "seq": sequence,
 "output": "json",
 }
 resp = requests.post(url, data=payload)
 resp.raise_for_status

 # Async job → poll
 job_url = resp.json.get("resultURL", "")
 if not job_url:
 return resp.json

 for _ in range(30):
 time.sleep(10)
 result = requests.get(job_url)
 if result.status_code == 200:
 data = result.json
 if data.get("status", "") == "DONE":
 hits = data.get("hits", {}).get("hit", [])
 print(f"Rfam cmscan: {len(hits)} family hits")
 return hits

 print("Rfam cmscan: timeout")
 return []
```

## 3. Rfam structuremapping

```python
def get_rfam_structure_mapping(rfam_acc):
 """
 Rfam 's PDB structuremappinginformationretrieval。

 ToolUniverse:
 Rfam_get_structure_mapping(rfam_acc=rfam_acc)
 Rfam_get_covariance_model(rfam_acc=rfam_acc)
 Rfam_get_tree_data(rfam_acc=rfam_acc)
 Rfam_get_sequence_regions(rfam_acc=rfam_acc)
 """
 # Structure mapping
 url_struct = (
 f"https://rfam.org/family/{rfam_acc}/structures"
 "?content-type=application/json"
 )
 resp_s = requests.get(url_struct)
 structures = resp_s.json if resp_s.status_code == 200 else []

 # Sequence regions
 url_regions = (
 f"https://rfam.org/family/{rfam_acc}/regions"
 "?content-type=application/json"
 )
 resp_r = requests.get(url_regions)
 regions = resp_r.json if resp_r.status_code == 200 else []

 print(f"Rfam {rfam_acc}: {len(structures)} PDB structures, "
 f"{len(regions) if isinstance(regions, list) else '?'} regions")
 return structures, regions
```

## 4. RNAcentral ncRNA search

```python
RNACENTRAL_API = "https://rnacentral.org/api/v1"


def rnacentral_search(query, page_size=10):
 """
 RNAcentral ncRNA search。

 Parameters:
 query: str — search term (gene name, accession, keyword)

 ToolUniverse:
 RNAcentral_search(query=query)
 """
 url = f"{RNACENTRAL_API}/rna/"
 params = {"query": query, "page_size": page_size}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 results = data.get("results", [])
 entries = []
 for r in results:
 entries.append({
 "rnacentral_id": r.get("rnacentral_id", ""),
 "description": r.get("description", ""),
 "rna_type": r.get("rna_type", ""),
 "length": r.get("length", 0),
 "num_xrefs": r.get("xref_count", 0),
 })

 df = pd.DataFrame(entries)
 print(f"RNAcentral '{query}': {data.get('count', 0)} total, "
 f"{len(df)} returned")
 return df


def rnacentral_get_by_accession(accession):
 """
 RNAcentral accessionfrom ncRNA detailsinformationretrieval。

 ToolUniverse:
 RNAcentral_get_by_accession(accession=accession)
 """
 url = f"{RNACENTRAL_API}/rna/{accession}/"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 print(f"RNAcentral {accession}: {data.get('description', '')}")
 return data
```

## 5. ncRNA integrated analysispipeline

```python
def ncRNA_integrated_search(sequence, rfam_acc=None):
 """
 sequence's ncRNA integrated analysis。

 ToolUniverse (cross-cutting):
 Rfam_search_sequence(sequence) → Rfam_get_family(rfam_acc)
 RNAcentral_search(query)
 """
 pipeline = {"sequence_length": len(sequence)}

 # Step 1: Rfam family identification
 rfam_hits = rfam_sequence_search(sequence)
 pipeline["rfam_hits"] = len(rfam_hits) if isinstance(rfam_hits, list) else 0

 # Step 2: If Rfam family found, get details
 if rfam_hits and isinstance(rfam_hits, list) and len(rfam_hits) > 0:
 top_hit = rfam_hits[0]
 top_acc = top_hit.get("acc", rfam_acc or "")
 if top_acc:
 family = get_rfam_family(top_acc)
 pipeline["rfam_family"] = top_acc

 # Step 3: RNAcentral search
 rna_df = rnacentral_search(sequence[:30]) # truncate for search
 pipeline["rnacentral_hits"] = len(rna_df)

 print(f"ncRNA pipeline: Rfam={pipeline.get('rfam_family', 'none')}, "
 f"RNAcentral={pipeline['rnacentral_hits']} hits")
 return pipeline
```

## References

### Output Files

| File | Format |
|---|---|
| `results/rfam_family.json` | JSON |
| `results/rfam_cmscan_hits.json` | JSON |
| `results/rfam_structures.json` | JSON |
| `results/rnacentral_search.csv` | CSV |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| Rfam | `Rfam_get_family` | information |
| Rfam | `Rfam_search_sequence` | sequence→ |
| Rfam | `Rfam_get_covariance_model` | variance |
| Rfam | `Rfam_get_structure_mapping` | PDB mapping |
| Rfam | `Rfam_get_tree_data` | phylogeny |
| Rfam | `Rfam_get_sequence_regions` | sequence |
| Rfam | `Rfam_id_to_accession` | ID→accessiontransformation |
| RNAcentral | `RNAcentral_search` | ncRNA search |
| RNAcentral | `RNAcentral_get_by_accession` | detailsretrieval |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-gene-expression-transcriptomics` | analysis |
| `scientific-genome-sequence-tools` | sequenceretrieval |
| `scientific-structural-proteomics` | RNA structure |
| `scientific-biothings-idmapping` | ID mapping |

### Dependencies

`requests`, `pandas`
