---
name: scientific-ensembl-genomics
description: |
 Ensembl REST API skill。genesequenceretrieval
 VEP (Variant Effect Predictor) annotation
 elementphylogenyphasesearchclassificationintegrationpipeline。
---

# Scientific Ensembl Genomics

Ensembl REST API (rest.ensembl.org) utilizingdata
pipeline is provided。geneinformationretrieval、VEP prediction、
phasesearch、phylogenyanalysisintegration。

## When to Use

- Ensembl Gene ID fromgeneinformationcoordinates is retrievedand
- VEP 'spredictionwhen needed (SIFT/PolyPhen/CADD)
- gene's loglog is searchedand
- Ensembl ↔ UniProt / RefSeq / HGNC 's ID transformation when needed
- genome's element (promoter/enhancer) is searchedand
- typecomparisondata is retrievedand

---

## Quick Start

## 1. gene

```python
import requests
import pandas as pd

ENSEMBL_REST = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def lookup_gene(gene_id, expand=True):
 """
 Ensembl geneinformationretrieval。

 Parameters:
 gene_id: str — Ensembl Gene ID (example: "ENSG00000141510")
 expand: bool — information

 """
 url = f"{ENSEMBL_REST}/lookup/id/{gene_id}"
 params = {"expand": 1 if expand else 0}
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 data = resp.json

 info = {
 "id": data.get("id"),
 "display_name": data.get("display_name"),
 "biotype": data.get("biotype"),
 "species": data.get("species"),
 "assembly_name": data.get("assembly_name"),
 "seq_region_name": data.get("seq_region_name"),
 "start": data.get("start"),
 "end": data.get("end"),
 "strand": data.get("strand"),
 "description": data.get("description"),
 }

 if expand and "Transcript" in data:
 info["n_transcripts"] = len(data["Transcript"])
 info["canonical_transcript"] = data.get("canonical_transcript")

 print(f"Gene: {info['display_name']} ({info['id']}), "
 f"chr{info['seq_region_name']}:{info['start']}-{info['end']}")
 return info
```

## 2. sequenceretrieval

```python
def get_sequence(seq_id, seq_type="genomic", species="homo_sapiens"):
 """
 Ensembl sequenceretrieval (DNA/cDNA/CDS/protein)。

 Parameters:
 seq_id: str — Ensembl ID (Gene/Transcript/Translation)
 seq_type: str — "genomic", "cdna", "cds", "protein"
 species: str — organism/species

 """
 url = f"{ENSEMBL_REST}/sequence/id/{seq_id}"
 params = {"type": seq_type}
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 data = resp.json

 result = {
 "id": data.get("id"),
 "seq_type": seq_type,
 "molecule": data.get("molecule"),
 "length": len(data.get("seq", "")),
 "sequence": data.get("seq"),
 }

 print(f"Sequence: {result['id']} ({seq_type}), {result['length']} bp/aa")
 return result
```

## 3. VEP (Variant Effect Predictor)

```python
def vep_region(species, chromosome, position, allele,
 sift=True, polyphen=True, cadd=False):
 """
 VEP by/viaprediction。

 Parameters:
 species: str — "homo_sapiens"
 chromosome: str — number
 position: int — genomecoordinates
 allele: str — (example: "T")
 sift: bool — SIFT prediction
 polyphen: bool — PolyPhen prediction
 cadd: bool — CADD 

 ensembl_vep_region(
 species=species, region=f"{chromosome}:{position}:{position}",
 allele=allele, SIFT="b", PolyPhen="b"
 )
 """
 region = f"{chromosome}:{position}:{position}"
 url = f"{ENSEMBL_REST}/vep/{species}/region/{region}/{allele}"
 params = {}
 if sift:
 params["SIFT"] = "b"
 if polyphen:
 params["PolyPhen"] = "b"
 if cadd:
 params["CADD"] = 1

 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 results = resp.json

 consequences = []
 for r in results:
 for tc in r.get("transcript_consequences", []):
 cons = {
 "gene_symbol": tc.get("gene_symbol"),
 "gene_id": tc.get("gene_id"),
 "transcript_id": tc.get("transcript_id"),
 "consequence_terms": tc.get("consequence_terms", []),
 "impact": tc.get("impact"),
 "biotype": tc.get("biotype"),
 "amino_acids": tc.get("amino_acids"),
 "codons": tc.get("codons"),
 }
 if "sift_prediction" in tc:
 cons["sift"] = f"{tc['sift_prediction']}({tc.get('sift_score')})"
 if "polyphen_prediction" in tc:
 cons["polyphen"] = f"{tc['polyphen_prediction']}({tc.get('polyphen_score')})"
 consequences.append(cons)

 df = pd.DataFrame(consequences)
 print(f"VEP {chromosome}:{position} {allele}: "
 f"{len(df)} transcript consequences")
 return df
```

## 4. (ID transformation)

```python
def get_xrefs(ensembl_id, external_db=None):
 """
 Ensembl ID from DB 's ID retrieval。

 Parameters:
 ensembl_id: str — Ensembl ID
 external_db: str — filter DB (example: "UniProt", "RefSeq", "HGNC")

 """
 url = f"{ENSEMBL_REST}/xrefs/id/{ensembl_id}"
 params = {}
 if external_db:
 params["external_db"] = external_db

 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 xrefs = resp.json

 rows = []
 for x in xrefs:
 rows.append({
 "primary_id": x.get("primary_id"),
 "display_id": x.get("display_id"),
 "dbname": x.get("dbname"),
 "description": x.get("description", "")[:100],
 })

 df = pd.DataFrame(rows)
 print(f"Cross-references for {ensembl_id}: {len(df)} entries")
 return df
```

## 5. phasesearch (log/log)

```python
def get_homology(species, gene_symbol, target_species=None,
 homology_type="orthologues"):
 """
 genephasesearch。

 Parameters:
 species: str — organism/species
 gene_symbol: str — gene symbol
 target_species: str — organism/species (None alltype)
 homology_type: str — "orthologues", "paralogues", "all"

 ensembl_get_homology(
 species=species, symbol=gene_symbol,
 target_species=target_species, type=homology_type
 )
 """
 url = f"{ENSEMBL_REST}/homology/symbol/{species}/{gene_symbol}"
 params = {"type": homology_type}
 if target_species:
 params["target_species"] = target_species

 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status

 homologies = resp.json.get("data", [{}])[0].get("homologies", [])

 rows = []
 for h in homologies:
 target = h.get("target", {})
 rows.append({
 "type": h.get("type"),
 "target_species": target.get("species"),
 "target_gene_id": target.get("id"),
 "target_symbol": target.get("protein_id"),
 "perc_id": target.get("perc_id"),
 "perc_pos": target.get("perc_pos"),
 "dn_ds": h.get("dn_ds"),
 })

 df = pd.DataFrame(rows)
 print(f"Homologs of {gene_symbol} ({species}): {len(df)} found")
 return df
```

## 6. elementsearch

```python
def get_regulatory_features(species, region):
 """
 genome's element (promoter/enhancer/CTCF) search。

 Parameters:
 species: str — organism/species (example: "homo_sapiens")
 region: str — genome (example: "7:140000000-140100000")

 """
 url = f"{ENSEMBL_REST}/overlap/region/{species}/{region}"
 params = {"feature": "regulatory"}

 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 features = resp.json

 rows = []
 for f in features:
 rows.append({
 "id": f.get("id"),
 "feature_type": f.get("feature_type"),
 "start": f.get("start"),
 "end": f.get("end"),
 "strand": f.get("strand"),
 "description": f.get("description", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Regulatory features in {region}: {len(df)}")
 return df
```

## 7. genephylogeny

```python
def get_gene_tree(gene_id, prune_species=None):
 """
 gene's phylogenyretrieval。

 Parameters:
 gene_id: str — Ensembl Gene ID
 prune_species: list — phylogenyorganism/species

 """
 url = f"{ENSEMBL_REST}/genetree/member/id/{gene_id}"
 params = {"sequence": "none", "aligned": 0}
 if prune_species:
 params["prune_species"] = ";".join(prune_species)

 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 tree = resp.json

 result = {
 "tree_id": tree.get("tree", {}).get("id"),
 "type": tree.get("tree", {}).get("type"),
 "n_members": _count_leaves(tree.get("tree", {})),
 }

 print(f"Gene tree {result['tree_id']}: {result['n_members']} members")
 return tree


def _count_leaves(node):
 """phylogenynumber/count 。"""
 if "children" not in node:
 return 1
 return sum(_count_leaves(c) for c in node["children"])
```

---

## Pipeline Integration

```
bioinformatics ───→ ensembl-genomics ───→ variant-interpretation
 (Ensembl Gene ID) (VEP annotation) (ACMG/AMP classification)
 │ │ ↓
genome-sequence-tools ──┘ │ variant-effect-prediction
 (BLAST/dbSNP) │ (AlphaMissense/CADD)
 ↓
 regulatory-genomics → epigenomics-chromatin
 (RegulomeDB/ReMap) (ChIP-seq/ATAC-seq)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/ensembl_gene_info.json` | geneinformation | → bioinformatics |
| `results/vep_consequences.csv` | VEP | → variant-interpretation |
| `results/homology_table.csv` | log/log | → phylogenetics |
| `results/regulatory_features.csv` | element | → regulatory-genomics |


| Tool Name | Usage |
|---------|------|
| `ensembl_lookup_gene` | gene |
| `ensembl_get_sequence` | sequenceretrieval |
| `ensembl_get_variants` | retrieval |
| `ensembl_get_variation` | details |
| `ensembl_get_variation_phenotypes` | tabletype |
| `ensembl_vep_region` | VEP prediction |
| `ensembl_get_xrefs` | |
| `ensembl_get_xrefs_by_name` | name xref |
| `ensembl_get_regulatory_features` | element |
| `ensembl_get_genetree` | genephylogeny |
| `ensembl_get_homology` | phasesearch |
| `ensembl_get_alignment` | sequence |
| `ensembl_get_taxonomy` | classificationinformation |
| `ensembl_get_species` | organism/specieslist |
| `ensembl_get_ontology_term` | GO |
| `ensembl_get_overlap_features` | |
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
