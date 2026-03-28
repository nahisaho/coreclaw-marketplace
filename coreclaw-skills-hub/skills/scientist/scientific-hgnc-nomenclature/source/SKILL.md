---
name: scientific-hgnc-nomenclature
description: |
 HGNC nomenclature skill. Official gene symbol resolution, gene name standardization, symbol history tracking, and gene family classification via HGNC database.
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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
