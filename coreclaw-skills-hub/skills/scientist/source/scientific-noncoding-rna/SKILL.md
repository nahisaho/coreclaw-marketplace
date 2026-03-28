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
| `scientific-gene-expression-transcriptomics` | analysis |
| `scientific-genome-sequence-tools` | sequenceretrieval |
| `scientific-structural-proteomics` | RNA structure |
| `scientific-biothings-idmapping` | ID mapping |

### Dependencies

`requests`, `pandas`
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
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
