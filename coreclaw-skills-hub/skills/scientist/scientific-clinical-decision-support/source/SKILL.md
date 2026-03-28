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

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
