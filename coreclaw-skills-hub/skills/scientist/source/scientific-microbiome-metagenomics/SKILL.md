---
name: scientific-microbiome-metagenomics
description: |
 microbiomeanalysisskill。16S rRNA analysis（DADA2）
 genomeanalysis（MetaPhlAn / HUMAnN）α/β 
 amountanalysis（DESeq2 / ANCOM-BC）
 dataanalysis（CoDA）pipeline。
tu_tools:
 - key: mgnify
 name: MGnify
 description: EBI analysis
---

# Scientific Microbiome & Metagenomics

microbiomeanalysis's Standard Pipeline is provided。
16S rRNA andgenomedata's
quality control、classification、evaluation、
amountanalysis、annotation systematichandles。

## When to Use

- 16S rRNA 'sanalysiswhen needed
- genome's classification is performedand
- group's α / β is comparedand
- group amount'swhen needed
- data（compositional data）'sanalysis is performedand

---

## Quick Start

## 1. 16S rRNA analysis（DADA2）

```python
import numpy as np
import pandas as pd

def dada2_pipeline(fastq_dir, trim_left=20, trunc_len_f=240, trunc_len_r=200,
 min_overlap=12):
 """
 DADA2 analysispipeline。

 procedure:
 1. filterAndTrim — filter + 
 2. learnErrors — error
 3. dada — ASV（Amplicon Sequence Variant）
 4. mergePairs — 
 5. removeBimeraDenovo — 
 6. assignTaxonomy — SILVA/GTDB by/viaclassification

 ASV vs OTU:
 ASV 100% sequencedegradation（1 ）
 OTU 97% degreeclustering（method）
 """
 import subprocess

 r_script = f"""
 library(dada2)

 path <- "{fastq_dir}"
 fnFs <- sort(list.files(path, pattern="_R1_001.fastq.gz", full.names=TRUE))
 fnRs <- sort(list.files(path, pattern="_R2_001.fastq.gz", full.names=TRUE))

 # Filter and trim
 filtFs <- file.path(path, "filtered", basename(fnFs))
 filtRs <- file.path(path, "filtered", basename(fnRs))
 out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs,
 trimLeft={trim_left}, truncLen=c({trunc_len_f},{trunc_len_r}),
 maxN=0, maxEE=c(2,2), truncQ=2, rm.phix=TRUE)

 # Error learning
 errF <- learnErrors(filtFs, multithread=TRUE)
 errR <- learnErrors(filtRs, multithread=TRUE)

 # Denoise
 dadaFs <- dada(filtFs, err=errF, multithread=TRUE)
 dadaRs <- dada(filtRs, err=errR, multithread=TRUE)

 # Merge
 merged <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, minOverlap={min_overlap})

 # ASV table
 seqtab <- makeSequenceTable(merged)
 seqtab.nochim <- removeBimeraDenovo(seqtab, method="consensus")

 # Taxonomy
 taxa <- assignTaxonomy(seqtab.nochim, "silva_nr99_v138.1_train_set.fa.gz")

 write.csv(seqtab.nochim, "results/asv_table.csv")
 write.csv(taxa, "results/taxonomy.csv")
 """

 with open("_dada2_pipeline.R", "w") as f:
 f.write(r_script)
 subprocess.run(["Rscript", "_dada2_pipeline.R"], check=True)

 asv_table = pd.read_csv("results/asv_table.csv", index_col=0)
 taxonomy = pd.read_csv("results/taxonomy.csv", index_col=0)
 print(f" DADA2: {asv_table.shape[1]} ASVs from {asv_table.shape[0]} samples")
 return asv_table, taxonomy
```

## 2. classification

```python
def shotgun_taxonomic_profiling(fastq_files, method="metaphlan"):
 """
 genomeclassification。

 method:
 - "metaphlan": MetaPhlAn 4 — clade-specific marker gene
 - "kraken2": Kraken2 — k-mer （high-speed、）
 - "sourmash": sourmash — MinHash 

 MetaPhlAn: degree（amounttype's）
 Kraken2: degree（large-scaledata）
 """
 import subprocess

 profiles = []
 for fq in fastq_files:
 sample = fq.split("/")[-1].replace(".fastq.gz", "")

 if method == "metaphlan":
 cmd = (f"metaphlan {fq} --input_type fastq "
 f"--nproc 8 -o {sample}_profile.txt "
 f"--bowtie2out {sample}.bt2out")
 elif method == "kraken2":
 cmd = (f"kraken2 --db kraken2_db --threads 8 "
 f"--report {sample}_report.txt "
 f"--output {sample}_kraken.txt {fq}")

 subprocess.run(cmd, shell=True, check=True)
 profile = pd.read_csv(f"{sample}_profile.txt", sep="\t",
 comment="#", header=None)
 profile["sample"] = sample
 profiles.append(profile)

 merged = pd.concat(profiles, ignore_index=True)
 print(f" Profiling ({method}): {len(fastq_files)} samples processed")
 return merged
```

## 3. α / β analysis

```python
from scipy.spatial.distance import braycurtis, pdist, squareform
from scipy.stats import mannwhitneyu, kruskal
from skbio.diversity import alpha_diversity, beta_diversity

def alpha_diversity_analysis(asv_table, metadata, group_col,
 metrics=None):
 """
 α （group）analysis。

 :
 - observed_features: observationtypenumber/count（Richness）
 - shannon: Shannon entropy H' = -Σ pᵢ ln(pᵢ)
 - simpson: Simpson index D = 1 - Σ pᵢ²
 - chao1: Chao1 typenumber/count S_est = S_obs + f₁²/(2·f₂)
 - faith_pd: Faith's Phylogenetic Diversity（phylogeny）
 """
 if metrics is None:
 metrics = ["observed_features", "shannon", "simpson", "chao1"]

 results = {}
 for metric in metrics:
 values = alpha_diversity(metric, asv_table.values, asv_table.index)
 results[metric] = values

 alpha_df = pd.DataFrame(results, index=asv_table.index)
 alpha_df = alpha_df.join(metadata[[group_col]])

 # groupcomparison
 groups = alpha_df[group_col].unique
 comparisons = {}
 for metric in metrics:
 if len(groups) == 2:
 g1 = alpha_df[alpha_df[group_col] == groups[0]][metric]
 g2 = alpha_df[alpha_df[group_col] == groups[1]][metric]
 stat, pval = mannwhitneyu(g1, g2)
 else:
 group_data = [alpha_df[alpha_df[group_col] == g][metric] for g in groups]
 stat, pval = kruskal(*group_data)
 comparisons[metric] = {"statistic": stat, "p_value": pval}

 print(f" α diversity: {len(metrics)} indices computed for {len(alpha_df)} samples")
 return alpha_df, comparisons


def beta_diversity_analysis(asv_table, metadata, group_col,
 metric="braycurtis", n_perms=999):
 """
 β （group）analysis。

 :
 - braycurtis: Bray-Curtis dissimilarity
 - jaccard: Jaccard distance
 - unifrac: UniFrac（phylogeny、necessary）
 - aitchison: Aitchison distance（CoDA recommended）

 testing:
 - PERMANOVA (adonis2): group's significant
 - PERMDISP: variancetesting
 """
 dm = beta_diversity(metric, asv_table.values, asv_table.index)

 # PERMANOVA
 from skbio.stats.distance import permanova
 groups = metadata.loc[asv_table.index, group_col]
 permanova_result = permanova(dm, groups, permutations=n_perms)

 # PCoA
 from skbio.stats.ordination import pcoa
 pcoa_result = pcoa(dm)

 print(f" β diversity ({metric}): PERMANOVA R²={permanova_result['test statistic']:.4f}, "
 f"p={permanova_result['p-value']:.4f}")
 return dm, pcoa_result, permanova_result
```

## 4. amountanalysis

```python
def differential_abundance(asv_table, metadata, group_col,
 formula="~group", method="ancombc"):
 """
 amountanalysis — group significant different's。

 method:
 - "ancombc": ANCOM-BC2 — correctiondatasupport（recommended）
 - "deseq2": DESeq2 — 'sbinomial distribution（RNA-seq ）
 - "aldex2": ALDEx2 — CLR transformation + effect size

 data's problem:
 phaseamount=1 's correlation。
 CLR transformation: clr(x) = log(xᵢ / geometric_mean(x))
 """
 import subprocess

 if method == "ancombc":
 r_script = f"""
 library(ANCOMBC)
 library(phyloseq)
 # ANCOM-BC2 analysis
 res <- ancombc2(data=ps, fix_formula="{formula}",
 p_adj_method="holm", alpha=0.05)
 write.csv(res$res, "results/da_results.csv")
 """
 with open("_da_analysis.R", "w") as f:
 f.write(r_script)
 subprocess.run(["Rscript", "_da_analysis.R"], check=True)
 results = pd.read_csv("results/da_results.csv", index_col=0)

 elif method == "deseq2":
 r_script = f"""
 library(DESeq2)
 dds <- DESeqDataSetFromMatrix(countData=asv_counts,
 colData=sample_data,
 design={formula})
 dds <- DESeq(dds)
 res <- results(dds)
 write.csv(as.data.frame(res), "results/da_results.csv")
 """
 with open("_da_analysis.R", "w") as f:
 f.write(r_script)
 subprocess.run(["Rscript", "_da_analysis.R"], check=True)
 results = pd.read_csv("results/da_results.csv", index_col=0)

 n_sig = (results.get("padj", results.get("q_val", pd.Series)) < 0.05).sum
 print(f" DA ({method}): {n_sig} differentially abundant taxa")
 return results
```

## 5. 

```python
def functional_profiling(fastq_files, method="humann"):
 """
 genome。

 method:
 - "humann": HUMAnN 3 — UniRef90/MetaCyc pathway
 - "picrust2": PICRUSt2 — 16S fromprediction

 HUMAnN output:
 1. Gene families (UniRef90/UniRef50)
 2. Pathway abundance (MetaCyc)
 3. Pathway coverage
 """
 import subprocess

 for fq in fastq_files:
 sample = fq.split("/")[-1].replace(".fastq.gz", "")
 cmd = (f"humann --input {fq} --output humann_results/{sample}/ "
 f"--threads 8 --nucleotide-database chocophlan "
 f"--protein-database uniref")
 subprocess.run(cmd, shell=True, check=True)

 # results's
 subprocess.run("humann_join_tables -i humann_results/ -o results/pathway_abundance.tsv "
 "--file_name pathabundance", shell=True, check=True)
 subprocess.run("humann_join_tables -i humann_results/ -o results/genefamilies.tsv "
 "--file_name genefamilies", shell=True, check=True)

 pathways = pd.read_csv("results/pathway_abundance.tsv", sep="\t", index_col=0)
 print(f" HUMAnN: {pathways.shape[0]} pathways across {pathways.shape[1]} samples")
 return pathways
```

## References

### Output Files

| File | Format |
|---|---|
| `results/asv_table.csv` | CSV |
| `results/taxonomy.csv` | CSV |
| `results/alpha_diversity.csv` | CSV |
| `results/beta_distance_matrix.csv` | CSV |
| `results/da_results.csv` | CSV |
| `results/pathway_abundance.tsv` | TSV |
| `figures/alpha_boxplot.png` | PNG |
| `figures/pcoa_plot.png` | PNG |
| `figures/barplot_taxonomy.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| MGnify | `MGnify_search_studies` | genomeresearchsearch |
| MGnify | `MGnify_list_analyses` | genomeanalysislist |
| KEGG | `kegg_get_pathway_info` | metabolic pathway information |
| KEGG | `kegg_search_pathway` | pathwaysearch |
| MetaCyc | `MetaCyc_search_pathways` | metabolic pathway search |
| PubMed | `PubMed_search_articles` | microbiomeliteraturesearch |

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-metabolomics](../scientific-metabolomics/SKILL.md) | metabolite-correlation |
| [scientific-network-analysis](../scientific-network-analysis/SKILL.md) | network |
| [scientific-statistical-testing](../scientific-statistical-testing/SKILL.md) | testingcorrection |
| [scientific-multi-omics](../scientific-multi-omics/SKILL.md) | multi-omics integration |
| [scientific-causal-inference](../scientific-causal-inference/SKILL.md) | causal inference（-tabletype） |

#### Dependencies

- scikit-bio, biom-format, qiime2, dada2 (R), ANCOM-BC (R), DESeq2 (R), HUMAnN, MetaPhlAn
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
