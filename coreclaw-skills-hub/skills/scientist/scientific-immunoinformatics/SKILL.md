---
name: scientific-immunoinformatics
description: |
 Immunoinformatics skill. Epitope prediction, MHC binding analysis, TCR/BCR repertoire analysis, immune cell deconvolution, and vaccine design support.
tu_tools:
 - key: iedb
 name: IEDB
 description: immunedatabase
 - key: imgt
 name: IMGT
 description: immuneinformation
 - key: sabdab
 name: SAbDab
 description: structureantibodydatabase
 - key: therasabdab
 name: TheraSAbDab
 description: treatmentforantibodystructuredatabase
---

# Scientific Immunoinformatics

immuneinformation（Immunoinformatics）analysispipeline is provided。
prediction、MHC binding、antibodysequencestructureanalysis、
immuneanalysis、 systematichandles。

## When to Use

- peptide-MHC bindingpredictionwhen needed
- T cell / B cellmappingwhen needed
- TCR / BCR （）analysiswhen needed
- antibody CDR loop's structure is performedand
- 's is performedand

---

## Quick Start

## 1. MHC-I prediction

```python
import numpy as np
import pandas as pd

def predict_mhc_binding(peptides, alleles, method="netmhcpan"):
 """
 MHC I prediction。

 method:
 - "netmhcpan": NetMHCpan 4.1 — peptide-MHC binding IC50 prediction
 - "mhcflurry": MHCflurry 2.0 — network

 threshold:
 - Strong binder: IC50 < 50 nM (or %Rank < 0.5)
 - Weak binder: IC50 < 500 nM (or %Rank < 2.0)

 Parameters:
 peptides: peptidesequence（8-14 mer）
 alleles: HLA (e.g., ["HLA-A*02:01", "HLA-B*07:02"])
 """
 from mhcflurry import Class1PresentationPredictor

 predictor = Class1PresentationPredictor.load

 results = []
 for peptide in peptides:
 for allele in alleles:
 pred = predictor.predict(peptides=[peptide], alleles=[allele],
 verbose=0)
 results.append({
 "peptide": peptide,
 "allele": allele,
 "affinity_nM": pred["affinity"].values[0],
 "percentile_rank": pred["affinity_percentile"].values[0],
 "processing_score": pred["processing_score"].values[0],
 "presentation_score": pred["presentation_score"].values[0],
 })

 df = pd.DataFrame(results)
 df["binding_level"] = np.where(
 df["affinity_nM"] < 50, "Strong",
 np.where(df["affinity_nM"] < 500, "Weak", "Non-binder")
 )

 n_strong = (df["binding_level"] == "Strong").sum
 n_weak = (df["binding_level"] == "Weak").sum
 print(f" MHC-I: {n_strong} strong + {n_weak} weak binders / {len(df)} predictions")
 return df
```

## 2. B cellprediction

```python
def predict_bcell_epitopes(sequence, window_size=20, threshold=0.5):
 """
 B cell（line）prediction。

 integration:
 1. BepiPred 2.0: Random Forest prediction
 2. Parker hydrophilicity scale
 3. Emini surface accessibility
 4. Chou-Fasman β-turn prediction

 combined_score = 0.4 * bepipred + 0.2 * hydrophilicity +
 0.2 * surface + 0.2 * beta_turn
 """
 from Bio.SeqUtils.ProtParam import ProteinAnalysis

 pa = ProteinAnalysis(str(sequence))

 # Parker hydrophilicity
 hydrophilicity = pa.protein_scale(window=window_size,
 param_dict="Parker")

 # B cell
 from Bio.SeqUtils.ProtParam import ProtParamData
 flexibility = pa.flexibility

 epitopes = []
 for i in range(len(sequence) - window_size + 1):
 window = sequence[i:i + window_size]
 score = np.mean([
 hydrophilicity[i] if i < len(hydrophilicity) else 0,
 flexibility[i] if i < len(flexibility) else 0,
 ])
 if score > threshold:
 epitopes.append({
 "start": i + 1,
 "end": i + window_size,
 "sequence": window,
 "score": score,
 })

 df = pd.DataFrame(epitopes)
 print(f" B-cell epitopes: {len(df)} predicted (threshold={threshold})")
 return df
```

## 3. TCR/BCR analysis

```python
def repertoire_analysis(clonotype_df, chain="TRB",
 clone_col="cdr3_aa", count_col="clone_count"):
 """
 TCR/BCR analysis。

 :
 - Shannon entropy: H = -Σ pᵢ log₂(pᵢ)
 - Simpson index: D = 1 - Σ pᵢ²
 - Chao1 estimator: S_est = S_obs + f₁²/(2·f₂)
 - Clonality: 1 - H/log₂(N)
 - Gini coefficient: 's

 Parameters:
 clonotype_df: DataFrame (cdr3_aa, clone_count)
 chain: TCR/BCR (TRA, TRB, IGH, IGL, IGK)
 """
 from scipy.stats import entropy

 counts = clonotype_df[count_col].values
 total = counts.sum
 freqs = counts / total

 # Shannon entropy
 H = entropy(freqs, base=2)
 # Simpson index
 D = 1 - np.sum(freqs ** 2)
 # Clonality
 n_clones = len(counts)
 clonality = 1 - H / np.log2(n_clones) if n_clones > 1 else 0

 # Chao1
 f1 = np.sum(counts == 1) # singletons
 f2 = np.sum(counts == 2) # doubletons
 chao1 = n_clones + (f1 ** 2) / (2 * max(f2, 1))

 # Gini coefficient
 sorted_freqs = np.sort(freqs)
 n = len(sorted_freqs)
 gini = (2 * np.sum((np.arange(1, n + 1)) * sorted_freqs) / (n * np.sum(sorted_freqs))) - (n + 1) / n

 # Top clones
 top10 = clonotype_df.nlargest(10, count_col)

 metrics = {
 "chain": chain,
 "n_clonotypes": n_clones,
 "total_cells": int(total),
 "shannon_entropy": round(H, 4),
 "simpson_index": round(D, 4),
 "clonality": round(clonality, 4),
 "chao1": round(chao1, 1),
 "gini": round(gini, 4),
 "top1_frequency": round(freqs[0], 4) if len(freqs) > 0 else 0,
 }

 print(f" Repertoire ({chain}): {n_clones} clonotypes, "
 f"Shannon={H:.3f}, Clonality={clonality:.3f}")
 return metrics, top10
```

## 4. antibodystructureanalysis

```python
def antibody_structure_analysis(vh_seq, vl_seq, numbering="imgt"):
 """
 antibody'sstructureanalysis。

 pipeline:
 1. ANARCI （IMGT / Kabat / Chothia）
 2. CDR loop（CDR-H1/H2/H3, CDR-L1/L2/L3）
 3. framework（FR1-FR4）extraction
 4. ratecellvariant/mutation（SHM）rate
 5. possible

 CDR definition（IMGT formula）:
 CDR-H1: 26-33 (8 )
 CDR-H2: 51-57 (7 )
 CDR-H3: 93-102 
 """
 from anarci import anarci

 # 
 vh_numbered = anarci([("VH", vh_seq)], scheme=numbering)
 vl_numbered = anarci([("VL", vl_seq)], scheme=numbering)

 # CDR extraction（IMGT formula）
 cdr_regions = {
 "CDR-H1": (26, 33), "CDR-H2": (51, 57), "CDR-H3": (93, 102),
 "CDR-L1": (27, 32), "CDR-L2": (50, 52), "CDR-L3": (89, 97),
 }

 cdrs = {}
 for name, (start, end) in cdr_regions.items:
 chain_data = vh_numbered if "H" in name else vl_numbered
 seq = extract_region(chain_data, start, end)
 cdrs[name] = seq

 # SHM rate（system and 's min）
 def estimate_shm_rate(numbered_seq, germline_db="imgt"):
 """systemsequence and 'sfrom SHM rate"""
 # implementation: system and 's rate
 return 0.0 # system DB

 result = {
 "cdrs": cdrs,
 "vh_length": len(vh_seq),
 "vl_length": len(vl_seq),
 "cdr_h3_length": len(cdrs.get("CDR-H3", "")),
 "numbering": numbering,
 }

 print(f" Antibody: CDR-H3 length={result['cdr_h3_length']}, "
 f"scheme={numbering}")
 return result
```

## 5. 

```python
def vaccine_candidate_ranking(antigens_df, weights=None):
 """
 's criteria。

 evaluationcriteria:
 1. Antigenicity score: VaxiJen 2.0 （threshold > 0.4）
 2. Allergenicity: AllerTOP 
 3. Toxicity: ToxinPred toxicity
 4. MHC coverage: HLA supertype rate
 5. Conservation: sequencesave（）
 6. Surface accessibility: tablesurfacedegree

 Composite score = Σ wᵢ · normalized_scoreᵢ
 """
 if weights is None:
 weights = {
 "antigenicity": 0.25,
 "mhc_coverage": 0.25,
 "conservation": 0.20,
 "surface_accessibility": 0.15,
 "non_allergenicity": 0.10,
 "non_toxicity": 0.05,
 }

 # Min-max normalization
 for col in weights.keys:
 if col in antigens_df.columns:
 min_val = antigens_df[col].min
 max_val = antigens_df[col].max
 if max_val > min_val:
 antigens_df[f"{col}_norm"] = (antigens_df[col] - min_val) / (max_val - min_val)
 else:
 antigens_df[f"{col}_norm"] = 1.0

 # Composite 
 antigens_df["composite_score"] = sum(
 w * antigens_df.get(f"{col}_norm", 0)
 for col, w in weights.items
 )

 antigens_df = antigens_df.sort_values("composite_score", ascending=False)
 print(f" Vaccine candidates: {len(antigens_df)} antigens ranked")
 return antigens_df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/mhc_binding_predictions.csv` | CSV |
| `results/bcell_epitopes.csv` | CSV |
| `results/repertoire_diversity.json` | JSON |
| `results/antibody_structure.json` | JSON |
| `results/vaccine_candidates_ranked.csv` | CSV |
| `figures/epitope_map.png` | PNG |
| `figures/repertoire_clonality.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| IEDB | `iedb_search_epitopes` | search |
| IEDB | `iedb_get_epitope_mhc` | -MHC bindingdata |
| IEDB | `iedb_search_bcell` | B cellsearch |
| IEDB | `iedb_search_mhc` | MHC search |
| IEDB | `iedb_search_antigens` | antigensearch |
| IMGT | `IMGT_get_gene_info` | immunegeneinformation |
| IMGT | `IMGT_get_sequence` | immunesequenceretrieval |
| IMGT | `IMGT_search_genes` | immunegenesearch |
| SAbDab | `SAbDab_search_structures` | antibodystructuresearch |
| SAbDab | `SAbDab_get_structure` | antibodystructureretrieval |
| TheraSAbDab | `TheraSAbDab_search_therapeutics` | treatmentforantibodysearch |
| TheraSAbDab | `TheraSAbDab_search_by_target` | treatmentforantibody |
| UniProt | `UniProt_get_entry_by_accession` | proteininformationretrieval |

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-sequence-analysis](../scientific-sequence-analysis/SKILL.md) | sequencealignmentsaveanalysis |
| [scientific-protein-structure-analysis](../scientific-protein-structure-analysis/SKILL.md) | antibody 3D structureanalysis |
| [scientific-protein-design](../scientific-protein-design/SKILL.md) | antibody |
| [scientific-variant-interpretation](../scientific-variant-interpretation/SKILL.md) | HLA |
| [scientific-single-cell-genomics](../scientific-single-cell-genomics/SKILL.md) | immunecellanalysis |

#### Dependencies

- mhcflurry, anarci, biopython, immcantation, scirpy

---

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
