---
name: scientific-clinical-decision-support
description: |
 Clinical decision support skill. Evidence-based clinical guidelines, risk scoring models, diagnostic algorithms, treatment pathway selection, and clinical prediction rules.
---

# Scientific Clinical Decision Support

clinical decision supportsupportskill。-basedtreatmentrecommended's generation、
pathway'sdesign、patient units'ssupport is provided。

## When to Use

- -basedtreatmentrecommendedstructurewhen needed
- pathway/ is designedand
- patient'sanalysis is performedand
- biomarker-basedtreatmentselection is supportedand
- tumor（variant/mutationfile → treatmentrecommended） is performedand
- clinical trial's / criteriaanalysiswhen needed

## Quick Start

### clinical decision supportsupportpipeline

```
Input: patientfile / disease / biomarker
 ↓
Step 1: Evidence Gathering
 - guideline search (NCCN, ESMO, etc.)
 - clinical trial search (ClinicalTrials.gov)
 - literature (PubMed)
 ↓
Step 2: Patient Stratification
 - biomarkerclassification
 - 
 - evaluation
 ↓
Step 3: Treatment Options
 - standardtreatment's
 - treatment'sevaluation
 - clinical trial
 ↓
Step 4: Recommendation Synthesis
 - 
 - recommendedintensityevaluation
 - -min
 ↓
Output: Clinical Decision Report
```

---

## Phase 1: Evidence Framework

### andrecommendedintensity

```python
EVIDENCE_LEVELS = {
 "1a": "Systematic review of RCTs",
 "1b": "Individual RCT",
 "2a": "Systematic review of cohort studies",
 "2b": "Individual cohort study",
 "3a": "Systematic review of case-control studies",
 "3b": "Individual case-control study",
 "4": "Case series / poor quality cohort",
 "5": "Expert opinion",
}

RECOMMENDATION_GRADES = {
 "A": {"description": "Strong recommendation", "evidence": "1a, 1b"},
 "B": {"description": "Moderate recommendation", "evidence": "2a, 2b, 3a"},
 "C": {"description": "Weak recommendation", "evidence": "3b, 4"},
 "D": {"description": "Very weak recommendation", "evidence": "5, expert opinion"},
}

def grade_recommendation(evidence_sources):
 """
 GRADE by/viaevaluation。
 """
 best_level = min(
 (s.get("evidence_level", "5") for s in evidence_sources),
 key=lambda x: float(x.replace("a", ".1").replace("b", ".2"))
 )

 if best_level.startswith("1"):
 return "A", "Strong"
 elif best_level.startswith("2") or best_level == "3a":
 return "B", "Moderate"
 elif best_level in ("3b", "4"):
 return "C", "Weak"
 else:
 return "D", "Very Weak"
```

---

## Phase 2: Precision Oncology

### variant/mutationfile → treatmentrecommended

```python
def precision_oncology_workflow(tumor_type, mutations):
 """
 tumorworkflow。
 variant/mutationfilefrom actionable targets 、
 treatmentrecommended is generated。
 """
 workflow = {
 "step1": "variant/mutation → OncoKB annotation",
 "step2": "Actionable mutations 's (Level 1-4)",
 "step3": "tumorverification",
 "step4": "clinical trial's",
 "step5": "treatmentrecommendedreportgeneration",
 }

 # OncoKB Actionability Levels
 actionability = {
 "Level_1": "FDA-approved, same tumor type",
 "Level_2": "Standard care, different tumor type",
 "Level_3A": "Clinical evidence, same tumor",
 "Level_3B": "Clinical evidence, different tumor",
 "Level_4": "Preclinical evidence",
 }

 return workflow


# keycancerbiomarker
CANCER_BIOMARKERS = {
 "EGFR": {
 "tumor_types": ["NSCLC"],
 "mutations": ["L858R", "ex19del", "T790M", "C797S"],
 "therapies": {
 "L858R/ex19del": ["osimertinib", "erlotinib", "gefitinib"],
 "T790M": ["osimertinib"],
 }
 },
 "BRAF": {
 "tumor_types": ["Melanoma", "NSCLC", "CRC", "Thyroid"],
 "mutations": ["V600E", "V600K"],
 "therapies": {
 "V600E": ["vemurafenib + cobimetinib", "dabrafenib + trametinib",
 "encorafenib + binimetinib"],
 }
 },
 "ALK": {
 "tumor_types": ["NSCLC"],
 "mutations": ["Fusion"],
 "therapies": {
 "Fusion": ["alectinib", "lorlatinib", "crizotinib", "ceritinib"],
 }
 },
 "MSI-H/dMMR": {
 "tumor_types": ["Pan-cancer"],
 "therapies": {
 "MSI-H": ["pembrolizumab", "nivolumab"],
 }
 },
}
```

---

## Phase 3: Clinical Trial Matching

### clinical trial

```python
def match_clinical_trials(patient_profile):
 """
 ClinicalTrials.gov API usingclinical trial。
 """
 import requests

 params = {
 "query.cond": patient_profile.get("condition"),
 "query.intr": patient_profile.get("biomarker", ""),
 "filter.overallStatus": "RECRUITING",
 "pageSize": 20,
 }

 response = requests.get(
 "https://clinicaltrials.gov/api/v2/studies",
 params=params
 )

 trials = []
 if response.status_code == 200:
 for study in response.json.get("studies", []):
 protocol = study.get("protocolSection", {})
 trials.append({
 "nct_id": protocol.get("identificationModule", {}).get("nctId"),
 "title": protocol.get("identificationModule", {}).get("briefTitle"),
 "phase": protocol.get("designModule", {}).get("phases", []),
 "status": protocol.get("statusModule", {}).get("overallStatus"),
 "interventions": protocol.get("armsInterventionsModule", {}).get("interventions", []),
 })

 return trials
```

---

## Report Template

```markdown
# Clinical Decision Support Report

**Patient Profile**: [anonymized]
**Condition**: [disease]
**Date**: [date]

## 1. Clinical Context

## 2. Biomarker Profile
| Biomarker | Result | Clinical Significance |
|-----------|--------|----------------------|

## 3. Evidence-Based Treatment Options
| Option | Evidence Level | Recommendation Grade | Notes |
|--------|---------------|---------------------|-------|

## 4. Clinical Guideline Alignment
### 4.1 NCCN Guidelines
### 4.2 ESMO Guidelines
### 4.3 National Guidelines

## 5. Clinical Trial Options
| NCT ID | Title | Phase | Status | Relevance |
|--------|-------|-------|--------|-----------|

## 6. Risk-Benefit Analysis
| Treatment | Expected Benefit | Key Risks | NNT/NNH |
|-----------|-----------------|-----------|---------|

## 7. Recommendations
### 7.1 First-line
### 7.2 Second-line
### 7.3 Monitoring Plan

## Disclaimer
This report is for research and educational purposes only.
Clinical decisions must be made by qualified healthcare professionals.
```

---

## Completeness Checklist

- [ ] search: + clinical trial + literature
- [ ] patient: biomarker + 
- [ ] treatmentselection: standardtreatment + + clinical trial
- [ ] : allrecommended GRADE 
- [ ] all: druginteraction + verification
- [ ] term: researchpurposefor's

## Best Practices

1. ****: NCCN/ESMO 's latestverification
2. ****: allrecommendedbasis
3. **patientunitsfactor**: 、、druginteraction
4. **clinical trialsearch**: standardtreatmentcase's selection
5. **term**: AI tool's

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/clinical_decision_report.md` | clinical decision supportreport（Markdown） | allanalysiscompletion |
| `results/clinical_recommendation.json` | recommendedtermdata（JSON） | GRADE evaluationcompletion |
| `results/trial_matches.json` | clinical trialresults（JSON） | searchcompletion |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| ClinicalTrials | `search_clinical_trials` | clinical trial search |
| ClinicalTrials | `clinical_trials_get_details` | trial detail retrieval |
| PharmGKB | `PharmGKB_get_dosing_guidelines` | PGx dosing guidelines |
| PharmGKB | `PharmGKB_get_clinical_annotations` | annotation |
| CPIC | `CPIC_get_guidelines` | CPIC |
| DGIdb | `DGIdb_get_drug_gene_interactions` | drug-gene interaction |
| PubMed | `PubMed_search_articles` | search |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-variant-interpretation` | ← results's application |
| `scientific-drug-repurposing` | ← 'sevaluation |
| `scientific-survival-clinical` | ← analysisclinical trialdata |
| `scientific-meta-analysis` | ← 'sintegration |
| `scientific-deep-research` | ← latest's |
| `scientific-presentation-design` | → results'spresentation |
| `scientific-academic-writing` | → publishing research results |
| `scientific-clinical-trials-analytics` | ← clinical trialanalysis |
| `scientific-pharmacogenomics` | ← PGx biomarkeramount |

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
