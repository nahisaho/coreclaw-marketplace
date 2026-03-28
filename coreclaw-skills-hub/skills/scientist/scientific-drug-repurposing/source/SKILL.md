---
name: scientific-drug-repurposing
description: |
 Drug repurposing skill. Computational drug repositioning, network-based prediction, molecular similarity-based repurposing, and clinical trial evidence mining for new indications.
tu_tools:
 - key: pharos
 name: Pharos
 description: IDG Pharos/TCRD target knowledge base
---

# Scientific Drug Repurposing

existing's novelsearch/explorationskill。ToolUniverse（mims-harvard）'s 
Drug Repurposing SATORI integration、
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

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| ChEMBL | `ChEMBL_search_drugs` | drugsearch |
| ChEMBL | `ChEMBL_get_drug_mechanisms` | drugfor |
| OpenTargets | `OpenTargets_get_associated_drugs_by_disease_efoId` | diseasedrug |
| DGIdb | `DGIdb_get_drug_gene_interactions` | drug-gene interaction |
| ClinicalTrials | `search_clinical_trials` | clinical trial |
| FAERS | `FAERS_count_reactions_by_drug_event` | adverse event data |
| PubMed | `PubMed_search_articles` | literature |

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
