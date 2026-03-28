---
name: scientific-parasite-genomics
description: |
 Parasite genomics skill. Parasite genome analysis, drug resistance marker identification, population genetics of parasites, and host-parasite interaction genomics.
---

# Scientific Parasite Genomics

VEuPathDB (PlasmoDB, VectorBase, ToxoDB, TriTrypDB)
's REST API utilizinganalysispipelineproviding
.

## When to Use

- genome (PlasmoDB) is searchedand
- 'sgenome (VectorBase) is searchedand
- genome (ToxoDB) is searchedand
- /genome (TriTrypDB) is searchedand
- 'swhen needed
- 's comparison is performedand

---

## Quick Start

## 1. VEuPathDB genesearch

```python
import requests
import pandas as pd
import numpy as np

VEUPATHDB_SITES = {
 "plasmo": "https://plasmodb.org/plasmo/service",
 "vector": "https://vectorbase.org/vectorbase/service",
 "toxo": "https://toxodb.org/toxo/service",
 "tritryp": "https://tritrypdb.org/tritrypdb/service",
}


def veupathdb_search_genes(organism, query, db="plasmo",
 limit=100):
 """
 VEuPathDB — genesearch。

 Parameters:
 organism: str — organism/species (example: "Plasmodium falciparum 3D7")
 query: str — searchkeyword (example: "kinase", "transporter")
 db: str — database ("plasmo", "vector", "toxo", "tritryp")
 limit: int — maximum results
 """
 base = VEUPATHDB_SITES.get(db, VEUPATHDB_SITES["plasmo"])
 url = f"{base}/record-types/gene/searches/GenesByTextSearch"

 payload = {
 "searchConfig": {
 "parameters": {
 "text_expression": query,
 "text_fields": "Gene ID,Gene Name or Symbol,"
 "Gene product",
 "organism": [organism],
 }
 },
 "reportConfig": {
 "attributes": ["primary_key", "gene_name",
 "gene_product", "gene_type",
 "chromosome", "start_min",
 "end_max", "strand"],
 "pagination": {"offset": 0, "numRecords": limit},
 },
 }
 headers = {"Content-Type": "application/json"}
 resp = requests.post(url, json=payload, headers=headers,
 timeout=60)
 resp.raise_for_status
 data = resp.json

 results = []
 for rec in data.get("records", []):
 attrs = rec.get("attributes", {})
 results.append({
 "gene_id": attrs.get("primary_key", ""),
 "gene_name": attrs.get("gene_name", ""),
 "product": attrs.get("gene_product", ""),
 "gene_type": attrs.get("gene_type", ""),
 "chromosome": attrs.get("chromosome", ""),
 "start": attrs.get("start_min", None),
 "end": attrs.get("end_max", None),
 "strand": attrs.get("strand", ""),
 })

 df = pd.DataFrame(results)
 print(f"VEuPathDB ({db}) genes: {len(df)} results "
 f"(organism={organism}, query={query})")
 return df
```

## 2. geneannotation

```python
def veupathdb_gene_annotation(gene_id, db="plasmo"):
 """
 VEuPathDB — geneannotationretrieval。

 Parameters:
 gene_id: str — gene ID (example: "PF3D7_1133400")
 db: str — database
 """
 base = VEUPATHDB_SITES.get(db, VEUPATHDB_SITES["plasmo"])
 url = f"{base}/record-types/gene/records/{gene_id}"

 params = {
 "attributes": "all",
 "tables": "GoTerms,InterPro,MetabolicPathways,"
 "PubMed,EcNumber",
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 attrs = data.get("attributes", {})
 tables = data.get("tables", {})

 annotation = {
 "gene_id": gene_id,
 "gene_name": attrs.get("gene_name", ""),
 "product": attrs.get("gene_product", ""),
 "molecular_weight": attrs.get("molecular_weight", ""),
 "isoelectric_point": attrs.get("isoelectric_point", ""),
 "signal_peptide": attrs.get("signal_peptide", ""),
 "transmembrane_domains": attrs.get("transmembrane_domains", ""),
 }

 # GO Term retrieval
 go_terms = []
 for go_rec in tables.get("GoTerms", []):
 go_terms.append({
 "go_id": go_rec.get("go_id", ""),
 "go_term": go_rec.get("go_term_name", ""),
 "ontology": go_rec.get("ontology", ""),
 "evidence": go_rec.get("evidence_code", ""),
 })
 annotation["go_terms"] = go_terms

 # InterPro 
 domains = []
 for d in tables.get("InterPro", []):
 domains.append({
 "interpro_id": d.get("interpro_primary_id", ""),
 "name": d.get("interpro_name", ""),
 "description": d.get("interpro_description", ""),
 })
 annotation["domains"] = domains

 print(f"VEuPathDB annotation: {gene_id}, "
 f"{len(go_terms)} GO terms, {len(domains)} domains")
 return annotation
```

## 3. 

```python
def parasite_drug_target_screen(organism, db="plasmo",
 essentiality_threshold=0.5):
 """
 genome — 。

 Parameters:
 organism: str — organism/species
 db: str — database
 essentiality_threshold: float — requiredthreshold
 """
 # search
 kinases = veupathdb_search_genes(organism, "kinase", db=db)
 # search
 proteases = veupathdb_search_genes(organism, "protease", db=db)
 # search
 transporters = veupathdb_search_genes(
 organism, "transporter", db=db)

 all_targets = pd.concat([kinases, proteases, transporters],
 ignore_index=True)
 all_targets = all_targets.drop_duplicates(subset=["gene_id"])

 # 
 all_targets["target_class"] = "unknown"
 all_targets.loc[
 all_targets["gene_id"].isin(kinases["gene_id"]),
 "target_class"] = "kinase"
 all_targets.loc[
 all_targets["gene_id"].isin(proteases["gene_id"]),
 "target_class"] = "protease"
 all_targets.loc[
 all_targets["gene_id"].isin(transporters["gene_id"]),
 "target_class"] = "transporter"

 print(f"Drug target screen: {len(all_targets)} candidates "
 f"(kinases={len(kinases)}, proteases={len(proteases)}, "
 f"transporters={len(transporters)})")
 return all_targets
```

## 4. integrationpipeline

```python
def parasite_genomics_pipeline(organism, query,
 db="plasmo",
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 organism: str — organism/species (example: "Plasmodium falciparum 3D7")
 query: str — search query
 db: str — database
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) genesearch
 genes = veupathdb_search_genes(organism, query, db=db)
 genes.to_csv(output_dir / "genes.csv", index=False)

 # 2) gene'sannotation
 annotations = []
 for gene_id in genes["gene_id"].head(10):
 try:
 ann = veupathdb_gene_annotation(gene_id, db=db)
 annotations.append(ann)
 except Exception:
 continue
 ann_df = pd.DataFrame([{
 k: v for k, v in a.items
 if not isinstance(v, list)
 } for a in annotations])
 ann_df.to_csv(output_dir / "annotations.csv", index=False)

 # 3) 
 targets = parasite_drug_target_screen(organism, db=db)
 targets.to_csv(output_dir / "drug_targets.csv", index=False)

 print(f"Parasite genomics pipeline: {output_dir}")
 return {
 "genes": genes,
 "annotations": annotations,
 "drug_targets": targets,
 }
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
infectious-disease → parasite-genomics → phylogenetics
 (information) (genome) (phylogenyanalysis)
 │ │ ↓
 drug-discovery ─────────┘ comparative-genomics
 (search/exploration) │ (comparison)
 ↓
 pathway-enrichment
 (pathway analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/genes.csv` | genelist | → phylogenetics |
| `results/annotations.csv` | annotation | → pathway-enrichment |
| `results/drug_targets.csv` | | → drug-discovery |
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
