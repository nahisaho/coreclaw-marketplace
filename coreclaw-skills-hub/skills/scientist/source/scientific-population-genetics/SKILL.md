---
name: scientific-population-genetics
description: |
 population geneticsanalysisskill。allele frequencyanalysisHardy-Weinberg testing
 structureanalysis（PCA / ADMIXTURE）Fst minselection（iHS / XP-EHH）
 （LD）analysisGWAS Catalog / gnomAD dataintegrationpipeline。
---

# Scientific Population Genetics

population geneticsanalysispipeline is provided。
allele frequency、structure、min、selection、
's analysis systematic、GWAS CataloggnomAD and 'sintegration is supported。

## When to Use

- allele frequencydistribution and Hardy-Weinberg testingwhen needed
- structure（PCA / ADMIXTURE / STRUCTURE） analysiswhen needed
- 's min（Fst） is evaluatedand
- selection（iHS / Tajima's D / XP-EHH）when needed
- GWAS 'spopulation genetics is performedand

---

## Quick Start

## 1. QCallele frequencyanalysis

```python
import numpy as np
import pandas as pd

def genotype_qc(plink_prefix, mind=0.02, geno=0.02, maf=0.01,
 hwe_p=1e-6):
 """
 QC pipeline（PLINK 2）。

 filtercriteria:
 - --mind: unitsrate ≤ mind
 - --geno: SNP rate ≤ geno
 - --maf: Minor Allele Frequency ≥ maf
 - --hwe: Hardy-Weinberg p ≥ hwe_p（'s）

 addition QC:
 - 
 - IBD （: π̂ > 0.25）
 - PCA 
 """
 import subprocess

 # Step 1: ratefilter
 cmd = (f"plink2 --bfile {plink_prefix} "
 f"--mind {mind} --geno {geno} --maf {maf} "
 f"--hwe {hwe_p} "
 f"--make-bed --out {plink_prefix}_qc")
 subprocess.run(cmd, shell=True, check=True)

 # Step 2: IBD （）
 cmd = (f"plink2 --bfile {plink_prefix}_qc "
 f"--indep-pairwise 50 5 0.2 --out {plink_prefix}_prune")
 subprocess.run(cmd, shell=True, check=True)

 cmd = (f"plink2 --bfile {plink_prefix}_qc "
 f"--extract {plink_prefix}_prune.prune.in "
 f"--genome --out {plink_prefix}_ibd")
 subprocess.run(cmd, shell=True, check=True)

 return f"{plink_prefix}_qc"


def allele_frequency_stats(genotype_matrix, populations):
 """
 allele frequency。

 :
 - MAF: Minor Allele Frequency
 - Het: Observed heterozygosity = n_het / n_total
 - Expected Het (He): 2pq
 - HWE: Hardy-Weinberg testing (χ² test)
 H₀: f(AA) = p², f(Aa) = 2pq, f(aa) = q²
 """
 from scipy.stats import chi2

 results = []
 for pop in populations["population"].unique:
 pop_idx = populations[populations["population"] == pop].index
 geno_pop = genotype_matrix.loc[pop_idx]

 for snp in geno_pop.columns:
 counts = geno_pop[snp].value_counts
 n = counts.sum
 n_0 = counts.get(0, 0) # AA
 n_1 = counts.get(1, 0) # Aa
 n_2 = counts.get(2, 0) # aa

 p = (2 * n_0 + n_1) / (2 * n)
 q = 1 - p
 maf = min(p, q)

 # HWE test
 exp_0 = n * p**2
 exp_1 = n * 2*p*q
 exp_2 = n * q**2
 if exp_0 > 0 and exp_1 > 0 and exp_2 > 0:
 chi2_stat = ((n_0-exp_0)**2/exp_0 + (n_1-exp_1)**2/exp_1 +
 (n_2-exp_2)**2/exp_2)
 hwe_p = 1 - chi2.cdf(chi2_stat, df=1)
 else:
 hwe_p = 1.0

 het_obs = n_1 / n
 het_exp = 2 * p * q

 results.append({
 "snp": snp, "population": pop,
 "MAF": round(maf, 4), "p": round(p, 4),
 "Het_obs": round(het_obs, 4), "Het_exp": round(het_exp, 4),
 "HWE_p": round(hwe_p, 6),
 })

 return pd.DataFrame(results)
```

## 2. structureanalysis

```python
def population_structure(plink_prefix, n_components=10, method="pca"):
 """
 structureanalysis。

 method:
 - "pca": PCA — 's 2D/3D visualization
 - "admixture": ADMIXTURE — eachunits's rate
 K=2〜10 、CV error 's K selection

 PCA on genotypes:
 X (n_samples × n_snps) as
 variance C = XᵀX / n_snps 's valuedegradation
 """
 import subprocess

 if method == "pca":
 cmd = (f"plink2 --bfile {plink_prefix} "
 f"--pca {n_components} --out {plink_prefix}_pca")
 subprocess.run(cmd, shell=True, check=True)

 eigenvec = pd.read_csv(f"{plink_prefix}_pca.eigenvec", sep="\t")
 eigenval = pd.read_csv(f"{plink_prefix}_pca.eigenval", header=None)
 var_explained = eigenval[0] / eigenval[0].sum

 print(f" PCA: PC1={var_explained[0]:.3f}, PC2={var_explained[1]:.3f}")
 return eigenvec, var_explained

 elif method == "admixture":
 cv_errors = {}
 for K in range(2, 11):
 cmd = f"admixture --cv {plink_prefix}.bed {K}"
 result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
 # CV error extraction
 for line in result.stdout.split("\n"):
 if "CV error" in line:
 cv_errors[K] = float(line.split(": ")[1])

 best_K = min(cv_errors, key=cv_errors.get)
 Q = pd.read_csv(f"{plink_prefix}.{best_K}.Q", sep=" ", header=None)

 print(f" ADMIXTURE: best K={best_K} (CV error={cv_errors[best_K]:.4f})")
 return Q, cv_errors, best_K
```

## 3. min（Fst）

```python
def calculate_fst(genotype_matrix, populations, method="weir_cockerham"):
 """
 min Fst 。

 Weir-Cockerham (1984) amount:
 F_ST = σ²_a / (σ²_a + σ²_b + σ²_w)
 σ²_a: variance
 σ²_b: unitsvariance
 σ²_w: units（）variance

 :
 Fst = 0: min（）
 0 < Fst < 0.05: min
 0.05 ≤ Fst < 0.15: degree's min
 0.15 ≤ Fst < 0.25: min
 Fst ≥ 0.25: min

 genome-wide Fst: all SNP 'smean
 per-SNP Fst: 's
 """
 pop_labels = populations["population"]
 unique_pops = pop_labels.unique

 fst_per_snp = []
 for snp in genotype_matrix.columns:
 # allele frequency
 pop_freqs = {}
 pop_sizes = {}
 for pop in unique_pops:
 idx = pop_labels[pop_labels == pop].index
 geno = genotype_matrix.loc[idx, snp].dropna
 p = (2 * (geno == 0).sum + (geno == 1).sum) / (2 * len(geno))
 pop_freqs[pop] = p
 pop_sizes[pop] = len(geno)

 # Weir-Cockerham Fst
 n_pops = len(unique_pops)
 n_total = sum(pop_sizes.values)
 p_bar = sum(pop_freqs[p] * pop_sizes[p] for p in unique_pops) / n_total
 n_bar = n_total / n_pops

 MSP = sum(pop_sizes[p] * (pop_freqs[p] - p_bar)**2
 for p in unique_pops) / (n_pops - 1)
 MSG = sum(pop_sizes[p] * pop_freqs[p] * (1 - pop_freqs[p])
 for p in unique_pops) / (n_total - n_pops)

 nc = (n_total - sum(n**2 for n in pop_sizes.values) / n_total) / (n_pops - 1)

 if (MSP + (nc - 1) * MSG) > 0:
 fst = (MSP - MSG) / (MSP + (nc - 1) * MSG)
 else:
 fst = 0

 fst_per_snp.append({"snp": snp, "Fst": max(fst, 0), "p_bar": p_bar})

 fst_df = pd.DataFrame(fst_per_snp)
 genome_fst = fst_df["Fst"].mean

 print(f" Fst: genome-wide={genome_fst:.4f}, "
 f"max per-SNP={fst_df['Fst'].max:.4f}")
 return fst_df, genome_fst
```

## 4. selection

```python
def selection_scan(haplotype_matrix, positions, method="ihs"):
 """
 selection's。

 method:
 - "ihs": Integrated Haplotype Score — 'sselection
 |iHS| > 2: selection
 - "tajima_d": Tajima's D — testing
 D > 0: selection or 
 D < 0: 'sselection or 
 D ≈ 0: evolution
 - "xpehh": Cross-Population EHH — 'sselection

 iHS:
 each SNP about、 (derived) and (ancestral) 's 
 Extended Haplotype Homozygosity (EHH) comparison。
 iHS = ln(iHH_A / iHH_D) → standardization
 """
 if method == "tajima_d":
 # Tajima's D
 from allel import tajima_d
 import allel

 D_values = []
 window_size = 50000
 step = 10000

 for start in range(0, positions[-1], step):
 end = start + window_size
 mask = (positions >= start) & (positions < end)
 if mask.sum > 5:
 ac = allel.AlleleCountsArray(
 haplotype_matrix[:, mask].sum(axis=0).reshape(-1, 1))
 D = tajima_d(ac)
 D_values.append({"start": start, "end": end, "D": D,
 "n_snps": mask.sum})

 df = pd.DataFrame(D_values)
 print(f" Tajima's D: mean={df['D'].mean:.3f}, "
 f"range=[{df['D'].min:.3f}, {df['D'].max:.3f}]")
 return df

 elif method == "ihs":
 import allel
 ihs = allel.ihs(haplotype_matrix, positions)
 # standardization
 ihs_std = (ihs - np.nanmean(ihs)) / np.nanstd(ihs)

 n_sig = np.sum(np.abs(ihs_std) > 2)
 print(f" iHS: {n_sig} candidate regions (|iHS|>2)")
 return ihs_std
```

## References

### Output Files

| File | Format |
|---|---|
| `results/allele_frequencies.csv` | CSV |
| `results/pca_eigenvec.csv` | CSV |
| `results/admixture_Q.csv` | CSV |
| `results/fst_per_snp.csv` | CSV |
| `results/selection_scan.csv` | CSV |
| `figures/pca_populations.png` | PNG |
| `figures/admixture_barplot.png` | PNG |
| `figures/manhattan_fst.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| gnomAD | `gnomad_get_variant` | frequency |
| gnomAD | `gnomad_get_gene_constraints` | gene |
| gnomAD | `gnomad_get_region` | |
| gnomAD | `gnomad_search_variants` | search |
| GWAS | `GWAS_search_associations_by_gene` | gene GWAS |
| GWAS | `gwas_search_studies` | GWAS researchsearch |
| GWAS | `gwas_get_variants_for_trait` | shape |
| GWAS | `gwas_get_associations_for_snp` | SNP |
| GWAS | `gwas_get_snps_for_gene` | gene SNP |

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-variant-interpretation](../scientific-variant-interpretation/SKILL.md) | |
| [scientific-bioinformatics](../scientific-bioinformatics/SKILL.md) | genome annotation |
| [scientific-disease-research](../scientific-disease-research/SKILL.md) | disease-gene |
| [scientific-statistical-testing](../scientific-statistical-testing/SKILL.md) | testing |
| [scientific-pca-tsne](../scientific-pca-tsne/SKILL.md) | dimensionality reduction |
| [scientific-pharmacogenomics](../scientific-pharmacogenomics/SKILL.md) | PGx frequency |
| [scientific-epigenomics-chromatin](../scientific-epigenomics-chromatin/SKILL.md) | epigenome |

#### Dependencies

- scikit-allel, plink2, admixture, pandas, numpy, scipy
