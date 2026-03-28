---
name: scientific-experiment-template
description: |
 Experiment template skill. Standardized experimental protocol generation, reproducible experiment setup, parameter configuration templates, and lab notebook formatting.
---

# Scientific Experiment Template

standardizationExperimental Designautomatedgeneratesskill。IMRaDshapeformula
structuretemplate than、reproducibility's highExperimental Design is supported。

## When to Use

- experiment's designwhen needed
- existing's experiment standardizationwhen needed
- and experimentprotocolwhen needed
- researchfor's Experimental Design is createdand

## Quick Start

### Step 1: researchchallenge's clear
's researchfrombelow/following extraction:
- researchbackground（research's）
- researchpurpose（）
- null hypothesis / alternative hypothesis

### Step 2: experiment'sdesign
- experiment（experiment / factorexperiment / observationresearch）
- number/countnumber/countnumber/count
- sample size's basis（powermin）

### Step 3: 
- （typenumber's）
- （proofreadinginformation）
- 

### Step 4: experimentprocedure's details
numberstep:
1. preprocessing
2. measurementData Retrieval
3. postprocessing

### Step 5: evaluation metric's definition
- keyevaluation metric（Primary endpoint）
- evaluation metric（Secondary endpoints）
- analysismethod（ttesting / ANOVA / regressionmin）
- significance level（α = 0.05）

### Step 6: 
- chartshapeformula's
- and
- 

## Output Format

`experiment_template.md` below/following's structuregeneration:

```markdown
# Experimental Design: [title]

## 1. researchbackgroundpurpose
## 2. hypothesis
## 3. experiment
## 4. 
## 5. experimentprocedure
## 6. evaluation metricanalysis
## 7. 
## 8. cautionterm
## 9. referenceliterature
```

## Examples

**Prompt Examples:**
- 「ZnO's conditionoptimization's experimenttemplate」
- 「CRISPR-Cas9by/viaexperiment's design」
- 「drug's protocol」

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | experimentprotocolstandardizationtoolsearch |

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
