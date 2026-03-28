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
