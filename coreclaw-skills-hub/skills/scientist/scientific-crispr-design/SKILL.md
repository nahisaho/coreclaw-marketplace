---
name: scientific-crispr-design
description: |
 CRISPR design skill. Guide RNA design, off-target analysis, CRISPR screen analysis, gene knockout/knock-in design, and editing efficiency prediction.
---

# Scientific CRISPR Design

CRISPR gRNA designevaluationactivityprediction integration
rate RNA selectionpipeline is provided。

## When to Use

- CRISPR-Cas9/Cas12a 's gRNA is designedand
- PAM sequencesearchand 's is performedand
- (CFD/MIT) all is evaluatedand
- gRNA activity (CRISPRscan/Rule Set 2) ratepredictionwhen needed
- CRISPR library is builtand
- verificationfor PCR is designedand

---

## Quick Start

## 1. PAM sequencesearchgRNA 

```python
import re
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq


# PAM definition
PAM_PATTERNS = {
 "SpCas9": {"pam": "NGG", "guide_len": 20,
 "pam_side": "3prime"},
 "SaCas9": {"pam": "NNGRRT", "guide_len": 21,
 "pam_side": "3prime"},
 "Cas12a": {"pam": "TTTV", "guide_len": 23,
 "pam_side": "5prime"},
 "xCas9": {"pam": "NG", "guide_len": 20,
 "pam_side": "3prime"},
}


def iupac_to_regex(pam):
 """IUPAC → tabletransformation。"""
 iupac = {
 "N": "[ACGT]", "R": "[AG]", "Y": "[CT]",
 "S": "[GC]", "W": "[AT]", "K": "[GT]",
 "M": "[AC]", "B": "[CGT]", "D": "[AGT]",
 "H": "[ACT]", "V": "[ACG]",
 }
 return "".join(iupac.get(c, c) for c in pam)


def find_grna_candidates(sequence, cas_type="SpCas9",
 strand="both"):
 """
 gRNA 's 。

 Parameters:
 sequence: str — DNA sequence
 cas_type: str — Cas 
 strand: str — "sense"/"antisense"/"both"
 """
 config = PAM_PATTERNS[cas_type]
 pam_re = iupac_to_regex(config["pam"])
 gl = config["guide_len"]
 side = config["pam_side"]
 seq = sequence.upper

 candidates = []

 def _search_strand(s, s_name):
 for m in re.finditer(
 f"(?=({pam_re}))", s):
 pos = m.start
 if side == "3prime":
 start = pos - gl
 if start < 0:
 continue
 guide = s[start:pos]
 else: # 5prime
 start = pos + len(config["pam"])
 end = start + gl
 if end > len(s):
 continue
 guide = s[start:end]

 if len(guide) != gl:
 continue

 gc = (guide.count("G")
 + guide.count("C")) / gl

 candidates.append({
 "guide": guide,
 "pam": m.group(1),
 "position": pos,
 "strand": s_name,
 "gc_content": round(gc, 3),
 "length": gl,
 })

 if strand in ("sense", "both"):
 _search_strand(seq, "+")
 if strand in ("antisense", "both"):
 rc = str(Seq(seq).reverse_complement)
 _search_strand(rc, "-")

 df = pd.DataFrame(candidates)

 # GC filter (30-70%)
 if not df.empty:
 df = df[(df["gc_content"] >= 0.30)
 & (df["gc_content"] <= 0.70)]

 print(f"CRISPR {cas_type}: "
 f"{len(df)} gRNA candidates "
 f"(GC 30-70%)")
 return df.reset_index(drop=True)
```

## 2. 

```python
import numpy as np


# CFD implementation (Doench 2016)
def cfd_score(guide, off_target):
 """
 CFD (Cutting Frequency Determination) 。

 Parameters:
 guide: str — gRNA sequence (20nt)
 off_target: str — 
 """
 # 
 mm_penalty = {
 1: 0.0, 2: 0.0, 3: 0.014, 4: 0.0,
 5: 0.0, 6: 0.395, 7: 0.317, 8: 0.0,
 9: 0.389, 10: 0.079, 11: 0.445,
 12: 0.508, 13: 0.613, 14: 0.851,
 15: 0.732, 16: 0.828, 17: 0.615,
 18: 0.804, 19: 0.685, 20: 0.583,
 }

 score = 1.0
 for i in range(min(len(guide),
 len(off_target))):
 if guide[i] != off_target[i]:
 pos = i + 1
 penalty = mm_penalty.get(pos, 0.5)
 score *= (1.0 - penalty)

 return round(score, 4)


def score_off_targets(guide, genome_fasta,
 max_mismatches=4):
 """
 genome。

 Parameters:
 guide: str — gRNA sequence
 genome_fasta: str — reference genome
 max_mismatches: int — number/count
 """
 results = []
 gl = len(guide)
 guide_upper = guide.upper

 for record in SeqIO.parse(
 genome_fasta, "fasta"):
 seq = str(record.seq).upper
 for i in range(len(seq) - gl - 3):
 site = seq[i:i + gl]
 pam = seq[i + gl:i + gl + 3]
 if not re.match("[ACGT]GG", pam):
 continue

 mm = sum(1 for a, b in
 zip(guide_upper, site)
 if a != b)
 if mm <= max_mismatches:
 results.append({
 "chrom": record.id,
 "position": i,
 "site": site,
 "pam": pam,
 "mismatches": mm,
 "cfd_score": cfd_score(
 guide_upper, site),
 })

 df = pd.DataFrame(results)
 df = df.sort_values("cfd_score",
 ascending=False)
 print(f"Off-target: {len(df)} sites "
 f"(≤{max_mismatches} mm)")
 return df
```

## 3. gRNA activityprediction

```python
def rule_set2_score(guide_30mer):
 """
 Rule Set 2 activity (Doench 2016 )。

 Parameters:
 guide_30mer: str — 30nt sequence
 (4nt upstream + 20nt guide + 3nt PAM
 + 3nt downstream)
 """
 seq = guide_30mer.upper
 if len(seq) != 30:
 print(f"Warning: expected 30nt, "
 f"got {len(seq)}")
 return 0.0

 guide = seq[4:24]
 gc = (guide.count("G")
 + guide.count("C")) / 20

 # 
 score = 0.5

 # GC range
 if 0.40 <= gc <= 0.70:
 score += 0.1
 elif gc < 0.30 or gc > 0.80:
 score -= 0.2

 # PAM 
 if guide[-1] == "G":
 score += 0.05
 if guide[-4] == "C":
 score += 0.03

 # T times (Pol III )
 if "TTTT" in guide:
 score -= 0.3

 return round(max(0, min(1, score)), 3)


def rank_grnas(candidates_df, genome_fasta=None):
 """
 gRNA 。

 Parameters:
 candidates_df: pd.DataFrame — gRNA 
 genome_fasta: str | None — analysisfor
 """
 df = candidates_df.copy

 # activity (30mer guide 's)
 df["activity_score"] = df["guide"].apply(
 lambda g: rule_set2_score(
 "AAAA" + g + "GGGNNN"
 if len(g) == 20
 else g.ljust(30, "N")))

 # (genome)
 if genome_fasta:
 ot_scores = []
 for guide in df["guide"]:
 ot = score_off_targets(
 guide, genome_fasta, 3)
 specificity = (
 1.0 / (1.0 + len(ot))
 if not ot.empty else 1.0)
 ot_scores.append(round(specificity, 3))
 df["specificity"] = ot_scores
 else:
 df["specificity"] = 1.0

 # 
 df["composite_score"] = (
 df["activity_score"] * 0.5
 + df["specificity"] * 0.3
 + df["gc_content"].clip(0.4, 0.6) * 0.2
 ).round(3)

 df = df.sort_values("composite_score",
 ascending=False)
 print(f"gRNA ranking: top score = "
 f"{df['composite_score'].iloc[0]}")
 return df
```

## 4. sgRNA libraryconstruction

```python
def build_sgrna_library(gene_list,
 genome_fasta,
 guides_per_gene=4,
 cas_type="SpCas9"):
 """
 for sgRNA libraryconstruction。

 Parameters:
 gene_list: list[dict] — gene list
 [{"gene": "TP53", "sequence": "ATCG..."}]
 genome_fasta: str — reference genome
 guides_per_gene: int — gene gRNA number/count
 cas_type: str — Cas 
 """
 library = []

 for gene_info in gene_list:
 gene = gene_info["gene"]
 seq = gene_info["sequence"]

 candidates = find_grna_candidates(
 seq, cas_type)

 if candidates.empty:
 print(f" {gene}: no candidates")
 continue

 ranked = rank_grnas(candidates)
 top = ranked.head(guides_per_gene)

 for _, row in top.iterrows:
 library.append({
 "gene": gene,
 "guide": row["guide"],
 "position": row["position"],
 "strand": row["strand"],
 "gc_content": row["gc_content"],
 "activity": row["activity_score"],
 "composite": row["composite_score"],
 })

 df = pd.DataFrame(library)
 n_genes = df["gene"].nunique
 print(f"Library: {len(df)} sgRNAs for "
 f"{n_genes} genes")
 return df
```

---

## Pipeline Integration

```
genome-sequence-tools → crispr-design → perturbation-analysis
 (genomesequenceretrieval) (gRNA design) (experimentanalysis)
 │ │ ↓
 variant-effect-prediction ─┘ functional-genomics
 (variant/mutationprediction) 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `grna_candidates.csv` | gRNA | → |
| `off_target_report.csv` | evaluation | → allverification |
| `sgrna_library.csv` | sgRNA library | → perturbation-analysis |

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
