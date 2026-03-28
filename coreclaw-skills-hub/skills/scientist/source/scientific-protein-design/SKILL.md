---
name: scientific-protein-design
description: |
 proteindesignskill。ESM protein、de novo design、evolution's
 calculation、prediction。 claude-scientific-skills 's ESM/Adaptyv skill integration。
 「protein design」「ESM evaluation」「 prediction」 。
---

# Scientific Protein Design

calculationproteindesignskill。ESM (Evolutionary Scale Modeling) etc.'s 
protein、de novo design、sequenceoptimization、
expressionprediction integrationworkflow is provided。

## When to Use

- protein's de novo design is performedand
- ESM proteinsequence is evaluatedand
- evolution's librarydesignwhen needed
- variant/mutation's to 'spredictionwhen needed
- （antibody/peptide/protein） is designedand
- enzyme's activitydesignwhen needed

## Quick Start

### proteindesignpipeline

```
Phase 1: Target Definition
 - designtarget'sdefinition（/enzyme/）
 - structure'sretrieval
 - design'ssettings
 ↓
Phase 2: Backbone Generation
 - De novo generation（RFdiffusion ）
 - specification
 - save
 ↓
Phase 3: Sequence Design
 - ProteinMPNN sequencedesign
 - ESM 
 - 
 ↓
Phase 4: In Silico Validation
 - ESMFold structureprediction
 - pLDDT / pTM evaluation
 - design-predictiondegree (RMSD)
 ↓
Phase 5: Developability Assessment
 - prediction
 - expressionprediction
 - 
 - 
```

---

## Phase 1: ESM protein

### ESM-2 / ESM-1v by/viasequenceanalysis

```python
import torch
import esm

def load_esm_model(model_name="esm2_t33_650M_UR50D"):
 """
 ESM-2 's 。
 : 8M, 35M, 150M, 650M, 3B, 15B
 recommended: 650M (degree and degree's)
 """
 model, alphabet = esm.pretrained.esm2_t33_650M_UR50D
 batch_converter = alphabet.get_batch_converter
 model.eval
 return model, alphabet, batch_converter


def compute_sequence_loglikelihood(model, alphabet, batch_converter, sequence):
 """
 sequence's number/countlikelihoodcalculation。design's asfor。
 """
 data = [("protein", sequence)]
 batch_labels, batch_strs, batch_tokens = batch_converter(data)

 with torch.no_grad:
 results = model(batch_tokens, repr_layers=[33])

 logits = results["logits"]
 log_probs = torch.log_softmax(logits, dim=-1)

 # each'samino acid's number/countrateretrieval
 token_log_probs = []
 for i, aa in enumerate(sequence):
 aa_idx = alphabet.get_idx(aa)
 token_log_probs.append(log_probs[0, i+1, aa_idx].item)

 return {
 "sequence": sequence,
 "mean_log_likelihood": sum(token_log_probs) / len(token_log_probs),
 "total_log_likelihood": sum(token_log_probs),
 "per_position": token_log_probs,
 }
```

---

## Phase 2: variant/mutationprediction

### Zero-shot variant/mutation

```python
def predict_mutation_effect(model, alphabet, batch_converter, wt_sequence, mutations):
 """
 ESM by/via zero-shot variant/mutationprediction。
 mutations: [("A", 42, "V"), ("G", 100, "D"),...] # (wt_aa, pos, mut_aa)

 output: eachvariant/mutation's ΔLL (log-likelihood ratio)
 = variant/mutation, = variant/mutation
 """
 wt_data = [("wt", wt_sequence)]
 _, _, wt_tokens = batch_converter(wt_data)

 with torch.no_grad:
 wt_results = model(wt_tokens)

 wt_logits = wt_results["logits"]
 wt_log_probs = torch.log_softmax(wt_logits, dim=-1)

 mutation_effects = []
 for wt_aa, pos, mut_aa in mutations:
 wt_idx = alphabet.get_idx(wt_aa)
 mut_idx = alphabet.get_idx(mut_aa)
 # pos 0-indexed、tokens 1-indexed (BOS token)
 delta_ll = (wt_log_probs[0, pos+1, mut_idx] - wt_log_probs[0, pos+1, wt_idx]).item

 mutation_effects.append({
 "mutation": f"{wt_aa}{pos+1}{mut_aa}",
 "delta_log_likelihood": delta_ll,
 "prediction": "Beneficial" if delta_ll > 0 else "Neutral" if delta_ll > -2 else "Deleterious",
 })

 return sorted(mutation_effects, key=lambda x: x["delta_log_likelihood"], reverse=True)
```

---

## Phase 3: De novo designworkflow

### designtaskpipeline

```markdown
## Task-Specific Pipelines

### Binder Design (design)
1. structureretrieval → definition
2. RFdiffusion generation (≥5 candidates)
3. ProteinMPNN sequencedesign (≥8 sequences/backbone)
4. ESMFold structureverification
5. Interface evaluation (pAE at interface)

### Scaffold Design (design)
1. specification (α/β/mixed)
2. (50-200 residues)
3. save
4. optimization

### Enzyme Redesign (enzymedesign)
1. activity
2. catalystsave
3. 
4. energyoptimization
```

---

## Phase 4: In Silico Validation

### ESMFold verificationcriteria

```python
def validate_design(designed_sequence, target_structure_path=None):
 """
 designsequence's in silico verification。
 ESMFold structureprediction、metricsevaluation。
 """
 validation = {
 "sequence_length": len(designed_sequence),
 "esm_log_likelihood": None, # mean LL
 "esmfold_plddt": None, # mean pLDDT
 "esmfold_ptm": None, # pTM score
 "rmsd_to_target": None, # if target provided
 "pass_criteria": {},
 }

 # Pass/Fail criteria
 criteria = {
 "pLDDT": {"threshold": 70, "direction": ">"},
 "pTM": {"threshold": 0.5, "direction": ">"},
 "RMSD": {"threshold": 2.0, "direction": "<"}, # Å
 }

 return validation


# expressionsystemrecommended
EXPRESSION_SYSTEMS = {
 "simple_scaffold": {"recommended": "E. coli", "alternative": "Insect cells"},
 "disulfide_containing": {"recommended": "Mammalian", "alternative": "Insect cells"},
 "glycosylated": {"recommended": "Mammalian (CHO/HEK)", "alternative": None},
 "toxic_protein": {"recommended": "Cell-free", "alternative": "Insect cells"},
 "large_complex": {"recommended": "Insect cells (baculovirus)", "alternative": "Mammalian"},
}
```

---

## Report Template

```markdown
# Protein Design Report: [PROJECT NAME]

**Design Type**: [Binder / Scaffold / Enzyme]
**Target**: [target protein]
**Date**: [date]

## 1. Design Objective

## 2. Target Analysis
### 2.1 Structure Used
### 2.2 Design Constraints
### 2.3 Key Residues

## 3. Backbone Candidates
| # | Method | Topology | Size | Score |
|---|--------|----------|------|-------|

## 4. Sequence Designs (Top 10)
| Rank | Backbone | Sequence | MPNN Score | ESM LL | pLDDT | pTM |
|------|----------|----------|------------|--------|-------|-----|

## 5. Validation Results
### 5.1 Structure Prediction
### 5.2 Design-Target RMSD
### 5.3 Interface Quality (if binder)

## 6. Developability
| Metric | Value | Status |
|--------|-------|--------|
| Aggregation risk | | |
| Isoelectric point | | |
| Expression prediction | | |

## 7. Final Candidates
### 7.1 Recommended for testing
### 7.2 Sequences (FASTA format)

## 8. Experimental Recommendations
### 8.1 Expression System
### 8.2 Purification Strategy
### 8.3 Characterization Assays
```

---

## Completeness Checklist

- [ ] structure: PDB or AlphaFold for
- [ ] : ≥5 generation
- [ ] sequencedesign: ≥8 sequence/
- [ ] ESM : all's LL calculation
- [ ] structureverification: pLDDT >70 & pTM >0.5
- [ ] expressionsystemrecommended: designrecommended
- [ ] : ≥3 passing designs

## Best Practices

1. ****: sequencesearch/exploration（temperature parameter ）
2. **Negative design also**: structure
3. **variant/mutationfrom**: Consensus mutations 
4. **experiment**: design-testing-cycle design
5. ****: calculationand degree's explicit

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `results/design_report.md` | designreport（Markdown） | alldesigncompletion |
| `results/design_candidates.json` | designdata（JSON） | completion |
| `results/esm_scores.json` | ESM data（JSON） | variant/mutationcompletion |

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

| Skill | Integration |
|---|---|
| `scientific-protein-structure-analysis` | ← structuredata'sproviding |
| `scientific-sequence-analysis` | ← sequenceevolutioninformation |
| `scientific-lab-automation` | → designprotein's expressionprotocol |
| `scientific-admet-pharmacokinetics` | → proteintreatment's PK evaluation |
| `scientific-academic-writing` | → publishing research results |
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
