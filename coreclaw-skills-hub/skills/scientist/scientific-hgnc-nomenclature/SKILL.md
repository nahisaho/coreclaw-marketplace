---
name: scientific-hgnc-nomenclature
description: |
 HGNC nomenclature skill. Official gene symbol resolution, gene name standardization, symbol history tracking, and gene family classification via HGNC database.
tu_tools:
 - key: hgnc
 name: HGNC
 description: genemethodsearch
---

# Scientific HGNC Nomenclature

HGNC (HUGO Gene Nomenclature Committee) REST API utilizing
formulagene symbolsearch/
genedatabase ID phasereference
pipeline.

## When to Use

- genefromformula HGNC is retrievedand
- gene symbol (previous symbol) latesttransformationwhen needed
- gene/loop's is retrievedand
- HGNC ID ↔ Ensembl / NCBI Gene / UniProt 's is performedand
- gene (protein-coding, ncRNA ) filterwhen needed

---

## Quick Start

## 1. HGNC search

```python
import requests
import pandas as pd

HGNC_BASE = "https://rest.genenames.org"
HEADERS = {"Accept": "application/json"}


def hgnc_search(query):
 """
 HGNC — gene symbol/namesearch。

 Parameters:
 query: str — search query (/name)
 """
 url = f"{HGNC_BASE}/search/{query}"
 resp = requests.get(url, headers=HEADERS,
 timeout=30)
 resp.raise_for_status
 data = resp.json.get("response", {})
 docs = data.get("docs", [])

 rows = []
 for doc in docs:
 rows.append({
 "hgnc_id": doc.get("hgnc_id", ""),
 "symbol": doc.get("symbol", ""),
 "name": doc.get("name", ""),
 "locus_type": doc.get("locus_type", ""),
 "status": doc.get("status", ""),
 })

 df = pd.DataFrame(rows)
 print(f"HGNC search '{query}': {len(df)} hits")
 return df


def hgnc_fetch_symbol(symbol):
 """
 HGNC — formulagenedetailsretrieval。

 Parameters:
 symbol: str — formulagene symbol (example: "BRCA1")
 """
 url = f"{HGNC_BASE}/fetch/symbol/{symbol}"
 resp = requests.get(url, headers=HEADERS,
 timeout=30)
 resp.raise_for_status
 docs = resp.json.get("response", {}).get(
 "docs", [])

 if not docs:
 print(f"HGNC: {symbol} not found")
 return {}

 doc = docs[0]
 info = {
 "hgnc_id": doc.get("hgnc_id", ""),
 "symbol": doc.get("symbol", ""),
 "name": doc.get("name", ""),
 "locus_type": doc.get("locus_type", ""),
 "location": doc.get("location", ""),
 "alias_symbol": doc.get("alias_symbol", []),
 "prev_symbol": doc.get("prev_symbol", []),
 "ensembl_gene_id": doc.get(
 "ensembl_gene_id", ""),
 "entrez_id": doc.get("entrez_id", ""),
 "uniprot_ids": doc.get("uniprot_ids", []),
 "gene_group": doc.get("gene_group", []),
 }

 print(f"HGNC: {symbol} → {info['name']} "
 f"({info['locus_type']})")
 return info
```

## 2. /

```python
def hgnc_resolve_alias(alias):
 """
 HGNC — fromformula to。

 Parameters:
 alias: str — or
 """
 # 1) alias_symbol search
 url = f"{HGNC_BASE}/fetch/alias_symbol/{alias}"
 resp = requests.get(url, headers=HEADERS,
 timeout=30)
 resp.raise_for_status
 docs = resp.json.get("response", {}).get(
 "docs", [])

 if docs:
 symbols = [d["symbol"] for d in docs]
 print(f"HGNC alias '{alias}' → "
 f"{', '.join(symbols)}")
 return symbols

 # 2) prev_symbol search
 url2 = f"{HGNC_BASE}/fetch/prev_symbol/{alias}"
 resp2 = requests.get(url2, headers=HEADERS,
 timeout=30)
 resp2.raise_for_status
 docs2 = resp2.json.get("response", {}).get(
 "docs", [])

 if docs2:
 symbols = [d["symbol"] for d in docs2]
 print(f"HGNC prev '{alias}' → "
 f"{', '.join(symbols)}")
 return symbols

 print(f"HGNC: '{alias}' not resolved")
 return []


def hgnc_resolve_batch(aliases):
 """
 HGNC — batch。

 Parameters:
 aliases: list[str] — /
 """
 results = []
 for alias in aliases:
 resolved = hgnc_resolve_alias(alias)
 results.append({
 "input": alias,
 "resolved": resolved[0] if resolved
 else "UNRESOLVED",
 "ambiguous": len(resolved) > 1,
 })

 df = pd.DataFrame(results)
 n_resolved = (df["resolved"] != "UNRESOLVED").sum
 print(f"HGNC batch: {n_resolved}/{len(df)} "
 f"resolved")
 return df
```

## 3. gene/loop

```python
def hgnc_gene_group(group_name):
 """
 HGNC — gene/loopretrieval。

 Parameters:
 group_name: str — loop
 (example: "Kinases", "Ion channels")
 """
 url = (f"{HGNC_BASE}/search/"
 f"gene_group:%22{group_name}%22")
 resp = requests.get(url, headers=HEADERS,
 timeout=30)
 resp.raise_for_status
 docs = resp.json.get("response", {}).get(
 "docs", [])

 rows = []
 for doc in docs:
 rows.append({
 "symbol": doc.get("symbol", ""),
 "name": doc.get("name", ""),
 "locus_type": doc.get("locus_type", ""),
 "location": doc.get("location", ""),
 })

 df = pd.DataFrame(rows)
 print(f"HGNC group '{group_name}': "
 f"{len(df)} members")
 return df
```

## 4. HGNC integrationpipeline

```python
def hgnc_pipeline(symbols, aliases=None,
 output_dir="results"):
 """
 HGNC integrationmethodpipeline。

 Parameters:
 symbols: list[str] — formula
 aliases: list[str] | None — 
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) details
 details = []
 for sym in symbols:
 info = hgnc_fetch_symbol(sym)
 if info:
 details.append(info)
 detail_df = pd.DataFrame(details)
 detail_df.to_csv(
 output_dir / "hgnc_details.csv",
 index=False)

 # 2) 
 if aliases:
 alias_df = hgnc_resolve_batch(aliases)
 alias_df.to_csv(
 output_dir / "hgnc_alias_resolved.csv",
 index=False)

 # 3) ID 
 xref_rows = []
 for d in details:
 xref_rows.append({
 "symbol": d.get("symbol", ""),
 "hgnc_id": d.get("hgnc_id", ""),
 "ensembl": d.get("ensembl_gene_id", ""),
 "entrez": d.get("entrez_id", ""),
 "uniprot": (d.get("uniprot_ids", [""])[0]
 if d.get("uniprot_ids")
 else ""),
 })
 xref_df = pd.DataFrame(xref_rows)
 xref_df.to_csv(
 output_dir / "hgnc_xref.csv",
 index=False)

 print(f"HGNC pipeline → {output_dir}")
 return {"details": detail_df, "xref": xref_df}
```

---

## Pipeline Integration

```
biothings-idmapping → hgnc-nomenclature → genome-sequence-tools
 (MyGene/MyVariant) (formula) (sequenceanalysis)
 │ │ ↓
 gene-expression ────────────┘ variant-interpretation
 (RNA-seq) 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/hgnc_details.csv` | genedetails | → gene-expression |
| `results/hgnc_alias_resolved.csv` | | → biothings-idmapping |
| `results/hgnc_xref.csv` | ID phasereference | → genome-sequence-tools |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `hgnc` | HGNC | genemethodsearch |

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
