---
name: scientific-experiment-template
description: |
 experimenttemplategenerationskill。researchpurposehypothesismethodexperimentconditionevaluationcriteria
 structureExperimental Design automated.
 「experimenttemplate」「Experimental Design」「experimentprotocol」 。
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

---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Experimental Design)

Before execution, define:
- [ ] **Factors and levels**: complete factor list with ranges
- [ ] **Response variable**: measurement method, precision
- [ ] **Design type**: factorial / fractional / RSM / sequential
- [ ] **Sample size**: power analysis with effect size justification

#### Pass Criteria
- Design matrix is orthogonal or near-orthogonal
- All factors have >= 2 levels with scientific justification
- Randomization order specified
- Blocking/stratification applied for known confounders
- Statistical model specified before data collection
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
