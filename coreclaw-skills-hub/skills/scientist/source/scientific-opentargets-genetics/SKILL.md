---
name: scientific-opentargets-genetics
description: |
 Open Targets Platform skill。Open Targets Platform
 GraphQL API using-disease
 L2G pharmacogenomicssearch。
 ToolUniverse integration: opentarget。
tu_tools:
 - key: opentarget
 name: Open Targets
 description: -disease GraphQL API
---

# Scientific Open Targets Genetics

Open Targets Platform GraphQL API utilizing-disease
retrievalsearchL2G
pipeline is provided。

## When to Use

- gene  and disease's is searchedand
- data is retrievedand
- GWAS fromgene L2G mappingwhen needed
- 'ssafety profile is verifiedand
- pharmacogenomicsdata is searchedand

---

## Quick Start

## 1. -disease

```python
import requests
import pandas as pd

OT_API = ("https://api.platform.opentargets.org"
 "/api/v4/graphql")


def ot_target_disease_assoc(target_id, limit=25):
 """
 Open Targets — -disease。

 Parameters:
 target_id: str — Ensembl Gene ID
 (example: "ENSG00000012048" = BRCA1)
 limit: int — maximum results
 """
 query = """
 query targetDisease($id: String!, $size: Int!) {
 target(ensemblId: $id) {
 id
 approvedSymbol
 associatedDiseases(page: {size: $size, index: 0}) {
 count
 rows {
 disease { id name }
 score
 datatypeScores {
 componentId: id
 score
 }
 }
 }
 }
 }
 """
 variables = {"id": target_id, "size": limit}
 resp = requests.post(OT_API,
 json={"query": query,
 "variables": variables},
 timeout=30)
 resp.raise_for_status
 data = resp.json["data"]["target"]

 rows = []
 for r in data["associatedDiseases"]["rows"]:
 row = {
 "target_id": target_id,
 "target_symbol": data["approvedSymbol"],
 "disease_id": r["disease"]["id"],
 "disease_name": r["disease"]["name"],
 "overall_score": r["score"],
 }
 for dt in r["datatypeScores"]:
 row[dt["componentId"]] = dt["score"]
 rows.append(row)

 df = pd.DataFrame(rows)
 total = data["associatedDiseases"]["count"]
 print(f"OT associations: {data['approvedSymbol']} "
 f"→ {len(df)}/{total} diseases")
 return df
```

## 2. 

```python
def ot_drug_evidence(target_id, disease_id, limit=50):
 """
 Open Targets — 。

 Parameters:
 target_id: str — Ensembl Gene ID
 disease_id: str — EFO Disease ID
 (example: "EFO_0000305" = breast carcinoma)
 limit: int — maximum results
 """
 query = """
 query drugEvidence($ensemblId: String!,
 $efoId: String!,
 $size: Int!) {
 disease(efoId: $efoId) {
 id
 name
 evidences(
 ensemblIds: [$ensemblId]
 datasourceIds: ["chembl"]
 size: $size
 ) {
 count
 rows {
 id
 score
 drug {
 id name drugType
 maximumClinicalTrialPhase
 mechanismsOfAction {
 rows { actionType }
 }
 }
 clinicalPhase
 clinicalStatus
 urls { niceName url }
 }
 }
 }
 }
 """
 variables = {"ensemblId": target_id,
 "efoId": disease_id,
 "size": limit}
 resp = requests.post(OT_API,
 json={"query": query,
 "variables": variables},
 timeout=30)
 resp.raise_for_status
 data = resp.json["data"]["disease"]

 results = []
 for ev in data["evidences"]["rows"]:
 drug = ev.get("drug", {})
 moas = drug.get("mechanismsOfAction", {})
 moa_list = [m["actionType"]
 for m in moas.get("rows", [])]
 results.append({
 "disease": data["name"],
 "drug_id": drug.get("id", ""),
 "drug_name": drug.get("name", ""),
 "drug_type": drug.get("drugType", ""),
 "max_phase": drug.get(
 "maximumClinicalTrialPhase", 0),
 "clinical_phase": ev.get("clinicalPhase", ""),
 "clinical_status": ev.get(
 "clinicalStatus", ""),
 "moa": "; ".join(moa_list),
 "score": ev.get("score", 0),
 })

 df = pd.DataFrame(results)
 print(f"OT drug evidence: {len(df)} entries")
 return df
```

## 3. L2G (Locus-to-Gene)

```python
def ot_l2g_variants(study_id, limit=50):
 """
 Open Targets Genetics — L2G -genemapping。

 Parameters:
 study_id: str — GWAS Study ID
 (example: "GCST004988")
 limit: int — maximum results
 """
 # OT Genetics API
 OT_GENETICS = ("https://api.genetics.opentargets.org"
 "/graphql")
 query = """
 query l2g($studyId: String!, $size: Int!) {
 studyLocus2GeneTable(studyId: $studyId,
 pageSize: $size) {
 rows {
 gene { id symbol }
 variant { id rsId }
 yProbaModel
 yProbaDistance
 yProbaInteraction
 yProbaMolecularQTL
 yProbaPathogenicity
 hasColoc
 distanceToLocus
 }
 }
 }
 """
 variables = {"studyId": study_id, "size": limit}
 resp = requests.post(OT_GENETICS,
 json={"query": query,
 "variables": variables},
 timeout=30)
 resp.raise_for_status
 data = resp.json["data"]["studyLocus2GeneTable"]

 rows = []
 for r in data["rows"]:
 rows.append({
 "gene_id": r["gene"]["id"],
 "gene_symbol": r["gene"]["symbol"],
 "variant_id": r["variant"]["id"],
 "rsid": r["variant"]["rsId"],
 "l2g_score": r["yProbaModel"],
 "distance_score": r["yProbaDistance"],
 "interaction_score": r["yProbaInteraction"],
 "qtl_score": r["yProbaMolecularQTL"],
 "pathogenicity": r["yProbaPathogenicity"],
 "has_coloc": r["hasColoc"],
 })

 df = pd.DataFrame(rows)
 if not df.empty:
 df = df.sort_values("l2g_score", ascending=False)
 print(f"OT L2G: {study_id} → {len(df)} gene mappings")
 return df
```

## 4. Open Targets integrationpipeline

```python
def ot_pipeline(gene_symbol, ensembl_id,
 output_dir="results"):
 """
 Open Targets integrationpipeline。

 Parameters:
 gene_symbol: str — gene symbol (example: "BRCA1")
 ensembl_id: str — Ensembl Gene ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) -disease
 assoc = ot_target_disease_assoc(ensembl_id)
 assoc.to_csv(output_dir / "ot_associations.csv",
 index=False)

 # 2) disease's
 if not assoc.empty:
 top_disease = assoc.iloc[0]["disease_id"]
 drugs = ot_drug_evidence(ensembl_id, top_disease)
 drugs.to_csv(output_dir / "ot_drugs.csv",
 index=False)

 print(f"OT pipeline: {gene_symbol} → {output_dir}")
 return {"associations": assoc}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `opentarget` | Open Targets | -disease GraphQL (~55 tools) |

## Pipeline Integration

```
disease-research → opentargets-genetics → drug-target-profiling
 (diseasegene) (OT Platform API) 
 │ │ ↓
variant-interpretation ────┘ pharmacogenomics
 (ClinVar/VEP) │ 
 ↓
 gnomad-variants
 (frequency)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/ot_associations.csv` | -disease | → disease-research |
| `results/ot_drugs.csv` | | → drug-target-profiling |
---

## Harness Optimization (v0.4.0)

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
