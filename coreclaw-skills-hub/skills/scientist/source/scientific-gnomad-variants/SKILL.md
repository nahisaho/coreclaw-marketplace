---
name: scientific-gnomad-variants
description: |
 gnomAD skill。gnomAD (Genome Aggregation Database)
 GraphQL API usingallele frequencygene
 (pLI/LOEUF)
 Data Retrieval。---

# Scientific gnomAD Variants

gnomAD (Genome Aggregation Database) GraphQL API utilizing
allele frequencyretrievalgene (pLI/LOEUF/Z-scores)
datapipeline
is provided.

## When to Use

- 'sallele frequency (AF) is verifiedand
- gene's LoF (pLI/LOEUF) is evaluatedand
- genome'swhen needed
- (gnomAD v4 exome/genome) frequency is comparedand
- ClinVar/VEP annotationand frequencyintegrationwhen needed

---

## Quick Start

## 1. frequency

```python
import requests
import pandas as pd

GNOMAD_API = "https://gnomad.broadinstitute.org/api"


def gnomad_variant(variant_id, dataset="gnomad_r4"):
 """
 gnomAD — frequencyretrieval。

 Parameters:
 variant_id: str — ID
 (example: "1-55516888-G-A", chr-pos-ref-alt)
 dataset: str — dataset
 (example: "gnomad_r4", "gnomad_r3")
 """
 query = """
 query gnomadVariant($variantId: String!,
 $dataset: DatasetId!) {
 variant(variantId: $variantId,
 dataset: $dataset) {
 variant_id
 chrom
 pos
 ref
 alt
 exome {
 ac
 an
 af
 ac_hom
 populations {
 id
 ac
 an
 af
 }
 }
 genome {
 ac
 an
 af
 ac_hom
 populations {
 id
 ac
 an
 af
 }
 }
 rsids
 transcript_consequences {
 gene_symbol
 transcript_id
 consequence
 hgvsc
 hgvsp
 lof
 lof_filter
 polyphen_prediction
 sift_prediction
 }
 }
 }
 """
 variables = {"variantId": variant_id,
 "dataset": dataset}
 resp = requests.post(GNOMAD_API,
 json={"query": query,
 "variables": variables},
 timeout=30)
 resp.raise_for_status
 data = resp.json.get("data", {}).get("variant")

 if not data:
 print(f"gnomAD: {variant_id} not found")
 return {}

 exome = data.get("exome") or {}
 genome = data.get("genome") or {}

 result = {
 "variant_id": data["variant_id"],
 "chrom": data["chrom"],
 "pos": data["pos"],
 "ref": data["ref"],
 "alt": data["alt"],
 "rsids": "; ".join(data.get("rsids", [])),
 "exome_af": exome.get("af", 0),
 "exome_ac": exome.get("ac", 0),
 "exome_an": exome.get("an", 0),
 "exome_hom": exome.get("ac_hom", 0),
 "genome_af": genome.get("af", 0),
 "genome_ac": genome.get("ac", 0),
 "genome_an": genome.get("an", 0),
 "genome_hom": genome.get("ac_hom", 0),
 }

 # frequency (exome)
 for pop in exome.get("populations", []):
 result[f"exome_{pop['id']}_af"] = pop.get("af", 0)

 print(f"gnomAD variant: {variant_id} "
 f"(exome AF={result['exome_af']:.6f})")
 return result
```

## 2. gene (pLI/LOEUF)

```python
def gnomad_gene_constraint(gene_symbol,
 dataset="gnomad_r4"):
 """
 gnomAD — generetrieval。

 Parameters:
 gene_symbol: str — gene symbol (example: "BRCA1")
 dataset: str — dataset
 """
 query = """
 query geneConstraint($gene: String!,
 $dataset: DatasetId!) {
 gene(gene_symbol: $gene,
 reference_genome: GRCh38) {
 gene_id
 symbol
 gnomad_constraint {
 exp_lof
 exp_mis
 exp_syn
 obs_lof
 obs_mis
 obs_syn
 oe_lof
 oe_lof_lower
 oe_lof_upper
 oe_mis
 oe_syn
 lof_z
 mis_z
 syn_z
 pLI
 }
 }
 }
 """
 variables = {"gene": gene_symbol,
 "dataset": dataset}
 resp = requests.post(GNOMAD_API,
 json={"query": query,
 "variables": variables},
 timeout=30)
 resp.raise_for_status
 gene = resp.json.get("data", {}).get("gene")

 if not gene:
 print(f"gnomAD gene: {gene_symbol} not found")
 return {}

 c = gene.get("gnomad_constraint") or {}
 result = {
 "gene_id": gene["gene_id"],
 "symbol": gene["symbol"],
 "pLI": c.get("pLI", None),
 "LOEUF": c.get("oe_lof_upper", None),
 "oe_lof": c.get("oe_lof", None),
 "oe_mis": c.get("oe_mis", None),
 "oe_syn": c.get("oe_syn", None),
 "lof_z": c.get("lof_z", None),
 "mis_z": c.get("mis_z", None),
 "syn_z": c.get("syn_z", None),
 "exp_lof": c.get("exp_lof", None),
 "obs_lof": c.get("obs_lof", None),
 }
 pli = result.get("pLI") or 0
 loeuf = result.get("LOEUF") or 0
 print(f"gnomAD constraint: {gene_symbol} "
 f"(pLI={pli:.3f}, LOEUF={loeuf:.3f})")
 return result
```

## 3. 

```python
def gnomad_region(chrom, start, stop,
 dataset="gnomad_r4", limit=500):
 """
 gnomAD — retrieval。

 Parameters:
 chrom: str — (example: "1")
 start: int — start (GRCh38)
 stop: int — end
 dataset: str — dataset
 limit: int — maximum results
 """
 query = """
 query regionVariants($chrom: String!,
 $start: Int!,
 $stop: Int!,
 $dataset: DatasetId!) {
 region(chrom: $chrom, start: $start,
 stop: $stop,
 reference_genome: GRCh38) {
 variants(dataset: $dataset) {
 variant_id
 pos
 ref
 alt
 exome { af ac an }
 genome { af ac an }
 rsids
 }
 }
 }
 """
 variables = {"chrom": chrom, "start": start,
 "stop": stop, "dataset": dataset}
 resp = requests.post(GNOMAD_API,
 json={"query": query,
 "variables": variables},
 timeout=30)
 resp.raise_for_status
 data = resp.json.get("data", {}).get("region", {})

 rows = []
 for v in data.get("variants", [])[:limit]:
 exome = v.get("exome") or {}
 genome = v.get("genome") or {}
 rows.append({
 "variant_id": v["variant_id"],
 "pos": v["pos"],
 "ref": v["ref"],
 "alt": v["alt"],
 "rsids": "; ".join(v.get("rsids", [])),
 "exome_af": exome.get("af", 0),
 "genome_af": genome.get("af", 0),
 })

 df = pd.DataFrame(rows)
 print(f"gnomAD region: {chrom}:{start}-{stop} "
 f"→ {len(df)} variants")
 return df
```

## 4. gnomAD integrationpipeline

```python
def gnomad_pipeline(gene_symbol, chrom, start, stop,
 output_dir="results"):
 """
 gnomAD integrationpipeline。

 Parameters:
 gene_symbol: str — gene symbol
 chrom: str — 
 start: int — start
 stop: int — end
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) gene
 constraint = gnomad_gene_constraint(gene_symbol)
 pd.DataFrame([constraint]).to_csv(
 output_dir / "gnomad_constraint.csv",
 index=False)

 # 2) 
 variants = gnomad_region(chrom, start, stop)
 variants.to_csv(
 output_dir / "gnomad_region.csv",
 index=False)

 # 3) extraction (AF < 0.01)
 if not variants.empty:
 rare = variants[
 (variants["exome_af"] < 0.01) |
 (variants["genome_af"] < 0.01)
 ]
 rare.to_csv(
 output_dir / "gnomad_rare.csv",
 index=False)
 print(f" Rare variants: {len(rare)}")

 print(f"gnomAD pipeline: {gene_symbol} "
 f"→ {output_dir}")
 return {"constraint": constraint,
 "variants": variants}
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
variant-interpretation → gnomad-variants → variant-effect-prediction
 (ClinVar ) (gnomAD API) (VEP/CADD/REVEL)
 │ │ ↓
 civic-evidence ──────────────┘ rare-disease-genetics
 (CIViC ) │ (disease)
 ↓
 opentargets-genetics
 (OT )
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gnomad_constraint.csv` | gene | → rare-disease-genetics |
| `results/gnomad_region.csv` | | → variant-interpretation |
| `results/gnomad_rare.csv` | | → variant-effect-prediction |
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
