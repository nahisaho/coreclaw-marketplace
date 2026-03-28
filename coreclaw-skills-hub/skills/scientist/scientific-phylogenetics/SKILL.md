---
name: scientific-phylogenetics
description: |
 Phylogenetics skill. Phylogenetic tree construction (ML/Bayesian), multiple sequence alignment, divergence time estimation, and evolutionary analysis pipelines.
---

# Scientific Phylogenetics

ETE Toolkit / scikit-bio and
moleculephylogenyanalysisevolutionpipeline is provided。

## When to Use

- moleculephylogenyconstructionvisualizationwhen needed (NJ/ML/Bayesianmethod)
- sequencealignmentfromphylogenywhen needed
- min (molecule) is performedand
- phylogeny (PD: Phylogenetic Diversity) calculationwhen needed
- sequenceconfiguration is performedand
- phylogenycomparisonmethod (PGLS ) shapeevolutionanalysiswhen needed

---

## Quick Start

## 1. ETE Toolkit phylogenyconstruction

```python
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace
import subprocess
import tempfile


def build_phylogenetic_tree(sequences_fasta, method="fasttree", model="GTR"):
 """
 sequencealignmentfromphylogenyconstruction。

 Parameters:
 sequences_fasta: str — FASTA file path 
 method: str — "fasttree", "raxml", "iqtree"
 model: str — evolution ("GTR", "JTT", "WAG", "LG")

 K-Dense: etetoolkit — Phylogenetics toolkit
 """
 commands = {
 "fasttree": ["fasttree", "-gtr", "-nt", sequences_fasta],
 "raxml": [
 "raxmlHPC", "-s", sequences_fasta, "-n", "tree",
 "-m", f"GTRGAMMA", "-p", "12345",
 ],
 "iqtree": [
 "iqtree2", "-s", sequences_fasta,
 "-m", model, "-bb", "1000", "--prefix", "iqtree_out",
 ],
 }

 cmd = commands.get(method, commands["fasttree"])
 result = subprocess.run(cmd, capture_output=True, text=True)

 if method == "fasttree":
 newick = result.stdout
 elif method == "iqtree":
 with open("iqtree_out.treefile", "r") as f:
 newick = f.read
 else:
 newick = result.stdout

 tree = Tree(newick)
 print(f"Phylogenetic tree ({method}, {model}): "
 f"{len(tree)} leaves, {len(list(tree.traverse))} total nodes")
 return tree


def visualize_tree(tree, output_file="phylogenetic_tree.png",
 layout="rectangular", show_support=True):
 """
 ETE3 phylogenyvisualization。

 Parameters:
 tree: ete3.Tree — phylogeny
 output_file: str — output
 layout: str — "rectangular", "circular"
 show_support: bool — value table
 """
 ts = TreeStyle
 ts.mode = "c" if layout == "circular" else "r"
 ts.show_leaf_name = True
 ts.show_branch_length = True
 ts.show_branch_support = show_support
 ts.branch_vertical_margin = 10

 # Node styling
 for node in tree.traverse:
 nstyle = NodeStyle
 if node.is_leaf:
 nstyle["fgcolor"] = "#2196F3"
 nstyle["size"] = 8
 else:
 nstyle["fgcolor"] = "#E91E63"
 nstyle["size"] = 5
 if show_support and node.support >= 0.9:
 nstyle["fgcolor"] = "#4CAF50"
 node.set_style(nstyle)

 tree.render(output_file, tree_style=ts, w=800, units="px")
 print(f"Tree rendered: {output_file} ({layout} layout)")
 return output_file
```

## 2. sequencealignment

```python
from Bio import AlignIO, SeqIO
from Bio.Align.Applications import MafftCommandline, MuscleCommandline


def run_multiple_alignment(input_fasta, method="mafft", output_fasta=None):
 """
 sequencealignment。

 Parameters:
 input_fasta: str — input FASTA 
 method: str — "mafft", "muscle", "clustalw"
 output_fasta: str — output path
 """
 if output_fasta is None:
 output_fasta = input_fasta.replace(".fasta", f"_aligned_{method}.fasta")

 if method == "mafft":
 cmd = f"mafft --auto {input_fasta} > {output_fasta}"
 elif method == "muscle":
 cmd = f"muscle -in {input_fasta} -out {output_fasta}"
 else:
 cmd = f"clustalw2 -INFILE={input_fasta} -OUTFILE={output_fasta}"

 subprocess.run(cmd, shell=True, check=True)

 alignment = AlignIO.read(output_fasta, "fasta")
 print(f"Alignment ({method}): {len(alignment)} sequences, "
 f"{alignment.get_alignment_length} positions")
 return alignment
```

## 3. phylogeny (Phylogenetic Diversity)

```python
import skbio
from skbio import TreeNode
from skbio.diversity import alpha_diversity, beta_diversity
import numpy as np


def calculate_phylogenetic_diversity(newick_string, sample_otus):
 """
 phylogeny (Faith's PD, UniFrac) calculation。

 Parameters:
 newick_string: str — Newick shapeformulaphylogeny
 sample_otus: dict — {sample_id: {otu_id: abundance}}

 K-Dense: scikit-bio — PD & UniFrac
 """
 tree = TreeNode.read([newick_string])

 # Prepare OTU table
 all_otus = sorted(set(
 otu for otus in sample_otus.values for otu in otus
 ))
 sample_names = list(sample_otus.keys)
 otu_table = np.zeros((len(sample_names), len(all_otus)))
 for i, sample in enumerate(sample_names):
 for j, otu in enumerate(all_otus):
 otu_table[i, j] = sample_otus[sample].get(otu, 0)

 # Faith's PD (alpha diversity)
 pd_values = alpha_diversity("faith_pd", otu_table, ids=sample_names, tree=tree,
 otu_ids=all_otus)
 print(f"Faith's PD: mean={pd_values.mean:.3f}, "
 f"range=[{pd_values.min:.3f}, {pd_values.max:.3f}]")

 # Weighted UniFrac (beta diversity)
 unifrac_dm = beta_diversity("weighted_unifrac", otu_table,
 ids=sample_names, tree=tree, otu_ids=all_otus)
 print(f"Weighted UniFrac: mean distance = "
 f"{unifrac_dm.condensed_form.mean:.4f}")

 return {"faith_pd": pd_values, "unifrac": unifrac_dm}
```

## 4. moleculemin

```python
def estimate_divergence_times(tree, calibrations, rate_model="strict"):
 """
 moleculeby/viamin。

 Parameters:
 tree: ete3.Tree — phylogeny
 calibrations: dict — {(taxon1, taxon2): (min_age, max_age)}
 e.g., {("human", "mouse"): (85, 95)} # MYA
 rate_model: str — "strict" or "relaxed"
 """
 # Branch length to relative time conversion
 total_length = max(tree.get_distance(leaf) for leaf in tree.get_leaves)

 # Apply calibration
 for (t1, t2), (min_age, max_age) in calibrations.items:
 node1 = tree.search_nodes(name=t1)
 node2 = tree.search_nodes(name=t2)
 if node1 and node2:
 ancestor = tree.get_common_ancestor(node1[0], node2[0])
 dist = tree.get_distance(ancestor)
 calibration_age = (min_age + max_age) / 2
 rate = dist / calibration_age if calibration_age > 0 else 1
 print(f"Calibration {t1}-{t2}: {calibration_age} MYA, rate={rate:.6f}")

 # Estimate ages for all internal nodes
 node_ages = {}
 for node in tree.traverse("postorder"):
 if not node.is_leaf:
 dist = tree.get_distance(node)
 # Simple proportional dating
 estimated_age = (dist / total_length) * max(
 (min_age + max_age) / 2
 for (min_age, max_age) in calibrations.values
 )
 node_ages[node.name or f"node_{id(node)}"] = estimated_age

 return node_ages
```

## 5. sequenceconfiguration

```python
def ancestral_sequence_reconstruction(alignment_file, tree_file, model="JTT"):
 """
 methodby/viasequenceconfiguration。

 Parameters:
 alignment_file: str — alignmentfile path
 tree_file: str — phylogenyfile path (Newick)
 model: str — amino acid
 """
 # Using IQ-TREE for ASR
 cmd = [
 "iqtree2", "-s", alignment_file, "-te", tree_file,
 "-m", model, "-asr", "--prefix", "asr_output",
 ]
 result = subprocess.run(cmd, capture_output=True, text=True)

 if result.returncode == 0:
 # Parse ancestral sequences
 asr_file = "asr_output.state"
 ancestral_seqs = {}
 if os.path.exists(asr_file):
 import csv
 with open(asr_file) as f:
 reader = csv.reader(f, delimiter="\t")
 for row in reader:
 if row and not row[0].startswith("#"):
 node = row[0]
 site = row[1]
 state = row[2]
 if node not in ancestral_seqs:
 ancestral_seqs[node] = []
 ancestral_seqs[node].append(state)

 print(f"ASR ({model}): {len(ancestral_seqs)} ancestral nodes reconstructed")
 return ancestral_seqs
 else:
 print(f"ASR failed: {result.stderr[:200]}")
 return None
```

---

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/phylogenetic_tree.nwk` | Newick phylogeny | → infectious-disease, microbiome |
| `figures/phylogenetic_tree.png` | phylogenyvisualization | → publication-figures, presentation |
| `results/divergence_times.json` | min | → population-genetics, environmental-ecology |
| `results/ancestral_sequences.fasta` | sequence | → protein-design, sequence-analysis |
| `results/phylo_diversity.json` | phylogeny | → microbiome-metagenomics |

## Pipeline Integration

```
sequence-analysis ──→ phylogenetics ──→ infectious-disease
 (alignment) (phylogenyconstruction) (phylogenyanalysis)
 │
 ├──→ microbiome-metagenomics (UniFrac)
 ├──→ population-genetics (min)
 └──→ environmental-ecology (phylogeny)
```

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
