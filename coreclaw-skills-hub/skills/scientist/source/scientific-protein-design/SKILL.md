---
name: scientific-protein-design
description: |
 proteindesignskill。ESM protein、de novo design、evolution's
 calculation、prediction。ToolUniverse 's Protein Therapeutic Design
 and claude-scientific-skills 's ESM/Adaptyv skill integration。
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

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| UniProt | `UniProt_get_entry_by_accession` | protein entry retrieval |
| UniProt | `UniProt_get_sequence_by_accession` | amino acid sequence retrieval |
| InterPro | `InterPro_get_protein_domains` | domain annotation |
| Proteins API | `proteins_api_get_features` | protein feature information |
| Proteins API | `proteins_api_get_variants` | knownvariant/mutationinformation |
| AlphaMissense | `AlphaMissense_get_residue_scores` | prediction |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-protein-structure-analysis` | ← structuredata'sproviding |
| `scientific-sequence-analysis` | ← sequenceevolutioninformation |
| `scientific-lab-automation` | → designprotein's expressionprotocol |
| `scientific-admet-pharmacokinetics` | → proteintreatment's PK evaluation |
| `scientific-academic-writing` | → publishing research results |
