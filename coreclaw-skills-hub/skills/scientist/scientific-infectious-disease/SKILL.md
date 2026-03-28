---
name: scientific-infectious-disease
description: |
 Infectious disease skill. Pathogen genomics, antimicrobial resistance prediction, epidemiological modeling, phylogenetic tracking, and outbreak analysis pipelines.
---

# Scientific Infectious Disease Genomics

andinfectious disease'sintegrated analysispipeline is provided。
sequence、phylogenyanalysis、gene、
、number/count systematichandles。

## When to Use

- 's allgenomedata'sanalysiswhen needed
- （AMR）geneclassificationwhen needed
- molecule（MLST, cgMLST, SNP） is performedand
- 's is estimatedand
- SIR / SEIR 'ssimulationwhen needed

---

## Quick Start

## 1. genomepreprocessing

```python
import numpy as np
import pandas as pd

def pathogen_qc_pipeline(fastq_r1, fastq_r2, reference_genome,
 min_depth=30, min_coverage=0.95):
 """
 WGS preprocessingpipeline。

 procedure:
 1. Fastp — read QC + adapter trimming
 2. BWA-MEM2 — mapping
 3. Samtools / Picard — dupmark + sort
 4. FreeBayes / GATK — variant calling
 5. / degree QC

 criteria:
 - mean_depth ≥ min_depth (: 30x)
 - genome_coverage ≥ min_coverage (: 95%)
 """
 import subprocess

 cmds = [
 # QC + trimming
 f"fastp -i {fastq_r1} -I {fastq_r2} -o trim_R1.fq.gz -O trim_R2.fq.gz "
 f"--json qc_report.json",
 # Mapping
 f"bwa-mem2 mem -t 8 {reference_genome} trim_R1.fq.gz trim_R2.fq.gz | "
 f"samtools sort -@ 4 -o aligned.bam",
 # Mark duplicates
 f"samtools markdup aligned.bam dedup.bam",
 f"samtools index dedup.bam",
 # Variant calling
 f"freebayes -f {reference_genome} dedup.bam > variants.vcf",
 # Coverage stats
 f"samtools depth -a dedup.bam | awk '{{sum+=$3; n++}} END {{print sum/n}}'"
 ]

 for cmd in cmds:
 subprocess.run(cmd, shell=True, check=True)

 print(f" Pipeline complete: variants.vcf generated")
 return "variants.vcf"
```

## 2. AMR gene

```python
def detect_amr_genes(assembly_fasta, database="resfinder"):
 """
 （AMR）gene's 。

 database:
 - ResFinder: gene
 - CARD (RGI): AMR database
 - AMRFinderPlus: NCBI integration AMR 

 results:
 - gene（acquired resistance genes）
 - pointvariant/mutation（point mutations）
 - tabletypeprediction
 """
 import subprocess
 import json

 if database == "resfinder":
 cmd = (f"python -m resfinder -ifa {assembly_fasta} "
 f"--acquired --point -o resfinder_results/")
 subprocess.run(cmd, shell=True, check=True)

 with open("resfinder_results/ResFinder_results_tab.txt") as f:
 lines = f.readlines
 results = parse_resfinder_output(lines)

 elif database == "card":
 cmd = f"rgi main -i {assembly_fasta} -o rgi_results -t contig -a BLAST"
 subprocess.run(cmd, shell=True, check=True)
 results = pd.read_csv("rgi_results.txt", sep="\t")

 n_genes = len(results) if isinstance(results, list) else len(results)
 print(f" AMR: {n_genes} resistance genes detected ({database})")
 return results


def parse_resfinder_output(lines):
 """ResFinder output."""
 results = []
 for line in lines[1:]:
 fields = line.strip.split("\t")
 if len(fields) >= 6:
 results.append({
 "gene": fields[0],
 "identity": float(fields[1]),
 "coverage": float(fields[2]),
 "phenotype": fields[5] if len(fields) > 5 else "Unknown",
 })
 return results
```

## 3. molecule

```python
def molecular_typing(assembly_fasta, organism, scheme="mlst"):
 """
 molecule。

 scheme:
 - "mlst": Multi-Locus Sequence Typing（7 gene）
 - "cgmlst": core genome MLST（number/count〜number/countgene）
 - "wgmlst": whole genome MLST

 MLST:
 eachgene's number's
 Sequence Type（ST）.
 """
 import subprocess

 if scheme == "mlst":
 cmd = f"mlst {assembly_fasta} --scheme {organism}"
 result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
 fields = result.stdout.strip.split("\t")
 typing = {
 "file": fields[0],
 "scheme": fields[1],
 "ST": fields[2],
 "alleles": fields[3:],
 }
 elif scheme == "cgmlst":
 cmd = f"chewbbaca AlleleCall -i {assembly_fasta} -g schema/ -o cgmlst_results/"
 subprocess.run(cmd, shell=True, check=True)
 typing = {"scheme": "cgMLST", "results_dir": "cgmlst_results/"}

 print(f" Typing: ST={typing.get('ST', 'N/A')} ({scheme})")
 return typing
```

## 4. phylogenyanalysis

```python
def phylogenetic_analysis(alignment_fasta, method="iqtree", model="GTR+G"):
 """
 phylogenyanalysispipeline。

 method:
 - "iqtree": IQ-TREE 2 — method（ModelFinder automatedselection）
 - "raxml": RAxML-NG — method
 - "beast": BEAST 2 — Bayesianphylogeny

 :
 - SNP → 
 - tMRCA (time) 
 """
 import subprocess
 from Bio import Phylo

 if method == "iqtree":
 cmd = (f"iqtree2 -s {alignment_fasta} -m {model} "
 f"-bb 1000 -alrt 1000 -nt AUTO")
 subprocess.run(cmd, shell=True, check=True)
 tree = Phylo.read(f"{alignment_fasta}.treefile", "newick")

 return tree


def transmission_network(snp_matrix, max_snp_distance=10):
 """
 SNP 's network。

 criteria:
 - : SNP ≤ max_snp_distance
 - : SNP ≤ 2 × max_snp_distance

 :
 1. SNP calculation
 2. thresholdbelow/following's edgeas
 3. direction
 """
 import networkx as nx

 G = nx.Graph
 samples = snp_matrix.index.tolist
 G.add_nodes_from(samples)

 for i, s1 in enumerate(samples):
 for j, s2 in enumerate(samples):
 if i < j:
 dist = snp_matrix.iloc[i, j]
 if dist <= max_snp_distance:
 G.add_edge(s1, s2, weight=dist, snp_distance=dist)

 mst = nx.minimum_spanning_tree(G)
 clusters = list(nx.connected_components(G))

 print(f" Transmission: {G.number_of_edges} links, "
 f"{len(clusters)} clusters")
 return G, mst, clusters
```

## 5. SIR / SEIR 

```python
from scipy.integrate import odeint

def sir_model(y, t, beta, gamma, N):
 """
 SIR 。

 dS/dt = -β · S · I / N
 dI/dt = β · S · I / N - γ · I
 dR/dt = γ · I

 R₀ = β / γ (basicnumber/count)
 """
 S, I, R = y
 dSdt = -beta * S * I / N
 dIdt = beta * S * I / N - gamma * I
 dRdt = gamma * I
 return [dSdt, dIdt, dRdt]


def seir_model(y, t, beta, sigma, gamma, N):
 """
 SEIR （）。

 dS/dt = -β · S · I / N
 dE/dt = β · S · I / N - σ · E
 dI/dt = σ · E - γ · I
 dR/dt = γ · I

 σ: 's number/count (1/incubation_period)
 """
 S, E, I, R = y
 dSdt = -beta * S * I / N
 dEdt = beta * S * I / N - sigma * E
 dIdt = sigma * E - gamma * I
 dRdt = gamma * I
 return [dSdt, dEdt, dIdt, dRdt]


def run_epidemic_simulation(model="SIR", N=1e6, I0=10, R0=2.5,
 gamma=1/10, sigma=1/5, days=180):
 """
 infectious diseasesimulation。

 Parameters:
 R0: basicnumber/count
 gamma: timesrate (1/period)
 sigma: rate (1/period、SEIR 's)
 days: simulationnumber/count
 """
 beta = R0 * gamma
 t = np.linspace(0, days, days * 10)

 if model == "SIR":
 y0 = [N - I0, I0, 0]
 sol = odeint(sir_model, y0, t, args=(beta, gamma, N))
 df = pd.DataFrame(sol, columns=["S", "I", "R"])
 elif model == "SEIR":
 y0 = [N - I0, 0, I0, 0]
 sol = odeint(seir_model, y0, t, args=(beta, sigma, gamma, N))
 df = pd.DataFrame(sol, columns=["S", "E", "I", "R"])

 df["t"] = t
 peak_I = df["I"].max
 peak_day = df.loc[df["I"].idxmax, "t"]

 print(f" {model}: R₀={R0:.1f}, peak infection={peak_I:.0f} at day {peak_day:.0f}")
 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/amr_genes.csv` | CSV |
| `results/mlst_typing.json` | JSON |
| `results/snp_matrix.csv` | CSV |
| `results/transmission_network.json` | JSON |
| `results/epidemic_simulation.csv` | CSV |
| `figures/phylogenetic_tree.png` | PNG |
| `figures/transmission_network.png` | PNG |
| `figures/epidemic_curves.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| EUHealthInfo | `euhealthinfo_search_infectious_diseases` | infectious diseasedata |
| EUHealthInfo | `euhealthinfo_search_surveillance` | |
| CDC | `cdc_data_search_datasets` | CDC dataset search |
| CDC | `cdc_data_get_dataset` | CDC data retrieval |
| NCBI | `BLAST_nucleotide_search` | sequence |
| NCBI | `NCBI_get_sequence` | genomesequenceretrieval |
| PubMed | `PubMed_search_articles` | infectious diseaseliteraturesearch |
| ClinicalTrials | `search_clinical_trials` | infectious diseasetreatmentclinical trial |

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-sequence-analysis](../scientific-sequence-analysis/SKILL.md) | sequencealignmentBLAST |
| [scientific-bioinformatics](../scientific-bioinformatics/SKILL.md) | genome annotation |
| [scientific-network-analysis](../scientific-network-analysis/SKILL.md) | networkvisualization |
| [scientific-survival-clinical](../scientific-survival-clinical/SKILL.md) | infectious diseaseanalysis |
| [scientific-bayesian-statistics](../scientific-bayesian-statistics/SKILL.md) | Bayesianphylogeny |

#### Dependencies

- biopython, ete3, scipy, networkx, subprocess (fastp, bwa-mem2, freebayes, iqtree2)

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
