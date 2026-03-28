---
name: scientific-research-methodology
description: |
 researchmethodresearchskill。systematicresearchdesign、
 framework、method、researchIRB、researchevaluation、
 methodincludingresearch's skillgroup。
 「researchdesign」「」「research design」 。
tu_tools:
 - key: open_alex
 name: OpenAlex
 description: researchmethod's literatureconstruction
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `open_alex` | OpenAlex | researchmethod's literatureconstruction |

## References

### Output Files

| File | Format | Generation Timing |
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
