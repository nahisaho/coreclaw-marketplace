---
name: scientific-biobank-cohort
description: |
 large-scaledataanalysisskill。UK Biobank /
 BBJ / All of Us 'slarge-scaledatafor/against
 searchGWAS summaryPheWAS pipeline。
tu_tools:
 - key: clinvar
 name: ClinVar
 description: significancedatasearch
---

# Scientific Biobank Cohort

UK Biobank (BBJ)All of Us 'slarge-scale
data utilizingsearchGWAS summary
PheWAS analysispipeline is provided。

## When to Use

- 's is searchedand
- GWAS summarydatavisualizationwhen needed
- PheWAS (Phenome-Wide Association Study) is performedand
- 's basicwhen needed
- -comprehensivesearchwhen needed

---

## Quick Start

## 1. search

```python
import pandas as pd
import numpy as np


def phenotype_dictionary(pheno_file, category=None,
 keyword=None):
 """
 — search。

 Parameters:
 pheno_file: str — CSV 
 (UK Biobank Data-Field listing )
 category: str — filter
 keyword: str — keywordfilter
 """
 df = pd.read_csv(pheno_file)

 if category:
 df = df[df["Category"].str.contains(
 category, case=False, na=False)]
 if keyword:
 mask = (
 df["Field"].str.contains(
 keyword, case=False, na=False)
 | df["Description"].str.contains(
 keyword, case=False, na=False)
 )
 df = df[mask]

 print(f"Phenotype dict: {len(df)} fields matched")
 return df


def cohort_demographics(pheno_df, age_col="age",
 sex_col="sex"):
 """
 — summary。

 Parameters:
 pheno_df: DataFrame — data
 age_col: str — 
 sex_col: str — 
 """
 summary = {
 "n_participants": len(pheno_df),
 "age_mean": pheno_df[age_col].mean,
 "age_std": pheno_df[age_col].std,
 "sex_distribution": (
 pheno_df[sex_col]
.value_counts(normalize=True)
.to_dict
 ),
 }
 print(f"Cohort: n={summary['n_participants']}, "
 f"age={summary['age_mean']:.1f}±"
 f"{summary['age_std']:.1f}")
 return summary
```

## 2. GWAS summary

```python
def load_gwas_summary(sumstat_file, p_threshold=5e-8,
 sep="\t"):
 """
 GWAS summaryfileloadfilter。

 Parameters:
 sumstat_file: str — summaryfile path
 (TSV: CHR, POS, SNP, A1, A2, BETA, SE, P)
 p_threshold: float — P valuethreshold
 sep: str — delimiter
 """
 df = pd.read_csv(sumstat_file, sep=sep)

 # standardcolumnnormalization
 col_map = {
 "chromosome": "CHR", "chr": "CHR",
 "position": "POS", "pos": "POS", "bp": "POS",
 "rsid": "SNP", "snp": "SNP", "variant_id": "SNP",
 "effect_allele": "A1", "a1": "A1",
 "other_allele": "A2", "a2": "A2",
 "beta": "BETA", "effect_size": "BETA",
 "se": "SE", "standard_error": "SE",
 "pval": "P", "p_value": "P", "pvalue": "P",
 }
 df.columns = [col_map.get(c.lower, c)
 for c in df.columns]

 # filter
 sig = df[df["P"] < p_threshold].copy
 sig.sort_values("P", inplace=True)

 print(f"GWAS summary: {len(df)} total, "
 f"{len(sig)} significant (P<{p_threshold})")
 return sig


def manhattan_data(gwas_df, chr_col="CHR",
 pos_col="POS", p_col="P"):
 """
 Manhattan plotfordatatransformation。

 Parameters:
 gwas_df: DataFrame — GWAS summary
 chr_col: str — 
 pos_col: str — 
 p_col: str — P value
 """
 df = gwas_df.copy
 df["-log10P"] = -np.log10(df[p_col])

 # calculation
 chr_lengths = (
 df.groupby(chr_col)[pos_col].max
.sort_index
 )
 chr_offsets = chr_lengths.cumsum.shift(1).fillna(0)
 df["cumpos"] = df.apply(
 lambda r: r[pos_col] + chr_offsets.get(
 r[chr_col], 0),
 axis=1)

 print(f"Manhattan data: {len(df)} variants, "
 f"max -log10P={df['-log10P'].max:.1f}")
 return df
```

## 3. PheWAS (Phenome-Wide Association Study)

```python
def phewas_analysis(genotype_series, pheno_df,
 pheno_cols=None,
 p_threshold=0.05):
 """
 PheWAS — 1for/againsttabletype。

 Parameters:
 genotype_series: Series — genetype
 (0/1/2 )
 pheno_df: DataFrame — data
 pheno_cols: list — testingtabletype
 p_threshold: float — Bonferroni threshold
 """
 from scipy import stats

 if pheno_cols is None:
 pheno_cols = [c for c in pheno_df.columns
 if pheno_df[c].dtype in
 [np.float64, np.int64]]

 results = []
 for col in pheno_cols:
 mask = pheno_df[col].notna
 if mask.sum < 50:
 continue
 geno = genotype_series[mask]
 pheno = pheno_df.loc[mask, col]

 # number/countvalue → lineshaperegression 
 slope, intercept, r, p, se = stats.linregress(
 geno, pheno)
 results.append({
 "phenotype": col,
 "beta": slope,
 "se": se,
 "p_value": p,
 "n": mask.sum,
 })

 df = pd.DataFrame(results)
 n_tests = len(df)
 bonf = p_threshold / n_tests if n_tests > 0 else 0.05
 df["significant"] = df["p_value"] < bonf
 df.sort_values("p_value", inplace=True)

 n_sig = df["significant"].sum
 print(f"PheWAS: {n_tests} phenotypes tested, "
 f"{n_sig} significant (Bonferroni)")
 return df
```

## 4. integrationpipeline

```python
def biobank_pipeline(sumstat_file, pheno_file=None,
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 sumstat_file: str — GWAS summaryfile
 pheno_file: str — file
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) GWAS summaryload
 gwas = load_gwas_summary(sumstat_file)
 gwas.to_csv(output_dir / "gwas_significant.csv",
 index=False)

 # 2) Manhattan plotdata
 manhattan = manhattan_data(gwas)
 manhattan.to_csv(
 output_dir / "manhattan_data.csv", index=False)

 # 3) search (usepossible)
 if pheno_file:
 pheno_dict = phenotype_dictionary(pheno_file)
 pheno_dict.to_csv(
 output_dir / "phenotype_dict.csv",
 index=False)

 print(f"Biobank pipeline → {output_dir}")
 return {"gwas": gwas, "manhattan": manhattan}
```

---

## Pipeline Integration

```
epidemiology-public-health → biobank-cohort → population-genetics
  (GWAS/PheWAS) (analysis)
 │ │ ↓
 mendelian-randomization ───────┘ rare-disease-genetics
 (causal inference) (Mendelian analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gwas_significant.csv` | Genome-wide significant SNP | → population-genetics |
| `results/manhattan_data.csv` | Manhattan plotdata | → GWAS visualization |
| `results/phenotype_dict.csv` | | → PheWAS |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `clinvar` | ClinVar | significancedatasearch |
