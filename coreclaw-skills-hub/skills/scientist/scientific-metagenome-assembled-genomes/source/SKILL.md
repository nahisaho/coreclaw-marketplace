---
name: scientific-metagenome-assembled-genomes
description: |
 Metagenome-assembled genomes (MAG) skill. Metagenomic binning, genome quality assessment (CheckM), taxonomic classification, and functional annotation of MAGs.
---

# Scientific Metagenome-Assembled Genomes

genomefromunitsgenome (MAG) builds
evaluationclassificationannotation's
integrationpipeline is provided。

## When to Use

- genomedatafrom MAG constructionwhen needed
- (MetaBAT2/CONCOCT/MaxBin2) is executedand
- CheckM/CheckM2 genomeall is evaluatedand
- GTDB-Tk MAG 's classificationpositioning is performedand
- dRep MAG when needed
- Prokka/Bakta MAG 's annotation is performedand

---

## Quick Start

## 1. MetaBAT2 

```python
import subprocess
import pandas as pd
from pathlib import Path


def run_metabat2(assembly_fasta, bam_file,
 output_dir="metabat2_bins",
 min_contig=2500):
 """
 MetaBAT2 — genome。

 Parameters:
 assembly_fasta: str — assembly FASTA
 bam_file: str — BAM
 output_dir: str — output directory
 min_contig: int — 
 """
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 # degreetablegeneration
 depth_file = out / "depth.txt"
 subprocess.run([
 "jgi_summarize_bam_contig_depths",
 "--outputDepth", str(depth_file),
 bam_file
 ], check=True)

 # MetaBAT2 
 subprocess.run([
 "metabat2",
 "-i", assembly_fasta,
 "-a", str(depth_file),
 "-o", str(out / "bin"),
 "-m", str(min_contig),
 "--seed", "42",
 ], check=True)

 bins = list(out.glob("bin.*.fa"))
 print(f"MetaBAT2: {len(bins)} bins generated")
 return bins
```

## 2. CheckM2 evaluation

```python
def run_checkm2(bin_dir, output_dir="checkm2_out",
 threads=8):
 """
 CheckM2 — MAG evaluation
 (all / / N50)。

 Parameters:
 bin_dir: str — directory
 output_dir: str — output directory
 threads: int — thread count
 """
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 subprocess.run([
 "checkm2", "predict",
 "--input", bin_dir,
 "--output-directory", str(out),
 "--threads", str(threads),
 "-x", "fa",
 ], check=True)

 report = out / "quality_report.tsv"
 df = pd.read_csv(report, sep="\t")

 # MIMAG criteriaby/viaclassification
 df["quality"] = df.apply(
 lambda r: (
 "high" if r["Completeness"] >= 90
 and r["Contamination"] < 5
 else "medium"
 if r["Completeness"] >= 50
 and r["Contamination"] < 10
 else "low"), axis=1)

 n_hq = (df["quality"] == "high").sum
 n_mq = (df["quality"] == "medium").sum
 n_lq = (df["quality"] == "low").sum
 print(f"CheckM2: {n_hq} HQ, {n_mq} MQ, "
 f"{n_lq} LQ MAGs")
 return df


def filter_quality_mags(checkm_df,
 min_completeness=50,
 max_contamination=10):
 """
 criteriaby/viaMAGfilter。

 Parameters:
 checkm_df: pd.DataFrame — CheckM2 results
 min_completeness: float — all (%)
 max_contamination: float — (%)
 """
 filtered = checkm_df[
 (checkm_df["Completeness"]
 >= min_completeness)
 & (checkm_df["Contamination"]
 <= max_contamination)
 ].copy

 print(f"Filter: {len(filtered)}/"
 f"{len(checkm_df)} MAGs passed "
 f"(≥{min_completeness}% comp, "
 f"≤{max_contamination}% contam)")
 return filtered
```

## 3. GTDB-Tk classification

```python
def run_gtdbtk(bin_dir, output_dir="gtdbtk_out",
 threads=8):
 """
 GTDB-Tk — genomeclassificationclassification
 (GTDB taxonomy)。

 Parameters:
 bin_dir: str — filterdirectory
 output_dir: str — output directory
 threads: int — thread count
 """
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 subprocess.run([
 "gtdbtk", "classify_wf",
 "--genome_dir", bin_dir,
 "--out_dir", str(out),
 "--cpus", str(threads),
 "-x", "fa",
 ], check=True)

 # /classificationresultsintegration
 results = []
 for domain in ["bac120", "ar53"]:
 tsv = (out / f"gtdbtk.{domain}."
 "summary.tsv")
 if tsv.exists:
 df = pd.read_csv(tsv, sep="\t")
 df["domain_marker"] = domain
 results.append(df)

 if results:
 combined = pd.concat(results,
 ignore_index=True)
 print(f"GTDB-Tk: {len(combined)} MAGs "
 f"classified")
 return combined

 print("GTDB-Tk: no classification results")
 return pd.DataFrame
```

## 4. dRep 

```python
def run_drep(bin_dir, output_dir="drep_out",
 ani_threshold=0.95):
 """
 dRep — MAG (ANI )。

 Parameters:
 bin_dir: str — directory
 output_dir: str — output directory
 ani_threshold: float — ANI threshold
 """
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 subprocess.run([
 "dRep", "dereplicate",
 str(out),
 "-g", f"{bin_dir}/*.fa",
 "-sa", str(ani_threshold),
 "--ignoreGenomeQuality",
 ], check=True)

 derep = list(
 (out / "dereplicated_genomes").glob("*.fa"))
 print(f"dRep: {len(derep)} dereplicated MAGs "
 f"(ANI ≥ {ani_threshold})")
 return derep
```

## 5. MAG Pipeline Integration

```python
def mag_pipeline(assembly_fasta, bam_file,
 output_dir="mag_results",
 threads=8):
 """
 MAG integrationpipeline。

 Parameters:
 assembly_fasta: str — genomeassembly
 bam_file: str — BAM
 output_dir: str — output
 threads: int — thread count
 """
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 # 1) 
 bins = run_metabat2(
 assembly_fasta, bam_file,
 str(out / "bins"))

 # 2) evaluation
 checkm = run_checkm2(
 str(out / "bins"),
 str(out / "checkm2"),
 threads)

 # 3) filter (MIMAG medium+)
 quality = filter_quality_mags(checkm)

 # 4) GTDB-Tk classification
 taxonomy = run_gtdbtk(
 str(out / "bins"),
 str(out / "gtdbtk"),
 threads)

 # 5) 
 derep = run_drep(
 str(out / "bins"),
 str(out / "drep"))

 print(f"MAG pipeline: {len(bins)} bins → "
 f"{len(quality)} QC passed → "
 f"{len(derep)} dereplicated")

 # === Pipeline Integrationfor's structureoutput ===
 results = Path(output_dir) / "results"
 results.mkdir(parents=True, exist_ok=True)

 # 1) MAGsummaryCSV (→ phylogenetics, environmental-ecology)
 quality.to_csv(results / "mag_quality_summary.csv", index=False)
 print(f" ✔ MAG quality summary: {results / 'mag_quality_summary.csv'}")

 # 2) classificationsummaryCSV (→ phylogenetics)
 if not taxonomy.empty:
 taxonomy.to_csv(results / "mag_taxonomy.csv", index=False)
 print(f" ✔ MAG taxonomy: {results / 'mag_taxonomy.csv'}")

 # 3) tableMAG FASTAintegration (→ phylogenetics, annotation)
 representative_fasta = results / "representative_mags.fasta"
 with open(representative_fasta, "w") as f:
 for mag_path in derep:
 mag_name = Path(mag_path).stem
 with open(mag_path) as mag_f:
 for line in mag_f:
 if line.startswith(">"):
 f.write(f">{mag_name}_{line[1:]}")
 else:
 f.write(line)
 print(f" ✔ Representative MAGs FASTA: {representative_fasta}")

 # 4) pipelinesummaryJSON
 import json
 pipeline_summary = {
 "total_bins": len(bins),
 "quality_passed": len(quality),
 "high_quality": int((quality["quality"] == "high").sum) if "quality" in quality.columns else 0,
 "medium_quality": int((quality["quality"] == "medium").sum) if "quality" in quality.columns else 0,
 "dereplicated": len(derep),
 "classified": len(taxonomy) if not taxonomy.empty else 0,
 }
 with open(results / "mag_pipeline_summary.json", "w") as f:
 json.dump(pipeline_summary, f, indent=2)
 print(f" ✔ Pipeline summary: {results / 'mag_pipeline_summary.json'}")

 return {
 "bins": bins,
 "checkm": checkm,
 "quality": quality,
 "taxonomy": taxonomy,
 "dereplicated": derep,
 }
```

---

## Pipeline Integration

```
microbiome-metagenomics → metagenome-assembled-genomes → environmental-ecology
 (genomeanalysis) (MAG construction) (systemintegration)
 │ │ ↓
 long-read-sequencing ─────────┘ phylogenomics
 (assembly) (phylogenyanalysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `*_bins/bin.*.fa` | genome | → dRep, GTDB-Tk |
| `checkm2_out/quality_report.tsv` | report | → filter |
| `gtdbtk_out/*.summary.tsv` | classificationresults | → phylogenomics |
| `drep_out/dereplicated_genomes/` | MAG | → environmental-ecology |

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
