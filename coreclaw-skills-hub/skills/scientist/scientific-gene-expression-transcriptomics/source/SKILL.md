---
name: scientific-gene-expression-transcriptomics
description: |
 Gene expression and transcriptomics skill. RNA-seq analysis pipeline, gene quantification, isoform analysis, co-expression networks, and transcriptome-wide association.
---

# Scientific Gene Expression & Transcriptomics

bulk RNA-seq / 'sgene expressiondata、
GEO datasetretrieval→preprocessing→expression→GSEA→tissueexpressionreference's 
integrationpipeline is provided。

## When to Use

- GEO frombulk RNA-seq/dataset retrievalpreprocessingwhen needed
- DESeq2 by/viaexpressiongene (DEG) analysiswhen needed
- GTEx tissueexpressionfileeQTL datawhen needed
- geneanalysis (GSEA/ORA) is performedand
- Expression Atlas /expressionexperiment is searchedand

---

## Quick Start

## 1. GEO datasetretrieval

```python
import pandas as pd
import GEOparse


def fetch_geo_dataset(accession, output_dir="data/geo"):
 """
 GEO (Gene Expression Omnibus) dataset's retrievalpreprocessing。

 GEO ID shapeformula:
 - GSE: Series (expressiondataset)
 - GPL: Platform (/definition)
 - GSM: Sample (units)
 - GDS: Dataset 
 """
 import os
 os.makedirs(output_dir, exist_ok=True)

 gse = GEOparse.get_GEO(geo=accession, destdir=output_dir)

 print(f" GEO Accession: {accession}")
 print(f" Title: {gse.metadata['title'][0]}")
 print(f" Platform: {list(gse.gpls.keys)}")
 print(f" Samples: {len(gse.gsms)}")
 print(f" Type: {gse.metadata.get('type', ['unknown'])}")

 # dataextraction
 metadata = []
 for gsm_name, gsm in gse.gsms.items:
 meta = {"sample_id": gsm_name}
 meta.update({k: v[0] if v else None
 for k, v in gsm.metadata.items
 if k in ["title", "source_name_ch1", "characteristics_ch1"]})
 metadata.append(meta)

 metadata_df = pd.DataFrame(metadata)

 # expressionretrieval
 pivot_df = gse.pivot_samples("VALUE")
 print(f" Expression matrix: {pivot_df.shape[0]} genes × {pivot_df.shape[1]} samples")

 return gse, metadata_df, pivot_df
```

## 2. DESeq2 expressionanalysis (PyDESeq2)

```python
import numpy as np
import pandas as pd


def deseq2_differential_expression(count_matrix, metadata, design_factor,
 contrast=None, alpha=0.05,
 lfc_threshold=1.0):
 """
 PyDESeq2 by/viaexpressionanalysispipeline。

 1. input (genes × samples)
 2. normalization (median of ratios)
 3. variance (shrinkage)
 4. GLM (NB distribution)
 5. Wald testing
 6. LFC (apeglm)
 7. FDR correction (Benjamini-Hochberg)
 """
 from pydeseq2.dds import DeseqDataSet
 from pydeseq2.ds import DeseqStats

 # DeseqDataSet construction
 dds = DeseqDataSet(
 counts=count_matrix,
 metadata=metadata,
 design_factors=design_factor,
 )

 # normalization + variance + testing
 dds.deseq2

 # resultsretrieval
 stat_res = DeseqStats(dds, contrast=contrast, alpha=alpha)
 stat_res.summary

 results_df = stat_res.results_df.copy

 # LFC 
 stat_res.lfc_shrink(coeff=contrast)
 results_df["log2FoldChange_shrunk"] = stat_res.results_df["log2FoldChange"]

 # filter
 sig = results_df[
 (results_df["padj"] < alpha) &
 (results_df["log2FoldChange"].abs > lfc_threshold)
 ]

 sig_up = sig[sig["log2FoldChange"] > 0]
 sig_down = sig[sig["log2FoldChange"] < 0]

 print(f" DESeq2 results:")
 print(f" Total genes tested: {len(results_df)}")
 print(f" Significant (FDR < {alpha}, |log2FC| > {lfc_threshold}):")
 print(f" UP: {len(sig_up)}")
 print(f" DOWN: {len(sig_down)}")

 return results_df, sig


def generate_volcano_plot(results_df, alpha=0.05, lfc_threshold=1.0,
 output_file="figures/volcano_rnaseq.png"):
 """
 Volcano plotgeneration。
 """
 import matplotlib.pyplot as plt

 fig, ax = plt.subplots(figsize=(8, 6))

 results_df["-log10_padj"] = -np.log10(results_df["padj"].clip(lower=1e-300))

 # min
 colors = []
 for _, row in results_df.iterrows:
 if row["padj"] < alpha and row["log2FoldChange"] > lfc_threshold:
 colors.append("red")
 elif row["padj"] < alpha and row["log2FoldChange"] < -lfc_threshold:
 colors.append("blue")
 else:
 colors.append("gray")

 ax.scatter(results_df["log2FoldChange"], results_df["-log10_padj"],
 c=colors, alpha=0.5, s=5)
 ax.axhline(-np.log10(alpha), color="gray", linestyle="--", lw=0.5)
 ax.axvline(lfc_threshold, color="gray", linestyle="--", lw=0.5)
 ax.axvline(-lfc_threshold, color="gray", linestyle="--", lw=0.5)
 ax.set_xlabel("log2 Fold Change")
 ax.set_ylabel("-log10(adjusted p-value)")
 ax.set_title("Volcano Plot — Differential Expression")
 plt.tight_layout
 plt.savefig(output_file, dpi=300)
 plt.close

 return output_file
```

## 3. GTEx tissueexpressioneQTL 

```python
import pandas as pd


def query_gtex_expression(gene_name, tissue=None):
 """
 GTEx (Genotype-Tissue Expression) tissueexpressionfile。

 GTEx v8: 54 tissue, 948, 17,382 。
 TPM (Transcripts Per Million) 'sexpression level。
 """
 print(f" GTEx gene expression query: {gene_name}")
 if tissue:
 print(f" Tissue: {tissue}")
 else:
 print(" All tissues (54 tissue sites)")

 return {"gene": gene_name, "tissue": tissue}


def query_gtex_eqtl(gene_name, tissue, pvalue_threshold=1e-5):
 """
 GTEx eQTL (expression Quantitative Trait Loci) 。

 eQTL = gene expressionamountvariant/mutation
 - cis-eQTL: gene's ±1 Mb 'svariant/mutation
 - trans-eQTL: genefromvariant/mutation
 """
 print(f" GTEx eQTL query: gene={gene_name}, tissue={tissue}")
 print(f" P-value threshold: {pvalue_threshold}")
 print(" Types: cis-eQTL (primary), trans-eQTL")

 return {"gene": gene_name, "tissue": tissue}
```

## 4. geneanalysis (GSEA)

```python
import pandas as pd
import numpy as np


def gsea_preranked(ranked_gene_list, gene_sets="MSigDB_Hallmark_2020",
 n_permutations=1000, min_size=15, max_size=500):
 """
 GSEA (Gene Set Enrichment Analysis) — Preranked。

 input: log2FC × -log10(p) gene list
 geneDB:
 - MSigDB Hallmark (H)
 - GO Biological Process (C5:BP)
 - KEGG Pathways (C2:KEGG)
 - Reactome (C2:REACTOME)
 """
 import gseapy as gp

 # = sign(log2FC) × -log10(pvalue)
 results = gp.prerank(
 rnk=ranked_gene_list,
 gene_sets=gene_sets,
 processes=4,
 permutation_num=n_permutations,
 min_size=min_size,
 max_size=max_size,
 outdir="results/gsea",
 seed=42,
 )

 sig_terms = results.res2d[results.res2d["FDR q-val"] < 0.05]

 print(f" GSEA results ({gene_sets}):")
 print(f" Gene sets tested: {len(results.res2d)}")
 print(f" Significant (FDR < 0.05): {len(sig_terms)}")
 if len(sig_terms) > 0:
 print(f" Top enriched:")
 for _, row in sig_terms.head(5).iterrows:
 direction = "UP" if row["NES"] > 0 else "DOWN"
 print(f" {row['Term']} (NES={row['NES']:.2f}, {direction})")

 return results


def overrepresentation_analysis(gene_list, background=None,
 gene_sets="GO_Biological_Process_2021"):
 """
 genepresentationanalysis (ORA)。

 Fisher exact test 'sanalysis。
 DEG → to 'smapping。
 """
 import gseapy as gp

 results = gp.enrich(
 gene_list=gene_list,
 gene_sets=gene_sets,
 background=background,
 outdir="results/ora",
 )

 sig = results.res2d[results.res2d["Adjusted P-value"] < 0.05]

 print(f" ORA results ({gene_sets}):")
 print(f" Input genes: {len(gene_list)}")
 print(f" Significant terms: {len(sig)}")

 return results
```

## References

### Output Files

| File | Format |
|---|---|
| `results/geo_expression_matrix.csv` | CSV |
| `results/deseq2_results.csv` | CSV |
| `results/gsea/` | directory |
| `results/ora/` | directory |
| `figures/volcano_rnaseq.png` | PNG |
| `figures/ma_plot.png` | PNG |
| `figures/gsea_dotplot.png` | PNG |

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

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-bioinformatics` | bulk RNA-seq |
| `scientific-single-cell-genomics` | scRNA-seq (singlecell) |
| `scientific-epigenomics-chromatin` | expression-epigenomeintegration |
| `scientific-multi-omics` | multi-omics integration |
| `scientific-network-analysis` | expressionnetwork |

### Dependencies

`pydeseq2`, `GEOparse`, `gseapy`, `pandas`, `numpy`, `matplotlib`, `scipy`
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
