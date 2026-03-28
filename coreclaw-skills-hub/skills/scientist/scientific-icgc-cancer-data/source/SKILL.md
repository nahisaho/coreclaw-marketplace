---
name: scientific-icgc-cancer-data
description: |
 ICGC cancer data skill. International Cancer Genome Consortium data retrieval, pan-cancer mutation analysis, driver mutation identification, and multi-project comparison.
---

# Scientific ICGC Cancer Data

ICGC (International Cancer Genome Consortium) ARGO DCC API 
utilizingcancergenomedatasearchvariant/mutationcancertypecross-cuttinganalysis
pipeline.

## When to Use

- cancergenome'sdata is searchedand
- cancertype and 'scellvariant/mutationfile is investigatedand
- variant/mutation's information is retrievedand
- cancergenome's variant/mutationminwhen needed
- PCAWG (Pan-Cancer Analysis of Whole Genomes) data utilizingwhen needed
- cancergenevariant/mutation'scomparisondatawhen needed

---

## Quick Start

## 1. ICGC search

```python
import requests
import pandas as pd

ICGC_BASE = "https://dcc.icgc.org/api/v1"


def icgc_search_projects(query=None, limit=50):
 """
 ICGC — cancergenomesearch。

 Parameters:
 query: str — searchkeyword (example: "lung", "BRCA")
 limit: int — maximum results
 """
 url = f"{ICGC_BASE}/projects"
 params = {"size": limit, "from": 1}
 if query:
 params["filters"] = (
 f'{{"project":{{"primarySite":'
 f'{{"is":["{query}"]}}}}}}'
 )

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 results.append({
 "project_id": hit.get("id", ""),
 "project_name": hit.get("name", ""),
 "primary_site": hit.get("primarySite", ""),
 "tumour_type": hit.get("tumourType", ""),
 "tumour_subtype": hit.get("tumourSubtype", ""),
 "primary_country": "; ".join(
 hit.get("primaryCountries", [])),
 "total_donors": hit.get("totalDonorCount", 0),
 "ssm_count": hit.get("ssmCount", 0),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("total_donors", ascending=False)

 total = data.get("pagination", {}).get("total", 0)
 print(f"ICGC projects: {len(df)}/{total} "
 f"(query='{query}')")
 return df


def icgc_search_donors(project_id, limit=100):
 """
 ICGC — search。

 Parameters:
 project_id: str — project ID (example: "BRCA-US")
 limit: int — maximum results
 """
 url = f"{ICGC_BASE}/donors"
 params = {
 "size": limit,
 "filters": (
 f'{{"donor":{{"projectId":'
 f'{{"is":["{project_id}"]}}}}}}'
 ),
 }

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 results.append({
 "donor_id": hit.get("id", ""),
 "project_id": project_id,
 "primary_site": hit.get("primarySite", ""),
 "gender": hit.get("gender", ""),
 "vital_status": hit.get("vitalStatus", ""),
 "age_at_diagnosis": hit.get("ageAtDiagnosis"),
 "disease_status": hit.get(
 "diseaseStatusLastFollowup", ""),
 "ssm_count": hit.get("ssmCount", 0),
 })

 df = pd.DataFrame(results)
 total = data.get("pagination", {}).get("total", 0)
 print(f"ICGC donors: {len(df)}/{total} "
 f"(project={project_id})")
 return df
```

## 2. cellvariant/mutation (SSM) search

```python
def icgc_search_mutations(gene_symbol=None,
 project_id=None,
 consequence_type=None,
 limit=100):
 """
 ICGC — cellvariant/mutation (Simple Somatic Mutation) search。

 Parameters:
 gene_symbol: str — gene symbol (example: "TP53")
 project_id: str — project ID
 consequence_type: str — variant/mutation
 (example: "missense_variant")
 limit: int — maximum results
 """
 url = f"{ICGC_BASE}/mutations"
 filters = {}

 if gene_symbol:
 filters["gene"] = {"symbol": {"is": [gene_symbol]}}
 if project_id:
 filters["donor"] = {"projectId": {"is": [project_id]}}
 if consequence_type:
 filters["mutation"] = {
 "consequenceType": {"is": [consequence_type]}
 }

 import json
 params = {
 "size": limit,
 "filters": json.dumps(filters) if filters else "{}",
 }

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 # key consequence retrieval
 consequences = hit.get("consequences", [])
 top_cons = consequences[0] if consequences else {}

 results.append({
 "mutation_id": hit.get("id", ""),
 "chromosome": hit.get("chromosome", ""),
 "start": hit.get("start"),
 "end": hit.get("end"),
 "mutation": hit.get("mutation", ""),
 "type": hit.get("type", ""),
 "gene_symbol": top_cons.get("geneSymbol", ""),
 "consequence_type": top_cons.get("type", ""),
 "aa_mutation": top_cons.get("aaMutation", ""),
 "affected_donors": hit.get(
 "affectedDonorCountTotal", 0),
 "affected_projects": hit.get(
 "affectedProjectCount", 0),
 "functional_impact": hit.get(
 "functionalImpact", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("affected_donors",
 ascending=False)

 total = data.get("pagination", {}).get("total", 0)
 print(f"ICGC mutations: {len(df)}/{total} "
 f"(gene={gene_symbol}, project={project_id})")
 return df
```

## 3. cancertypevariant/mutationsummary

```python
def icgc_cancer_stats(project_id=None):
 """
 ICGC — cancertypesummary。

 Parameters:
 project_id: str — project ID (None all)
 """
 if project_id:
 url = f"{ICGC_BASE}/projects/{project_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 stats = {
 "project_id": project_id,
 "project_name": data.get("name", ""),
 "primary_site": data.get("primarySite", ""),
 "total_donors": data.get("totalDonorCount", 0),
 "total_specimens": data.get(
 "totalSpecimenCount", 0),
 "ssm_count": data.get("ssmCount", 0),
 "repository": "; ".join(
 data.get("repository", [])),
 }
 print(f"ICGC stats: {project_id} — "
 f"{stats['total_donors']} donors, "
 f"{stats['ssm_count']} mutations")
 return stats
 else:
 # alloverview
 projects = icgc_search_projects(limit=200)
 summary = {
 "total_projects": len(projects),
 "total_donors": projects[
 "total_donors"].sum,
 "total_ssm": projects["ssm_count"].sum,
 "top_sites": projects.groupby(
 "primary_site")["total_donors"].sum(
 ).sort_values(ascending=False).head(10
 ).to_dict,
 }
 print(f"ICGC summary: {summary['total_projects']} "
 f"projects, {summary['total_donors']} donors")
 return summary


def icgc_gene_mutation_frequency(gene_symbol, top_n=20):
 """
 ICGC — genecancertypevariant/mutationfrequency。

 Parameters:
 gene_symbol: str — gene symbol
 top_n: int — topcancertypenumber/count
 """
 mutations = icgc_search_mutations(
 gene_symbol=gene_symbol, limit=500)

 if mutations.empty:
 return pd.DataFrame

 # 
 freq = mutations.groupby("gene_symbol").agg(
 total_mutations=("mutation_id", "count"),
 total_affected_donors=("affected_donors", "sum"),
 mutation_types=("consequence_type",
 lambda x: "; ".join(x.unique[:5])),
 ).reset_index

 print(f"ICGC gene frequency: {gene_symbol} — "
 f"{len(freq)} entries")
 return freq
```

## 4. ICGC integrationpipeline

```python
def icgc_pipeline(gene_symbols, cancer_site=None,
 output_dir="results"):
 """
 ICGC integrationpipeline。

 Parameters:
 gene_symbols: list[str] — gene list
 cancer_site: str — cancerfilter
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) search
 projects = icgc_search_projects(query=cancer_site)
 projects.to_csv(output_dir / "projects.csv", index=False)

 # 2) genevariant/mutationsearch
 all_mutations = []
 for gene in gene_symbols:
 try:
 muts = icgc_search_mutations(
 gene_symbol=gene, limit=200)
 muts["query_gene"] = gene
 all_mutations.append(muts)
 except Exception as e:
 print(f" Warning: {gene} — {e}")
 continue

 if all_mutations:
 combined = pd.concat(all_mutations,
 ignore_index=True)
 combined.to_csv(output_dir / "mutations.csv",
 index=False)

 # 3) cancertype
 if not projects.empty:
 top_project = projects.iloc[0]["project_id"]
 stats = icgc_cancer_stats(project_id=top_project)
 pd.DataFrame([stats]).to_csv(
 output_dir / "cancer_stats.csv", index=False)

 print(f"ICGC pipeline: {output_dir}")
 return {"projects": projects}
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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

## Pipeline Integration

```
cancer-genomics → icgc-cancer-data → precision-oncology
 (cancergenomeall) (ICGC DCC API) (tumor)
 │ │ ↓
 tcga-data ────────────┘ clinical-decision-support
 (TCGA data) │ (clinical decision support)
 ↓
 variant-interpretation
 (variant/mutation)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/projects.csv` | list | → cancer-genomics |
| `results/mutations.csv` | cellvariant/mutation | → variant-interpretation |
| `results/cancer_stats.csv` | cancertype | → precision-oncology |
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
