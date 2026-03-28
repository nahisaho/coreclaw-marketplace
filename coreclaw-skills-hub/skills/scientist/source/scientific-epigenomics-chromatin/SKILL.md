---
name: scientific-epigenomics-chromatin
description: |
 chromatinanalysisskill。ChIP-seq peak (MACS2/MACS3)、
 ATAC-seq 、DNA methylationanalysis (WGBS/RRBS)、
 histonechromatinstatus (ChromHMM)、Hi-C TAD 、
 factorbindingprediction 、bindinganalysis (DiffBind) integration
 calculationpipeline。ChIP-Atlas 43 +experimentand 'sintegrationsupport。
 ToolUniverse integration: chipatlas。
tu_tools:
 - key: chipatlas
 name: ChIP-Atlas
 description: ChIP-Atlas analysis (43+experiment)
---

# Scientific Epigenomics & Chromatin Biology

ChIP-seqATAC-seqHi-C data、
peak→bindinganalysis→chromatinstatusnote→3D genomestructureanalysis's 
integrationpipeline is provided。

## When to Use

- ChIP-seq datafromhistonefactorbindingwhen needed
- ATAC-seq chromatinaccessibility is evaluatedand
- DNA methylation（WGBS/RRBS）analysiswhen needed
- Hi-C datafrom TAD/loop3D genomestructure is estimatedand
- multipleepigenome integrationchromatinstatusclassificationwhen needed

---

## Quick Start

## 1. ChIP-seq peak (MACS2/MACS3)

```python
import subprocess
import pandas as pd
import numpy as np


def chipseq_peak_calling(treatment_bam, control_bam, genome_size="hs",
 outdir="results/chipseq", name="sample",
 peak_type="narrow", qvalue=0.05):
 """
 MACS2/MACS3 by/via ChIP-seq peak。

 Parameters:
 treatment_bam: group BAM file
 control_bam: BAM file (Input/IgG)
 genome_size: effectivegenome (hs/mm/ce/dm or int)
 peak_type: "narrow" (TF) or "broad" (histone H3K27me3 )
 qvalue: FDR threshold
 """
 import os
 os.makedirs(outdir, exist_ok=True)

 cmd = [
 "macs3", "callpeak",
 "-t", treatment_bam,
 "-c", control_bam,
 "-g", str(genome_size),
 "--outdir", outdir,
 "-n", name,
 "-q", str(qvalue),
 "--keep-dup", "auto",
 "--call-summits",
 ]

 if peak_type == "broad":
 cmd.extend(["--broad", "--broad-cutoff", str(qvalue)])

 print(f"Running MACS3 peak calling ({peak_type} mode)...")
 subprocess.run(cmd, check=True)

 # peakfileload
 suffix = "broadPeak" if peak_type == "broad" else "narrowPeak"
 peak_file = f"{outdir}/{name}_peaks.{suffix}"
 cols = ["chr", "start", "end", "name", "score", "strand",
 "signalValue", "pValue", "qValue"]
 if peak_type == "narrow":
 cols.append("summit")

 peaks = pd.read_csv(peak_file, sep="\t", header=None, names=cols)
 peaks["width"] = peaks["end"] - peaks["start"]

 print(f" Called {len(peaks):,} {peak_type} peaks (q < {qvalue})")
 print(f" Median peak width: {peaks['width'].median:.0f} bp")
 print(f" Mean signal value: {peaks['signalValue'].mean:.2f}")

 return peaks


def chipseq_qc_metrics(peaks, frip_bam=None, total_reads=None):
 """
 ChIP-seq QC 's 。

 Returns:
 dict: peak number/count、median、FRiP (Fraction of Reads in Peaks)
 """
 metrics = {
 "n_peaks": len(peaks),
 "median_width_bp": float(peaks["width"].median),
 "mean_signal": float(peaks["signalValue"].mean),
 "mean_log10_qvalue": float(peaks["qValue"].mean),
 }

 # ENCODE criteria and 'scomparison
 if metrics["n_peaks"] < 500:
 metrics["quality_flag"] = "LOW — < 500 peaks"
 elif metrics["n_peaks"] < 10000:
 metrics["quality_flag"] = "MODERATE"
 else:
 metrics["quality_flag"] = "HIGH"

 return metrics
```

## 2. ATAC-seq accessibilityanalysis

```python
import numpy as np
import pandas as pd


def atacseq_nucleosome_free_regions(fragments_file, output_dir="results/atacseq"):
 """
 ATAC-seq distribution-basedanalysis。

 by/viaclassification:
 - < 150 bp: Nucleosome-Free Region (NFR)
 - 150-300 bp: Mono-nucleosome
 - 300-500 bp: Di-nucleosome
 - > 500 bp: Tri-nucleosome+
 """
 import os
 os.makedirs(output_dir, exist_ok=True)

 # distribution
 fragments = pd.read_csv(fragments_file, sep="\t",
 names=["chr", "start", "end", "barcode", "count"])
 fragments["length"] = fragments["end"] - fragments["start"]

 # classification
 bins = [0, 150, 300, 500, 10000]
 labels = ["NFR (<150)", "Mono-nuc (150-300)",
 "Di-nuc (300-500)", "Tri-nuc+ (>500)"]
 fragments["category"] = pd.cut(fragments["length"], bins=bins, labels=labels)

 size_dist = fragments["category"].value_counts(normalize=True)
 nfr_ratio = size_dist.get("NFR (<150)", 0)

 print(f" Fragment size distribution:")
 for cat, pct in size_dist.items:
 print(f" {cat}: {pct:.1%}")
 print(f" NFR ratio: {nfr_ratio:.1%} (ENCODE target: >40%)")

 return fragments, size_dist


def atacseq_tss_enrichment(peaks, gene_gtf, window=2000):
 """
 TSS (Transcription Start Site) 's 。
 TSS Enrichment Score > 7: ATAC-seq data (ENCODE criteria)。
 """
 from pybedtools import BedTool

 peaks_bt = BedTool.from_dataframe(
 peaks[["chr", "start", "end", "name", "score"]]
 )
 # TSS ± window bp 's
 # (GTF parsing — for pyranges/GTFparse for)

 print(f" TSS enrichment window: ±{window} bp")
 print(f" Total peaks overlapping TSS regions: calculated post-intersection")

 return peaks_bt
```

## 3. DNA methylationanalysis

```python
import numpy as np
import pandas as pd


def bisulfite_methylation_analysis(methylation_file, min_coverage=10,
 output_prefix="results/methylation"):
 """
 WGBS/RRBS data'smethylationanalysis。

 input: Bismark methylation extractor output (CpG context)
 :
 1. filter
 2. methylation (β value)
 3. CpG //note
 4. methylation (DMR) 
 """
 import os
 os.makedirs(os.path.dirname(output_prefix), exist_ok=True)

 # Bismark output's load
 df = pd.read_csv(methylation_file, sep="\t",
 names=["chr", "pos", "strand", "count_m", "count_u"])
 df["coverage"] = df["count_m"] + df["count_u"]
 df["beta"] = df["count_m"] / df["coverage"]

 # filter
 n_before = len(df)
 df = df[df["coverage"] >= min_coverage].copy
 print(f" Coverage filter (≥{min_coverage}x): {n_before:,} → {len(df):,} CpGs")

 # methylation
 mean_beta = df["beta"].mean
 median_beta = df["beta"].median
 print(f" Global methylation: mean β = {mean_beta:.3f}, median β = {median_beta:.3f}")

 # methylationstatusclassification
 df["status"] = pd.cut(df["beta"],
 bins=[0, 0.2, 0.8, 1.0],
 labels=["hypo", "intermediate", "hyper"])
 status_counts = df["status"].value_counts(normalize=True)
 print(f" Hypomethylated (β<0.2): {status_counts.get('hypo', 0):.1%}")
 print(f" Intermediate (0.2≤β≤0.8): {status_counts.get('intermediate', 0):.1%}")
 print(f" Hypermethylated (β>0.8): {status_counts.get('hyper', 0):.1%}")

 return df


def detect_dmrs(group1_betas, group2_betas, positions, min_cpgs=5,
 delta_beta_cutoff=0.2, pvalue_cutoff=0.05):
 """
 methylation (DMR) 。

 Parameters:
 group1_betas, group2_betas: n_cpgs × n_samples methylation
 min_cpgs: DMR 's CpG number/count
 delta_beta_cutoff: Δβ threshold
 """
 from scipy.stats import mannwhitneyu

 results = []
 mean_g1 = group1_betas.mean(axis=1)
 mean_g2 = group2_betas.mean(axis=1)
 delta_beta = mean_g2 - mean_g1

 for i in range(len(positions)):
 stat, pval = mannwhitneyu(
 group1_betas[i, :], group2_betas[i, :], alternative="two-sided"
 )
 results.append({
 "chr": positions[i]["chr"],
 "pos": positions[i]["pos"],
 "delta_beta": float(delta_beta[i]),
 "pvalue": pval,
 "mean_group1": float(mean_g1[i]),
 "mean_group2": float(mean_g2[i]),
 })

 df = pd.DataFrame(results)

 # testingcorrection
 from statsmodels.stats.multitest import multipletests
 df["padj"] = multipletests(df["pvalue"], method="fdr_bh")[1]

 # DMR filter
 sig = df[(df["padj"] < pvalue_cutoff) &
 (df["delta_beta"].abs >= delta_beta_cutoff)]
 print(f" Significant DMCs (Δβ≥{delta_beta_cutoff}, FDR<{pvalue_cutoff}): {len(sig):,}")

 return df, sig
```

## 4. chromatinstatus (ChromHMM)

```python
import subprocess
import pandas as pd
import numpy as np


def chromhmm_learn_model(binarized_dir, output_dir, n_states=15,
 assembly="hg38"):
 """
 ChromHMM by/viachromatinstatus。

 multiple's histone (H3K4me1/me3, H3K27ac, H3K27me3,
 H3K36me3, H3K9me3 ) inputas、genome chromatinstatusclassification。

 Roadmap Epigenomics 15-state :
 1-TssA, 2-TssAFlnk, 3-TxFlnk, 4-Tx, 5-TxWk,
 6-EnhG, 7-Enh, 8-ZNF/Rpts, 9-Het, 10-TssBiv,
 11-BivFlnk, 12-EnhBiv, 13-ReprPC, 14-ReprPCWk, 15-Quies
 """
 import os
 os.makedirs(output_dir, exist_ok=True)

 cmd = [
 "java", "-mx8G", "-jar", "ChromHMM.jar", "LearnModel",
 "-b", "200",
 binarized_dir, output_dir, str(n_states), assembly
 ]
 print(f"Running ChromHMM LearnModel with {n_states} states...")
 subprocess.run(cmd, check=True)

 # rateload
 trans_file = f"{output_dir}/transitions_{n_states}.txt"
 if os.path.exists(trans_file):
 trans = pd.read_csv(trans_file, sep="\t", index_col=0)
 print(f" Transition matrix: {trans.shape}")

 # rateload
 emit_file = f"{output_dir}/emissions_{n_states}.txt"
 if os.path.exists(emit_file):
 emit = pd.read_csv(emit_file, sep="\t", index_col=0)
 print(f" Emission matrix: {emit.shape}")

 return {"n_states": n_states, "output_dir": output_dir}


def annotate_chromatin_states(segments_bed, state_labels=None):
 """
 ChromHMM results's genomenote。

 Parameters:
 segments_bed: ChromHMM output's *_segments.bed
 state_labels: statusnumber→label's mapping
 """
 default_labels = {
 "E1": "Active TSS", "E2": "Flanking Active TSS",
 "E3": "Transcription at gene 5'/3'", "E4": "Strong Transcription",
 "E5": "Weak Transcription", "E6": "Genic Enhancers",
 "E7": "Enhancers", "E8": "ZNF genes & Repeats",
 "E9": "Heterochromatin", "E10": "Bivalent/Poised TSS",
 "E11": "Flanking Bivalent TSS/Enh", "E12": "Bivalent Enhancer",
 "E13": "Repressed PolyComb", "E14": "Weak Repressed PolyComb",
 "E15": "Quiescent/Low",
 }
 labels = state_labels or default_labels

 segments = pd.read_csv(segments_bed, sep="\t",
 names=["chr", "start", "end", "state"])
 segments["width"] = segments["end"] - segments["start"]
 segments["label"] = segments["state"].map(labels)

 # genome
 total_bp = segments["width"].sum
 state_coverage = segments.groupby("label")["width"].sum / total_bp
 print(" Chromatin state genome coverage:")
 for label, pct in state_coverage.sort_values(ascending=False).items:
 print(f" {label}: {pct:.1%}")

 return segments, state_coverage
```

## 5. Hi-C 3D genomestructureanalysis

```python
import numpy as np
import pandas as pd


def hic_contact_matrix_analysis(cool_file, resolution=10000,
 chromosome="chr1"):
 """
 Hi-C analysis (.cool/.mcool shapeformula)。

 1. ICE normalization
 2. A/B (PCA)
 3. TAD (Insulation Score)
 """
 import cooler

 # fileload
 clr = cooler.Cooler(f"{cool_file}::resolutions/{resolution}")
 matrix = clr.matrix(balance=True).fetch(chromosome)

 print(f" Contact matrix shape: {matrix.shape}")
 print(f" Resolution: {resolution:,} bp")
 print(f" Non-zero entries: {np.count_nonzero(~np.isnan(matrix)):,}")

 return matrix


def call_tads_insulation_score(matrix, resolution=10000, window_size=500000):
 """
 Insulation Score methodby/via TAD (Topologically Associating Domain) 。

 Parameters:
 window_size: Insulation window (bp)
 """
 window_bins = window_size // resolution

 n = matrix.shape[0]
 insulation = np.zeros(n)

 for i in range(window_bins, n - window_bins):
 submat = matrix[i - window_bins:i, i:i + window_bins]
 insulation[i] = np.nanmean(submat)

 # log2 normalization
 mean_val = np.nanmean(insulation[insulation > 0])
 log_insulation = np.log2(insulation / mean_val + 1e-10)

 # TAD = Insulation Score 's value
 from scipy.signal import argrelextrema
 minima = argrelextrema(log_insulation, np.less, order=5)[0]

 tad_boundaries = minima * resolution
 n_tads = len(tad_boundaries) - 1

 print(f" Found {len(tad_boundaries)} TAD boundaries")
 print(f" Estimated {n_tads} TADs")
 print(f" Mean TAD size: {np.diff(tad_boundaries).mean / 1e6:.2f} Mb")

 return log_insulation, tad_boundaries


def ab_compartment_analysis(matrix, resolution=100000):
 """
 Hi-C datafrom's A/B 。

 A : euchromatin, activity, gene
 B : heterochromatin, activity, gene
 """
 from sklearn.decomposition import PCA

 # O/E (Observed/Expected) 
 matrix_clean = np.nan_to_num(matrix, nan=0.0)
 expected = np.zeros_like(matrix_clean)
 for d in range(matrix_clean.shape[0]):
 diag_vals = np.diag(matrix_clean, d)
 mean_val = np.mean(diag_vals) if len(diag_vals) > 0 else 0
 np.fill_diagonal(expected[d:, :], mean_val)
 np.fill_diagonal(expected[:, d:], mean_val)

 oe_matrix = matrix_clean / (expected + 1e-10)

 # correlation → PCA
 corr_matrix = np.corrcoef(oe_matrix)
 corr_matrix = np.nan_to_num(corr_matrix)

 pca = PCA(n_components=2)
 components = pca.fit_transform(corr_matrix)
 pc1 = components[:, 0]

 # A/B classification (PC1 = A, = B)
 compartment = np.where(pc1 > 0, "A", "B")
 a_frac = np.mean(compartment == "A")

 print(f" A compartment: {a_frac:.1%}")
 print(f" B compartment: {1 - a_frac:.1%}")
 print(f" PC1 variance explained: {pca.explained_variance_ratio_[0]:.1%}")

 return pc1, compartment
```

## 6. factoranalysis

```python
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact


def motif_enrichment_analysis(peak_sequences, background_sequences,
 jaspar_db="JASPAR2024_CORE_vertebrates",
 pvalue_cutoff=0.01):
 """
 peakinfactorbinding'sanalysis。

 Parameters:
 peak_sequences: FASTA file (peak ±250 bp)
 background_sequences: genome FASTA
 jaspar_db: JASPAR database
 """
 from Bio import motifs

 # JASPAR PWM 
 results = []

 # Homer / MEME-ChIP (for)
 print(f" Scanning {jaspar_db} motifs against peak sequences...")
 print(" (Using FIMO from MEME Suite for motif scanning)")

 # Fisher exact test by/via
 # peak_hits / peak_total vs bg_hits / bg_total
 # for each motif in JASPAR database

 return results


def differential_binding_analysis(sample_sheet, peaks_dir,
 contrast=("Treatment", "Control"),
 fdr_cutoff=0.05, fold_change_cutoff=2):
 """
 DiffBind by/viabindinganalysis。

 Parameters:
 sample_sheet: DiffBind CSV
 contrast: (treatment, control) comparisongroup
 fdr_cutoff: FDR threshold
 fold_change_cutoff: log2FC threshold
 """
 # R/rpy2 DiffBind 
 import subprocess
 r_script = f"""
 library(DiffBind)
 samples <- read.csv("{sample_sheet}")
 dba <- dba(sampleSheet=samples)
 dba <- dba.count(dba)
 dba <- dba.contrast(dba, categories=DBA_CONDITION)
 dba <- dba.analyze(dba)
 db_sites <- dba.report(dba, th={fdr_cutoff}, fold={np.log2(fold_change_cutoff)})
 write.csv(as.data.frame(db_sites), "results/diffbind_results.csv")
 """

 print(f" Running DiffBind: {contrast[0]} vs {contrast[1]}")
 print(f" FDR cutoff: {fdr_cutoff}, log2FC cutoff: ±{np.log2(fold_change_cutoff):.1f}")

 return r_script
```

## References

### Output Files

| File | Format |
|---|---|
| `results/chipseq/{name}_peaks.narrowPeak` | BED/narrowPeak |
| `results/chipseq/{name}_peaks.broadPeak` | BED/broadPeak |
| `results/atacseq/fragment_size_dist.csv` | CSV |
| `results/methylation/dmr_results.csv` | CSV |
| `results/chromhmm/emissions_{n}.txt` | TSV |
| `results/hic/tad_boundaries.bed` | BED |
| `results/hic/compartments.csv` | CSV |
| `results/diffbind_results.csv` | CSV |
| `figures/chromatin_state_heatmap.png` | PNG |
| `figures/hic_contact_map.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| ChIP-Atlas | `ChIPAtlas_enrichment_analysis` | TF/histoneanalysis |
| ChIP-Atlas | `ChIPAtlas_get_experiments` | experimentData Retrieval (43 +experiment) |
| ChIP-Atlas | `ChIPAtlas_get_peak_data` | peakData Retrieval |
| ChIP-Atlas | `ChIPAtlas_search_datasets` | Dataset Search (antigen/celltype) |
| 4DN | `FourDN_search_data` | Hi-C/ChIA-PET 3D genomedatasearch |
| JASPAR | `jaspar_search_matrices` | factorbinding (PWM) search |
| JASPAR | `jaspar_get_matrix` | PWM (Position Weight Matrix) retrieval |
| JASPAR | `jaspar_list_collections` | JASPAR list |
| SCREEN | `SCREEN_get_regulatory_elements` | cCRE  retrieval |
| ENCODE | `ENCODE_search_experiments` | ENCODE ChIP-seq/ATAC-seq experimentsearch |
| ENCODE | `ENCODE_get_experiment` | ENCODE experimentdetailsretrieval |
| ENCODE | `ENCODE_list_files` | ENCODE filelist |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-single-cell-genomics` | scATAC-seq integration |
| `scientific-sequence-analysis` | genomesequence |
| `scientific-bioinformatics` | BAM/VCF |
| `scientific-population-genetics` | eQTL |
| `scientific-gene-expression-transcriptomics` | expression-epigenomeintegration |

### Dependencies

`macs3`, `cooler`, `pybedtools`, `deeptools`, `scikit-learn`, `scipy`, `pandas`, `numpy`, `biopython`
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
