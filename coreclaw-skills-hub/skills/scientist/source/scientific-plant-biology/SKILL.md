---
name: scientific-plant-biology
description: |
 integrationskill。Plant Reactome metabolismpathway
 TAIR Arabidopsis genomeinformationPhytozome comparison
 Ensembl Plants typeloganalysis。
tu_tools:
 - key: tair
 name: TAIR
 description: genomedatasearch
---

# Scientific Plant Biology

Plant Reactome / TAIR / Phytozome / Ensembl Plants utilizing
genomemetabolismpathwayintegrated analysispipeline is provided。

## When to Use

- metabolismpathway analysis (Plant Reactome) is executedand
- Arabidopsis thaliana 's geneproteininformation is retrievedand
- type's comparisonanalysis is performedand
- loglogwhen needed
- forgene is exploredand
- tabletypedata and genetypeintegrationwhen needed

---

## Quick Start

## 1. Plant Reactome pathwaysearch

```python
import requests
import pandas as pd
import json

PLANT_REACTOME = "https://plantreactome.gramene.org/ContentService"


def plant_reactome_search(query, species="Oryza sativa"):
 """
 Plant Reactome — metabolism/pathwaysearch。

 Parameters:
 query: str — search query (example: "photosynthesis")
 species: str — species name
 """
 url = f"{PLANT_REACTOME}/search/query"
 params = {"query": query, "species": species, "cluster": True}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for group in data.get("results", []):
 for entry in group.get("entries", []):
 results.append({
 "stId": entry.get("stId", ""),
 "name": entry.get("name", ""),
 "species": entry.get("species", ""),
 "type": entry.get("exactType", ""),
 "compartment": entry.get("compartmentNames", []),
 })

 df = pd.DataFrame(results)
 print(f"Plant Reactome: '{query}' → {len(df)} entries ({species})")
 return df


def plant_reactome_pathway_detail(pathway_id):
 """
 Plant Reactome pathwaydetailsretrieval。

 Parameters:
 pathway_id: str — pathway ID (example: "R-OSA-1119616")
 """
 url = f"{PLANT_REACTOME}/data/pathway/{pathway_id}/containedEvents"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 events = resp.json

 steps = []
 for event in events:
 steps.append({
 "stId": event.get("stId", ""),
 "name": event.get("displayName", ""),
 "type": event.get("className", ""),
 "input_count": len(event.get("input", [])),
 "output_count": len(event.get("output", [])),
 "catalyst": event.get("catalystActivity", [{}])[0].get(
 "displayName", "") if event.get("catalystActivity") else "",
 })

 df = pd.DataFrame(steps)
 print(f"Pathway {pathway_id}: {len(df)} reaction steps")
 return df
```

## 2. TAIR Arabidopsis geneinformation

```python
TAIR_BASE = "https://www.arabidopsis.org/api"


def tair_gene_search(gene_id=None, gene_name=None, keyword=None):
 """
 TAIR — Arabidopsis thaliana geneinformationretrieval。

 Parameters:
 gene_id: str — AGI ID (example: "AT1G01010")
 gene_name: str — gene name (example: "FLC")
 keyword: str — keyword search
 """
 if gene_id:
 url = f"{TAIR_BASE}/gene/{gene_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json
 return pd.DataFrame([{
 "agi_id": data.get("locus", ""),
 "name": data.get("name", ""),
 "description": data.get("description", ""),
 "chromosome": data.get("chromosome", ""),
 "start": data.get("start", ""),
 "end": data.get("end", ""),
 "strand": data.get("strand", ""),
 "gene_model_type": data.get("gene_model_type", ""),
 }])

 # keyword search
 search_term = gene_name or keyword or ""
 url = f"{TAIR_BASE}/search/gene"
 params = {"query": search_term, "limit": 50}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for gene in data.get("results", []):
 results.append({
 "agi_id": gene.get("locus", ""),
 "name": gene.get("name", ""),
 "description": gene.get("description", ""),
 "chromosome": gene.get("chromosome", ""),
 })

 df = pd.DataFrame(results)
 print(f"TAIR: '{search_term}' → {len(df)} genes")
 return df


def tair_gene_expression(gene_id):
 """
 TAIR — gene expressionretrieval。

 Parameters:
 gene_id: str — AGI ID
 """
 url = f"{TAIR_BASE}/gene/{gene_id}/expression"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 tissues = []
 for expr in data.get("expression", []):
 tissues.append({
 "tissue": expr.get("tissue", ""),
 "stage": expr.get("developmental_stage", ""),
 "level": expr.get("expression_level", ""),
 "source": expr.get("source", ""),
 })

 df = pd.DataFrame(tissues)
 print(f"TAIR expression: {gene_id} → {len(df)} tissue records")
 return df
```

## 3. Ensembl Plants typecomparison

```python
ENSEMBL_PLANTS = "https://rest.ensembl.org"


def ensembl_plants_orthologs(gene_id, source_species="arabidopsis_thaliana",
 target_species=None):
 """
 Ensembl Plants — typelogsearch。

 Parameters:
 gene_id: str — Ensembl Gene ID or symbol
 source_species: str — type
 target_species: str — type (None = alltype)
 """
 url = f"{ENSEMBL_PLANTS}/homology/id/{gene_id}"
 params = {
 "type": "orthologues",
 "content-type": "application/json",
 "compara": "plants",
 }
 if target_species:
 params["target_species"] = target_species

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 orthologs = []
 for homology in data.get("data", [{}])[0].get("homologies", []):
 target = homology.get("target", {})
 orthologs.append({
 "source_gene": gene_id,
 "source_species": source_species,
 "target_gene": target.get("id", ""),
 "target_species": target.get("species", ""),
 "target_protein": target.get("protein_id", ""),
 "identity": target.get("perc_id", 0),
 "dn_ds": homology.get("dn_ds", None),
 "type": homology.get("type", ""),
 })

 df = pd.DataFrame(orthologs)
 print(f"Ensembl Plants orthologs: {gene_id} → {len(df)} homologs")
 return df
```

## 4. Phytozome comparison

```python
PHYTOZOME_BASE = "https://phytozome-next.jgi.doe.gov/api"


def phytozome_gene_family(gene_id, species="Athaliana"):
 """
 Phytozome — genecomparison。

 Parameters:
 gene_id: str — gene ID
 species: str — type
 """
 url = f"{PHYTOZOME_BASE}/search"
 params = {"query": gene_id, "organism": species}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 families = []
 for hit in data.get("hits", []):
 families.append({
 "gene_id": hit.get("gene_id", ""),
 "family_id": hit.get("family_id", ""),
 "family_name": hit.get("family_name", ""),
 "species": hit.get("organism", ""),
 "annotation": hit.get("annotation", ""),
 "pfam_domains": hit.get("pfam", []),
 })

 df = pd.DataFrame(families)
 print(f"Phytozome: {gene_id} → {len(df)} family members")
 return df
```

## 5. integrationpipeline

```python
def plant_biology_pipeline(gene_query, species="Oryza sativa",
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 gene_query: str — gene/pathway
 species: str — type
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) Plant Reactome pathway
 pathways = plant_reactome_search(gene_query, species=species)
 pathways.to_csv(output_dir / "plant_pathways.csv", index=False)

 # 2) TAIR (Arabidopsis )
 tair_genes = tair_gene_search(keyword=gene_query)
 tair_genes.to_csv(output_dir / "tair_genes.csv", index=False)

 # 3) Ensembl Plants log
 if len(tair_genes) > 0:
 top_gene = tair_genes.iloc[0]["agi_id"]
 orthologs = ensembl_plants_orthologs(top_gene)
 orthologs.to_csv(output_dir / "orthologs.csv", index=False)
 else:
 orthologs = pd.DataFrame

 print(f"Plant biology pipeline: {output_dir}")
 return {
 "pathways": pathways,
 "tair_genes": tair_genes,
 "orthologs": orthologs,
 }
```

---

## Pipeline Integration

```
pathway-enrichment → plant-biology → environmental-ecology
 (KEGG/Reactome) (PlantReactome) (ecology/environment)
 │ │ ↓
 gene-annotation ────────┘ marine-ecology
 (GO/InterPro) │ (OBIS/WoRMS)
 ↓
 comparative-genomics
 (Ensembl comparison)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/plant_pathways.csv` | Plant Reactome pathway | → pathway-enrichment |
| `results/tair_genes.csv` | TAIR Arabidopsis gene | → gene-annotation |
| `results/orthologs.csv` | typelog | → comparative-genomics |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `tair` | TAIR | genomedatasearch |
---

## Harness Optimization (v0.4.0)

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
