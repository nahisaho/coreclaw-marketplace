---
name: scientific-cell-line-resources
description: |
 cellskill。Cellosaurus celldatabasesearch、
 STR file、、
 celldata (tissuediseasetype) retrievalpipeline。
---

# Scientific Cell Line Resources

Cellosaurus and celldatabase
pipeline.

## When to Use

- cell's formulaaccessionnumber is verifiedand
- cell's (tissuediseasetype) is investigatedand
- STR file cell'sverificationwhen needed
- cell's  is verifiedand
- experimentforcell's referenceliteraturedatabase is retrievedand

---

## Quick Start

## 1. Cellosaurus cellsearch

```python
import requests
import pandas as pd

CELLOSAURUS_API = "https://api.cellosaurus.org"


def search_cellosaurus(query, limit=25):
 """
 Cellosaurus cellsearch。

 Parameters:
 query: str — cell (e.g., "HeLa", "MCF-7", "A549")
 limit: int — maximum retrieval count

 """
 params = {"q": query, "rows": limit, "format": "json"}
 resp = requests.get(f"{CELLOSAURUS_API}/search/cell-line", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for cell_line in data.get("result", {}).get("cellLineList", []):
 cl = cell_line.get("cellLine", {})
 results.append({
 "accession": cl.get("accession", ""),
 "name": cl.get("name", ""),
 "synonyms": [s.get("value", "") for s in cl.get("synonymList", [])],
 "category": cl.get("category", ""),
 "sex": cl.get("sex", ""),
 "species": cl.get("species", {}).get("value", ""),
 "diseases": [
 d.get("terminology", {}).get("value", "")
 for d in cl.get("diseaseList", [])
 ],
 "derived_from_site": cl.get("derivedFromSite", {}).get("value", ""),
 "is_contaminated": cl.get("isContaminated", False),
 "is_problematic": cl.get("isProblematic", False),
 })

 df = pd.DataFrame(results)
 print(f"Cellosaurus search '{query}': {len(df)} cell lines")
 return df
```

## 2. celldetailsinformationretrieval

```python
def get_cellosaurus_entry(accession):
 """
 Cellosaurus celldetailsinformationretrieval。

 Parameters:
 accession: str — Cellosaurus accession (e.g., "CVCL_0030")
 """
 resp = requests.get(
 f"{CELLOSAURUS_API}/cell-line/{accession}",
 params={"format": "json"}
 )
 resp.raise_for_status
 data = resp.json

 cl = data.get("cellLine", {})
 entry = {
 "accession": cl.get("accession", ""),
 "name": cl.get("name", ""),
 "category": cl.get("category", ""),
 "sex": cl.get("sex", ""),
 "age": cl.get("age", ""),
 "species": cl.get("species", {}).get("value", ""),
 "diseases": [
 {
 "name": d.get("terminology", {}).get("value", ""),
 "accession": d.get("terminology", {}).get("accession", ""),
 }
 for d in cl.get("diseaseList", [])
 ],
 "derived_from_site": cl.get("derivedFromSite", {}).get("value", ""),
 "is_contaminated": cl.get("isContaminated", False),
 "contamination_comment": cl.get("contaminationComment", ""),
 "str_profile": cl.get("strList", []),
 "references": [
 {
 "pmid": r.get("pubmedId", ""),
 "title": r.get("title", ""),
 }
 for r in cl.get("referenceList", [])
 ],
 "cross_references": [
 {
 "database": xr.get("database", ""),
 "accession": xr.get("accession", ""),
 }
 for xr in cl.get("xrefList", [])
 ],
 }

 print(f"Cellosaurus {accession}: {entry['name']} "
 f"({entry['species']}, {entry['category']})")
 return entry
```

## 3. STR fileverification

```python
def check_str_profile(accession, str_data=None):
 """
 STR (Short Tandem Repeat) fileby/viacellverification。

 Parameters:
 accession: str — Cellosaurus accession
 str_data: dict — measurement STR data {marker: alleles}
 """
 entry = get_cellosaurus_entry(accession)
 ref_str = entry.get("str_profile", [])

 if not ref_str:
 print(f"WARNING: {accession} has no STR profile in Cellosaurus")
 return {"match": None, "message": "No reference STR profile available"}

 ref_markers = {}
 for marker in ref_str:
 name = marker.get("marker", "")
 alleles = marker.get("alleles", "")
 ref_markers[name] = alleles

 if str_data is None:
 print(f"Reference STR for {accession}: {len(ref_markers)} markers")
 return {"reference_str": ref_markers, "marker_count": len(ref_markers)}

 # Calculate match percentage
 matched = 0
 total = 0
 details = []
 for marker, ref_alleles in ref_markers.items:
 if marker in str_data:
 total += 1
 measured = str_data[marker]
 if set(str(ref_alleles).split(",")) == set(str(measured).split(",")):
 matched += 1
 details.append({"marker": marker, "match": True})
 else:
 details.append({
 "marker": marker, "match": False,
 "reference": ref_alleles, "measured": measured,
 })

 match_pct = (matched / total * 100) if total > 0 else 0
 result = {
 "match_percentage": match_pct,
 "matched": matched,
 "total_compared": total,
 "is_authenticated": match_pct >= 80,
 "details": details,
 }

 status = "PASS" if result["is_authenticated"] else "FAIL"
 print(f"STR verification {accession}: {match_pct:.1f}% match → {status}")
 return result
```

## 4. problemcell

```python
def check_contamination_status(cell_line_names):
 """
 cell's/verification。

 Parameters:
 cell_line_names: list — cell
 """
 results = []
 for name in cell_line_names:
 df = search_cellosaurus(name, limit=1)
 if df.empty:
 results.append({
 "name": name, "found": False,
 "is_contaminated": None, "is_problematic": None,
 })
 continue

 row = df.iloc[0]
 results.append({
 "name": name,
 "found": True,
 "accession": row.get("accession", ""),
 "official_name": row.get("name", ""),
 "is_contaminated": row.get("is_contaminated", False),
 "is_problematic": row.get("is_problematic", False),
 "species": row.get("species", ""),
 "diseases": row.get("diseases", []),
 })

 df = pd.DataFrame(results)
 contaminated = df["is_contaminated"].sum if "is_contaminated" in df else 0
 problematic = df["is_problematic"].sum if "is_problematic" in df else 0
 print(f"Cell line check: {len(cell_line_names)} lines, "
 f"{contaminated} contaminated, {problematic} problematic")
 return df
```

---

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

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/cell_lines.csv` | celldata | → cancer-genomics, precision-oncology |
| `results/str_verification.json` | STR verificationresults | → lab-automation, lab-data-management |
| `results/contamination_report.json` | report | → research-methodology |

## Pipeline Integration

```
cancer-genomics ──→ cell-line-resources ──→ lab-automation
 (COSMIC/DepMap) (Cellosaurus STR) (protocol)
 │
 ├──→ precision-oncology (tumorcell)
 ├──→ disease-research (disease)
 └──→ human-protein-atlas (expressiondata)
```
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
