---
name: scientific-experiment-fork
description: |
 Experimental Designskill。existing's experiment condition changeexperiment
 designs。Experimental Designmethod（DOE）-basedparameterssearch/exploration support。
 「experiment design」「conditionexperiment」「parameterssearch/exploration」 。
---

# Scientific Experiment Fork

existing's experiment、parameters changeexperiment systematicdesignsskill。
Experimental Designmethod（DOE: Design of Experiments）-basedrateparameterssearch/exploration support。

## When to Use

- successexperiment's conditionoptimizationwhen needed
- parameterssystematicsearch/explorationwhen needed
- 's 's experiment and
- orthogonal arrayresponse surfacemethod is appliedand

## Quick Start

### Step 1: experiment's min
- 's experimentconditionresults's
- keyparameters's
- success/failure's min

### Step 2: changeparameters's
- sensitivity analysisby/viaimportantparameters'sextraction
- eachparameters's range's
- parameters and parameters's min

### Step 3: Experimental Design'sdesign
- allfactorexperiment / partialfactorexperiment
- orthogonal array（L8, L16, L27）
- response surfacemethod（Box-Behnken, CCD）
- Latin hypercubesampling

### Step 4: experimentcondition'sgeneration

### Step 5: results'sprediction

## Output Format

`forked_experiment.md`:

```markdown
# Experimental Design

## experiment's
## changeparameters
## experimentcondition
| Run | Param A | Param B | Param C | Expected |
|-----|---------|---------|---------|----------|
## results
## comparisonevaluationdesign
```

## Examples

- 「ZnO's temperature200-500°Cexperiment design」
- 「's PCRcondition temperature optimization」
- 「degree's foramountreactioncurvelineexperiment design」

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | Experimental Designmethodparameterssearch/explorationtoolsearch |
