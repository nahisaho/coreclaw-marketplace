---
name: scientific-research-methodology
description: |
 Research methodology skill. Study design planning, sampling strategy selection, measurement validity/reliability assessment, and methodological quality framework.
---

# Scientific Research Methodology

researchmethod'sskill。systematicresearch、hypothesisgenerationframework、
、research、research'sevaluation、
integrationprovides。

## When to Use

- novelresearch's design systematic and
- structurewhen needed
- research（observation/experiment/experiment） selectionwhen needed
- research's phylogenyevaluationwhen needed
- （IRB/）'swhen needed
- research's and methodwhen needed

## Quick Start

### researchdesignpipeline

```
Phase 1: Ideation（）
 - 
 - literaturemin
 - 
 ↓
Phase 2: Research Question（researchchallenge'sdefinition）
 - PICO/FINER criteria
 - hypothesis's shapeformula
 - 'ssettings
 ↓
Phase 3: Study Design（research）
 - selection
 - sample sizecalculation
 - 
 ↓
Phase 4: Methodology（method）
 - datadesign
 - analysisdesign（SAP）
 - 
 ↓
Phase 5: Validity & Rigor（）
 - 
 - 
 - reproducibilitydesign
```

---

## Phase 1: framework

### structure

```python
BRAINSTORMING_FRAMEWORKS = {
 "SCAMPER": {
 "S": "Substitute（）: 's also 's？",
 "C": "Combine（binding）: and？",
 "A": "Adapt（）: min's for？",
 "M": "Modify/Magnify（fix/）: change？",
 "P": "Put to other uses（for）: 's for？",
 "E": "Eliminate（）: ？",
 "R": "Reverse/Rearrange（/sequence）: structure？",
 },
 "Cross_Domain": {
 "description": "min's fromframework",
 "steps": [
 "1. min's problem",
 "2. 's structure itemsmin",
 "3. min's solution min",
 "4. evaluates",
 ],
 "examples": [
 "network（CS）→ genenetwork（）",
 "quality control（）→ clinical trial's（）",
 "evolution（CS）→ moleculeoptimization（）",
 ]
 },
 "TRIZ": {
 "description": "'s systematic",
 "principles": [
 "Segmentation（min）",
 "Extraction（extraction）",
 "Local quality（）",
 "Asymmetry（）",
 "Merging（integration）",
 ]
 },
}
```

### hypothesisclassification

```markdown
## Hypothesis Types

| Type | Format | Example |
|------|--------|---------|
| **Directional** | X increases Y | BMI |
| **Non-directional** | X affects Y | BMI |
| **Null (H₀)** | X does not affect Y | BMI |
| **Mechanistic** | X causes Y via Z | metabolismrate BMI |
| **Interaction** | X modifies Z's effect on Y | 's BMI |
```

---

## Phase 2: researchselection

### classification

```python
STUDY_DESIGNS = {
 "experimental": {
 "RCT": {
 "description": "randomizationcomparison",
 "strength": "causal inferencealso",
 "when": "'sevaluation",
 "bias_control": ["randomization", "blinding", "allocation concealment"],
 "evidence_level": "1b",
 },
 "crossover": {
 "description": "",
 "strength": "comparison（units）",
 "when": "disease、washout possible",
 },
 "factorial": {
 "description": "",
 "strength": "multiple'sinteraction",
 "when": "2+ evaluation",
 },
 },
 "observational": {
 "cohort": {
 "description": "research",
 "strength": "ratepossible",
 "when": "→'s",
 "evidence_level": "2b",
 },
 "case_control": {
 "description": "caseresearch",
 "strength": "disease",
 "when": "disease'sfactorsearch/exploration",
 "evidence_level": "3b",
 },
 "cross_sectional": {
 "description": "cross-cuttingresearch",
 "strength": "rate's",
 "when": "evaluation",
 "evidence_level": "4",
 },
 },
 "qualitative": {
 "grounded_theory": "datafrom'sconstruction",
 "phenomenology": "'s papers's",
 "ethnography": "context's",
 "case_study": "example's",
 },
}

def recommend_design(research_question):
 """
 researchchallenge's fromrecommended。
 """
 rq_type = research_question.get("type")
 recommendations = {
 "causation": ["RCT", "quasi_experimental"],
 "association": ["cohort", "case_control"],
 "prevalence": ["cross_sectional"],
 "prediction": ["cohort", "validation_study"],
 "exploration": ["qualitative", "mixed_methods"],
 }
 return recommendations.get(rq_type, ["cross_sectional"])
```

---

## Phase 3: FINER criteriaby/viaevaluation

### researchchallenge'sevaluation

```markdown
## FINER Criteria

| Criterion | Question | Score (1-5) |
|-----------|----------|-------------|
| **F**easible | time possible？ | |
| **I**nteresting | researchand？ | |
| **N**ovel | ？ | |
| **E**thical | problem？ | |
| **R**elevant | significance？ | |
| **Total** | | /25 |

### criteria
- 20-25: Excellent — designstart
- 15-19: Good — fix possible
- 10-14: Fair — necessary
- <10: Poor — papers necessary
```

---

## Phase 4: 

### classification and

```python
BIAS_TYPES = {
 "selection_bias": {
 "description": "selection's",
 "countermeasures": ["randomization", "stratification", "matching"],
 },
 "information_bias": {
 "description": "information's",
 "countermeasures": ["blinding", "standardized_instruments", "validated_scales"],
 },
 "confounding": {
 "description": "confounding factorsby/via",
 "countermeasures": ["randomization", "stratification", "regression_adjustment",
 "propensity_score", "instrumental_variables"],
 },
 "performance_bias": {
 "description": "'s",
 "countermeasures": ["double_blinding", "placebo_control"],
 },
 "attrition_bias": {
 "description": "'s",
 "countermeasures": ["ITT_analysis", "sensitivity_analysis", "IPCW"],
 },
 "reporting_bias": {
 "description": "'s（p-hacking、HARKing）",
 "countermeasures": ["pre_registration", "registered_report", "SAP"],
 },
}
```

---

## Phase 5: research

### IRB / 

```markdown
## Ethics Review Checklist

### basicprinciples（ / report）
- [ ] **Respect for persons**: 
- [ ] **Beneficence**: 's 、'smaximize
- [ ] **Justice**: selection

### 
- [ ] researchdesign（protocol）
- [ ] 
- [ ] unitsinformationdesign
- [ ] phase
- [ ] datadesign
- [ ] design

### necessary
- [ ] tissue's for
- [ ] （also 、、）
- [ ] information's
- [ ] research
```

---

## Report Template

```markdown
# Research Methodology Plan: [Title]

**PI**: [Name] | **Date**: [date]

## 1. Research Question
## 2. FINER Evaluation
## 3. Study Design
## 4. Methodology
### 4.1 Participants / Samples
### 4.2 Interventions / Exposures
### 4.3 Outcomes
### 4.4 Data Collection
### 4.5 Statistical Analysis Plan
## 5. Bias Control Strategy
## 6. Ethics Considerations
## 7. Timeline
## 8. Feasibility Assessment
```

---

## Completeness Checklist

- [ ] researchchallenge: PICO + FINER evaluation
- [ ] : research's explicitselection and basis
- [ ] sample size: formulapowermin
- [ ] : and also 3 's
- [ ] analysisdesign (SAP): Pre-registration support
- [ ] : IRB/'s

## Best Practices

1. **Pre-registration**: keyanalysis (OSF, ClinicalTrials.gov)
2. **SAP **: dataanalysisdesign
3. **Pilot study**: papersresearch feasibility verification
4. ****: limitation 
5. **reproducibility design**: protocoldata's design

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

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `docs/methodology_design.md` | methoddesign（Markdown） | completion |
| `docs/study_design.json` | researchstructuredata（JSON） | completion |
| `docs/ethics_checklist.md` | （Markdown） | completion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-hypothesis-pipeline` | ← hypothesis-basedmethoddesign |
| `scientific-deep-research` | ← research's methodinvestigation |
| `scientific-grant-writing` | → method researchdesign |
| `scientific-doe` | → research-basedExperimental Design |
| `scientific-academic-writing` | → Methods writing |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Writing/Review)

Before execution, define:
- [ ] **Target venue**: journal name, word/page limit, citation style
- [ ] **Document structure**: required sections (IMRaD / custom)
- [ ] **Quality standard**: PRISMA / CONSORT / ARRIVE as applicable
- [ ] **Completeness check**: all required sections present

#### Pass Criteria
- All citations verifiable (DOI or PMID present)
- No placeholder text remaining ([TODO], [CITE], etc.)
- Figure/table references match actual figures/tables
- Word count within target range
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
