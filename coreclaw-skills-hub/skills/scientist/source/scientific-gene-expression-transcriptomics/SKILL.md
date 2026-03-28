---
name: scientific-gene-expression-transcriptomics
description: |
 gene expressionanalysisskill。GEO (Gene Expression Omnibus) from's 
 datasetretrievalpreprocessing、DESeq2 (PyDESeq2) by/viaexpressionanalysis、
 GTEx tissueexpressionreferenceeQTL analysis、Expression Atlas (EBI GXA) integration、
 geneanalysis (GSEA)、bulk RNA-seq data's
 standardanalysispipeline。
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

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| GEO | `geo_search_datasets` | GEO Dataset Search |
| GEO | `geo_get_dataset_info` | datasetdetailsretrieval |
| GEO | `geo_get_sample_info` | informationretrieval |
| GTEx | `GTEx_get_median_gene_expression` | tissuemedianexpression level |
| GTEx | `GTEx_get_gene_expression` | expressiondata |
| GTEx | `GTEx_get_top_expressed_genes` | expressiongeneretrieval |
| GTEx | `GTEx_get_eqtl_genes` | eQTL gene (eGenes) |
| GTEx | `GTEx_get_single_tissue_eqtls` | singletissue eQTL |
| GTEx | `GTEx_get_multi_tissue_eqtls` | tissue eQTL |
| GTEx | `GTEx_calculate_eqtl` | eQTL calculation |
| Expression Atlas | `ExpressionAtlas_search_experiments` | experimentsearch |
| Expression Atlas | `ExpressionAtlas_get_baseline` | expression |
| Expression Atlas | `ExpressionAtlas_search_differential` | expressionexperiment |
| ArrayExpress | `arrayexpress_search_experiments` | ArrayExpress experimentsearch |

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
