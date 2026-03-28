---
name: scientific-drug-repurposing
description: |
 Drug repurposing skill. Computational drug repositioning, network-based prediction, molecular similarity-based repurposing, and clinical trial evidence mining for new indications.
---

# Scientific Drug Repurposing

existing's novelsearch/explorationskill。Drug Repurposing SATORI integration、
systematicevaluates。

## When to Use

- existing's novel is exploredand
- diseasefor/againstexistingtreatment comprehensivewhen needed
- networkby/viasearch/exploration is performedand
- compoundlibrary is evaluatedand
- （）'ssearch/exploration is performedand

## Quick Start

### 7 items's

```
Strategy 1: Target-Based（type）
 Disease → Target genes → Known drugs for targets → Validation

Strategy 2: Compound-Based（compoundtype）
 Drug → All known targets → Other diseases of targets → Score

Strategy 3: Disease-Driven（diseasetype）
 Disease → DEGs/GWAS targets → Pathway → Drugs in pathway

Strategy 4: Mechanism-Based（type）
 Known MOA → Drugs with similar MOA → New indications

Strategy 5: Network-Based（networktype）
 Disease module → Proximity analysis → Proximal drugs

Strategy 6: Phenotype-Based（tabletypetype）
 Adverse events → Therapeutic potential → Repurpose

Strategy 7: Structure-Based（structuretype）
 Active compound → Similar structures → Approved analogs
```

---

## Strategy 1: Target-Based Repurposing

### workflow

```python
def target_based_repurposing(disease_name):
 """
 disease → → existing 'spipeline。
 """
 pipeline = {
 "step1_disease": "EFO/MONDO IDdisease",
 "step2_targets": "Open Targets top 50 retrieval",
 "step3_drugs": " ChEMBL/DrugBank existingsearch",
 "step4_filter": "'s and different",
 "step5_validate": "literature + structureverification",
 "step6_score": "criteria",
 }
 return pipeline

# number/count
def repurposing_score(candidate):
 """
 's 。
 """
 score = 0.0
 weights = {
 "target_association": 0.25, # Open Targets score
 "drug_approval_status": 0.20, # FDA approved > Phase3 > Phase2
 "mechanism_relevance": 0.20, # MOA and disease's
 "safety_profile": 0.15, # knownsafety profile
 "literature_evidence": 0.10, # PubMed 
 "structural_fit": 0.10, # molecular docking
 }
 for key, weight in weights.items:
 score += candidate.get(key, 0) * weight
 return score
```

---

## Strategy 5: Network-Based Repurposing

### networkdegreeanalysis

```python
import networkx as nx
import numpy as np

def network_proximity(drug_targets, disease_genes, ppi_network):
 """
 networkdegreemethodby/viaevaluation。
 Guney et al., Nature Communications 2016 。

 d(S,T) = 1/|T| * Σ min d(s,t) for s in S
 """
 G = ppi_network # PPI network (NetworkX Graph)
 distances = []

 for dt in drug_targets:
 if dt not in G:
 continue
 min_dist = float('inf')
 for dg in disease_genes:
 if dg not in G:
 continue
 try:
 d = nx.shortest_path_length(G, dt, dg)
 min_dist = min(min_dist, d)
 except nx.NetworkXNoPath:
 continue
 if min_dist < float('inf'):
 distances.append(min_dist)

 if not distances:
 return {"proximity": None, "significance": "N/A"}

 proximity = np.mean(distances)

 return {
 "proximity": proximity,
 "significance": "Close" if proximity < 2.0 else "Moderate" if proximity < 4.0 else "Distant",
 "n_drug_targets_in_network": len([t for t in drug_targets if t in G]),
 "n_disease_genes_in_network": len([g for g in disease_genes if g in G]),
 }
```

---

## Candidate Evaluation Matrix

### criteriaevaluationtemplate

```markdown
## Repurposing Candidate Evaluation

### Candidate: [Drug Name]
| Criterion | Score (0-1) | Weight | Evidence |
|-----------|-------------|--------|----------|
| Target-disease association | | 0.25 | |
| FDA approval status | | 0.20 | |
| Mechanism relevance | | 0.20 | |
| Safety profile | | 0.15 | |
| Literature support | | 0.10 | |
| Structural compatibility | | 0.10 | |
| **Weighted Total** | | | |

### Evidence Summary
- Clinical trials: [NCT IDs]
- Case reports: [PMID]
- Mechanistic studies: [PMID]

### Risk Assessment
- Patent status: ___
- Formulation feasibility: ___
- Regulatory pathway: 505(b)(2) / Orphan / Standard
```

---

## Report Template

```markdown
# Drug Repurposing Report: [DISEASE / DRUG]

**Strategy**: [Target-Based / Network-Based / etc.]
**Date**: [date]

## 1. Background & Rationale

## 2. Methodology
### 2.1 Strategy Selection Justification
### 2.2 Data Sources
### 2.3 Scoring Criteria

## 3. Top Candidates
| Rank | Drug | Original Indication | Score | Key Evidence |
|------|------|---------------------|-------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## 4. Detailed Candidate Profiles
### 4.1 Candidate 1
### 4.2 Candidate 2
### 4.3 Candidate 3

## 5. Validation Evidence

## 6. Recommendations
### 6.1 Immediate Next Steps
### 6.2 Clinical Trial Design Considerations
### 6.3 Regulatory Path

## 7. Limitations & Caveats

## 8. Data Sources
```

---

## Completeness Checklist

- [ ] selection: 7 's and also 2 items for
- [ ] data: Open Targets + ChEMBL + DrugBank for
- [ ] number/count: top 10 
- [ ] : criteria amountevaluation
- [ ] : eachliterature
- [ ] all: known's forfileverification
- [ ] : key'sverification

## Best Practices

1. **multiple**: single's times
2. ****: 's FDA top
3. **also**: 's failureclinical trial verification
4. **foramount**: foramount different
5. **randomizationcomparison verification**: effective RCT verification

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/repurposing_candidates.json` | （JSON） | criteriacompletion |
| `results/repurposing_report.md` | evaluationreport（Markdown） | allanalysiscompletion |
| `results/network_proximity.json` | network（JSON） | networkanalysiscompletion |

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
| `scientific-drug-target-profiling` | ← information'suse |
| `scientific-admet-pharmacokinetics` | ← ADMET filtercompound |
| `scientific-network-analysis` | ← disease-drugnetworkconstruction |
| `scientific-deep-research` | ← literature |
| `scientific-clinical-decision-support` | → 'sclinical decision support |
| `scientific-academic-writing` | → publishing research results |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
